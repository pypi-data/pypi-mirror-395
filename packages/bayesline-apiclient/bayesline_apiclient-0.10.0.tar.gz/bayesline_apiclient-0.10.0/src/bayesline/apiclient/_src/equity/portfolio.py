import datetime as dt
import io
from typing import Any, Literal

import polars as pl
from bayesline.api import (
    AsyncSettingsRegistry,
    AsyncTask,
    SettingsRegistry,
    Task,
    TaskResponse,
)
from bayesline.api.equity import (
    AsyncDataTypeUploaderApi,
    AsyncPortfolioApi,
    AsyncPortfolioLoaderApi,
    AsyncUploadParserApi,
    DataTypeUploaderApi,
    PortfolioApi,
    PortfolioLoaderApi,
    PortfolioOrganizerSettings,
    PortfolioOrganizerSettingsMenu,
    PortfolioSettings,
    PortfolioSettingsMenu,
    UploadParserApi,
    UploadParserResult,
)
from bayesline.api.types import DateLike, IdType, to_date

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient
from bayesline.apiclient._src.equity.upload import (
    AsyncDataTypeUploaderClientImpl,
    DataTypeUploaderClientImpl,
)
from bayesline.apiclient._src.settings import (
    AsyncHttpSettingsRegistryClient,
    HttpSettingsRegistryClient,
)
from bayesline.apiclient._src.tasks import (
    AsyncDataFrameTaskClient,
    DataFrameTaskClient,
    as_blocking,
    async_as_blocking,
)


