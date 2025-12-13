import json
from typing import Literal

import httpx
from bayesline.api import (
    AsyncSettingsRegistry,
    AsyncTask,
    RawSettings,
    SettingsRegistry,
    Task,
    TaskResponse,
)
from bayesline.api.equity import (
    AsyncRiskDatasetApi,
    AsyncRiskDatasetLoaderApi,
    DatasetError,
    RiskDatasetApi,
    RiskDatasetLoaderApi,
    RiskDatasetMetadata,
    RiskDatasetProperties,
    RiskDatasetSettings,
    RiskDatasetSettingsMenu,
    RiskDatasetUpdateResult,
)

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient
from bayesline.apiclient._src.settings import (
    AsyncHttpSettingsRegistryClient,
    HttpSettingsRegistryClient,
)
from bayesline.apiclient._src.tasks import (
    AsyncPydanticTaskClient,
    AsyncTaskClient,
    PydanticTaskClient,
    TaskClient,
    as_blocking,
    async_as_blocking,
)


def _raise_for_status(response: httpx.Response) -> None:  # noqa: C901
    if response.status_code in (200, 202):
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
            elif details["type"] == "DatasetError":
                exc = DatasetError(_unescape(details["message"]))
    except (KeyError, ValueError, json.JSONDecodeError):
        # If we can't parse the response, fall back to default behavior
        pass

    if exc:
        raise exc

    response.raise_for_status()


