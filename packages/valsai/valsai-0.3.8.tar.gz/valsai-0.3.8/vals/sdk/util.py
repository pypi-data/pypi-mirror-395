import asyncio
import base64
import hashlib
import os
import sys
from collections import defaultdict
from io import BytesIO
from typing import Any, TYPE_CHECKING
import aiofiles
import aiohttp
import httpx
import requests
from tqdm import tqdm

from vals.graphql_client.client import Client as AriadneClient
from vals.sdk.auth import _get_auth_token, be_host
from vals.sdk.exceptions import ValsException

import tempfile
import pypandoc


if TYPE_CHECKING:
    from vals.sdk.types import File

VALS_ENV = os.getenv("VALS_ENV")


def read_pdf(file: BytesIO):
    """
    Convenience method to parse PDFs to strings
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        raise Exception(
            "To use read_pdf and read_docx, please run `pip install vals[parsing]`"
        )

    text = ""
    pdf_reader = PdfReader(file)
    num_pages = len(pdf_reader.pages)
    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        text += page.extract_text()
    return text


def read_docx(file: BytesIO) -> str:
    """
    Convenience method to parse DOCX files to plain text.
    Works with in-memory BytesIO streams.
    """
    try:
        # write the in-memory bytes to a temporary .docx file
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=True) as tmp:
            tmp.write(file.read())
            tmp.flush()

            # convert DOCX to plain text using pandoc
            text = pypandoc.convert_file(tmp.name, to="plain", format="docx")
            return text.strip()
    except ImportError:
        raise ImportError("To use read_docx, please run `pip install vals[parsing]`")
    except Exception as e:
        raise RuntimeError(f"Failed to parse DOCX: {e}")


def get_ariadne_client() -> AriadneClient:
    """
    Use the new codegen-based client
    """

    def append_auth_header(request: httpx.Request):
        request.headers["Authorization"] = _get_auth_token()
        return request

    return AriadneClient(
        url=f"{be_host()}/graphql/",
        http_client=httpx.AsyncClient(auth=append_auth_header, timeout=60),
    )


def md5_hash(file) -> str:
    """Produces an md5 hash of the file."""
    hasher = hashlib.md5()
    while chunk := file.read(8192):  # Read in 8 KB chunks
        hasher.update(chunk)
    hash = hasher.hexdigest()
    file.seek(0)
    return hash


def parse_file_id(file_id: str) -> tuple[str, str, str | None]:
    tokens = file_id.split("/")
    if len(tokens) != 2:
        raise Exception(f"Improperly formatted file_id: {file_id}")

    org, filename_with_hash = tokens

    hash, filename = filename_with_hash.split("-", 1)

    if len(hash) != 32:
        raise Exception(f"Improperly formatted file_id: {file_id}")

    return org, filename, hash


def read_files(file_ids: list[str]) -> dict[str, BytesIO]:
    response = requests.post(
        url=f"{be_host()}/download_files_bulk/",
        headers={"Authorization": _get_auth_token()},
        json={"file_ids": file_ids},
    )

    return {
        file["filename"]: BytesIO(base64.b64decode(file["content"]))
        for file in response.json()["files"]
    }


async def _download_file_async(file_id: str, client: httpx.AsyncClient):
    """Helper function to download a single file asynchronously"""
    response = await client.post(
        f"{be_host()}/download_files_bulk/",
        headers={"Authorization": _get_auth_token()},
        json={"file_ids": [file_id]},
    )

    if response.status_code != 200:
        raise Exception(f"Failed to download file {file_id}: {response.text}")

    result = response.json()["files"][0]

    result["file_id"] = file_id

    return result


async def _download_files_chunk_async(file_ids_chunk: list[str]):
    """Download a chunk of files asynchronously"""
    async with httpx.AsyncClient(timeout=60) as client:
        tasks = [_download_file_async(file_id, client) for file_id in file_ids_chunk]
        return await asyncio.gather(*tasks, return_exceptions=True)


async def download_files_bulk(
    files: list["File"],
    documents_download_path: str,
    max_concurrent_downloads: int = 50,
) -> dict[str, str]:
    """
    Download multiple files in parallel with a maximum of max_concurrent_downloads downloads at once.
    Process files as they are downloaded to minimize memory usage.

    Args:
        files: List of File objects to download
        download_path: Path where to save the downloaded files
        max_concurrent_downloads: Maximum number of concurrent downloads (default: 50)
    """
    if len(files) == 0:
        raise Exception("No files to download")

    file_id_to_file_path = {}
    os.makedirs(documents_download_path, exist_ok=True)

    # Pre-process files to identify duplicates by filename
    filename_count = defaultdict(set)
    for file in files:
        filename_count[file.file_name].add(file.hash)

    # Split files into chunks
    chunks = [
        files[i : i + max_concurrent_downloads]
        for i in range(0, len(files), max_concurrent_downloads)
    ]

    # Progress bar for the entire operation
    with tqdm(
        total=len(files), desc="Downloading and saving files", unit="file"
    ) as progress_bar:
        for chunk in chunks:
            # Download chunk of files
            chunk_results = await _download_files_chunk_async(
                [file.file_id for file in chunk]  # pyright: ignore[reportArgumentType]
            )

            # Process each result as it comes
            for i, result in enumerate(chunk_results):
                if isinstance(result, BaseException):
                    print(f"Error downloading {chunk[i]}: {result}")
                    progress_bar.update(1)
                    continue

                # Extract file info
                filename = result["filename"]
                hash = result["hash"]
                content = base64.b64decode(result["content"])

                # Determine file path - use hash directory if filename has duplicates
                file_path = os.path.join(documents_download_path, filename)
                relative_file_path = os.path.join(
                    os.path.basename(documents_download_path), filename
                )

                if len(filename_count[filename]) > 1 or os.path.exists(file_path):
                    hash_dir = os.path.join(documents_download_path, hash)
                    os.makedirs(hash_dir, exist_ok=True)
                    file_path = os.path.join(hash_dir, filename)
                    relative_file_path = os.path.join(
                        os.path.basename(documents_download_path), hash, filename
                    )

                # Write the file
                with open(file_path, "wb") as f:
                    f.write(content)

                file_id_to_file_path[result["file_id"]] = relative_file_path

                # Update progress
                progress_bar.update(1)

    progress_bar.close()

    return file_id_to_file_path


async def upload_file(file_path: str, temporary: bool = False) -> str:
    """Upload a file to the server asynchronously."""

    async with aiofiles.open(file_path, "rb") as f:
        file_data = await f.read()

    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("file", file_data, filename=os.path.basename(file_path))
        form.add_field("temporary", str(temporary).lower())

        async with session.post(
            f"{be_host()}/upload_file/",
            data=form,
            headers={"Authorization": _get_auth_token()},
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Failed to upload file {file_path}: {error_text}")

            response_json = await response.json()
            return response_json["file_id"]


async def dot_animation(stop_event: asyncio.Event):
    dots = [".    ", ". .  ", ". . ."]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write("\r" + dots[i % len(dots)])
        sys.stdout.flush()
        i += 1
        await asyncio.sleep(0.4)
    sys.stdout.write("\r" + " " * 10 + "\r")
    sys.stdout.flush()


def score_to_label(score: int, rubric: list[dict[str, Any]]) -> str | None:
    """Convert the given integer to the label from the rubric."""
    return next(
        (item["label"] for item in (rubric or []) if item["score"] == score),
        None,
    )


async def fetch_file_bytes(url: str) -> bytes:
    """
    Util specifically made to fetch a file from the server and return the bytes.

    Easier to handle than needing to create separate methods for different file types.
    """

    headers = {"Authorization": _get_auth_token()}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise ValsException(
                    f"Failed to fetch file from {url}: {await response.text()}"
                )

            return await response.read()


async def use_incremental_eval() -> bool:
    """
    Returns whether incremental eval is enabled.

    To disable, need to disable launchdarkly flag.
    """
    url = f"{be_host()}/use_incremental_eval"
    async with aiohttp.ClientSession() as session, session.get(url) as resp:
        resp.raise_for_status()
        payload = await resp.json()
        return bool(payload.get("enabled", True))
