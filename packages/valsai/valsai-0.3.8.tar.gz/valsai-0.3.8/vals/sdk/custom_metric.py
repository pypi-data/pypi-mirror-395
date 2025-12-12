import asyncio
import inspect
import json
from typing import Awaitable, Callable, Literal

import pandas as pd
from pydantic import BaseModel, PrivateAttr

from vals.graphql_client import Client
from vals.sdk.util import dot_animation, get_ariadne_client, upload_file


class CustomMetric(BaseModel):
    """Represents a custom metric in the vals platform."""

    # server only
    _id: str | None = None
    _archived: bool | None = None
    _file_id: str | None = None

    # user can provide
    project_id: str
    name: str
    python_file_path: str | Literal["vals"]
    description: str | None = None

    _client: Client = PrivateAttr(default_factory=get_ariadne_client)

    def __init__(
        self,
        name: str,
        python_file_path: str | Literal["vals"],
        project_id: str = "default-project",
        description: str | None = None,
    ):
        """
        Create a new custom metric locally. Not uploaded to the server yet.
        """
        super().__init__(
            project_id=project_id,
            name=name,
            python_file_path=python_file_path,
            description=description,
        )

    @property
    def id(self) -> str:
        if self._id is None:
            raise Exception("Custom metric does not exist.")
        return self._id

    @classmethod
    async def from_id(cls, id: str) -> "CustomMetric":
        """
        Get a custom metric from the server by ID
        """
        client = get_ariadne_client()
        result = await client.get_custom_metric(id=id)

        custom_metric = cls(
            name=result.custom_metric.name,
            description=result.custom_metric.description,
            python_file_path="vals",
        )
        custom_metric._id = result.custom_metric.id
        custom_metric.project_id = result.custom_metric.project.slug
        custom_metric._archived = result.custom_metric.archived
        custom_metric._file_id = result.custom_metric.file_id

        return custom_metric

    async def pull(self) -> None:
        """
        Refresh this CustomMetric instance with the latest data from the server.
        """
        if not self._id:
            raise Exception("Custom metric does not exist.")

        updated = await self.__class__.from_id(self._id)
        self.__dict__.update(updated.__dict__)

    async def create(self) -> str:
        """
        Create this custom metric on the server.
        Returns the ID of the custom metric.
        """
        if self._id:
            raise Exception("Custom metric already exists.")

        self._file_id = await upload_file(self.python_file_path, temporary=True)

        result = await self._client.upsert_custom_metric(
            id=None,
            project_id=self.project_id,
            name=self.name,
            description=self.description,
            file_id=self._file_id,
            update_past=False,
        )
        metric = result.upsert_custom_metric
        if not metric:
            raise Exception("Unable to create custom metric.")

        self._id = str(metric.metric.id)
        return self._id

    async def update(self, update_past: bool = False) -> None:
        """
        Update this custom metric on the server
        """
        if not self._id or not self._file_id:
            raise Exception("Custom metric does not exist.")
        if self._archived:
            raise Exception("Custom metric is archived.")

        if self.python_file_path != "vals":
            self._file_id = await upload_file(self.python_file_path)

        result = await self._client.upsert_custom_metric(
            id=self._id,
            project_id=self.project_id,
            name=self.name,
            description=self.description,
            file_id=self._file_id,
            update_past=update_past,
        )
        if not result.upsert_custom_metric:
            raise Exception("Unable to update custom metric.")

    async def archive(self) -> None:
        """
        Archive this custom metric on the server
        """
        if not self._id:
            raise Exception("Custom metric does not exist.")
        if self._archived:
            raise Exception("Custom metric is already archived.")

        result = await self._client.set_archived_status_custom_metrics([self._id], True)
        if not result.set_archived_status_custom_metrics:
            raise Exception("Unable to archive custom metric.")
        self._archived = True

    async def restore(self) -> None:
        """
        Restore this custom metric on the server
        """
        if not self._id:
            raise Exception("Custom metric does not exist.")
        if not self._archived:
            raise Exception("Custom metric is not archived.")

        result = await self._client.set_archived_status_custom_metrics(
            [self._id], False
        )
        if not result.set_archived_status_custom_metrics:
            raise Exception("Unable to restore custom metric.")
        self._archived = False

    async def run(self, run_id: str, persist: bool = False) -> str:
        """
        Run this custom metric on a run.
        Starts the custom metric task and polls until completion.
        """
        if not self._id or not self._file_id:
            raise Exception("This custom metric does not exist.")

        result = await self._client.start_custom_metric_task(
            run_id=run_id,
            file_id=self._file_id,
        )
        if not result.start_custom_metric_task:
            raise Exception("Unable to run custom metric.")

        message_id = result.start_custom_metric_task.message_id
        if not message_id:
            raise Exception("Unable to poll custom metric.")

        stop_event = asyncio.Event()
        animation_task = asyncio.create_task(dot_animation(stop_event))
        try:
            while True:
                result = await self._client.poll_custom_metric_task(message_id)
                if not result.poll_custom_metric_task:
                    raise Exception("Unable to poll custom metric.")

                response = result.poll_custom_metric_task
                match response.status:
                    case "pending":
                        await asyncio.sleep(3)
                        continue
                    case "success":
                        try:
                            if not response.result:
                                raise Exception("No result found.")
                            response_dict = json.loads(response.result)
                            value = float(response_dict[self._file_id][run_id])

                            if persist:
                                await self.update_custom_metric_result(
                                    run_id,
                                    local=False,
                                    custom_metric_result=value,
                                    custom_metric_id=self._id,
                                )

                            return f"{value:.2f}"
                        except Exception as e:
                            raise Exception(f"Failed to parse result: {e}")
                    case "fail":
                        raise Exception(
                            f"Error running custom metric: {response.error}"
                        )
                    case _:
                        raise Exception(f"Unknown status: {response.status}")
        finally:
            stop_event.set()
            await animation_task

    @staticmethod
    async def _get_run_dataframe(run_id: str) -> pd.DataFrame:
        """Get a dataframe of the run results."""
        client = get_ariadne_client()
        result = await client.get_run_dataframe(run_id=run_id)
        rows = result.get_run_dataframe
        if not rows:
            raise Exception(
                "Failed to get run dataframe, ensure the run exists and was successfull."
            )

        # Convert each GraphQL object to a dict
        parsed_rows = []
        for row in rows:
            row_dict = row.__dict__.copy()

            # Convert stringified JSON to actual dict
            modifiers = json.loads(row_dict.get("modifiers", "{}"))
            row_dict.pop("modifiers", None)  # Remove the JSON string
            row_dict.update(
                {f"modifiers.{k}": v for k, v in modifiers.items()}
            )  # Flatten

            # Convert input/output_context from string to dict
            for context_field in ["input_context", "output_context"]:
                if context_field in row_dict:
                    try:
                        row_dict[context_field] = json.loads(row_dict[context_field])
                    except json.JSONDecodeError:
                        row_dict[context_field] = {}

            parsed_rows.append(row_dict)

        df = pd.DataFrame(parsed_rows)
        return df

    @classmethod
    async def update_custom_metric_result(
        cls,
        run_id: str,
        local: bool,
        custom_metric_result: float,
        custom_metric_id: str | None = None,
        custom_metric_name: str | None = None,
    ) -> str:
        """
        Update the result of a custom metric for a run.
        """
        client = get_ariadne_client()

        result = await client.update_custom_metric_result(
            run_id=run_id,
            local=local,
            custom_metric_result=custom_metric_result,
            custom_metric_id=custom_metric_id,
            custom_metric_name=custom_metric_name,
        )

        if not result.update_custom_metric_result:
            raise Exception(f"Failed to update custom metric result for run {run_id}")

        return result.update_custom_metric_result.id

    @classmethod
    async def run_local(
        cls,
        run_id: str,
        name: str,
        function: Callable[[pd.DataFrame], float]
        | Callable[[pd.DataFrame], Awaitable[float]],
        persist: bool = False,
    ):
        df = await cls._get_run_dataframe(run_id)

        result = function(df)
        # Await if it's async
        if inspect.isawaitable(result):
            result = await result

        if persist:
            _ = await cls.update_custom_metric_result(
                run_id,
                local=True,
                custom_metric_result=result,
                custom_metric_name=name,
            )
            # TODO: maybe use id
        return result