class AsyncPortfolioClientImpl(AsyncPortfolioApi):

    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        settings: PortfolioSettings,
        tqdm_progress: bool = False,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._settings = settings
        self._tqdm_progress = tqdm_progress

    @property
    def name(self) -> str:
        return (
            self._client.sync()
            .post("name", body={"settings": self._settings.model_dump()})
            .json()
        )

    async def get_id_types(self) -> dict[str, list[IdType]]:
        return (
            await self._client.post(
                "id-types", body={"settings": self._settings.model_dump()}
            )
        ).json()

    async def get_coverage_as_task(
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> AsyncTask[pl.DataFrame]:
        params: dict[str, Any] = {"by": str(by), "metric": str(metric)}
        if stats is not None:
            params["stats"] = stats
        response = await self._client.post(
            "coverage",
            params=params,
            body={"names": names, "settings": self._settings.model_dump()},
        )
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @async_as_blocking(task_func=get_coverage_as_task)
    async def get_coverage(
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def get_portfolio_names(self) -> list[str]:
        response = await self._client.post(
            "names", body={"settings": self._settings.model_dump()}
        )
        return response.json()

    async def get_portfolio_groups(self) -> dict[str, list[str]]:
        response = await self._client.post(
            "groups", body={"settings": self._settings.model_dump()}
        )
        return response.json()

    async def get_dates(
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]:
        response = await self._client.post(
            "dates",
            params={"collapse": collapse},
            body={"names": names, "settings": self._settings.model_dump()},
        )
        response_data = response.json()
        if response.status_code == 404:
            raise KeyError(response_data["detail"])
        elif response.status_code == 400:
            raise ValueError(response_data["detail"])
        return {p: [to_date(d) for d in response_data[p]] for p in response_data.keys()}

    async def get_portfolio_as_task(
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> AsyncTask[pl.DataFrame]:
        response = await self._client.post(
            "data",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "id_type": id_type,
            },
            body={"names": names, "settings": self._settings.model_dump()},
        )
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @async_as_blocking(task_func=get_portfolio_as_task)
    async def get_portfolio(
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        raise NotImplementedError()


class PortfolioClientImpl(PortfolioApi):

    def __init__(
        self,
        client: ApiClient,
        tasks_client: ApiClient,
        settings: PortfolioSettings,
        tqdm_progress: bool = False,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress
        self._settings = settings

    @property
    def name(self) -> str:
        return self._client.post(
            "name", body={"settings": self._settings.model_dump()}
        ).json()

    def get_id_types(self) -> dict[str, list[IdType]]:
        return self._client.post(
            "id-types", body={"settings": self._settings.model_dump()}
        ).json()

    def get_coverage_as_task(
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> Task[pl.DataFrame]:
        params: dict[str, Any] = {"by": str(by), "metric": str(metric)}
        if stats is not None:
            params["stats"] = stats
        response = self._client.post(
            "coverage",
            params=params,
            body={"names": names, "settings": self._settings.model_dump()},
        )
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return DataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @as_blocking(task_func=get_coverage_as_task)
    def get_coverage(
        self,
        names: str | list[str] | None = None,
        *,
        by: Literal["date", "asset"] = "date",
        metric: Literal["count", "holding"] = "count",
        stats: list[str] | None = None,
    ) -> pl.DataFrame:
        raise NotImplementedError()

    def get_portfolio_names(self) -> list[str]:
        response = self._client.post(
            "names", body={"settings": self._settings.model_dump()}
        )
        return response.json()

    def get_portfolio_groups(self) -> dict[str, list[str]]:
        response = self._client.post(
            "groups", body={"settings": self._settings.model_dump()}
        )
        return response.json()

    def get_dates(
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]:
        response = self._client.post(
            "dates",
            params={"collapse": collapse},
            body={"names": names, "settings": self._settings.model_dump()},
        )
        response_data = response.json()
        if response.status_code == 404:
            raise KeyError(response_data["detail"])
        elif response.status_code == 400:
            raise ValueError(response_data["detail"])
        return {p: [to_date(d) for d in response_data[p]] for p in response_data.keys()}

    def get_portfolio_as_task(
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> Task[pl.DataFrame]:
        response = self._client.post(
            "data",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "id_type": id_type,
            },
            body={"names": names, "settings": self._settings.model_dump()},
        )
        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return DataFrameTaskClient(
            self._tasks_client,
            response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @as_blocking(task_func=get_portfolio_as_task)
    def get_portfolio(
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        raise NotImplementedError()


class PortfolioParserClientImpl(UploadParserApi):

    def __init__(self, client: ApiClient, parser_name: str):
        self._client = client.append_base_path(parser_name)
        self._parser_name = parser_name

    @property
    def name(self) -> str:
        return self._parser_name

    def output_schema(self) -> dict[str, pl.DataType]:
        raise NotImplementedError()

    def get_examples(self) -> list[pl.DataFrame]:
        response = self._client.options("")
        result = []
        for bytes in response.iter_bytes():
            result.append(pl.read_parquet(io.BytesIO(bytes)))
        return result

    def can_handle(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> UploadParserResult:
        params = {}
        if name:
            params["name"] = name
        out = io.BytesIO()
        raw_df.write_parquet(out)
        response = self._client.put("", body=out.getvalue(), params=params)
        return UploadParserResult.model_validate(response.json())

    def parse(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> tuple[pl.DataFrame, UploadParserResult]:
        params = {}
        if name:
            params["name"] = name
        out = io.BytesIO()
        raw_df.write_parquet(out)
        response = self._client.post("", body=out.getvalue(), params=params)
        result = UploadParserResult.model_validate_json(response.headers["X-Metadata"])
        df = pl.read_parquet(io.BytesIO(response.content))
        return df, result


class AsyncPortfolioParserClientImpl(AsyncUploadParserApi):

    def __init__(self, client: AsyncApiClient, parser_name: str):
        self._client = client.append_base_path(parser_name)
        self._parser_name = parser_name

    @property
    def name(self) -> str:
        return self._parser_name

    async def output_schema(self) -> dict[str, pl.DataType]:
        raise NotImplementedError()

    async def get_examples(self) -> list[pl.DataFrame]:
        response = await self._client.options("")
        result = []
        async for bytes in response.aiter_bytes():
            result.append(pl.read_parquet(io.BytesIO(bytes)))
        return result

    async def can_handle(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> UploadParserResult:
        params = {}
        if name:
            params["name"] = name
        out = io.BytesIO()
        raw_df.write_parquet(out)
        response = await self._client.put("", body=out.getvalue(), params=params)
        return UploadParserResult.model_validate(response.json())

    async def parse(
        self, raw_df: pl.DataFrame, *, name: str | None = None
    ) -> tuple[pl.DataFrame, UploadParserResult]:
        params = {}
        if name:
            params["name"] = name
        out = io.BytesIO()
        raw_df.write_parquet(out)
        response = await self._client.post("", body=out.getvalue(), params=params)
        result = UploadParserResult.model_validate_json(response.headers["X-Metadata"])
        df = pl.read_parquet(io.BytesIO(response.content))
        return df, result


class AsyncPortfolioLoaderClientImpl(AsyncPortfolioLoaderApi):
    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        tqdm_progress: bool = False,
    ):
        self._client = client.append_base_path("portfolio")
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio"),
            PortfolioSettings,
            PortfolioSettingsMenu,
        )
        self._uploader = AsyncDataTypeUploaderClientImpl(
            client.append_base_path("uploaders/portfolios"),
            tasks_client,
            tqdm_progress=tqdm_progress,
        )
        self._organizer_settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio-organizer"),
            PortfolioOrganizerSettings,
            PortfolioOrganizerSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[PortfolioSettings, PortfolioSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | PortfolioSettings
    ) -> AsyncPortfolioApi:
        if isinstance(ref_or_settings, PortfolioSettings):
            settings_menu = await self._settings.available_settings()
            ref_or_settings.validate_settings(settings_menu)
            return AsyncPortfolioClientImpl(
                self._client,
                self._tasks_client,
                settings=ref_or_settings,
                tqdm_progress=self._tqdm_progress,
            )
        else:
            portfoliohierarchy_settings = await self.settings.get(ref_or_settings)
            return AsyncPortfolioClientImpl(
                self._client,
                self._tasks_client,
                settings=portfoliohierarchy_settings,
                tqdm_progress=self._tqdm_progress,
            )

    @property
    def uploader(self) -> AsyncDataTypeUploaderApi:
        return self._uploader

    @property
    def organizer_settings(
        self,
    ) -> AsyncSettingsRegistry[
        PortfolioOrganizerSettings, PortfolioOrganizerSettingsMenu
    ]:
        return self._organizer_settings


class PortfolioLoaderClientImpl(PortfolioLoaderApi):
    def __init__(self, client: ApiClient, tasks_client: ApiClient, tqdm_progress: bool):
        self._client = client.append_base_path("portfolio")
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio"),
            PortfolioSettings,
            PortfolioSettingsMenu,
        )
        self._uploader = DataTypeUploaderClientImpl(
            client.append_base_path("uploaders/portfolios"),
            tasks_client,
            tqdm_progress,
        )
        self._organizer_settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio-organizer"),
            PortfolioOrganizerSettings,
            PortfolioOrganizerSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[PortfolioSettings, PortfolioSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | PortfolioSettings) -> PortfolioApi:
        if isinstance(ref_or_settings, PortfolioSettings):
            settings_menu = self._settings.available_settings()
            ref_or_settings.validate_settings(settings_menu)
            return PortfolioClientImpl(
                self._client,
                self._tasks_client,
                settings=ref_or_settings,
                tqdm_progress=self._tqdm_progress,
            )
        else:
            portfoliohierarchy_settings = self.settings.get(ref_or_settings)
            return PortfolioClientImpl(
                self._client,
                self._tasks_client,
                settings=portfoliohierarchy_settings,
                tqdm_progress=self._tqdm_progress,
            )

    @property
    def uploader(self) -> DataTypeUploaderApi:
        return self._uploader

    @property
    def organizer_settings(
        self,
    ) -> SettingsRegistry[PortfolioOrganizerSettings, PortfolioOrganizerSettingsMenu]:
        return self._organizer_settings
