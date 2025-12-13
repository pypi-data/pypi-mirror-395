import json
from collections.abc import Sequence

import httpx
from bayesline.api import (
    ACLError,
    ACLValidationError,
    AsyncPermissionsApi,
    GroupCreationError,
    GroupDeletionError,
    GroupMembership,
    GroupMembershipError,
    GroupUpdateError,
    PermissionDeniedError,
    PermissionGrantError,
    PermissionLevel,
    PermissionsApi,
    PrincipalNotFoundError,
    PrincipalType,
    ResourceNotFoundError,
    ResourceType,
    RoleAssignmentError,
    RoleType,
    UserGroup,
    UserPermissionsSummary,
    UserRole,
)

from bayesline.apiclient._src.apiclient import ApiClient, AsyncApiClient


def _unescape(s: str) -> str:
    """Unescape JSON-encoded strings."""
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return s


def _raise_from_type(exception_type: str, message: str) -> None:
    """Raise the appropriate exception based on the type string."""
    exception_map = {
        "PermissionDeniedError": PermissionDeniedError,
        "ResourceNotFoundError": ResourceNotFoundError,
        "PrincipalNotFoundError": PrincipalNotFoundError,
        "ACLValidationError": ACLValidationError,
        "PermissionGrantError": PermissionGrantError,
        "GroupCreationError": GroupCreationError,
        "GroupUpdateError": GroupUpdateError,
        "GroupDeletionError": GroupDeletionError,
        "GroupMembershipError": GroupMembershipError,
        "RoleAssignmentError": RoleAssignmentError,
        "KeyError": KeyError,
        "ValueError": ValueError,
        "ACLError": ACLError,
    }

    exception_class = exception_map.get(exception_type)
    if exception_class:
        raise exception_class(message) from None


def _raise_for_status(response: httpx.Response) -> None:
    """Convert HTTP error responses back to appropriate exceptions."""
    if response.status_code in {200, 201, 202, 204}:
        return

    try:
        details = response.json()["detail"]
        if "type" in details:
            message = _unescape(details["message"])
            _raise_from_type(details["type"], message)
    except (KeyError, ValueError, json.JSONDecodeError):
        # If we can't parse the response, fall back to default behavior
        pass

    # Fall back to raising HTTPStatusError for unhandled cases
    response.raise_for_status()


