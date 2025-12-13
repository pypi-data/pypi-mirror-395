import os
import warnings

import httpx
from bayesline.api import (
    AsyncBayeslineApi,
    AsyncIncidentsServiceApi,
    AsyncPermissionsApi,
    AsyncTasksApi,
    BayeslineApi,
    IncidentsServiceApi,
    NewAsyncSettingsRegistry,
    NewSettingsRegistry,
    PermissionsApi,
    TasksApi,
)
from bayesline.api.equity import AsyncBayeslineEquityApi, BayeslineEquityApi

from bayesline.apiclient._src.apiclient import ApiClient, AsyncApiClient
from bayesline.apiclient._src.equity.client import (
    AsyncBayeslineEquityApiClient,
    BayeslineEquityApiClient,
)
from bayesline.apiclient._src.maintenance import (
    AsyncIncidentsServiceClientImpl,
    IncidentsServiceClientImpl,
)
from bayesline.apiclient._src.permissions import (
    AsyncPermissionsApiClient,
    PermissionsApiClient,
)
from bayesline.apiclient._src.settings_new import (
    AsyncSettingsRegistryClient,
    SettingsRegistryClient,
)
from bayesline.apiclient._src.tasks import AsyncTasksClient, TasksClient


def _get_client_server_version_warning_message(
    endpoint: str, proxy: str | None = None, client: httpx.Client | None = None
) -> str | None:
    client = client or httpx.Client(verify=False, proxy=proxy)  # noqa: S501
    try:
        response = client.get(endpoint)
        if response.status_code != 200:
            return (
                f"{os.linesep}"
                f"Could not connect to the Bayesline API server at {endpoint}."
                f"{os.linesep}"
                f"Received status code {response.status_code}."
            )

        response_content = response.json()
        server_compat_client_version = response_content.get("client_version")

        if server_compat_client_version is None:
            return (
                f"{os.linesep}"
                "Could not determine the server compatible client version."
                f"{os.linesep}"
                "This API client might be incompatible with the server."
            )

        from bayesline.apiclient import __version__ as client_version

        if server_compat_client_version != client_version:
            return (
                f"{os.linesep}"
                f"The Bayesline API server at {endpoint} is compatible with "
                f"client version {server_compat_client_version}.{os.linesep}"
                f"You are on client version {client_version}.{os.linesep}"
                f"Install bayesline-apiclient at version "
                f"{server_compat_client_version}"
                f" to avoid compatibility issues.{os.linesep}"
                f"`pip install bayesline-apiclient=={server_compat_client_version}`"
            )
    except httpx.ConnectError as e:
        return (
            f"{os.linesep}"
            f"Could not connect to the Bayesline API server at {endpoint}."
            f"{os.linesep}"
            f"Please check the server URL,  port and possible proxies and try again."
            f"{os.linesep}"
            f"Error Message: {str(e)}"
        )
    except Exception as e:
        return (
            f"{os.linesep}"
            f"Could not determine the server compatible client version."
            f"{os.linesep}"
            f"Error Message: {str(e)}"
        )

    return None


def _check_client_server_version(
    endpoint: str, proxy: str | None, client: httpx.Client | None = None
) -> None:
    if message := _get_client_server_version_warning_message(
        endpoint=endpoint,
        proxy=proxy,
        client=client,
    ):
        warnings.warn(message, stacklevel=2)


class AsyncBayeslineApiClient(AsyncBayeslineApi):

    def __init__(self, client: AsyncApiClient, tqdm_progress: bool):
        self._client = client.append_base_path("v1")
        self._permissions_client = AsyncPermissionsApiClient(self._client)
        self._incidents_client = AsyncIncidentsServiceClientImpl(client)
        self._tasks_client = AsyncTasksClient(self._client)
        self._equity_client = AsyncBayeslineEquityApiClient(
            self._client, self._tasks_client.api_client, tqdm_progress
        )
        self._settings_registry_client = AsyncSettingsRegistryClient(self._client)

    @classmethod
    def new_client(
        cls: type["AsyncBayeslineApiClient"],
        *,
        endpoint: str = "https://api.bayesline.com",
        api_key: str,
        client: httpx.AsyncClient | httpx.Client | None = None,
        proxy: str | None = None,
        verify: bool = True,
        tqdm_progress: bool = False,
    ) -> AsyncBayeslineApi:
        _check_client_server_version(endpoint, proxy)
        return cls(
            AsyncApiClient(
                endpoint,
                auth_str=api_key,
                auth_type="API_KEY",
                client=client,
                proxy=proxy,
                verify=verify,
                submit_exceptions=False,
            ),
            tqdm_progress=tqdm_progress,
        )

    @property
    def equity(self) -> AsyncBayeslineEquityApi:
        return self._equity_client

    @property
    def settings_registry(self) -> NewAsyncSettingsRegistry:
        return self._settings_registry_client

    @property
    def permissions(self) -> AsyncPermissionsApi:
        return self._permissions_client

    @property
    def incidents(self) -> AsyncIncidentsServiceApi:
        return self._incidents_client

    @property
    def tasks(self) -> AsyncTasksApi:
        return self._tasks_client


class BayeslineApiClient(BayeslineApi):

    def __init__(self, client: ApiClient, tqdm_progress: bool):
        self._client = client.append_base_path("v1")
        self._permissions_client = PermissionsApiClient(self._client)
        self._incidents_client = IncidentsServiceClientImpl(client)
        self._tasks_client = TasksClient(self._client)
        self._equity_client = BayeslineEquityApiClient(
            self._client, self._tasks_client.api_client, tqdm_progress
        )
        self._settings_registry_client = SettingsRegistryClient(self._client)

    @classmethod
    def new_client(
        cls: type["BayeslineApiClient"],
        *,
        endpoint: str = "https://api.bayesline.com",
        api_key: str,
        client: httpx.Client | None = None,
        proxy: str | None = None,
        verify: bool = True,
        tqdm_progress: bool = True,
    ) -> BayeslineApi:
        _check_client_server_version(endpoint, proxy)
        return cls(
            ApiClient(
                endpoint,
                auth_str=api_key,
                auth_type="API_KEY",
                client=client,
                proxy=proxy,
                verify=verify,
                submit_exceptions=False,
            ),
            tqdm_progress=tqdm_progress,
        )

    @classmethod
    def new_async_client(
        cls: type["BayeslineApiClient"],
        *,
        endpoint: str = "https://api.bayesline.com",
        api_key: str,
        client: httpx.AsyncClient | None = None,
        proxy: str | None = None,
        verify: bool = True,
        tqdm_progress: bool = False,
    ) -> AsyncBayeslineApi:
        _check_client_server_version(endpoint, proxy)
        return AsyncBayeslineApiClient.new_client(
            endpoint=endpoint,
            api_key=api_key,
            client=client,
            proxy=proxy,
            verify=verify,
            tqdm_progress=tqdm_progress,
        )

    @property
    def equity(self) -> BayeslineEquityApi:
        return self._equity_client

    @property
    def settings_registry(self) -> NewSettingsRegistry:
        return self._settings_registry_client

    @property
    def permissions(self) -> PermissionsApi:
        return self._permissions_client

    @property
    def incidents(self) -> IncidentsServiceApi:
        return self._incidents_client

    @property
    def tasks(self) -> TasksApi:
        return self._tasks_client
