import datetime as dt
from typing import Any

import polars as pl
from bayesline.api import (
    AsyncSettingsRegistry,
    AsyncTask,
    SettingsRegistry,
    Task,
    TaskResponse,
)
from bayesline.api.equity import (
    AsyncPortfolioHierarchyApi,
    AsyncPortfolioHierarchyLoaderApi,
    PortfolioHierarchyApi,
    PortfolioHierarchyLoaderApi,
    PortfolioHierarchySettings,
    PortfolioHierarchySettingsMenu,
)
from bayesline.api.types import (
    DateLike,
    IdType,
    to_date,
    to_date_string,
)

from bayesline.apiclient._src.apiclient import ApiClient, AsyncApiClient
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


class PortfolioHierarchyClientImpl(PortfolioHierarchyApi):

    def __init__(
        self,
        client: ApiClient,
        tasks_client: ApiClient,
        settings: PortfolioHierarchySettings,
        tqdm_progress: bool = False,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._settings = settings
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> PortfolioHierarchySettings:
        return self._settings

    def get_id_types(self) -> dict[str, list[IdType]]:
        return self._client.post("id-types", body=self._settings.model_dump()).json()

    def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        response = self._client.post(
            "dates", body=self._settings.model_dump(), params={"collapse": collapse}
        )
        response_data = response.json()
        return {p: [to_date(d) for d in response_data[p]] for p in response_data.keys()}

    def get_as_task(
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> Task[pl.DataFrame]:
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = to_date_string(start_date)
        if end_date is not None:
            params["end_date"] = to_date_string(end_date)
        if id_type is not None:
            params["id_type"] = id_type
        response = self._client.post(
            "",
            params=params,
            body=self._settings.model_dump(),
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

    @as_blocking(task_func=get_as_task)
    def get(
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        raise NotImplementedError()


class AsyncPortfolioHierarchyClientImpl(AsyncPortfolioHierarchyApi):

    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        settings: PortfolioHierarchySettings,
        tqdm_progress: bool = False,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._settings = settings
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> PortfolioHierarchySettings:
        return self._settings

    async def get_id_types(self) -> dict[str, list[IdType]]:
        return (
            await self._client.post("id-types", body=self._settings.model_dump())
        ).json()

    async def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        response = await self._client.post(
            "dates", body=self._settings.model_dump(), params={"collapse": collapse}
        )
        response_data = response.json()
        return {p: [to_date(d) for d in response_data[p]] for p in response_data.keys()}

    async def get_as_task(
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> AsyncTask[pl.DataFrame]:
        params: dict[str, Any] = {}
        if start_date is not None:
            params["start_date"] = to_date_string(start_date)
        if end_date is not None:
            params["end_date"] = to_date_string(end_date)
        if id_type is not None:
            params["id_type"] = id_type
        response = await self._client.post(
            "",
            params=params,
            body=self._settings.model_dump(),
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

    @async_as_blocking(task_func=get_as_task)
    async def get(
        self,
        start_date: DateLike | None,
        end_date: DateLike | None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        raise NotImplementedError()


class PortfolioHierarchyLoaderClientImpl(PortfolioHierarchyLoaderApi):

    def __init__(
        self, client: ApiClient, tasks_client: ApiClient, tqdm_progress: bool = False
    ):
        self._client = client.append_base_path("portfoliohierarchy")
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio-hierarchy"),
            PortfolioHierarchySettings,
            PortfolioHierarchySettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[PortfolioHierarchySettings, PortfolioHierarchySettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | PortfolioHierarchySettings
    ) -> PortfolioHierarchyApi:
        if isinstance(ref_or_settings, PortfolioHierarchySettings):
            settings_menu = self._settings.available_settings()
            ref_or_settings.validate_settings(settings_menu)
            return PortfolioHierarchyClientImpl(
                self._client,
                self._tasks_client,
                settings=ref_or_settings,
                tqdm_progress=self._tqdm_progress,
            )
        else:
            portfoliohierarchy_settings = self.settings.get(ref_or_settings)
            return PortfolioHierarchyClientImpl(
                self._client,
                self._tasks_client,
                settings=portfoliohierarchy_settings,
                tqdm_progress=self._tqdm_progress,
            )


class AsyncPortfolioHierarchyLoaderClientImpl(AsyncPortfolioHierarchyLoaderApi):
    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        tqdm_progress: bool = False,
    ):
        self._client = client.append_base_path("portfoliohierarchy")
        self._tasks_client = tasks_client
        self._tqdm_progress = tqdm_progress
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio-hierarchy"),
            PortfolioHierarchySettings,
            PortfolioHierarchySettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[
        PortfolioHierarchySettings, PortfolioHierarchySettingsMenu
    ]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | PortfolioHierarchySettings
    ) -> AsyncPortfolioHierarchyApi:
        if isinstance(ref_or_settings, PortfolioHierarchySettings):
            settings_menu = await self._settings.available_settings()
            ref_or_settings.validate_settings(settings_menu)
            return AsyncPortfolioHierarchyClientImpl(
                self._client,
                self._tasks_client,
                settings=ref_or_settings,
                tqdm_progress=self._tqdm_progress,
            )
        else:
            portfoliohierarchy_settings = await self.settings.get(ref_or_settings)
            return AsyncPortfolioHierarchyClientImpl(
                self._client,
                self._tasks_client,
                settings=portfoliohierarchy_settings,
                tqdm_progress=self._tqdm_progress,
            )
