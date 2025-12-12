"""Client for authentication operations."""


from ..models import APIAccess, APIKey
from ..http_client import HTTPClient


class AuthClient:
    """Client for managing API keys."""

    def __init__(self, http_client: "HTTPClient"):
        self._http = http_client

    def create_api_key(self, key_name: str, access: APIAccess = APIAccess.READ) -> APIKey:
        data = {"keyName": key_name, "access": access.value}
        response = self._http.post("/api/v1/auth/api-keys", data)
        return APIKey(
            key_name=key_name,
            api_key=response.get("apiKey", ""),
            access=access,
        )

    def list_api_keys(self) -> list[APIKey]:
        response = self._http.get("/api/v1/auth/api-keys")
        if isinstance(response, list):
            return [APIKey.from_dict(key) for key in response]
        return []

    def delete_api_key(self, api_key_id: str) -> dict:
        return self._http.delete(f"/api/v1/auth/api-keys/{api_key_id}")