class PermissionsApiClient(PermissionsApi):

    def __init__(self, client: ApiClient):
        self._client = client

    # ===== Permission Check and Query =====
    def get_user_permissions(
        self,
        resource_type: ResourceType | None = None,
        resource_ids: Sequence[int] | None = None,
    ) -> UserPermissionsSummary:
        params = {}
        if resource_type is not None:
            params["resource_type"] = resource_type.value
        if resource_ids is not None:
            params["resource_ids"] = resource_ids

        response = self._client.get("/permissions/user-permissions", params=params)
        _raise_for_status(response)
        return UserPermissionsSummary.model_validate(response.json())

    def check_permission(
        self,
        resource_id: int,
        required_permission: PermissionLevel,
    ) -> bool:
        response = self._client.get(
            "/permissions/check-permission",
            params={
                "resource_id": resource_id,
                "required_permission": required_permission.value,
            },
        )
        _raise_for_status(response)
        return response.json()

    def get_accessible_resources(
        self,
        resource_type: ResourceType,
        required_permission: PermissionLevel,
    ) -> Sequence[int]:
        response = self._client.get(
            "/permissions/accessible-resources",
            params={
                "resource_type": resource_type.value,
                "required_permission": required_permission.value,
            },
        )
        _raise_for_status(response)
        return response.json()

    # ===== Permission Updates =====

    def grant_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None:
        response = self._client.post(
            "/permissions/grant-permission",
            body={},
            params={
                "resource_id": resource_id,
                "principal_type": principal_type.value,
                "principal_id": principal_id,
                "permission_level": permission_level.value,
            },
        )
        _raise_for_status(response)

    def revoke_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
    ) -> None:
        response = self._client.delete(
            "/permissions/revoke-permission",
            params={
                "resource_id": resource_id,
                "principal_type": principal_type.value,
                "principal_id": principal_id,
            },
        )
        _raise_for_status(response)

    def update_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None:
        response = self._client.put(
            "/permissions/update-permission",
            body={},
            params={
                "resource_id": resource_id,
                "principal_type": principal_type.value,
                "principal_id": principal_id,
                "permission_level": permission_level.value,
            },
        )
        _raise_for_status(response)

    # ===== Group Management =====

    def create_group(
        self,
        name: str,
        description: str,
    ) -> int:
        response = self._client.post(
            "/permissions/groups",
            body={},
            params={
                "name": name,
                "description": description,
            },
        )
        _raise_for_status(response)
        return response.json()["group_id"]

    def update_group(
        self,
        group_id: int,
        description: str,
    ) -> None:
        response = self._client.put(
            f"/permissions/groups/{group_id}",
            body={},
            params={"description": description},
        )
        _raise_for_status(response)

    def delete_group(
        self,
        group_id: int,
    ) -> None:
        response = self._client.delete(f"/permissions/groups/{group_id}")
        _raise_for_status(response)

    def list_groups(self) -> Sequence[UserGroup]:
        response = self._client.get("/permissions/groups")
        _raise_for_status(response)
        return [UserGroup.model_validate(group) for group in response.json()]

    # ===== Group Membership =====

    def add_user_to_group(
        self,
        group_id: int,
        user_id: str,
    ) -> None:
        response = self._client.post(
            f"/permissions/groups/{group_id}/members",
            body={},
            params={"user_id": user_id},
        )
        _raise_for_status(response)

    def remove_user_from_group(
        self,
        group_id: int,
        user_id: str,
    ) -> None:
        response = self._client.delete(
            f"/permissions/groups/{group_id}/members/{user_id}"
        )
        _raise_for_status(response)

    def list_group_members(
        self,
        group_id: int,
    ) -> Sequence[GroupMembership]:
        response = self._client.get(f"/permissions/groups/{group_id}/members")
        _raise_for_status(response)
        return [GroupMembership.model_validate(member) for member in response.json()]

    # ===== Role Management =====

    def assign_role(
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None:
        response = self._client.post(
            "/permissions/roles/assign",
            body={},
            params={
                "user_id": user_id,
                "role_type": role_type.value,
            },
        )
        _raise_for_status(response)

    def revoke_role(
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None:
        response = self._client.delete(
            "/permissions/roles/revoke",
            params={
                "user_id": user_id,
                "role_type": role_type.value,
            },
        )
        _raise_for_status(response)

    def list_user_roles(
        self,
        user_id: str | None = None,
    ) -> Sequence[UserRole]:
        endpoint = (
            f"/permissions/roles/users/{user_id}"
            if user_id
            else "/permissions/roles/users/"
        )
        response = self._client.get(endpoint)
        _raise_for_status(response)
        return [UserRole.model_validate(role) for role in response.json()]


class AsyncPermissionsApiClient(AsyncPermissionsApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client

    # ===== Permission Check and Query =====

    async def get_user_permissions(
        self,
        resource_type: ResourceType | None = None,
        resource_ids: Sequence[int] | None = None,
    ) -> UserPermissionsSummary:
        params = {}
        if resource_type is not None:
            params["resource_type"] = resource_type.value
        if resource_ids is not None:
            params["resource_ids"] = resource_ids

        response = await self._client.get(
            "/permissions/user-permissions", params=params
        )
        _raise_for_status(response)
        return UserPermissionsSummary.model_validate(response.json())

    async def check_permission(
        self,
        resource_id: int,
        required_permission: PermissionLevel,
    ) -> bool:
        response = await self._client.get(
            "/permissions/check-permission",
            params={
                "resource_id": resource_id,
                "required_permission": required_permission.value,
            },
        )
        _raise_for_status(response)
        return response.json()

    async def get_accessible_resources(
        self,
        resource_type: ResourceType,
        required_permission: PermissionLevel,
    ) -> Sequence[int]:
        response = await self._client.get(
            "/permissions/accessible-resources",
            params={
                "resource_type": resource_type.value,
                "required_permission": required_permission.value,
            },
        )
        _raise_for_status(response)
        return response.json()

    # ===== Permission Updates =====

    async def grant_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None:
        response = await self._client.post(
            "/permissions/grant-permission",
            body={},
            params={
                "resource_id": resource_id,
                "principal_type": principal_type.value,
                "principal_id": principal_id,
                "permission_level": permission_level.value,
            },
        )
        _raise_for_status(response)

    async def revoke_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
    ) -> None:
        response = await self._client.delete(
            "/permissions/revoke-permission",
            params={
                "resource_id": resource_id,
                "principal_type": principal_type.value,
                "principal_id": principal_id,
            },
        )
        _raise_for_status(response)

    async def update_permission(
        self,
        resource_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        permission_level: PermissionLevel,
    ) -> None:
        response = await self._client.put(
            "/permissions/update-permission",
            body={},
            params={
                "resource_id": resource_id,
                "principal_type": principal_type.value,
                "principal_id": principal_id,
                "permission_level": permission_level.value,
            },
        )
        _raise_for_status(response)

    # ===== Group Management =====

    async def create_group(
        self,
        name: str,
        description: str,
    ) -> int:
        response = await self._client.post(
            "/permissions/groups",
            body={},
            params={
                "name": name,
                "description": description,
            },
        )
        _raise_for_status(response)
        return response.json()["group_id"]

    async def update_group(
        self,
        group_id: int,
        description: str,
    ) -> None:
        response = await self._client.put(
            f"/permissions/groups/{group_id}",
            body={},
            params={"description": description},
        )
        _raise_for_status(response)

    async def delete_group(
        self,
        group_id: int,
    ) -> None:
        response = await self._client.delete(f"/permissions/groups/{group_id}")
        _raise_for_status(response)

    async def list_groups(self) -> Sequence[UserGroup]:
        response = await self._client.get("/permissions/groups")
        _raise_for_status(response)
        return [UserGroup.model_validate(group) for group in response.json()]

    # ===== Group Membership =====

    async def add_user_to_group(
        self,
        group_id: int,
        user_id: str,
    ) -> None:
        response = await self._client.post(
            f"/permissions/groups/{group_id}/members",
            body={},
            params={"user_id": user_id},
        )
        _raise_for_status(response)

    async def remove_user_from_group(
        self,
        group_id: int,
        user_id: str,
    ) -> None:
        response = await self._client.delete(
            f"/permissions/groups/{group_id}/members/{user_id}"
        )
        _raise_for_status(response)

    async def list_group_members(
        self,
        group_id: int,
    ) -> Sequence[GroupMembership]:
        response = await self._client.get(f"/permissions/groups/{group_id}/members")
        _raise_for_status(response)
        return [GroupMembership.model_validate(member) for member in response.json()]

    # ===== Role Management =====

    async def assign_role(
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None:
        response = await self._client.post(
            "/permissions/roles/assign",
            body={},
            params={
                "user_id": user_id,
                "role_type": role_type.value,
            },
        )
        _raise_for_status(response)

    async def revoke_role(
        self,
        user_id: str,
        role_type: RoleType,
    ) -> None:
        response = await self._client.delete(
            "/permissions/roles/revoke",
            params={
                "user_id": user_id,
                "role_type": role_type.value,
            },
        )
        _raise_for_status(response)

    async def list_user_roles(
        self,
        user_id: str | None = None,
    ) -> Sequence[UserRole]:
        endpoint = (
            f"/permissions/roles/users/{user_id}"
            if user_id
            else "/permissions/roles/users/"
        )
        response = await self._client.get(endpoint)
        _raise_for_status(response)
        return [UserRole.model_validate(role) for role in response.json()]