class AsyncRiskDatasetClientImpl(AsyncRiskDatasetApi):

    def __init__(
        self,
        client: AsyncApiClient,
        tasks_client: AsyncApiClient,
        dataset_name: str,
        settings: RiskDatasetSettings,
        tqdm_progress: bool,
    ) -> None:
        self._client = client
        self._tasks_client = tasks_client
        self._dataset_name = dataset_name
        self._settings = settings
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> RiskDatasetSettings:
        return self._settings

    async def describe(self) -> RiskDatasetProperties:
        response = await self._client.get(f"describe/{self._dataset_name}")
        _raise_for_status(response)
        return RiskDatasetProperties.model_validate(response.json())

    async def update_as_task(
        self, force: bool = False
    ) -> AsyncTask[RiskDatasetUpdateResult]:
        response = await self._client.post(
            f"update/{self._dataset_name}", body={}, params={"force": force}
        )
        _raise_for_status(response)
        if response.status_code != 202:
            raise DatasetError(f"Failed to create task: {response.json()}")

        response_model = TaskResponse.model_validate(response.json())

        return AsyncPydanticTaskClient(
            model_class=RiskDatasetUpdateResult,
            client=self._tasks_client,
            task_id=response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @async_as_blocking(task_func=update_as_task)
    async def update(self, force: bool = False) -> RiskDatasetUpdateResult:
        raise NotImplementedError()


class RiskDatasetClientImpl(RiskDatasetApi):

    def __init__(
        self,
        client: ApiClient,
        tasks_client: ApiClient,
        dataset_name: str,
        settings: RiskDatasetSettings,
        tqdm_progress: bool,
    ) -> None:
        self._client = client
        self._tasks_client = tasks_client
        self._dataset_name = dataset_name
        self._settings = settings
        self._tqdm_progress = tqdm_progress

    @property
    def settings(self) -> RiskDatasetSettings:
        return self._settings

    def describe(self) -> RiskDatasetProperties:
        response = self._client.get(f"describe/{self._dataset_name}")
        _raise_for_status(response)
        return RiskDatasetProperties.model_validate(response.json())

    def update_as_task(self, force: bool = False) -> Task[RiskDatasetUpdateResult]:
        response = self._client.post(
            f"update/{self._dataset_name}", body={}, params={"force": force}
        )
        _raise_for_status(response)
        if response.status_code != 202:
            raise DatasetError(f"Failed to create task: {response.json()}")

        response_model = TaskResponse.model_validate(response.json())

        return PydanticTaskClient(
            model_class=RiskDatasetUpdateResult,
            client=self._tasks_client,
            task_id=response_model.task_id,
            tqdm_progress=self._tqdm_progress,
        )

    @as_blocking(task_func=update_as_task)
    def update(self, force: bool = False) -> RiskDatasetUpdateResult:
        raise NotImplementedError()


class AsyncDatasetCreationTask(AsyncTaskClient[AsyncRiskDatasetApi]):

    def __init__(
        self,
        api_client: AsyncApiClient,
        response_model: TaskResponse,
        tqdm_progress: bool,
        dataset_client: AsyncApiClient,
    ):
        super().__init__(
            client=api_client,
            task_id=response_model.task_id,
            tqdm_progress=tqdm_progress,
        )
        self._response_model = response_model
        self._dataset_client = dataset_client

    async def get_result(self) -> AsyncRiskDatasetApi:
        response = await self._api_client.get(
            f"{self.task_id}/result", params={"type": "json"}
        )
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        self.raise_for_status(response)

        response_json = response.json()

        return AsyncRiskDatasetClientImpl(
            self._dataset_client,
            self._api_client,
            dataset_name=response_json["dataset_name"],
            settings=RiskDatasetSettings.model_validate(response_json["settings"]),
            tqdm_progress=self._tqdm_progress,
        )


class DatasetCreationTask(TaskClient[RiskDatasetApi]):

    def __init__(
        self,
        api_client: ApiClient,
        response_model: TaskResponse,
        tqdm_progress: bool,
        dataset_client: ApiClient,
    ):
        super().__init__(
            client=api_client,
            task_id=response_model.task_id,
            tqdm_progress=tqdm_progress,
        )
        self._response_model = response_model
        self._dataset_client = dataset_client

    def get_result(self) -> RiskDatasetApi:
        response = self._api_client.get(
            f"{self.task_id}/result", params={"type": "json"}
        )
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        self.raise_for_status(response)

        response_json = response.json()
        return RiskDatasetClientImpl(
            self._dataset_client,
            self._api_client,
            dataset_name=response_json["dataset_name"],
            settings=RiskDatasetSettings.model_validate(response_json["settings"]),
            tqdm_progress=self._tqdm_progress,
        )


class AsyncRiskDatasetLoaderClientImpl(AsyncRiskDatasetLoaderApi):

    def __init__(
        self, client: AsyncApiClient, tasks_client: AsyncApiClient, tqdm_progress: bool
    ):
        self._client = client.append_base_path("dataset")
        self._tasks_client = tasks_client
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/risk-dataset"),
            RiskDatasetSettings,
            RiskDatasetSettingsMenu,
        )
        self._tqdm_progress = tqdm_progress

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[RiskDatasetSettings, RiskDatasetSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | RiskDatasetSettings
    ) -> AsyncRiskDatasetApi:
        if isinstance(ref_or_settings, RiskDatasetSettings):
            raise ValueError(
                "Inline loads are not supported for the dataset API. "
                "Create a a new dataset and use its name to load it."
            )
        if isinstance(ref_or_settings, str):
            dataset_names = await self.get_dataset_names(status="available")
            if ref_or_settings not in dataset_names:
                raise DatasetError(f"Dataset with name {ref_or_settings} not found")
            name = ref_or_settings
        else:
            identifiers = await self.settings.ids()
            name = identifiers[ref_or_settings]

        if name in await self.settings.names():
            settings = await self.settings.get(ref_or_settings)
        else:
            settings = RiskDatasetSettings(reference_dataset=name)

        return AsyncRiskDatasetClientImpl(
            self._client,
            self._tasks_client,
            dataset_name=name,
            settings=settings,
            tqdm_progress=self._tqdm_progress,
        )

    async def get_default_dataset_name(self) -> str:
        response = await self._client.get("", params={"type": "default"})
        response.raise_for_status()
        return response.json()[0]

    async def get_dataset_names(
        self,
        *,
        mode: Literal["System", "User", "All"] = "All",
        status: Literal["ready", "available"] = "ready",
    ) -> list[str]:
        return (
            await self._client.get("", params={"mode": mode, "status": status})
        ).json()

    async def list_riskdatasets(self) -> list[RiskDatasetMetadata]:
        return [
            RiskDatasetMetadata.model_validate(d)
            for d in (await self._client.get("describe")).json()
        ]

    async def create_dataset_as_task(
        self, name: str, settings: RiskDatasetSettings
    ) -> AsyncTask[AsyncRiskDatasetApi]:
        existing_names = await self.get_dataset_names(status="available")
        if name in existing_names:
            raise DatasetError(f"Dataset with name {name} already exists")
        response = await self._client.post(f"create/{name}", body=settings)

        _raise_for_status(response)
        if response.status_code != 202:
            raise DatasetError(f"Failed to create task: {response.json()}")

        response_model = TaskResponse.model_validate(response.json())
        return AsyncDatasetCreationTask(
            self._tasks_client,
            response_model,
            self._tqdm_progress,
            self._client,
        )

    @async_as_blocking(task_func=create_dataset_as_task)
    async def create_dataset(
        self, name: str, settings: RiskDatasetSettings
    ) -> AsyncRiskDatasetApi:
        raise NotImplementedError()

    async def delete_dataset(self, name: str) -> RawSettings:
        response = await self._client.delete(f"{name}")
        _raise_for_status(response)

        response.raise_for_status()
        return RawSettings.model_validate(response.json())


