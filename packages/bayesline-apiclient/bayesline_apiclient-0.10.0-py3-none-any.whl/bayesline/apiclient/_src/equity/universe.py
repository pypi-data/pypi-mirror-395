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
    AsyncUniverseApi,
    AsyncUniverseLoaderApi,
    UniverseApi,
    UniverseLoaderApi,
    UniverseSettings,
    UniverseSettingsMenu,
)
from bayesline.api.types import (
    DateLike,
    IdType,
    to_date,
    to_date_string,
)

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient
from bayesline.apiclient._src.settings import (
    AsyncHttpSettingsRegistryClient,
    HttpSettingsRegistryClient,
)
from bayesline.apiclient._src.tasks import (
    AsyncDataFrameTaskClient,
    AsyncListTaskClient,
    DataFrameTaskClient,
    ListTaskClient,
    as_blocking,
    async_as_blocking,
)


class UniverseClientImpl(UniverseApi):

    def __init__(
        self,
        client: ApiClient,
        tasks_client: ApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
        tqdm_progress: bool,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._universe_settings = universe_settings
        self._id_types = id_types
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    def coverage_as_task(self, id_type: IdType | None = None) -> Task[list[str]]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = self._client.post(
            "coverage",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return ListTaskClient(
            self._tasks_client,
            response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @as_blocking(task_func=coverage_as_task)
    def coverage(self, id_type: IdType | None = None) -> list[str]:
        raise NotImplementedError()

    def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        response = self._client.post(
            "dates",
            params={"range_only": range_only, "trade_only": trade_only},
            body=self._universe_settings.model_dump(),
        )
        return [to_date(d) for d in response.json()]

    def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pl.DataFrame:
        params: dict[str, Any] = {
            "mode": mode,
            "filter_mode": filter_mode,
        }
        _check_and_add_id_type(self._id_types, id_type, params)
        response = self._client.post(
            "input-id-mapping",
            params=params,
            body=self._universe_settings.model_dump(),
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def counts_as_task(
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> Task[pl.DataFrame]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["dates"] = dates
        params["labels"] = labels
        body = {
            "universe_settings": self._universe_settings.model_dump(),
        }
        if categorical_hierarchy_levels is not None:
            body["categorical_hierarchy_levels"] = categorical_hierarchy_levels

        response = self._client.post("counts", params=params, body=body)

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

    @as_blocking(task_func=counts_as_task)
    def counts(
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> pl.DataFrame:
        raise NotImplementedError()

    def get_as_task(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> Task[pl.DataFrame]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        params["filter_tradedays"] = filter_tradedays

        response = self._client.post(
            "",
            params=params,
            body=self._universe_settings.model_dump(),
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
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        raise NotImplementedError()


class AsyncUniverseClientImpl(AsyncUniverseApi):

    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
        tqdm_progress: bool,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._universe_settings = universe_settings
        self._id_types = id_types
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    async def coverage_as_task(
        self, id_type: IdType | None = None
    ) -> AsyncTask[list[str]]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = await self._client.post(
            "coverage",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        if response.status_code != 202:
            try:
                response.raise_for_status()
            except Exception as e:
                raise Exception(f"Failed to create task: {response.json()}") from e

        response_model = TaskResponse.model_validate(response.json())
        return AsyncListTaskClient(
            self._tasks_client,
            response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @async_as_blocking(task_func=coverage_as_task)
    async def coverage(self, id_type: IdType | None = None) -> list[str]:
        raise NotImplementedError()

    async def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        response = await self._client.post(
            "dates",
            params={"range_only": range_only, "trade_only": trade_only},
            body=self._universe_settings.model_dump(),
        )
        return [to_date(d) for d in response.json()]

    async def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pl.DataFrame:
        params: dict[str, Any] = {
            "mode": mode,
            "filter_mode": filter_mode,
        }
        _check_and_add_id_type(self._id_types, id_type, params)
        response = await self._client.post(
            "input-id-mapping",
            params=params,
            body=self._universe_settings.model_dump(),
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def counts_as_task(
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> AsyncTask[pl.DataFrame]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["dates"] = dates
        params["labels"] = labels
        body = {
            "universe_settings": self._universe_settings.model_dump(),
        }
        if categorical_hierarchy_levels is not None:
            body["categorical_hierarchy_levels"] = categorical_hierarchy_levels

        response = await self._client.post(
            "counts",
            params=params,
            body=body,
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

    @async_as_blocking(task_func=counts_as_task)
    async def counts(
        self,
        dates: bool = True,
        categorical_hierarchy_levels: dict[str, int] | None = None,
        id_type: IdType | None = None,
        labels: bool = True,
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def get_as_task(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> AsyncTask[pl.DataFrame]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        params["filter_tradedays"] = filter_tradedays

        response = await self._client.post(
            "",
            params=params,
            body=self._universe_settings.model_dump(),
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
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        raise NotImplementedError()


class UniverseLoaderClientImpl(UniverseLoaderApi):
    def __init__(self, client: ApiClient, tasks_client: ApiClient, tqdm_progress: bool):
        self._client = client.append_base_path("universe")
        self._tasks_client = tasks_client
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/universe"),
            UniverseSettings,
            UniverseSettingsMenu,
        )
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> SettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | UniverseSettings) -> UniverseApi:
        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu = self._settings.available_settings(ref_or_settings.dataset)
            ref_or_settings.validate_settings(settings_menu)
            return UniverseClientImpl(
                self._client,
                self._tasks_client,
                ref_or_settings,
                settings_menu.id_types,
                self._tqdm_progress,
            )
        else:
            universe_settings = self.settings.get(ref_or_settings)
            id_types = self._settings.available_settings(
                universe_settings.dataset
            ).id_types
            return UniverseClientImpl(
                self._client,
                self._tasks_client,
                universe_settings,
                id_types,
                self._tqdm_progress,
            )


class AsyncUniverseLoaderClientImpl(AsyncUniverseLoaderApi):
    def __init__(
        self, client: AsyncApiClient, tasks_client: AsyncApiClient, tqdm_progress: bool
    ):
        self._client = client.append_base_path("universe")
        self._tasks_client = tasks_client
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/universe"),
            UniverseSettings,
            UniverseSettingsMenu,
        )
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> AsyncSettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | UniverseSettings
    ) -> AsyncUniverseApi:
        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu = await self._settings.available_settings(
                ref_or_settings.dataset
            )
            ref_or_settings.validate_settings(settings_menu)
            return AsyncUniverseClientImpl(
                self._client,
                self._tasks_client,
                ref_or_settings,
                settings_menu.id_types,
                self._tqdm_progress,
            )
        else:
            universe_settings = await self.settings.get(ref_or_settings)
            id_types = (
                await self._settings.available_settings(universe_settings.dataset)
            ).id_types
            return AsyncUniverseClientImpl(
                self._client,
                self._tasks_client,
                universe_settings,
                id_types,
                self._tqdm_progress,
            )


def _check_and_add_id_type(
    id_types: list[IdType],
    id_type: IdType | None,
    params: dict[str, Any],
) -> None:
    if id_type is not None:
        if id_type not in id_types:
            raise ValueError(f"given id type {id_type} is not supported")
        params["id_type"] = id_type
