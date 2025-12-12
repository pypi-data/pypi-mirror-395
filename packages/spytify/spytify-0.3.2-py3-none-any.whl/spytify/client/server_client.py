"""Server client to interact with the Spotify Web API."""

from base64 import b64encode

from spytify.client.base import BaseClient


class ServerClient(BaseClient):
    """Server client to interact with the Spotify Web API.

    This client is meant to be used in server-side applications using the
    client credentials authentication flow. Using this flow, the client
    can access all non-user-related endpoints of the Spotify Web API.
    """

    def __init__(self, client_id: str, client_secret: str):
        super().__init__(client_id)
        self._client_secret = client_secret

    def __validate_credentials(self):
        if not self._client_id:
            raise ValueError("Client ID not defined!")
        if not self._client_secret:
            raise ValueError("Client secret not defined!")

    def login(self):
        self.__validate_credentials()

        basic_data = f"{self._client_id}:{self._client_secret}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64encode(basic_data.encode()).decode()}",
        }
        payload = {"grant_type": "client_credentials"}

        response = self._post_request(
            route="/api/token",
            additional_headers=headers,
            data=payload,
            authorize=False,
            base_endpoint=self._LOGIN_BASE_ENDPOINT,
        )

        try:
            self._token = response["access_token"]
        except KeyError as e:
            self._logger.error("Could not get access token from response: %s", response)
            raise e
