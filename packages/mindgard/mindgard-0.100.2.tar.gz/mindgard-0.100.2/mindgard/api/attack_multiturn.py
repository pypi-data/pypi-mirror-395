# Standard library imports
import logging
import uuid
from typing import Any
from urllib.parse import urljoin

# Third party imports
from pydantic import BaseModel, Field

from .attack_prompt_events import AttackPromptEventsClient
from .exceptions import ClientException


class StartRequest(BaseModel):
    """
    Request model for starting a multiturn attack session.

    Attributes:
        project_id (str): The name of the target for the attack.
        goal (str): The goal or objective of the attack session.
        attack_name (str): The name of the attack to run.
    """

    project_id: str
    goal: str
    attack_name: str


class StartResponse(BaseModel):
    """
    Response model for a multiturn attack start request.

    Attributes:
        run_id (uuid.UUID): Unique identifier for the started run/session.
        state (str): The current state of the session.
    """

    run_id: uuid.UUID
    state: str


class ResultsRequest(BaseModel):
    """
    Request model for retrieving results of a multiturn attack session.

    Attributes:
        run_id (uuid.UUID): Unique identifier for the started run/session.
    """

    run_id: uuid.UUID


class ResultsResponse(BaseModel):
    """
    Response model for results of a multiturn attack session.

    Attributes:
        id (str): Unique identifier for the result.
        state (str): The current state of the session.
        project_id (str): The project ID.
        result (Any): The result data, if available.
    """

    state: str
    attack_session_ids: list[uuid.UUID] = Field(default_factory=list)


class AttackMultiturnClient(AttackPromptEventsClient):
    """
    Client for managing multiturn attack sessions via the API.

    Inherits from AttackPromptEventsClient and provides methods to start and interact
    with multiturn attack sessions, handling authentication and request formatting.

    Args:
        base_url (str): The base URL of the API endpoint.
        access_token (str): Bearer token for authentication.
    """

    def __init__(self, base_url: str, access_token: str):
        """
        Initialize the AttackMultiturnClient.

        Args:
            base_url (str): The base URL of the API endpoint.
            access_token (str): Bearer token for authentication.
        """
        super().__init__(base_url, access_token)
        self._attack_url = urljoin(base_url + "/", "user-attack-sessions")

    def start(self, req: StartRequest) -> StartResponse:
        """
        Start a new multiturn attack session.

        Args:
            req (StartRequest): The request containing target and goal information.

        Returns:
            StartResponse: The response containing the run ID and session state.

        Raises:
            ClientException: If the request fails or response validation fails.
        """
        response = self._session.post(self._attack_url, data=req.model_dump_json())

        if response.status_code != 201:
            logging.debug(f"Failed to start multiturn attack: {response.json()} - {response.status_code}")
            raise ClientException(response.text, response.status_code)

        try:
            return StartResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing StartResponse", response.status_code) from e

    def get_results(self, req: ResultsRequest) -> ResultsResponse:
        response = self._session.get(self._attack_url + f"/{req.run_id}")

        if response.status_code != 200:
            logging.debug(f"Failed to get multiturn attack: {response.json()} - {response.status_code}")
            raise ClientException(response.text, response.status_code)

        try:
            return ResultsResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing ResultsResponse", response.status_code) from e
