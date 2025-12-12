from __future__ import annotations
from ..http import WSApiHttp, ApiResponse
from ..models.entities.contacts.contact_info import ContactInfo
from ..models.requests.contacts.contact_create_request import ContactCreateRequest
from ..models.requests.contacts.contact_update_request import ContactUpdateRequest


class ContactsClient:
    def __init__(self, http: WSApiHttp) -> None:
        self._http = http

    # Standard methods
    def list(self) -> list[ContactInfo]:
        return self._http.send_json("GET", "/contacts", model=list[ContactInfo])

    def get(self, contact_id: str) -> ContactInfo:
        return self._http.send_json("GET", f"/contacts/{contact_id}", model=ContactInfo)

    def create(self, request: ContactCreateRequest) -> None:
        self._http.send_json("POST", "/contacts", model=None, json=request.model_dump(by_alias=True))

    def update(self, contact_id: str, request: ContactUpdateRequest) -> None:
        self._http.send_json("PUT", f"/contacts/{contact_id}", model=None, json=request.model_dump(by_alias=True))

    # Try methods
    def try_list(self) -> ApiResponse[list[ContactInfo]]:
        return self._http.try_send_json("GET", "/contacts", model=list[ContactInfo])

    def try_get(self, contact_id: str) -> ApiResponse[ContactInfo]:
        return self._http.try_send_json("GET", f"/contacts/{contact_id}", model=ContactInfo)

    def try_create(self, request: ContactCreateRequest) -> ApiResponse[object]:
        return self._http.try_send_json("POST", "/contacts", model=None, json=request.model_dump(by_alias=True))

    def try_update(self, contact_id: str, request: ContactUpdateRequest) -> ApiResponse[object]:
        return self._http.try_send_json("PUT", f"/contacts/{contact_id}", model=None, json=request.model_dump(by_alias=True))
