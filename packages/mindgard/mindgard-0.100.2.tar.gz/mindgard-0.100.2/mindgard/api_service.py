# Standard library imports
from typing import Any, Dict

# Third party imports
import requests
from requests import HTTPError
from tenacity import retry, stop_after_attempt, wait_fixed

from .constants import (
    API_RETRY_ATTEMPTS,
    API_RETRY_WAIT_BETWEEN_ATTEMPTS_SECONDS,
    VERSION,
)


class MGHTTPError(HTTPError):
    def __init__(self, response: requests.Response):
        self.response = response
        self.status_code = response.status_code

        try:
            body = response.json()
        except ValueError:
            body = response.text

        self.body = body
        self.message = body.get("error") if isinstance(body, dict) and "error" in body else str(body)

        super().__init__(self.message, response=response)

    def __str__(self) -> str:
        return f"[{self.status_code}] {self.message}"


def _standard_headers(access_token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": f"mindgard-cli/{VERSION}",
        "X-User-Agent": f"mindgard-cli/{VERSION}",
    }


@retry(
    stop=stop_after_attempt(API_RETRY_ATTEMPTS),
    wait=wait_fixed(API_RETRY_WAIT_BETWEEN_ATTEMPTS_SECONDS),
    reraise=True,
)
def api_post(url: str, access_token: str, payload: Dict[str, Any]) -> requests.Response:
    try:
        response = requests.post(url=url, json=payload, headers=_standard_headers(access_token))
        response.raise_for_status()
        return response
    except HTTPError as e:
        raise MGHTTPError(e.response) from e


@retry(
    stop=stop_after_attempt(API_RETRY_ATTEMPTS),
    wait=wait_fixed(API_RETRY_WAIT_BETWEEN_ATTEMPTS_SECONDS),
    reraise=True,
)
def api_get(url: str, access_token: str) -> requests.Response:
    response = requests.get(url=url, headers=_standard_headers(access_token))
    response.raise_for_status()
    return response
