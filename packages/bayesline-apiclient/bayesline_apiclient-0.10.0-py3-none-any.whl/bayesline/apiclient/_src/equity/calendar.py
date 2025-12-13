import datetime as dt
from typing import Any

from bayesline.api import (
    AsyncSettingsRegistry,
    SettingsRegistry,
)
from bayesline.api.equity import (
    AsyncCalendarApi,
    AsyncCalendarLoaderApi,
    CalendarApi,
    CalendarLoaderApi,
    CalendarSettings,
    CalendarSettingsMenu,
)
from bayesline.api.types import DateLike, to_date, to_date_string

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient
from bayesline.apiclient._src.settings import (
    AsyncHttpSettingsRegistryClient,
    HttpSettingsRegistryClient,
)


class CalendarClientImpl(CalendarApi):

    def __init__(
        self,
        client: ApiClient,
        calendar_settings: CalendarSettings,
    ):
        self._client = client
        self._calendar_settings = calendar_settings

    @property
    def settings(self) -> CalendarSettings:
        return self._calendar_settings

    def get(
        self, *, start: DateLike | None = None, end: DateLike | None = None
    ) -> list[dt.date]:
        params: dict[str, Any] = {}

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)

        response = self._client.post(
            "", params=params, body=self._calendar_settings.model_dump()
        )
        return [to_date(d) for d in response.json()]


class AsyncCalendarClientImpl(AsyncCalendarApi):
    def __init__(
        self,
        client: AsyncApiClient,
        calendar_settings: CalendarSettings,
    ):
        self._client = client
        self._calendar_settings = calendar_settings

    @property
    def settings(self) -> CalendarSettings:
        return self._calendar_settings

    async def get(
        self, *, start: DateLike | None = None, end: DateLike | None = None
    ) -> list[dt.date]:
        params: dict[str, Any] = {}

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)

        response = await self._client.post(
            "", params=params, body=self._calendar_settings.model_dump()
        )
        return [to_date(d) for d in response.json()]


class CalendarLoaderClientImpl(CalendarLoaderApi):

    def __init__(
        self,
        client: ApiClient,
    ):
        self._client = client.append_base_path("calendar")
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/calendar"),
            CalendarSettings,
            CalendarSettingsMenu,
        )

    @property
    def settings(self) -> SettingsRegistry[CalendarSettings, CalendarSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | CalendarSettings) -> CalendarApi:
        if isinstance(ref_or_settings, CalendarSettings):
            settings_menu = self._settings.available_settings(
                dataset_name=ref_or_settings.dataset
            )
            ref_or_settings.validate_settings(settings_menu)
            return CalendarClientImpl(
                self._client,
                ref_or_settings,
            )
        else:
            calendar_settings = self.settings.get(ref_or_settings)
            return CalendarClientImpl(
                self._client,
                calendar_settings,
            )


class AsyncCalendarLoaderClientImpl(AsyncCalendarLoaderApi):
    def __init__(
        self,
        client: AsyncApiClient,
    ):
        self._client = client.append_base_path("calendar")
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/calendar"),
            CalendarSettings,
            CalendarSettingsMenu,
        )

    @property
    def settings(self) -> AsyncSettingsRegistry[CalendarSettings, CalendarSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | CalendarSettings
    ) -> AsyncCalendarApi:
        if isinstance(ref_or_settings, CalendarSettings):
            settings_menu = await self._settings.available_settings(
                dataset_name=ref_or_settings.dataset
            )
            ref_or_settings.validate_settings(settings_menu)
            return AsyncCalendarClientImpl(
                self._client,
                ref_or_settings,
            )
        else:
            calendar_settings = await self.settings.get(ref_or_settings)
            return AsyncCalendarClientImpl(
                self._client,
                calendar_settings,
            )
