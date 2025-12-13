from collections.abc import Awaitable, Callable, Mapping, Sequence
from http import HTTPStatus
from typing import Any, Generic, Literal, TypeVar

from bayesline.api import (
    AsyncTypedSettingsRegistry,
    CouldNotDeleteSettingsError,
    CouldNotPermissionSettingsError,
    CouldNotSaveSettingsError,
    DeleteItemResult,
    DeleteResult,
    NewAsyncSettingsRegistry,
    NewSettingsRegistry,
    PermissionDeniedError,
    PermissionItemResult,
    PermissionResult,
    SaveItemResult,
    SaveResult,
    SettingResult,
    Settings,
    SettingsIdentifiers,
    SettingsRegistryError,
    SettingsTransferObject,
    TypedSettingsRegistry,
)
from httpx import Response

from .apiclient import ApiClient, AsyncApiClient

T = TypeVar("T", bound=Settings)


class AsyncTypedSettingsRegistryClient(AsyncTypedSettingsRegistry[T], Generic[T]):

    def __init__(
        self,
        settings_type: type[T],
        client: AsyncApiClient,
        user_fn: Callable[[], Awaitable[Mapping[str, str]]],
    ) -> None:
        self._settings_type = settings_type
        self._client = client
        self._user_fn = user_fn

    @property
    def settings_type(self) -> type[T]:
        return self._settings_type

    async def get_identifiers(
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers:
        return await _get_identifiers_async(self._client, which, self.settings_type)

    async def save(
        self,
        name_or_id: str | int,
        settings: T,
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveItemResult:
        result = await self.save_many(
            {name_or_id: settings}, overwrite=overwrite, raise_on_errors=raise_on_errors
        )
        return result[0]

    async def save_many(
        self,
        settings: Mapping[str | int, T],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult:
        return await _save_many_async(
            self._client, settings, overwrite, raise_on_errors, self._settings_type
        )

    async def read(self, name_or_id: str | int) -> SettingResult[T]:
        result = await self.read_many([name_or_id])
        return result[0]

    async def read_many(
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[T]]:
        return await _read_many_async(self._client, names_or_ids, [self._settings_type])

    async def delete(
        self, name_or_id: str | int, *, raise_on_errors: bool = True
    ) -> DeleteItemResult:
        result = await self.delete_many([name_or_id], raise_on_errors=raise_on_errors)
        return result.items[0]

    async def delete_many(
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult:
        return await _delete_many_async(self._client, names_or_ids, raise_on_errors)

    async def grant(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_setting: str | int,
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult:
        result = await self.grant_many(
            permission_to=permission_to,
            for_settings=[for_setting],
            to_groups=to_groups,
            to_users=to_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )
        return result.items[0]

    async def grant_many(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return await _permission_many_async(
            client=self._client,
            mode="grant",
            permission_to=permission_to,
            for_settings=for_settings,
            target_groups=to_groups,
            target_users=to_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    async def revoke(
        self,
        *,
        for_setting: str | int,
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult:
        result = await self.revoke_many(
            for_settings=[for_setting],
            from_groups=from_groups,
            from_users=from_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )
        return result.items[0]

    async def revoke_many(
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return await _permission_many_async(
            client=self._client,
            mode="revoke",
            permission_to=None,
            for_settings=for_settings,
            target_groups=from_groups,
            target_users=from_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    async def list_user_names(self) -> Mapping[str, str]:
        return await self._user_fn()


class TypedSettingsRegistryClient(TypedSettingsRegistry[T], Generic[T]):

    def __init__(
        self,
        settings_type: type[T],
        client: ApiClient,
        user_fn: Callable[[], Mapping[str, str]],
    ) -> None:
        self._settings_type = settings_type
        self._client = client
        self._user_fn = user_fn

    @property
    def settings_type(self) -> type[T]:
        return self._settings_type

    def get_identifiers(
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers:
        return _get_identifiers(self._client, which, self.settings_type)

    def save(
        self,
        name_or_id: str | int,
        settings: T,
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveItemResult:
        result = self.save_many(
            {name_or_id: settings}, overwrite=overwrite, raise_on_errors=raise_on_errors
        )
        return result[0]

    def save_many(
        self,
        settings: Mapping[str | int, T],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult:
        return _save_many_sync(
            self._client, settings, overwrite, raise_on_errors, self._settings_type
        )

    def read(self, name_or_id: str | int) -> SettingResult[T]:
        result = self.read_many([name_or_id])
        return result[0]

    def read_many(
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[T]]:
        return _read_many_sync(self._client, names_or_ids, [self._settings_type])

    def delete(
        self, name_or_id: str | int, *, raise_on_errors: bool = True
    ) -> DeleteItemResult:
        result = self.delete_many([name_or_id], raise_on_errors=raise_on_errors)
        return result.items[0]

    def delete_many(
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult:
        return _delete_many_sync(self._client, names_or_ids, raise_on_errors)

    def grant(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_setting: str | int,
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult:
        return self.grant_many(
            permission_to=permission_to,
            for_settings=[for_setting],
            to_groups=to_groups,
            to_users=to_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        ).items[0]

    def grant_many(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return _permission_many_sync(
            client=self._client,
            mode="grant",
            permission_to=permission_to,
            for_settings=for_settings,
            target_groups=to_groups,
            target_users=to_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    def revoke(
        self,
        *,
        for_setting: str | int,
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionItemResult:
        return self.revoke_many(
            for_settings=[for_setting],
            from_groups=from_groups,
            from_users=from_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        ).items[0]

    def revoke_many(
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return _permission_many_sync(
            client=self._client,
            mode="revoke",
            permission_to=None,
            for_settings=for_settings,
            target_groups=from_groups,
            target_users=from_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    def list_user_names(self) -> Mapping[str, str]:
        return self._user_fn()


class AsyncSettingsRegistryClient(NewAsyncSettingsRegistry):

    def __init__(self, client: AsyncApiClient) -> None:
        self._client = client.append_base_path("settings")
        self._user_client = client.append_base_path("auth/users")

    def __getitem__(self, settings_type: type[T]) -> AsyncTypedSettingsRegistry[T]:
        return AsyncTypedSettingsRegistryClient[T](
            settings_type, self._client, self.list_user_names
        )

    async def get_identifiers(
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers:
        return await _get_identifiers_async(self._client, which)

    async def save_many(
        self,
        settings: Mapping[str | int, Settings],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult:
        return await _save_many_async(
            self._client, settings, overwrite, raise_on_errors
        )

    async def read_many(
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[T]]:
        settings_types = list(await self.get_settings_types())
        return await _read_many_async(self._client, names_or_ids, settings_types)

    async def delete_many(
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult:
        return await _delete_many_async(self._client, names_or_ids, raise_on_errors)

    async def grant_many(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return await _permission_many_async(
            client=self._client,
            mode="grant",
            permission_to=permission_to,
            for_settings=for_settings,
            target_groups=to_groups,
            target_users=to_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    async def revoke_many(
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return await _permission_many_async(
            client=self._client,
            mode="revoke",
            permission_to=None,
            for_settings=for_settings,
            target_groups=from_groups,
            target_users=from_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    async def list_user_names(self) -> Mapping[str, str]:
        response = await self._user_client.options("/names")
        response.raise_for_status()
        return response.json()


class SettingsRegistryClient(NewSettingsRegistry):

    def __init__(self, client: ApiClient) -> None:
        self._client = client.append_base_path("settings")
        self._user_client = client.append_base_path("auth/users")

    def __getitem__(self, settings_type: type[T]) -> TypedSettingsRegistry[T]:
        return TypedSettingsRegistryClient[T](
            settings_type, self._client, self.list_user_names
        )

    def get_identifiers(
        self, which: Literal["all", "mine"] = "all"
    ) -> SettingsIdentifiers:
        return _get_identifiers(self._client, which)

    def save_many(
        self,
        settings: Mapping[str | int, Settings],
        *,
        overwrite: bool = False,
        raise_on_errors: bool = True,
    ) -> SaveResult:
        return _save_many_sync(self._client, settings, overwrite, raise_on_errors)

    def read_many(
        self, names_or_ids: Sequence[str | int]
    ) -> Sequence[SettingResult[T]]:
        settings_types = list(self.get_settings_types())
        return _read_many_sync(self._client, names_or_ids, settings_types)

    def delete_many(
        self, names_or_ids: Sequence[str | int], *, raise_on_errors: bool = True
    ) -> DeleteResult:
        return _delete_many_sync(self._client, names_or_ids, raise_on_errors)

    def grant_many(
        self,
        *,
        permission_to: Literal["read", "write", "delete", "admin"],
        for_settings: list[str | int],
        to_groups: list[str] | None = None,
        to_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return _permission_many_sync(
            client=self._client,
            mode="grant",
            permission_to=permission_to,
            for_settings=for_settings,
            target_groups=to_groups,
            target_users=to_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    def revoke_many(
        self,
        *,
        for_settings: list[str | int],
        from_groups: list[str] | None = None,
        from_users: list[str] | None = None,
        including_references: bool = False,
        raise_on_errors: bool = True,
    ) -> PermissionResult:
        return _permission_many_sync(
            client=self._client,
            mode="revoke",
            permission_to=None,
            for_settings=for_settings,
            target_groups=from_groups,
            target_users=from_users,
            including_references=including_references,
            raise_on_errors=raise_on_errors,
        )

    def list_user_names(self) -> Mapping[str, str]:
        response = self._user_client.options("/names")
        response.raise_for_status()
        return response.json()


def _get_identifiers(
    client: ApiClient,
    which: Literal["all", "mine"] = "all",
    settings_type: type[Settings] | None = None,
) -> SettingsIdentifiers:
    params: dict[str, Any] = {"which": which}
    if settings_type:
        params["settings_type"] = settings_type.__name__
    response = client.get("/", params=params)
    _handle_response(response)
    return SettingsIdentifiers.model_validate(response.json())


async def _get_identifiers_async(
    client: AsyncApiClient,
    which: Literal["all", "mine"] = "all",
    settings_type: type[Settings] | None = None,
) -> SettingsIdentifiers:
    params: dict[str, Any] = {"which": which}
    if settings_type:
        params["settings_type"] = settings_type.__name__
    response = await client.get("/", params=params)
    _handle_response(response)
    return SettingsIdentifiers.model_validate(response.json())


def _create_settings_transfer_objects(
    settings: Mapping[str | int, Settings],
) -> list[dict[str, Any]]:
    return [
        SettingsTransferObject(
            kind="valid",
            name=name_or_id if isinstance(name_or_id, str) else None,
            identifier=name_or_id if isinstance(name_or_id, int) else None,
            value=settings_obj.model_dump(),
            settings_type=settings_obj.__class__.__name__,
        ).model_dump()
        for name_or_id, settings_obj in settings.items()
    ]


def _save_many_sync(
    client: ApiClient,
    settings: Mapping[str | int, Settings],
    overwrite: bool,
    raise_on_errors: bool,
    settings_type: type[Settings] | None = None,
) -> SaveResult:
    body = {
        "settings": _create_settings_transfer_objects(settings),
        "settings_type": settings_type.__name__ if settings_type else None,
    }
    response = client.post(
        "/save",
        body=body,
        params={"overwrite": overwrite, "raise_on_errors": raise_on_errors},
    )
    _handle_response(response)
    return SaveResult.model_validate(response.json())


async def _save_many_async(
    client: AsyncApiClient,
    settings: Mapping[str | int, Settings],
    overwrite: bool,
    raise_on_errors: bool,
    settings_type: type[Settings] | None = None,
) -> SaveResult:
    body = {
        "settings": _create_settings_transfer_objects(settings),
        "settings_type": settings_type.__name__ if settings_type else None,
    }
    response = await client.post(
        "/save",
        body=body,
        params={"overwrite": overwrite, "raise_on_errors": raise_on_errors},
    )
    _handle_response(response)
    return SaveResult.model_validate(response.json())


def _read_many_sync(
    client: ApiClient,
    names_or_ids: Sequence[str | int],
    settings_types: list[type[Settings]],
) -> Sequence[SettingResult[T]]:
    response = client.post("/read", body={"names_or_ids": names_or_ids})
    _handle_response(response)
    stos = [SettingsTransferObject.model_validate(s) for s in response.json()]
    return [sto.to_settings(settings_types) for sto in stos]


async def _read_many_async(
    client: AsyncApiClient,
    names_or_ids: Sequence[str | int],
    settings_types: list[type[Settings]],
) -> Sequence[SettingResult[T]]:
    response = await client.post("/read", body={"names_or_ids": names_or_ids})
    _handle_response(response)
    stos = [SettingsTransferObject.model_validate(s) for s in response.json()]
    return [sto.to_settings(settings_types) for sto in stos]


def _delete_many_sync(
    client: ApiClient,
    names_or_ids: Sequence[str | int],
    raise_on_errors: bool,
) -> DeleteResult:
    response = client.post(
        "/delete",
        body={"names_or_ids": names_or_ids},
        params={"raise_on_errors": raise_on_errors},
    )
    _handle_response(response)
    return DeleteResult.model_validate(response.json())


async def _delete_many_async(
    client: AsyncApiClient,
    names_or_ids: Sequence[str | int],
    raise_on_errors: bool,
) -> DeleteResult:
    response = await client.post(
        "/delete",
        body={"names_or_ids": names_or_ids},
        params={"raise_on_errors": raise_on_errors},
    )
    _handle_response(response)
    return DeleteResult.model_validate(response.json())


def _permission_many_sync(
    client: ApiClient,
    mode: Literal["grant", "revoke"],
    permission_to: Literal["read", "write", "delete", "admin"] | None,
    for_settings: list[str | int],
    target_groups: list[str] | None,
    target_users: list[str] | None,
    including_references: bool,
    raise_on_errors: bool,
) -> PermissionResult:
    response = client.post(
        "/permission",
        body={
            "mode": mode,
            "permission_to": permission_to,
            "for_settings": for_settings,
            "target_groups": target_groups or [],
            "target_users": target_users or [],
            "including_references": including_references,
        },
        params={"raise_on_errors": raise_on_errors},
    )
    _handle_response(response)
    return PermissionResult.model_validate(response.json())


async def _permission_many_async(
    client: AsyncApiClient,
    mode: Literal["grant", "revoke"],
    permission_to: Literal["read", "write", "delete", "admin"] | None,
    for_settings: list[str | int],
    target_groups: list[str] | None,
    target_users: list[str] | None,
    including_references: bool,
    raise_on_errors: bool,
) -> PermissionResult:
    response = await client.post(
        "/permission",
        body={
            "mode": mode,
            "permission_to": permission_to,
            "for_settings": for_settings,
            "target_groups": target_groups or [],
            "target_users": target_users or [],
            "including_references": including_references,
        },
        params={"raise_on_errors": raise_on_errors},
    )
    _handle_response(response)
    return PermissionResult.model_validate(response.json())


def _handle_response(response: Response) -> None:
    exc_types: list[type[Exception]] = [
        CouldNotPermissionSettingsError,
        CouldNotDeleteSettingsError,
        CouldNotSaveSettingsError,
        ValueError,
        KeyError,
        PermissionDeniedError,
        SettingsRegistryError,
    ]
    if response.status_code != HTTPStatus.OK:
        response_json = {}
        try:
            response_json = response.json()
        except Exception:
            response.raise_for_status()

        if response.status_code == HTTPStatus.NOT_FOUND and (
            not isinstance(response_json["detail"], dict)
            or "type" not in response_json["detail"]
        ):
            raise KeyError(response_json["detail"])

        if "detail" in response_json and "message" in response_json["detail"]:
            detail = response_json["detail"]
            message = detail["message"]
            if "type" in detail:
                for exc_type in exc_types:
                    if exc_type.__name__ == detail["type"]:
                        raise exc_type(message)
            raise Exception(message)

    response.raise_for_status()
