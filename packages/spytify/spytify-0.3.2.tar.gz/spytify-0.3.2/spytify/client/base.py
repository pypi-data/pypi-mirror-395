"""Base client to interact with the Spotify Web API."""

import json
import logging
import re
import urllib
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, Self, Union

import requests


class BaseClient(ABC):
    """Base client to interact with the Spotify Web API.

    This class is meant to be inherited by other clients that interact with the
    Spotify Web API. It provides the basic methods to make requests to the API.
    The login method must be implemented by the child classes.
    """

    __API_BASE_ENDPOINT = "https://api.spotify.com/v1"
    _LOGIN_BASE_ENDPOINT = "https://accounts.spotify.com"
    _token = None

    def __init__(self, client_id: str = None):
        self._logger = logging.getLogger(__name__)
        self._client_id = client_id

    @classmethod
    def from_token(cls, token: str) -> Self:
        """Create a client from a stored token."""

        client = cls()
        client._token = token
        return client

    def __get_full_endpoint(self, route: str, base_endpoint: str = None):
        if not base_endpoint:
            base_endpoint = self.__API_BASE_ENDPOINT

        if not route.startswith("/"):
            route = "/" + route

        return f"{base_endpoint}{route}"

    def __sanitize_headers(self, headers: Dict):
        sanitized_headers = deepcopy(headers)

        if "Authorization" in sanitized_headers:
            sanitized_headers["Authorization"] = re.sub(
                r" .*", " <redacted>", sanitized_headers["Authorization"]
            )

        return sanitized_headers

    def _post_request(
        self,
        route: str,
        data: Dict | str,
        additional_headers: Dict = None,
        authorize=True,
        base_endpoint=None,
    ):
        """Make a POST request to the Spotify Web API."""

        if additional_headers is None:
            additional_headers = {}

        headers = additional_headers.copy()

        data_to_send = None
        if headers.get("Content-Type") == "application/x-www-form-urlencoded":
            data_to_send = data_to_send = urllib.parse.urlencode(data)
        elif headers.get("Content-Type") == "application/json":
            data_to_send = json.dumps(data)
        elif headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/json"
            data_to_send = json.dumps(data)
        else:
            data_to_send = data

        if authorize:
            if not self._token:
                raise ValueError(
                    "Authorization token not defined! Please login before using authorization!"
                )
            headers["Authorization"] = "Bearer " + self._token

        result = requests.post(
            self.__get_full_endpoint(route, base_endpoint),
            headers=headers,
            data=data_to_send,
            timeout=30,
        )

        if not result.ok:
            self._logger.debug("Request body: %s", result.request.body)
            self._logger.debug(
                "Request headers: %s", self.__sanitize_headers(result.request.headers)
            )
            if result.headers.get("Content-Type") == "application/json":
                self._logger.debug(result.json())
            else:
                self._logger.debug(result.content)

            raise RuntimeError(f"Request not ok: {result.status_code} {result.reason}")

        return result.json()

    def _get_request(
        self,
        route: str,
        additional_headers: Union[Dict, None] = None,
        params: Union[Dict, None] = None,
        authorize=True,
    ):
        """Make a GET request to the Spotify Web API."""

        if additional_headers is None:
            additional_headers = {}

        headers = additional_headers.copy()

        if authorize:
            if not self._token:
                raise ValueError(
                    "Authorization token not defined! Please login before using authorization!"
                )
            headers["Authorization"] = "Bearer " + self._token

        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        result = requests.get(
            self.__get_full_endpoint(route=route),
            headers=headers,
            params=params,
            timeout=30,
        )

        if not result.ok:
            self._logger.debug("Request body: %s", result.request.body)
            self._logger.debug(
                "Request headers: %s", self.__sanitize_headers(result.request.headers)
            )
            if result.headers.get("Content-Type") == "application/json":
                self._logger.debug(result.json())
            else:
                self._logger.debug(result.content)

            raise RuntimeError(f"Request not ok: {result.status_code} {result.reason}")

        return result.json()

    @abstractmethod
    def login(self):
        """Abstract method to login to the Spotify Web API."""

    def get_token(self) -> str:
        """Get the token stored in the client."""
        return self._token

    def get_playlist(
        self,
        playlist_id: str,
        market: str = None,
        fields: str = None,
        additional_types: str = None,
    ):
        """Get a playlist from the Spotify Web API."""

        params = {
            "market": market,
            "fields": fields,
            "additional_types": additional_types,
        }

        return self._get_request(
            route=f"/playlists/{playlist_id}",
            params=params,
            authorize=True,
        )

    def search(self, album: str = None, artist: str = None, track: str = None):
        """Search for an album, artist, or track in the Spotify Web API."""

        if not any([album, artist, track]):
            raise ValueError(
                "At least one of album, artist, or track must be provided!"
            )

        types = []
        query = ""

        if album:
            types.append("album")
            query += f"album:{album}"
        if artist:
            types.append("artist")
            query += f" artist:{artist}"
        if track:
            types.append("track")
            query += f" track:{track}"

        params = {
            "q": query,
            "type": ",".join(types),
        }

        return self._get_request(
            route="/search",
            params=params,
            authorize=True,
        )

    def get_artist_top_tracks(self, artist_id: str):
        """Get an artist's top tracks from the Spotify Web API."""

        return self._get_request(
            route=f"/artists/{artist_id}/top-tracks",
            authorize=True,
        )