class RiskDatasetLoaderClientImpl(RiskDatasetLoaderApi):

    def __init__(self, client: ApiClient, tasks_client: ApiClient, tqdm_progress: bool):
        self._client = client.append_base_path("dataset")
        self._tasks_client = tasks_client
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/risk-dataset"),
            RiskDatasetSettings,
            RiskDatasetSettingsMenu,
        )
        self._tqdm_progress = tqdm_progress

    @property
    def settings(
        self,
    ) -> SettingsRegistry[RiskDatasetSettings, RiskDatasetSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | RiskDatasetSettings) -> RiskDatasetApi:
        if isinstance(ref_or_settings, RiskDatasetSettings):
            raise ValueError(
                "Inline loads are not supported for the dataset API. "
                "Create a a new dataset and use its name to load it."
            )
        if isinstance(ref_or_settings, str):
            dataset_names = self.get_dataset_names(status="available")
            if ref_or_settings not in dataset_names:
                raise DatasetError(f"Dataset with name {ref_or_settings} not found")
            name = ref_or_settings
        else:
            identifiers = self.settings.ids()
            name = identifiers[ref_or_settings]

        if name in self.settings.names():
            settings = self.settings.get(ref_or_settings)
        else:
            settings = RiskDatasetSettings(reference_dataset=name)

        return RiskDatasetClientImpl(
            self._client,
            self._tasks_client,
            dataset_name=name,
            settings=settings,
            tqdm_progress=self._tqdm_progress,
        )

    def get_default_dataset_name(self) -> str:
        return self._client.get("", params={"type": "default"}).json()[0]

    def get_dataset_names(
        self,
        *,
        mode: Literal["System", "User", "All"] = "All",
        status: Literal["ready", "available"] = "ready",
    ) -> list[str]:
        return self._client.get("", params={"mode": mode, "status": status}).json()

    def list_riskdatasets(self) -> list[RiskDatasetMetadata]:
        return [
            RiskDatasetMetadata.model_validate(d)
            for d in self._client.get("describe").json()
        ]

    def create_dataset_as_task(
        self, name: str, settings: RiskDatasetSettings
    ) -> Task[RiskDatasetApi]:
        existing_names = self.get_dataset_names(status="available")
        if name in existing_names:
            raise DatasetError(f"Dataset with name {name} already exists")
        response = self._client.post(f"create/{name}", body=settings)

        _raise_for_status(response)
        if response.status_code != 202:
            raise DatasetError(f"Failed to create task: {response.json()}")

        response_model = TaskResponse.model_validate(response.json())
        return DatasetCreationTask(
            self._tasks_client,
            response_model,
            self._tqdm_progress,
            self._client,
        )

    @as_blocking(task_func=create_dataset_as_task)
    def create_dataset(
        self, name: str, settings: RiskDatasetSettings
    ) -> RiskDatasetApi:
        raise NotImplementedError()

    def delete_dataset(self, name: str) -> RawSettings:
        response = self._client.delete(f"{name}")
        _raise_for_status(response)

        response.raise_for_status()
        return RawSettings.model_validate(response.json())
