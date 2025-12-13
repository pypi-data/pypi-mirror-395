import datetime as dt
import io
import json
import zipfile
from pathlib import Path
from typing import Any, Literal

import httpx
import polars as pl
from bayesline.api import AsyncTask, Task, TaskResponse
from bayesline.api.equity import (
    AsyncDataTypeUploaderApi,
    AsyncUploaderApi,
    AsyncUploadersApi,
    AsyncUploadParserApi,
    DataTypeUploaderApi,
    MultiParserResult,
    UploadCommitResult,
    UploaderApi,
    UploadError,
    UploadersApi,
    UploadParserApi,
    UploadParserResult,
    UploadStagingResult,
)
from bayesline.api.types import DNFFilterExpressions, DnfFilterExpressions

from bayesline.apiclient._src.apiclient import (
    ApiClient,
    AsyncApiClient,
    TqdmContentStreamer,
    TqdmFileReader,
)
from bayesline.apiclient._src.tasks import (
    AsyncDataFrameDictTaskClient,
    AsyncDataFrameTaskClient,
    AsyncLazyFrameTaskClient,
    AsyncPydanticTaskClient,
    DataFrameDictTaskClient,
    DataFrameTaskClient,
    LazyFrameTaskClient,
    PydanticTaskClient,
    as_blocking,
    async_as_blocking,
)
from bayesline.apiclient._src.types import polars_json_to_dtype

_EXCEPTION_TYPES = [UploadError]


def _raise_for_status(response: httpx.Response) -> None:  # noqa: C901
    if response.status_code in {200, 202}:
        return

    def _unescape(s: str) -> str:
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            return s

    exc: Exception | None = None
    try:
        details = response.json()["detail"]
        if "type" in details:
            if details["type"] == "KeyError":
                exc = KeyError(_unescape(details["message"]))
            elif details["type"] == "ValueError":
                exc = ValueError(_unescape(details["message"]))
            elif details["type"] == "UploadError":
                exc = UploadError(_unescape(details["message"]))
    except (KeyError, ValueError, json.JSONDecodeError):
        # If we can't parse the response, fall back to default behavior
        pass

    if exc:
        raise exc

    response.raise_for_status()


