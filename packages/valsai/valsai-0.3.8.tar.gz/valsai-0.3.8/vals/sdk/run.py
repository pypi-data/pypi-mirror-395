import asyncio
from datetime import datetime
import json
from typing import Any

from asyncstdlib import cached_property
from asyncstdlib.functools import CachedProperty
from pydantic import BaseModel, PrivateAttr

from vals.graphql_client import Client, RunFragmentCustomMetrics, RunFragment
from vals.graphql_client.enums import RunStatus
from vals.sdk.auth import be_host, fe_host
from vals.sdk.custom_metric import CustomMetric
from vals.sdk.run_review import SingleRunReview
from vals.sdk.types import (
    ModelCustomOperatorFunctionType,
    ModelFunctionType,
    QuestionAnswerPair,
    RunMetadata,
    RunParameters,
    Test,
    TestResult,
)
from vals.sdk.util import fetch_file_bytes, get_ariadne_client
import io
import pandas as pd


class Run(BaseModel):
    model_config = {"ignored_types": (CachedProperty,)}

    id: str
    """UUID assigned to the run at time of creation."""

    project_id: str
    """Slug of the project the run is associated with."""

    _project_uuid: str = PrivateAttr()
    """Internal project uuid for use in the SDK."""

    name: str
    """Name of the run, can be changed by the user."""

    status: RunStatus
    """Status of the run, refresh by doing `await run.refresh()`"""

    error_message: str | None
    """Error message for the run. Will only be present if the run failed."""

    qa_set_id: str
    """UUID assigned to the qa set at the time the run was created. Is used to group all question answer pairs associated with the run."""

    test_suite_id: str
    """UUID assigned to the test suite at the time the run was created."""

    test_suite_title: str
    """Title of the test suite. If the run name was not specified at run time, the test suite title will be used."""

    model: str
    """Model used to perform the run."""

    pass_rate: float | None
    """Percentage of checks that passed"""

    pass_rate_error: float | None
    """Error margin for pass rate"""

    success_rate: float | None
    """Number of tests where all checks passed"""

    success_rate_error: float | None
    """Error margin for success rate"""

    average_duration: float
    """
    Average duration to produce an answer to a test. 
    Will default to 0 if no test results have been produced
    """

    average_input_tokens: float
    """
    Average input tokens provided to the model under test during the run.
    Will default to 0 if no test results have been produced
    """

    average_output_tokens: float
    """
    Average output tokens produced by the model under test during the run. 
    Will default to 0 if no test results have been produced
    """

    custom_metrics: list[RunFragmentCustomMetrics]

    archived: bool
    """Whether the run has been archived"""

    text_summary: str
    """Automatically generated summary of common error modes for the run."""

    timestamp: datetime
    """Timestamp of when the run was created."""

    completed_at: datetime | None
    """Timestamp of when the run was completed."""

    parameters: RunParameters
    """Parameters used to create the run."""

    run_review_id: str | None
    """ID of the run review for the run."""

    _client: Client = PrivateAttr(default_factory=get_ariadne_client)

    @staticmethod
    async def _pull_test_results(
        run_id: str,
        client: Client,
        tags: list[str] = [],
        operators: list[str] = [],
        search: str = "",
    ) -> list[TestResult]:
        offset = 0
        page_size = 100
        test_results: list[TestResult] = []
        while True:
            test_result_query_result = await client.pull_test_results_with_count(
                run_id=run_id,
                offset=offset,
                limit=page_size,
                tags=tags,
                operators=operators,
                search=search,
            )

            test_results.extend(
                [
                    TestResult.model_validate(test_result.model_dump())
                    for test_result in test_result_query_result.test_results_with_count.test_results
                ]
            )

            offset += page_size

            total_count = test_result_query_result.test_results_with_count.count
            if len(test_results) >= total_count:
                break

        return test_results

    @classmethod
    def from_graphql(cls, graphql_run: RunFragment) -> "Run":
        # Map maximum_threads to parallelism for backwards compatibility
        parameters_dict: dict[str, Any] = graphql_run.parameters.model_dump()
        model = parameters_dict.pop("model_under_test", "")

        if "maximum_threads" in parameters_dict:
            parameters_dict["parallelism"] = parameters_dict.pop("maximum_threads")
        parameters = RunParameters(**parameters_dict)

        run_review_id = None
        if graphql_run.run_review:
            run_review_id = graphql_run.run_review.id

        run = Run(
            id=graphql_run.run_id,
            run_review_id=run_review_id,
            project_id=graphql_run.project.slug,
            name=graphql_run.name,
            status=graphql_run.status,
            error_message=graphql_run.error_message
            if graphql_run.error_message
            else None,
            qa_set_id=graphql_run.qa_set.id,
            model=model,
            pass_rate=graphql_run.pass_rate.value if graphql_run.pass_rate else None,
            pass_rate_error=(
                graphql_run.pass_rate.error if graphql_run.pass_rate else None
            ),
            success_rate=(
                graphql_run.success_rate.value if graphql_run.success_rate else None
            ),
            success_rate_error=(
                graphql_run.success_rate.error if graphql_run.success_rate else None
            ),
            custom_metrics=graphql_run.custom_metrics,
            archived=graphql_run.archived,
            text_summary=graphql_run.text_summary,
            timestamp=graphql_run.timestamp,
            completed_at=graphql_run.completed_at,
            parameters=parameters,
            test_suite_title=graphql_run.test_suite.title,
            test_suite_id=graphql_run.test_suite.id,
            average_duration=graphql_run.average_duration,
            average_input_tokens=graphql_run.average_tokens_in,
            average_output_tokens=graphql_run.average_tokens_out,
        )

        run._project_uuid = graphql_run.project.id

        return run

    @staticmethod
    async def _create_from_pull_result(run_id: str, client: Client) -> "Run":
        """Helper method to create a Run instance from a pull_run query result"""

        result = await client.pull_run(run_id)

        return Run.from_graphql(result.run)

    @classmethod
    async def list_runs(
        cls,
        limit: int = 25,
        offset: int = 0,
        suite_id: str | None = None,
        show_archived: bool = False,
        model_under_test: str | list[str] = [],
        status: RunStatus | list[RunStatus] = [],
        search: str = "",
        project_id: str = "default-project",
    ) -> list["RunMetadata"]:
        """List runs associated with this organization

        Args:
            limit: Maximum number of runs to return
            offset: Number of runs to skip
            suite_id: Filter by specific suite ID
            show_archived: Include archived runs
            search: Search string for filtering runs
            project_id: Optional project ID to filter runs by project
        """
        client = get_ariadne_client()

        result = await client.list_runs(
            limit=limit,
            offset=offset,
            suite_id=suite_id,
            archived=show_archived,
            search=search,
            project_id=project_id,
            model_under_test=[model_under_test]
            if isinstance(model_under_test, str)
            else model_under_test,
            status=[status] if isinstance(status, RunStatus) else status,
        )
        return [
            RunMetadata.from_graphql(run) for run in result.runs_with_count.run_results
        ]

    @property
    def url(self) -> str:
        return f"{fe_host()}/project/{self.project_id}/results/{self.id}"

    @classmethod
    async def from_id(cls, run_id: str) -> "Run":
        """Pull most recent metadata and test results from the vals servers."""
        client = get_ariadne_client()

        return await cls._create_from_pull_result(run_id, client)

    async def refresh(self) -> None:
        """Refreshes the latest information from the server and updates the current instance."""
        updated_run = await self._create_from_pull_result(self.id, self._client)

        for field_name in Run.model_fields:
            setattr(self, field_name, getattr(updated_run, field_name))

    async def fetch_test_results(
        self, tags: list[str] = [], operators: list[str] = [], search: str = ""
    ) -> list[TestResult]:
        """Search method that allows for server side filtering. Use to speed up searches across large runs."""
        return await self._pull_test_results(
            self.id, self._client, tags, operators, search
        )

    @cached_property
    async def test_results(self) -> list["TestResult"]:
        """Lazy loaded property that fetches the test results in batches of 200 from the server each time it is requested.

        ```python
        run = await Run.from_id(run_id)

        # Pulled on request, cached until cleared
        test_results = await run.test_results

        # Clear the cache
        del run.test_results

        # Refetch the test results
        test_results = await run.test_results
        ```

        """
        return await self._pull_test_results(self.id, self._client)

    @cached_property
    async def qa_pairs(self) -> list[QuestionAnswerPair]:
        """
        Lazy loaded property that fetches the qa pairs in batches of 200 from the server each time it is requested.

        ```python
        run = await Run.from_id(run_id)

        # Pulled on request, cached until cleared
        qa_pairs = await run.qa_pairs

        # Clear the cache
        del run.qa_pairs

        # Refetch the qa pairs
        qa_pairs = await run.qa_pairs
        ```

        """
        qa_pairs = []
        current_offset = 0
        batch_size = 200

        if self.qa_set_id is None:
            raise ValueError(
                "This run has no qa set associated with it, please ensure that the run has been created before fetching qa pairs."
            )

        while True:
            result = await self._client.list_question_answer_pairs(
                qa_set_id=self.qa_set_id,  # pyright: ignore[reportArgumentType]
                offset=current_offset,
                limit=batch_size,
            )

            batch_results = [
                QuestionAnswerPair.from_graphql(graphql_qa_pair)
                for graphql_qa_pair in result.question_answer_pairs_with_count.question_answer_pairs
            ]

            qa_pairs.extend(batch_results)

            if len(batch_results) < batch_size:
                break

            current_offset += batch_size

        return qa_pairs

    async def wait_for_run_completion(
        self,
    ) -> RunStatus:
        """
        Block a process until a given run has finished running.

        Returns the status of the run after completion.
        """
        await asyncio.sleep(1)

        completed_statuses = [
            RunStatus.SUCCESS,
            RunStatus.ERROR,
            RunStatus.CANCELLED,
            RunStatus.PAUSE,
        ]

        while self.status not in completed_statuses:
            await asyncio.sleep(3)  # Poll every 3 seconds

            await self.refresh()

        return self.status

    async def fetch_csv(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns a tuple of two DataFrames: the run result and the test results.

        These dataframes are not valid stacked, in order to export as a single CSV, you will need to concatenate them.

        ```python
        run_result_df, test_results_df = await run.fetch_csv()

        combined = run_result_df.to_csv(index=False) + "\\n" + test_results_df.to_csv(index=False)

        with open("path/to/run.csv", "w") as f:
            f.write(combined)
        ```

        """
        csv_bytes = await fetch_file_bytes(
            f"{be_host()}/export_results_to_file/?run_id={self.id}"
        )

        decoded_csv = csv_bytes.decode("utf-8")
        lines = decoded_csv.split("\n")

        run_result_df = pd.read_csv(io.StringIO("\n".join(lines[:2])), engine="python")

        test_results_df = pd.read_csv(
            io.StringIO("\n".join(lines[2:])), engine="python"
        )

        return run_result_df, test_results_df

    async def fetch_json(self) -> dict[str, Any]:
        json_bytes = await fetch_file_bytes(
            f"{be_host()}/export_run_to_json/?run_id={self.id}"
        )

        decoded_json = json_bytes.decode("utf-8")

        return json.loads(decoded_json)

    async def retry_failing_tests(self) -> None:
        """Retry all failing tests in a run."""

        await self._client.rerun_tests(run_id=self.id)

    async def resume_run(
        self,
        model: str | ModelFunctionType | list[QuestionAnswerPair] | None = None,
        wait_for_completion: bool = False,
        upload_concurrency: int = 3,
        custom_operators: list[ModelCustomOperatorFunctionType] | None = None,
        parallelism: int | None = None,
    ) -> None:
        """Resume a run that was paused.

        This method will:
        1. Check for existing QA pairs that haven't been auto-evaluated
        2. Check for existing completed test results
        3. Run the remaining tests that haven't been processed yet
        """

        if model is None:
            model = self.model

        if custom_operators is None:
            custom_operators = []

        if parallelism is not None:
            self.parameters.parallelism = parallelism

        from vals.sdk.suite import Suite

        suite = await Suite.from_id(self.test_suite_id)

        query_result = await self._client.unfinished_tests(run_id=self.id)
        unfinished_tests = [
            Test.model_validate(test.model_dump())
            for test in query_result.unfinished_tests.unfinished_tests
        ]

        # Run the remaining tests, including existing QA pairs
        await self._client.update_run_status(
            run_id=self.id, status=RunStatus.IN_PROGRESS
        )

        await suite.run(
            model=model,
            model_name=self.model,
            run_name=self.name,
            wait_for_completion=wait_for_completion,
            parameters=self.parameters,
            upload_concurrency=upload_concurrency,
            custom_operators=custom_operators or [],
            eval_model_name=self.parameters.eval_model,
            run_id=self.id,
            qa_set_id=self.qa_set_id,
            remaining_tests=unfinished_tests,
            uploaded_qa_pairs=await self.qa_pairs,
        )

    async def pause_run(self):
        """Pause run."""
        result = await self._client.stop_run(run_id=self.id, status=RunStatus.PAUSE)
        if result.stop_run and not result.stop_run.success:
            raise Exception(f"Failed to pause run {self.id}")

    async def cancel_run(self):
        """Cancel run."""
        result = await self._client.stop_run(run_id=self.id, status=RunStatus.CANCELLED)
        if result.stop_run and not result.stop_run.success:
            raise Exception(f"Failed to cancel run {self.id}")

    async def rerun_all_checks(self, parameters: RunParameters | None = None) -> "Run":
        """
        Rerun all checks for a run, using existing QA pairs.
        returns a new Run object, rather than modifying the existing one.
        """

        if not parameters:
            parameters = self.parameters

        qa_pairs = await self.qa_pairs
        from vals.sdk.suite import Suite

        suite = await Suite.from_id(self.test_suite_id)
        return await suite.run(qa_pairs, parameters=parameters)

    @cached_property
    async def review(self) -> SingleRunReview:
        """
        Get the review for a run.

        Will raise a ValueError if no review has been created for the run.
        """
        review_id = self.run_review_id
        project_id = self.project_id

        if review_id is None:
            raise ValueError(
                "No run review has been created for this run. Please start the review process before trying to get the review."
            )

        return await SingleRunReview.from_id(review_id, project_id)

    async def update_custom_metric(
        self,
        local: bool,
        custom_metric_result: float,
        custom_metric_id: str | None = None,
        custom_metric_name: str | None = None,
    ) -> str:
        """
        Update the result of a custom metric for a run.
        """

        result = await CustomMetric.update_custom_metric_result(
            run_id=self.id,
            local=local,
            custom_metric_result=custom_metric_result,
            custom_metric_id=custom_metric_id,
            custom_metric_name=custom_metric_name,
        )

        return result
