# Standard library imports
import logging
import uuid
from typing import Literal, Optional
from urllib.parse import urljoin

# Third party imports
import requests
from pydantic import BaseModel

from ..exceptions import ClientException

ALLOWED_EVENT_TYPES = Literal["prompt_request", "complete"]
ALLOWED_EVENT_SUBJECTS = Literal[
    "GUARDRAIL_DETECT",
    "GUARDRAIL_FINGERPRINT",
    "INPUT_ENCODING",
    "OUTPUT_ENCODING",
    "NON_CONTEXTUAL",
    "OUTPUT_FORMAT_GENERATION",
    "OUTPUT_RENDERING_FORMAT",
    "CODE_GENERATION",
]
RESULT_EVENT_TYPE = Literal["prompt_result"]


class PopEventRequest(BaseModel):
    source_id: uuid.UUID
    event_type: list[ALLOWED_EVENT_TYPES]
    event_subject: ALLOWED_EVENT_SUBJECTS


class PromptRequest(BaseModel):
    id: Optional[str] = None
    prompt: str
    language: str


class PopEventResponse(BaseModel):
    event_id: str
    event_type: str
    source_id: uuid.UUID
    prompt_request: Optional[list[PromptRequest]] = None


class PromptResult(BaseModel):
    id: Optional[str] = None
    content: Optional[str] = None
    duration_ms: Optional[float] = None
    prompt_request: PromptRequest
    error_message: Optional[str] = None
    error_code: Optional[int] = None


class PushEventRequest(BaseModel):
    source_id: uuid.UUID
    event_type: RESULT_EVENT_TYPE
    event_subject: ALLOWED_EVENT_SUBJECTS
    prompt_result: list[PromptResult]


class PushEventResponse(BaseModel):
    event_id: str


class ReconPromptEventsClient:

    def __init__(self, base_url: str, access_token: str):
        self._base_url = base_url
        self._pop_events_url = urljoin(self._base_url + "/", "events/prompt_request_response/pop")
        self._push_events_url = urljoin(self._base_url + "/", "events/prompt_request_response/push")
        self._access_token = access_token
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json",
            }
        )

    def pop(self, request: PopEventRequest) -> Optional[PopEventResponse]:
        response = self._session.post(self._pop_events_url, data=request.model_dump_json())

        if response.status_code == 404:
            logging.debug(f"No event found for source_id={request.source_id}: {response.text}")
            return None

        if response.status_code != 200:
            logging.debug(f"Failed to get recon events: {response.text} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)

        try:
            return PopEventResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing PopEventResponse", response.status_code) from e

    def push(self, request: PushEventRequest) -> PushEventResponse:
        logging.debug(f"pushing event: {request}")
        for i in range(3):
            try:
                response = self._session.post(self._push_events_url, data=request.model_dump_json())
                break
            except requests.exceptions.ConnectionError:
                logging.debug(f"Connection error on try {i}! Trying again...")

        if response.status_code != 201:
            response_body = response.text
            logging.debug(
                f"Retrying with sanitized results as failed to get prompt results: {response_body} - {response.status_code}"
            )
            for result in request.prompt_result:
                result.content = ""
                result.error_code = -1
                result.error_message = "Failed to contact Mindgard"
            response = self._session.post(self._push_events_url, data=request.model_dump_json())

            if response.status_code != 201:
                logging.debug(
                    f"Retrying with sanitized results failed to get prompt results: {response.text} - {response.status_code}"
                )
                raise ClientException(response.text, response.status_code)

        logging.debug(f"Got prompt results: {response.json()} - {response.status_code}")
        return PushEventResponse.model_validate(response.json())
