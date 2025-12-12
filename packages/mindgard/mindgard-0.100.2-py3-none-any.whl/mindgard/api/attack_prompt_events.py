# Standard library imports
import logging
import time
import uuid
from typing import Optional
from urllib.parse import urljoin

# Third party imports
import requests
from pydantic import BaseModel

from .exceptions import ClientException

logger = logging.getLogger(__name__)


class PopRequest(BaseModel):
    """
    Request model for popping the next event in a user attack session.

    Attributes:
        runId (uuid.UUID): The unique identifier for the run/session.
    """

    runId: uuid.UUID


class PromptRequestEntry(BaseModel):
    """
    Represents a single prompt entry for OpenAI chat completion.

    Attributes:
        content (str): The text content of the prompt.
        role (str): The role (e.g., 'user', 'assistant').
    """

    content: str
    role: str


class OpenAIChatCompletion(BaseModel):
    """
    Container for OpenAI chat completion history.

    Attributes:
        OpenAI (Optional[list[PromptRequestEntry]]): List of prompt entries for OpenAI chat.
    """

    OpenAI: Optional[list[PromptRequestEntry]] = None


class Event(BaseModel):
    """
    Represents a prompt event in a user attack session.

    Attributes:
        id (uuid.UUID): Unique event identifier.
        sessionID (uuid.UUID): Session identifier.
        referrerID (uuid.UUID): Referrer identifier.
        attackName (str): Name of the attack.
        turnIndex (int): Index of the turn in the session.
        query (str): The prompt/query text.
        history (Optional[OpenAIChatCompletion]): Chat history for context.
    """

    id: uuid.UUID
    sessionID: uuid.UUID
    referrerID: uuid.UUID
    attackName: str
    turnIndex: int
    query: str
    history: Optional[OpenAIChatCompletion] = None


class PopResponse(BaseModel):
    """
    Response model for a pop event request.

    Attributes:
        runID (uuid.UUID): The run/session identifier.
        runStatus (str): Status of the run.
        event (Optional[Event]): The event data, if available.
    """

    runID: uuid.UUID
    runStatus: str
    event: Optional[Event] = None


class ResultPushRequest(BaseModel):
    """
    Request model for pushing the result of a prompt event.

    Attributes:
        requestEventID (uuid.UUID): Event ID being responded to.
        sessionID (uuid.UUID): Session identifier.
        referrerID (uuid.UUID): Referrer identifier.
        attackName (str): Name of the attack.
        turnIndex (int): Index of the turn.
        response (str): The model's response.
        durationMs (float): Duration in milliseconds.
        errorCode (Optional[int]): Error code, if any.
        errorMessage (Optional[str]): Error message, if any.
    """

    requestEventID: uuid.UUID
    sessionID: uuid.UUID
    referrerID: uuid.UUID
    attackName: str
    turnIndex: int
    response: str
    durationMs: float
    errorCode: Optional[int] = None
    errorMessage: Optional[str] = None


class AttackPromptEventsClient:
    """
    Client for interacting with the Prompt Events API.

    Provides methods to pop (retrieve) and push (submit) prompt events for user attack sessions.
    Handles authentication, request formatting, and error handling for communication with the backend service.

    Args:
        base_url (str): The base URL of the API endpoint.
        access_token (str): Bearer token for authentication.
    """

    def __init__(self, base_url: str, access_token: str):
        self._base_url = base_url
        self._pop_events_url = urljoin(self._base_url + "/", "user-attack-sessions/events/pop")
        self._push_events_url = urljoin(self._base_url + "/", "user-attack-sessions/events/push")
        self._access_token = access_token
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json",
            }
        )

    def pop(self, request: PopRequest) -> Optional[PopResponse]:
        """
        Retrieve the next available prompt event for a given run ID.

        Args:
            request (PopRequest): The request containing the run ID.

        Returns:
            Optional[PopResponse]: The response containing the event, or None if not found.

        Raises:
            ClientException: If the request fails or response validation fails.
        """
        response = self._session.post(self._pop_events_url, data=request.model_dump_json())
        if response.status_code == 404:
            logger.debug(f"No events found {request.model_dump()=} {response.text=} {response.status_code=}")
            return None

        if response.status_code != 200:
            logger.debug(f"Failed pop request {request.model_dump()=} {response.text=} {response.status_code=}")
            raise ClientException(message=response.text, status_code=response.status_code)

        try:
            return PopResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("problem validating PopResponse", response.status_code) from e

    def push(self, request: ResultPushRequest):
        """
        Submit the result of a prompt event, including response, timing, and error info.

        Args:
            request (ResultPushRequest): The request containing result data to push.

        Raises:
            ClientException: If the push request fails.
        """
        response = self._session.post(self._push_events_url, data=request.model_dump_json())

        if response.status_code != 201:
            logger.debug(f"Failed to push results {request.model_dump()=} {response.text=} {response.status_code=}")
            raise ClientException(message=str(response.json()), status_code=response.status_code)
