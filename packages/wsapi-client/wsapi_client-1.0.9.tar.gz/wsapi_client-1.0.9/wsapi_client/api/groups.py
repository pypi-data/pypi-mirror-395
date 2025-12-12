from __future__ import annotations
from typing import List
from ..http import WSApiHttp, ApiResponse
from ..models.entities.groups.group_info import GroupInfo
from ..models.entities.groups.group_created import GroupCreated
from ..models.entities.groups.group_picture_info import GroupPictureInfo
from ..models.entities.groups.group_picture_updated import GroupPictureUpdated
from ..models.entities.groups.group_invite_info import GroupInviteInfo
from ..models.requests.groups.group_create_request import GroupCreateRequest
from ..models.requests.groups.group_update_description_request import GroupUpdateDescriptionRequest
from ..models.requests.groups.group_update_name_request import GroupUpdateNameRequest
from ..models.requests.groups.group_update_picture_request import GroupUpdatePictureRequest
from ..models.requests.groups.group_update_participants_request import GroupUpdateParticipantsRequest


class GroupsClient:
    def __init__(self, http: WSApiHttp) -> None:
        self._http = http

    # Standard methods
    def list(self) -> list[GroupInfo]:
        return self._http.send_json("GET", "/groups", model=list[GroupInfo])

    def get(self, group_id: str) -> GroupInfo:
        return self._http.send_json("GET", f"/groups/{group_id}", model=GroupInfo)

    def get_picture(self, group_id: str) -> GroupPictureInfo:
        return self._http.send_json("GET", f"/groups/{group_id}/picture", model=GroupPictureInfo)

    def create(self, request: GroupCreateRequest) -> GroupCreated:
        return self._http.send_json("POST", "/groups", model=GroupCreated, json=request.model_dump(by_alias=True))

    def update_description(self, group_id: str, request: GroupUpdateDescriptionRequest) -> None:
        self._http.send_json("PUT", f"/groups/{group_id}/description", model=None, json=request.model_dump(by_alias=True))

    def update_name(self, group_id: str, request: GroupUpdateNameRequest) -> None:
        self._http.send_json("PUT", f"/groups/{group_id}/name", model=None, json=request.model_dump(by_alias=True))

    def update_picture(self, group_id: str, request: GroupUpdatePictureRequest) -> GroupPictureUpdated:
        return self._http.send_json("POST", f"/groups/{group_id}/picture", model=GroupPictureUpdated, json=request.model_dump(by_alias=True))

    def delete(self, group_id: str) -> None:
        self._http.send_json("DELETE", f"/groups/{group_id}", model=None)

    def get_invite_link(self, group_id: str) -> str:
        return self._http.send_json("GET", f"/groups/{group_id}/invite-link", model=str)

    def get_requests(self, group_id: str) -> List[str]:
        return self._http.send_json("GET", f"/groups/{group_id}/requests", model=list[str])

    def update_participants(self, group_id: str, request: GroupUpdateParticipantsRequest) -> None:
        self._http.send_json("PUT", f"/groups/{group_id}/participants", model=None, json=request.model_dump(by_alias=True))

    def get_invite_info(self, invite_code: str) -> GroupInviteInfo:
        return self._http.send_json("GET", f"/group-invites/{invite_code}", model=GroupInviteInfo)

    # Try variants
    def try_list(self) -> ApiResponse[list[GroupInfo]]:
        return self._http.try_send_json("GET", "/groups", model=list[GroupInfo])

    def try_get(self, group_id: str) -> ApiResponse[GroupInfo]:
        return self._http.try_send_json("GET", f"/groups/{group_id}", model=GroupInfo)

    def try_get_picture(self, group_id: str) -> ApiResponse[GroupPictureInfo]:
        return self._http.try_send_json("GET", f"/groups/{group_id}/picture", model=GroupPictureInfo)

    def try_create(self, request: GroupCreateRequest) -> ApiResponse[GroupCreated]:
        return self._http.try_send_json("POST", "/groups", model=GroupCreated, json=request.model_dump(by_alias=True))

    def try_update_description(self, group_id: str, request: GroupUpdateDescriptionRequest) -> ApiResponse[object]:
        return self._http.try_send_json("PUT", f"/groups/{group_id}/description", model=None, json=request.model_dump(by_alias=True))

    def try_update_name(self, group_id: str, request: GroupUpdateNameRequest) -> ApiResponse[object]:
        return self._http.try_send_json("PUT", f"/groups/{group_id}/name", model=None, json=request.model_dump(by_alias=True))

    def try_update_picture(self, group_id: str, request: GroupUpdatePictureRequest) -> ApiResponse[GroupPictureUpdated]:
        return self._http.try_send_json("POST", f"/groups/{group_id}/picture", model=GroupPictureUpdated, json=request.model_dump(by_alias=True))

    def try_delete(self, group_id: str) -> ApiResponse[object]:
        return self._http.try_send_json("DELETE", f"/groups/{group_id}", model=None)

    def try_get_invite_link(self, group_id: str) -> ApiResponse[str]:
        return self._http.try_send_json("GET", f"/groups/{group_id}/invite-link", model=str)

    def try_get_requests(self, group_id: str) -> ApiResponse[List[str]]:
        return self._http.try_send_json("GET", f"/groups/{group_id}/requests", model=list[str])

    def try_update_participants(self, group_id: str, request: GroupUpdateParticipantsRequest) -> ApiResponse[object]:
        return self._http.try_send_json("PUT", f"/groups/{group_id}/participants", model=None, json=request.model_dump(by_alias=True))

    def try_get_invite_info(self, invite_code: str) -> ApiResponse[GroupInviteInfo]:
        return self._http.try_send_json("GET", f"/group-invites/{invite_code}", model=GroupInviteInfo)
