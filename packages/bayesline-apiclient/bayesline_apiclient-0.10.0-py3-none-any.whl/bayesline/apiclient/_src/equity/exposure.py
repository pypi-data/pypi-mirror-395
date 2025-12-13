import datetime as dt
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
    AsyncExposureApi,
    AsyncExposureLoaderApi,
    AsyncUniverseApi,
    AsyncUniverseLoaderApi,
    ExposureApi,
    ExposureLoaderApi,
    ExposureSettings,
    ExposureSettingsMenu,
    UniverseApi,
    UniverseLoaderApi,
    UniverseSettings,
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
    DataFrameTaskClient,
    as_blocking,
    async_as_blocking,
)


class ExposureClientImpl(ExposureApi):

    def __init__(
        self,
        client: ApiClient,
        tasks_client: ApiClient,
        settings_registry: SettingsRegistry[ExposureSettings, ExposureSettingsMenu],
        exposure_settings: ExposureSettings,
        universe_api: UniverseLoaderApi,
        tqdm_progress: bool,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._settings_registry = settings_registry
        self._exposure_settings = exposure_settings
        self._universe_api = universe_api
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    def dates(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, UniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        self._validate_settings_menu(universe_settings)

        response = self._client.post(
            "dates",
            params={"range_only": range_only},
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [to_date(d) for d in response.json()]

    def coverage_stats_as_task(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> Task[pl.DataFrame]:
        self._validate_settings_menu(universe)

        params: dict[str, Any] = {}
        _add_id_type(id_type, params)
        params["by"] = by

        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, UniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = self._client.post(
            "/coverage-stats",
            params=params,
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
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

    @as_blocking(task_func=coverage_stats_as_task)
    def coverage_stats(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pl.DataFrame:
        raise NotImplementedError()

    def get_as_task(
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | UniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> Task[pl.DataFrame]:
        params, body = self._get_params_and_body(
            universe, standardize_universe, start, end, id_type, filter_tradedays
        )
        response = self._client.post("", params=params, body=body)

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
        universe: str | int | UniverseSettings | UniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | UniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        raise NotImplementedError()

    def _get_params_and_body(  # noqa: C901
        self,
        universe: str | int | UniverseSettings | UniverseApi,
        standardize_universe: str | int | UniverseSettings | UniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> tuple[dict[str, Any], dict[str, dict[str, Any] | None]]:
        self._validate_settings_menu(universe)

        params: dict[str, Any] = {}
        _add_id_type(id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        params["filter_tradedays"] = filter_tradedays

        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, UniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        if standardize_universe is not None:
            if isinstance(standardize_universe, str | int):
                standardize_universe_settings = self._universe_api.settings.get(
                    standardize_universe
                )
            elif isinstance(standardize_universe, UniverseSettings):
                standardize_universe_settings = standardize_universe
            elif isinstance(standardize_universe, UniverseApi):
                standardize_universe_settings = standardize_universe.settings
            else:
                raise ValueError(
                    f"illegal standardize universe input {standardize_universe}"
                )
        else:
            standardize_universe_settings = None

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
            "standardize_universe_settings": (
                None
                if standardize_universe_settings is None
                else standardize_universe_settings.model_dump()
            ),
        }
        return params, body

    def _validate_settings_menu(
        self, universe: str | int | UniverseSettings | UniverseApi
    ) -> None:
        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, UniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        settings_menu = self._settings_registry.available_settings(
            dataset_name=universe_settings.dataset
        )
        self._exposure_settings.validate_settings(settings_menu)


class AsyncExposureClientImpl(AsyncExposureApi):

    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        settings_registry: AsyncSettingsRegistry[
            ExposureSettings, ExposureSettingsMenu
        ],
        exposure_settings: ExposureSettings,
        universe_api: AsyncUniverseLoaderApi,
        tqdm_progress: bool,
    ):
        self._client = client
        self._tasks_client = tasks_client
        self._settings_registry = settings_registry
        self._exposure_settings = exposure_settings
        self._universe_api = universe_api
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    async def dates(
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        await self._validate_settings_menu(universe_settings)

        response = await self._client.post(
            "dates",
            params={"range_only": range_only},
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [to_date(d) for d in response.json()]

    async def coverage_stats_as_task(
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> AsyncTask[pl.DataFrame]:
        params: dict[str, Any] = {}

        await self._validate_settings_menu(universe)

        _add_id_type(id_type, params)
        params["by"] = by

        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = await self._client.post(
            "/coverage-stats",
            params=params,
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
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

    @async_as_blocking(task_func=coverage_stats_as_task)
    async def coverage_stats(
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def get_as_task(
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | AsyncUniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> AsyncTask[pl.DataFrame]:
        params, body = await self._get_params_and_body(
            universe, standardize_universe, start, end, id_type, filter_tradedays
        )
        response = await self._client.post("", params=params, body=body)

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
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        *,
        standardize_universe: str | int | UniverseSettings | AsyncUniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        raise NotImplementedError()

    async def _get_params_and_body(  # noqa: C901
        self,
        universe: str | int | UniverseSettings | AsyncUniverseApi,
        standardize_universe: str | int | UniverseSettings | AsyncUniverseApi | None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> tuple[dict[str, Any], dict[str, dict[str, Any] | None]]:
        await self._validate_settings_menu(universe)

        params: dict[str, Any] = {}
        _add_id_type(id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        params["filter_tradedays"] = filter_tradedays

        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, UniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        if standardize_universe is not None:
            if isinstance(standardize_universe, str | int):
                standardize_universe_settings = await self._universe_api.settings.get(
                    standardize_universe
                )
            elif isinstance(standardize_universe, UniverseSettings):
                standardize_universe_settings = standardize_universe
            elif isinstance(standardize_universe, AsyncUniverseApi):
                standardize_universe_settings = standardize_universe.settings
            else:
                raise ValueError(
                    f"illegal standardize universe input {standardize_universe}"
                )
        else:
            standardize_universe_settings = None

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
            "standardize_universe_settings": (
                None
                if standardize_universe_settings is None
                else standardize_universe_settings.model_dump()
            ),
        }
        return params, body

    async def _validate_settings_menu(
        self, universe: str | int | UniverseSettings | AsyncUniverseApi
    ) -> None:
        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        settings_menu = await self._settings_registry.available_settings(
            dataset_name=universe_settings.dataset
        )
        self._exposure_settings.validate_settings(settings_menu)


class ExposureLoaderClientImpl(ExposureLoaderApi):

    def __init__(
        self,
        client: ApiClient,
        tasks_client: ApiClient,
        universe_api: UniverseLoaderApi,
        tqdm_progress: bool,
    ):
        self._client = client.append_base_path("exposures")
        self._tasks_client = tasks_client
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/exposure"),
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> SettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | ExposureSettings) -> ExposureApi:
        if isinstance(ref_or_settings, ExposureSettings):
            return ExposureClientImpl(
                self._client,
                self._tasks_client,
                self._settings,
                ref_or_settings,
                self._universe_api,
                self._tqdm_progress,
            )
        else:
            exposure_settings = self.settings.get(ref_or_settings)
            return ExposureClientImpl(
                self._client,
                self._tasks_client,
                self._settings,
                exposure_settings,
                self._universe_api,
                self._tqdm_progress,
            )


class AsyncExposureLoaderClientImpl(AsyncExposureLoaderApi):

    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        universe_api: AsyncUniverseLoaderApi,
        tqdm_progress: bool,
    ):
        self._client = client.append_base_path("exposures")
        self._tasks_client = tasks_client
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/exposure"),
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> AsyncSettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ExposureSettings
    ) -> AsyncExposureApi:
        if isinstance(ref_or_settings, ExposureSettings):
            return AsyncExposureClientImpl(
                self._client,
                self._tasks_client,
                self._settings,
                ref_or_settings,
                self._universe_api,
                self._tqdm_progress,
            )
        else:
            exposure_settings = await self.settings.get(ref_or_settings)
            return AsyncExposureClientImpl(
                self._client,
                self._tasks_client,
                self._settings,
                exposure_settings,
                self._universe_api,
                self._tqdm_progress,
            )


def _add_id_type(
    id_type: IdType | None,
    params: dict[str, Any],
) -> None:
    if id_type is not None:
        params["id_type"] = id_type