class AsyncUploadParserClientImpl(AsyncUploadParserApi):

    def __init__(
        self, client: AsyncApiClient, parser_name: str, tqdm_progress: bool = False
    ):
        self._client = client.append_base_path(parser_name)
        self._parser_name = parser_name
        self._tqdm_progress = tqdm_progress

    @property
    def name(self) -> str:
        return self._parser_name

    async def output_schema(self) -> dict[str, pl.DataType]:
        return {
            k: polars_json_to_dtype(v)
            for k, v in (await self._client.get("output-schema")).json().items()
        }

    async def get_examples(self) -> list[pl.DataFrame]:
        response = await self._client.options("")
        raw = await response.aread()
        result = []
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for filename in zf.namelist():
                with zf.open(filename) as fileobj:
                    df = pl.read_parquet(fileobj)
                    result.append(df)
        return result

    async def can_handle(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> UploadParserResult:
        params = {}
        if name:
            params["name"] = name
        out = io.BytesIO()
        raw_df.write_parquet(out)
        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = await self._client.post(
                    "can-handle", body=stream, params=params
                )
        else:
            response = await self._client.post(
                "can-handle", body=out.getvalue(), params=params
            )
        return UploadParserResult.model_validate(response.json())

    async def parse(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> tuple[pl.DataFrame, UploadParserResult]:
        params = {}
        if name:
            params["name"] = name
        out = io.BytesIO()
        raw_df.write_parquet(out)
        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = await self._client.post("", body=stream, params=params)
        else:
            response = await self._client.post("", body=out.getvalue(), params=params)
        result = UploadParserResult.model_validate_json(response.headers["X-Metadata"])
        df = pl.read_parquet(io.BytesIO(response.content))
        return df, result


class AsyncUploaderClientImpl(AsyncUploaderApi):

    def __init__(
        self, client: AsyncApiClient, tasks_client: AsyncApiClient, tqdm_progress: bool
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress

    async def get_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        params = {"which": which}
        return {
            k: polars_json_to_dtype(v)
            for k, v in (await self._client.get("schema", params=params)).json().items()
        }

    async def get_summary_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        params = {"which": which}
        return {
            k: polars_json_to_dtype(v)
            for k, v in (await self._client.get("summary-schema", params=params))
            .json()
            .items()
        }

    async def get_detail_summary_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        params = {"which": which}
        return {
            k: polars_json_to_dtype(v)
            for k, v in (await self._client.get("detail-summary-schema", params=params))
            .json()
            .items()
        }

    async def get_commit_modes(self) -> dict[str, str]:
        return (await self._client.get("commit-modes")).json()

    async def get_parser_names(self) -> list[str]:
        return (await self._client.get("parsers")).json()

    async def get_parser(self, parser: str) -> AsyncUploadParserApi:
        if parser not in (parsers := await self.get_parser_names()):
            raise KeyError(f"Parser '{parser}' not found. Have {parsers}")
        return AsyncUploadParserClientImpl(
            self._client.append_base_path("parsers"), parser, self._tqdm_progress
        )

    async def can_handle(
        self, df: pl.DataFrame, *, parser: str | None = None, name: str | None = None
    ) -> MultiParserResult:
        out = io.BytesIO()
        df.write_parquet(out)
        params = {}
        if parser:
            params["parser"] = parser
        if name:
            params["name"] = name

        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = await self._client.post(
                    "can-handle", body=stream, params=params
                )
        else:
            response = await self._client.post(
                "can-handle", body=out.getvalue(), params=params
            )

        return MultiParserResult.model_validate(response.json())

    async def stage_df_as_task(
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> AsyncTask[UploadStagingResult]:
        out = io.BytesIO()
        df.write_parquet(out)
        params = {"name": name, "replace": replace}
        if parser:
            params["parser"] = parser

        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = await self._client.post("stage", body=stream, params=params)
        else:
            response = await self._client.post(
                "stage", body=out.getvalue(), params=params
            )

        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncPydanticTaskClient(
            UploadStagingResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=stage_df_as_task)
    async def stage_df(
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult:
        raise NotImplementedError()

    async def stage_file_as_task(
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> AsyncTask[UploadStagingResult]:
        params = {"name": name, "replace": replace}
        if parser:
            params["parser"] = parser

        files: dict[str, Any]
        if self._tqdm_progress:
            with TqdmFileReader(path) as f:
                files = {"file": f}
                response = await self._client.post(
                    "stage-file", body=None, files=files, params=params
                )
        else:
            with path.open("rb") as f:
                files = {"file": f}
                response = await self._client.post(
                    "stage-file", body=None, files=files, params=params
                )

        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncPydanticTaskClient(
            UploadStagingResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=stage_file_as_task)
    async def stage_file(
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult:
        raise NotImplementedError()

    async def get_staging_results(
        self, names: list[str] | None = None
    ) -> dict[str, UploadStagingResult]:
        params = {}
        if names:
            params["names"] = names
        response = await self._client.get("staging-results", params=params)
        return {
            k: UploadStagingResult.model_validate(v) for k, v in response.json().items()
        }

    async def wipe_staging(
        self,
        names: list[str] | None = None,
    ) -> dict[str, UploadStagingResult]:
        params = {}
        if names:
            params["names"] = names
        response = await self._client.delete("staging", params=params)
        _raise_for_status(response)
        return {
            k: UploadStagingResult.model_validate(v) for k, v in response.json().items()
        }

    async def get_staging_data_as_task(
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> AsyncTask[pl.LazyFrame]:
        params: dict[str, Any] = {"unique": unique}
        if columns:
            params["columns"] = columns
        if names:
            params["names"] = names
        response = await self._client.get("staging-data", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncLazyFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=get_staging_data_as_task)
    async def get_staging_data(
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> pl.LazyFrame:
        raise NotImplementedError()

    async def get_staging_data_summary_as_task(
        self, names: list[str] | None = None
    ) -> AsyncTask[pl.DataFrame]:
        params = {}
        if names:
            params["names"] = names
        response = await self._client.get("staging-data-summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=get_staging_data_summary_as_task)
    async def get_staging_data_summary(
        self, names: list[str] | None = None
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def get_staging_data_detail_summary_as_task(
        self, names: list[str] | None = None
    ) -> AsyncTask[pl.DataFrame]:
        params = {}
        if names:
            params["names"] = names
        response = await self._client.get("staging-data-detail-summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=get_staging_data_detail_summary_as_task)
    async def get_staging_data_detail_summary(
        self, names: list[str] | None = None
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def validate_staging_data_as_task(
        self, names: list[str] | None = None, short: bool = False
    ) -> AsyncTask[dict[str, pl.DataFrame]]:
        params: dict[str, Any] = {"short": short}
        if names:
            params["names"] = names
        response = await self._client.get("validate-staging-data", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDataFrameDictTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=validate_staging_data_as_task)
    async def validate_staging_data(
        self, names: list[str] | None = None, short: bool = False
    ) -> dict[str, pl.DataFrame]:
        raise NotImplementedError()

    async def commit_as_task(
        self, mode: str, names: list[str] | None = None
    ) -> AsyncTask[UploadCommitResult]:
        params: dict[str, Any] = {"mode": mode}
        if names:
            params["names"] = names
        response = await self._client.post("commit", body={}, params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncPydanticTaskClient(
            UploadCommitResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=commit_as_task)
    async def commit(
        self, mode: str, names: list[str] | None = None
    ) -> UploadCommitResult:
        raise NotImplementedError()

    async def fast_commit_as_task(
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> AsyncTask[UploadCommitResult]:
        params = {"mode": mode}
        if parser:
            params["parser"] = parser

        if isinstance(df, Path):
            files: dict[str, Any]
            if self._tqdm_progress:
                with TqdmFileReader(df) as f:
                    files = {"file": f}
                    response = await self._client.post(
                        "fast-commit-file", body=None, files=files, params=params
                    )
            else:
                with df.open("rb") as f:
                    files = {"file": f}
                    response = await self._client.post(
                        "fast-commit-file", body=None, files=files, params=params
                    )
        else:
            out = io.BytesIO()
            df.write_parquet(out)

            if self._tqdm_progress:
                with TqdmContentStreamer(out.getvalue()) as stream:
                    response = await self._client.post(
                        "fast-commit", body=stream, params=params
                    )
            else:
                response = await self._client.post(
                    "fast-commit", body=out.getvalue(), params=params
                )

        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncPydanticTaskClient(
            UploadCommitResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=fast_commit_as_task)
    async def fast_commit(
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> UploadCommitResult:
        raise NotImplementedError()

    async def get_data_as_task(  # noqa: C901
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> AsyncTask[pl.LazyFrame]:
        download_file_path: Path | None = None
        if download_to is not None:
            if isinstance(download_to, str):
                download_to = Path(download_to)
            if not download_to.exists():
                raise FileNotFoundError(
                    f"Download directory {download_to} does not exist"
                )
            if download_to.is_file():
                raise FileExistsError(
                    f"Download directory {download_to} must be a directory"
                )

            download_file_path = download_to / download_filename
            if "{i}" not in download_filename:
                raise ValueError("download_filename must contain the placeholder {i}")

        params: dict[str, Any] = {}
        body: dict[str, Any] = {"unique": unique}
        if columns:
            body["columns"] = columns

        if filters:
            body["filters"] = DnfFilterExpressions.from_dnf(filters).model_dump()

        if version is not None:
            params["version"] = version

        if head is not None:
            params["head"] = head

        response = await self._client.post("data", params=params, body=body)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncLazyFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
            out_path=download_file_path,
        )

    @async_as_blocking(task_func=get_data_as_task)
    async def get_data(
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> pl.LazyFrame:
        raise NotImplementedError()

    async def get_data_summary_as_task(
        self, version: int | dt.datetime | None = None
    ) -> AsyncTask[pl.DataFrame]:
        params = {}
        if version is not None:
            params["version"] = version
        response = await self._client.get("summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=get_data_summary_as_task)
    async def get_data_summary(
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def get_data_detail_summary_as_task(
        self, version: int | dt.datetime | None = None
    ) -> AsyncTask[pl.DataFrame]:
        params = {}
        if version is not None:
            params["version"] = version
        response = await self._client.get("detail-summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @async_as_blocking(task_func=get_data_detail_summary_as_task)
    async def get_data_detail_summary(
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def destroy(self) -> None:
        response = await self._client.delete("")
        if response.status_code != 200:
            raise Exception(f"Could not destroy dataset. {str(response.content)}")

    async def version_history(self) -> dict[int, dt.datetime]:
        return {
            int(k): dt.datetime.fromisoformat(v).astimezone(dt.UTC)
            for k, v in (await self._client.get("version-history")).json().items()
        }


class AsyncDataTypeUploaderClientImpl(AsyncDataTypeUploaderApi):

    def __init__(
        self, client: AsyncApiClient, tasks_client: AsyncApiClient, tqdm_progress: bool
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress

    async def get_datasets(self) -> list[str]:
        return (await self._client.get("")).json()

    async def get_dataset(self, dataset: str) -> AsyncUploaderApi:
        if dataset not in (datasets := await self.get_datasets()):
            raise KeyError(
                f"Dataset '{dataset}' not found. Available datasets: {datasets}"
            )
        return AsyncUploaderClientImpl(
            self._client.append_base_path(dataset),
            self._tasks_client,
            self._tqdm_progress,
        )

    async def create_dataset(self, dataset: str) -> AsyncUploaderApi:
        if dataset in await self.get_datasets():
            raise ValueError(f"Dataset '{dataset}' already exists")
        await self._client.post(dataset, body={})
        return AsyncUploaderClientImpl(
            self._client.append_base_path(dataset),
            self._tasks_client,
            self._tqdm_progress,
        )


class AsyncUploadersClientImpl(AsyncUploadersApi):

    def __init__(
        self, client: AsyncApiClient, tasks_client: AsyncApiClient, tqdm_progress: bool
    ):
        self._client = client.append_base_path("uploaders")
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress

    async def get_data_types(self) -> list[str]:
        return (await self._client.get("")).json()

    async def get_data_type(self, data_type: str) -> AsyncDataTypeUploaderApi:
        if data_type not in (data_types := await self.get_data_types()):
            raise KeyError(
                f"Data type '{data_type}' not found. Available data types: {data_types}"
            )
        return AsyncDataTypeUploaderClientImpl(
            self._client.append_base_path(data_type),
            self._tasks_client,
            self._tqdm_progress,
        )


class UploadParserClientImpl(UploadParserApi):

    def __init__(
        self, client: ApiClient, parser_name: str, tqdm_progress: bool = False
    ):
        self._client = client.append_base_path(parser_name)
        self._parser_name = parser_name
        self._tqdm_progress = tqdm_progress

    @property
    def name(self) -> str:
        return self._parser_name

    def output_schema(self) -> dict[str, pl.DataType]:
        return {
            k: polars_json_to_dtype(v)
            for k, v in (self._client.get("output-schema")).json().items()
        }

    def get_examples(self) -> list[pl.DataFrame]:
        response = self._client.options("")
        raw = response.read()
        result = []
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for filename in zf.namelist():
                with zf.open(filename) as fileobj:
                    df = pl.read_parquet(fileobj)
                    result.append(df)
        return result

    def can_handle(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> UploadParserResult:
        out = io.BytesIO()
        raw_df.write_parquet(out)
        params = {}
        if name:
            params["name"] = name

        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = self._client.post("can-handle", body=stream, params=params)
        else:
            response = self._client.post(
                "can-handle", body=out.getvalue(), params=params
            )

        return UploadParserResult.model_validate(response.json())

    def parse(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> tuple[pl.DataFrame, UploadParserResult]:
        out = io.BytesIO()
        raw_df.write_parquet(out)
        params = {}
        if name:
            params["name"] = name

        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = self._client.post("", body=stream, params=params)
        else:
            response = self._client.post("", body=out.getvalue(), params=params)

        result = UploadParserResult.model_validate_json(response.headers["X-Metadata"])
        df = pl.read_parquet(io.BytesIO(response.content))
        return df, result


class UploaderClientImpl(UploaderApi):

    def __init__(
        self,
        client: ApiClient,
        tasks_client: ApiClient,
        tqdm_progress: bool,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress

    def get_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        params = {"which": which}
        return {
            k: polars_json_to_dtype(v)
            for k, v in self._client.get("schema", params=params).json().items()
        }

    def get_summary_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        params = {"which": which}
        return {
            k: polars_json_to_dtype(v)
            for k, v in self._client.get("summary-schema", params=params).json().items()
        }

    def get_detail_summary_schema(
        self, which: Literal["data", "staging"] = "data"
    ) -> dict[str, pl.DataType]:
        params = {"which": which}
        return {
            k: polars_json_to_dtype(v)
            for k, v in self._client.get("detail-summary-schema", params=params)
            .json()
            .items()
        }

    def get_commit_modes(self) -> dict[str, str]:
        return self._client.get("commit-modes").json()

    def get_parser_names(self) -> list[str]:
        return self._client.get("parsers").json()

    def get_parser(self, parser: str) -> UploadParserApi:
        if parser not in (parsers := self.get_parser_names()):
            raise KeyError(f"Parser '{parser}' not found. Have {parsers}")
        return UploadParserClientImpl(
            self._client.append_base_path("parsers"), parser, self._tqdm_progress
        )

    def can_handle(
        self, df: pl.DataFrame, *, parser: str | None = None, name: str | None = None
    ) -> MultiParserResult:
        out = io.BytesIO()
        df.write_parquet(out)
        params = {}
        if parser:
            params["parser"] = parser
        if name:
            params["name"] = name

        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = self._client.post("can-handle", body=stream, params=params)
        else:
            response = self._client.post(
                "can-handle", body=out.getvalue(), params=params
            )

        return MultiParserResult.model_validate(response.json())

    def stage_df_as_task(
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> Task[UploadStagingResult]:
        out = io.BytesIO()
        df.write_parquet(out)
        params = {"name": name, "replace": replace}
        if parser:
            params["parser"] = parser

        if self._tqdm_progress:
            with TqdmContentStreamer(out.getvalue()) as stream:
                response = self._client.post("stage", body=stream, params=params)
        else:
            response = self._client.post("stage", body=out.getvalue(), params=params)

        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return PydanticTaskClient(
            UploadStagingResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=stage_df_as_task)
    def stage_df(
        self,
        name: str,
        df: pl.DataFrame,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult:
        raise NotImplementedError()

    def stage_file_as_task(
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> Task[UploadStagingResult]:
        params = {"name": name, "replace": replace}

        if parser:
            params["parser"] = parser

        files: dict[str, Any]
        if self._tqdm_progress:
            with TqdmFileReader(path) as f:
                files = {"file": f}
                response = self._client.post(
                    "stage-file", body=None, files=files, params=params
                )
        else:
            with path.open("rb") as f:
                files = {"file": f}
                response = self._client.post(
                    "stage-file", body=None, files=files, params=params
                )
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return PydanticTaskClient(
            UploadStagingResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=stage_file_as_task)
    def stage_file(
        self,
        path: Path,
        name: str | None = None,
        parser: str | None = None,
        replace: bool = False,
    ) -> UploadStagingResult:
        raise NotImplementedError()

    def get_staging_results(
        self, names: list[str] | None = None
    ) -> dict[str, UploadStagingResult]:
        params = {}
        if names:
            params["names"] = names
        response = self._client.get("staging-results", params=params)
        _raise_for_status(response)
        return {
            k: UploadStagingResult.model_validate(v) for k, v in response.json().items()
        }

    def wipe_staging(
        self,
        names: list[str] | None = None,
    ) -> dict[str, UploadStagingResult]:
        params = {}
        if names:
            params["names"] = names
        response = self._client.delete("staging", params=params)
        _raise_for_status(response)
        return {
            k: UploadStagingResult.model_validate(v) for k, v in response.json().items()
        }

    def get_staging_data_as_task(
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> Task[pl.LazyFrame]:
        params: dict[str, Any] = {"unique": unique}
        if columns:
            params["columns"] = columns
        if names:
            params["names"] = names
        response = self._client.get("staging-data", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return LazyFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=get_staging_data_as_task)
    def get_staging_data(
        self,
        names: list[str] | None = None,
        *,
        columns: list[str] | None = None,
        unique: bool = False,
    ) -> pl.LazyFrame:
        raise NotImplementedError()

    def get_staging_data_summary_as_task(
        self, names: list[str] | None = None
    ) -> Task[pl.DataFrame]:
        params = {}
        if names:
            params["names"] = names
        response = self._client.get("staging-data-summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return DataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=get_staging_data_summary_as_task)
    def get_staging_data_summary(self, names: list[str] | None = None) -> pl.DataFrame:
        raise NotImplementedError()

    def get_staging_data_detail_summary_as_task(
        self, names: list[str] | None = None
    ) -> Task[pl.DataFrame]:
        params = {}
        if names:
            params["names"] = names
        response = self._client.get("staging-data-detail-summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return DataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=get_staging_data_detail_summary_as_task)
    def get_staging_data_detail_summary(
        self, names: list[str] | None = None
    ) -> pl.DataFrame:
        raise NotImplementedError()

    def validate_staging_data_as_task(
        self, names: list[str] | None = None, short: bool = False
    ) -> Task[dict[str, pl.DataFrame]]:
        params: dict[str, Any] = {"short": short}
        if names:
            params["names"] = names
        response = self._client.get("validate-staging-data", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return DataFrameDictTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=validate_staging_data_as_task)
    def validate_staging_data(
        self, names: list[str] | None = None, short: bool = False
    ) -> dict[str, pl.DataFrame]:
        raise NotImplementedError()

    def commit_as_task(
        self, mode: str, names: list[str] | None = None
    ) -> Task[UploadCommitResult]:
        params: dict[str, Any] = {"mode": mode}
        if names:
            params["names"] = names
        response = self._client.post("commit", body={}, params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return PydanticTaskClient(
            UploadCommitResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=commit_as_task)
    def commit(self, mode: str, names: list[str] | None = None) -> UploadCommitResult:
        raise NotImplementedError()

    def fast_commit_as_task(
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> Task[UploadCommitResult]:
        params = {"mode": mode}
        if parser:
            params["parser"] = parser

        if isinstance(df, Path):
            files: dict[str, Any]
            if self._tqdm_progress:
                with TqdmFileReader(df) as f:
                    files = {"file": f}
                    response = self._client.post(
                        "fast-commit-file", body=None, files=files, params=params
                    )
            else:
                with df.open("rb") as f:
                    files = {"file": f}
                    response = self._client.post(
                        "fast-commit-file", body=None, files=files, params=params
                    )
        else:
            out = io.BytesIO()
            df.write_parquet(out)

            if self._tqdm_progress:
                with TqdmContentStreamer(out.getvalue()) as stream:
                    response = self._client.post(
                        "fast-commit", body=stream, params=params
                    )
            else:
                response = self._client.post(
                    "fast-commit", body=out.getvalue(), params=params
                )

        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return PydanticTaskClient(
            UploadCommitResult,
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=fast_commit_as_task)
    def fast_commit(
        self, df: pl.DataFrame | Path, mode: str, parser: str | None = None
    ) -> UploadCommitResult:
        raise NotImplementedError()

    def get_data_as_task(  # noqa: C901
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> Task[pl.LazyFrame]:
        download_file_path: Path | None = None
        if download_to is not None:
            if isinstance(download_to, str):
                download_to = Path(download_to)
            if not download_to.exists():
                raise FileNotFoundError(
                    f"Download directory {download_to} does not exist"
                )
            if download_to.is_file():
                raise FileExistsError(
                    f"Download directory {download_to} must be a directory"
                )

            download_file_path = download_to / download_filename
            if "{i}" not in download_filename:
                raise ValueError("download_filename must contain the placeholder {i}")

        params: dict[str, Any] = {}
        body: dict[str, Any] = {"unique": unique}
        if columns:
            body["columns"] = columns

        if filters:
            body["filters"] = DnfFilterExpressions.from_dnf(filters).model_dump()

        if version is not None:
            params["version"] = version

        if head is not None:
            params["head"] = head

        response = self._client.post("data", params=params, body=body)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return LazyFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
            out_path=download_file_path,
        )

    @as_blocking(task_func=get_data_as_task)
    def get_data(
        self,
        columns: list[str] | None = None,
        *,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
        head: int | None = None,
        version: int | dt.datetime | None = None,
        download_to: Path | str | None = None,
        download_filename: str = "data-{i}.parquet",
    ) -> pl.LazyFrame:
        raise NotImplementedError()

    def get_data_summary_as_task(
        self, version: int | dt.datetime | None = None
    ) -> Task[pl.DataFrame]:
        params = {}
        if version is not None:
            params["version"] = version
        response = self._client.get("summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return DataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=get_data_summary_as_task)
    def get_data_summary(
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame:
        raise NotImplementedError()

    def get_data_detail_summary_as_task(
        self, version: int | dt.datetime | None = None
    ) -> Task[pl.DataFrame]:
        params = {}
        if version is not None:
            params["version"] = version
        response = self._client.get("detail-summary", params=params)
        _raise_for_status(response)
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return DataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            self._tqdm_progress,
            exc_types=_EXCEPTION_TYPES,
        )

    @as_blocking(task_func=get_data_detail_summary_as_task)
    def get_data_detail_summary(
        self, version: int | dt.datetime | None = None
    ) -> pl.DataFrame:
        raise NotImplementedError()

    def destroy(self) -> None:
        response = self._client.delete("")
        if response.status_code != 200:
            raise Exception(f"Could not destroy dataset. {str(response.content)}")

    def version_history(self) -> dict[int, dt.datetime]:
        return {
            int(k): dt.datetime.fromisoformat(v).astimezone(dt.UTC)
            for k, v in self._client.get("version-history").json().items()
        }


class DataTypeUploaderClientImpl(DataTypeUploaderApi):

    def __init__(self, client: ApiClient, tasks_client: ApiClient, tqdm_progress: bool):
        self._client = client
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress

    def get_datasets(self) -> list[str]:
        return self._client.get("").json()

    def get_dataset(self, dataset: str) -> UploaderApi:
        if dataset not in (datasets := self.get_datasets()):
            raise KeyError(
                f"Dataset '{dataset}' not found. Available datasets: {datasets}"
            )
        return UploaderClientImpl(
            self._client.append_base_path(dataset),
            self._tasks_client,
            self._tqdm_progress,
        )

    def create_dataset(self, dataset: str) -> UploaderApi:
        if dataset in self.get_datasets():
            raise ValueError(f"Dataset '{dataset}' already exists")
        self._client.post(dataset, body={})
        return UploaderClientImpl(
            self._client.append_base_path(dataset),
            self._tasks_client,
            self._tqdm_progress,
        )


class UploadersClientImpl(UploadersApi):

    def __init__(self, client: ApiClient, tasks_client: ApiClient, tqdm_progress: bool):
        self._client = client.append_base_path("uploaders")
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress

    def get_data_types(self) -> list[str]:
        return self._client.get("").json()

    def get_data_type(self, data_type: str) -> DataTypeUploaderApi:
        if data_type not in (data_types := self.get_data_types()):
            raise KeyError(
                f"Data type '{data_type}' not found. Available data types: {data_types}"
            )
        return DataTypeUploaderClientImpl(
            self._client.append_base_path(data_type),
            self._tasks_client,
            self._tqdm_progress,
        )
