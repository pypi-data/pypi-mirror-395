import datetime as dt
from typing import Any

from bayesline.api import (
    AsyncIncidentsServiceApi,
    IncidentsServiceApi,
    IncidentSummary,
    IncidentSummaryItem,
)
from bayesline.api.types import DateLike

from bayesline.apiclient._src.apiclient import ApiClient, AsyncApiClient


def _date_like_to_str(date: DateLike | None) -> str | None:
    """Convert a DateLike object to an ISO format string.

    Parameters
    ----------
    date : DateLike | None
        The date-like object to convert.

    Returns
    -------
    str | None
        The ISO format string, or None if the input is None.
    """
    if date is None:
        return None
    if isinstance(date, dt.datetime):
        return date.isoformat()
    if isinstance(date, dt.date):
        return date.isoformat()
    if isinstance(date, str):
        return date
    raise ValueError(f"Invalid date type: {type(date)}")


class AsyncIncidentsServiceClientImpl(AsyncIncidentsServiceApi):
    """Async client for the incidents API."""

    def __init__(self, client: AsyncApiClient):
        self._client = client

    async def submit_incident(
        self, incident_id: str, source: str, body: dict[str, Any]
    ) -> IncidentSummaryItem:
        response = await self._client.post(
            f"/v1/maintenance/incidents/{incident_id}",
            body=body,
            params={"source": source},
        )
        return IncidentSummaryItem.model_validate(response.json())

    async def get_incident_summary(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        start_idx: int = 0,
        end_idx: int = 999999999,
    ) -> IncidentSummary:
        params = {
            k: v
            for k, v in {
                "start_date": _date_like_to_str(start_date),
                "end_date": _date_like_to_str(end_date),
                "start_idx": start_idx,
                "end_idx": end_idx,
            }.items()
            if v is not None
        }
        response = await self._client.get("/v1/maintenance/incidents", params=params)
        return IncidentSummary.model_validate(response.json())

    async def get_incident(self, incident_id: str) -> dict[str, dict[str, Any]]:
        response = await self._client.get(f"/v1/maintenance/incidents/{incident_id}")
        return response.json()


class IncidentsServiceClientImpl(IncidentsServiceApi):
    """Synchronous client for the incidents API."""

    def __init__(self, client: ApiClient):
        self._client = client

    def submit_incident(
        self, incident_id: str, source: str, body: dict[str, Any]
    ) -> IncidentSummaryItem:
        response = self._client.post(
            f"/v1/maintenance/incidents/{incident_id}",
            body=body,
            params={"source": source},
        )
        return IncidentSummaryItem.model_validate(response.json())

    def get_incident_summary(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        start_idx: int = 0,
        end_idx: int = 999999999,
    ) -> IncidentSummary:
        params = {
            k: v
            for k, v in {
                "start_date": _date_like_to_str(start_date),
                "end_date": _date_like_to_str(end_date),
                "start_idx": start_idx,
                "end_idx": end_idx,
            }.items()
            if v is not None
        }
        response = self._client.get("/v1/maintenance/incidents", params=params)
        return IncidentSummary.model_validate(response.json())

    def get_incident(self, incident_id: str) -> dict[str, dict[str, Any]]:
        response = self._client.get(f"/v1/maintenance/incidents/{incident_id}")
        return response.json()
