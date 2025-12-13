from bayesline.api import (
    AsyncSettingsRegistry,
    InvalidSettingsError,
    Mode,
    RawSettings,
    SettingsMenuType,
    SettingsMetaData,
    SettingsRegistry,
    SettingsType,
)

from .apiclient import ApiClient, AsyncApiClient


class HttpSettingsRegistryClient(SettingsRegistry[SettingsType, SettingsMenuType]):

    def __init__(
        self,
        client: ApiClient,
        settings_type: type[SettingsType],
        settings_menu_type: type[SettingsMenuType],
    ):
        self._client = client
        self._settings_type = settings_type
        self._settings_menu_type = settings_menu_type

    def available_settings(self, dataset_name: str | None = None) -> SettingsMenuType:
        params = {"dataset": dataset_name} if dataset_name else {}
        content = self._client.get("available-settings", params=params)
        return self._settings_menu_type.model_validate_json(content.text)

    def ids(self, mode: Mode = "Valid") -> dict[int, str]:
        return {v: k for k, v in self.names(mode=mode).items()}

    def names(self, mode: Mode = "Valid") -> dict[str, int]:
        return self._client.get("settings", params={"mode": mode}).json()

    def get_raw(self, name_or_id: list[str | int]) -> list[RawSettings]:
        result = self._client.post("raw-settings", body={"refs": name_or_id})
        return [RawSettings.model_validate(r) for r in result.json()]

    def get(self, name: str | int) -> SettingsType:
        content = self._client.get(f"settings/{name}")
        if content.status_code == 404:
            raise KeyError(f"Could not find settings for input: {name}")
        elif content.status_code == 400:
            raise InvalidSettingsError(content.json()["detail"])
        return self._settings_type.model_validate_json(content.text)

    def get_all(self) -> dict[str, SettingsType]:
        content = self._client.get("all-settings").json()
        return {
            name: self._settings_type.model_validate(settings)
            for name, settings in content.items()
        }

    def get_all_metadata(self) -> dict[str, SettingsMetaData]:
        content = self._client.get("all-settings-metadata").json()
        return {
            name: SettingsMetaData.model_validate(metadata)
            for name, metadata in content.items()
        }

    def get_metadata(self, name: str | int) -> SettingsMetaData:
        content = self._client.get(f"settings/{name}/metadata")
        return SettingsMetaData.model_validate_json(content.text)

    def _do_save(self, name: str, settings: SettingsType) -> int:
        content = self._client.post(f"settings/{name}", settings)
        if content.status_code == 400:
            raise ValueError(content.json()["detail"])
        return content.json()

    def _do_update(self, name: str | int, settings: SettingsType) -> RawSettings:
        content = self._client.put(f"settings/{name}", settings)
        if content.status_code == 404:
            raise KeyError(f"Could not find settings for input: {name}")
        return RawSettings.model_validate_json(content.text)

    def delete(self, name: str | int) -> RawSettings:
        content = self._client.delete(f"settings/{name}")
        if content.status_code == 404:
            raise KeyError(f"Could not find settings for input: {name}")
        return RawSettings.model_validate_json(content.text)


class AsyncHttpSettingsRegistryClient(
    AsyncSettingsRegistry[SettingsType, SettingsMenuType]
):

    def __init__(
        self,
        client: AsyncApiClient,
        settings_type: type[SettingsType],
        settings_menu_type: type[SettingsMenuType],
    ):
        self._client = client
        self._settings_type = settings_type
        self._settings_menu_type = settings_menu_type

    async def available_settings(
        self, dataset_name: str | None = None
    ) -> SettingsMenuType:
        params = {"dataset": dataset_name} if dataset_name else {}
        content = await self._client.get("available-settings", params=params)
        return self._settings_menu_type.model_validate_json(content.text)

    async def ids(self, mode: Mode = "Valid") -> dict[int, str]:
        return {v: k for k, v in (await self.names(mode=mode)).items()}

    async def names(self, mode: Mode = "Valid") -> dict[str, int]:
        return (await self._client.get("settings", params={"mode": mode})).json()

    async def get_raw(self, name_or_id: list[str | int]) -> list[RawSettings]:
        result = await self._client.post("raw-settings", body={"refs": name_or_id})
        return [RawSettings.model_validate(r) for r in result.json()]

    async def get(self, name: str | int) -> SettingsType:
        content = await self._client.get(f"settings/{name}")
        if content.status_code == 404:
            raise KeyError(f"Could not find settings for input: {name}")
        elif content.status_code == 400:
            raise InvalidSettingsError(content.json()["detail"])
        return self._settings_type.model_validate_json(content.text)

    async def get_all(self) -> dict[str, SettingsType]:
        content = (await self._client.get("all-settings")).json()
        return {
            name: self._settings_type.model_validate(settings)
            for name, settings in content.items()
        }

    async def get_all_metadata(self) -> dict[str, SettingsMetaData]:
        content = (await self._client.get("all-settings-metadata")).json()
        return {
            name: SettingsMetaData.model_validate(metadata)
            for name, metadata in content.items()
        }

    async def get_metadata(self, name: str | int) -> SettingsMetaData:
        content = await self._client.get(f"settings/{name}/metadata")
        return SettingsMetaData.model_validate_json(content.text)

    async def _do_save(self, name: str, settings: SettingsType) -> int:
        content = await self._client.post(f"settings/{name}", settings)
        if content.status_code == 400:
            raise ValueError(content.json()["detail"])
        return content.json()

    async def _do_update(self, name: str | int, settings: SettingsType) -> RawSettings:
        content = await self._client.put(f"settings/{name}", settings)
        if content.status_code == 404:
            raise KeyError(f"Could not find settings for input: {name}")
        return RawSettings.model_validate_json(content.text)

    async def delete(self, name: str | int) -> RawSettings:
        content = await self._client.delete(f"settings/{name}")
        if content.status_code == 404:
            raise KeyError(f"Could not find settings for input: {name}")
        return RawSettings.model_validate_json(content.text)
