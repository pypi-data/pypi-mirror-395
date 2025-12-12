# Standard library imports
import logging
import uuid
from typing import Optional
from urllib.parse import urljoin

# Third party imports
from pydantic import BaseModel

from ..exceptions import ClientException
from .recon_prompt_events import ReconPromptEventsClient


class StartNonContextualRequest(BaseModel):
    project_id: str


class StartNonContextualResponse(BaseModel):
    recon_id: uuid.UUID


class GetReconRequest(BaseModel):
    recon_id: uuid.UUID


class ReconResult(BaseModel):
    guardrail_detected: bool
    detected_guardrails: list[str] = []


class GetNonContextualResponse(BaseModel):
    id: uuid.UUID
    state: str
    result: Optional[ReconResult] = None
    reason: Optional[str] = None
    recommendation: Optional[str] = None
    project_id: str


class ReconNonContextualClient(ReconPromptEventsClient):
    def __init__(self, base_url: str, access_token: str):
        super().__init__(base_url, access_token)
        self._recon_noncontextual_url = urljoin(base_url + "/", "recon/non-contextual")

    def start_non_contextual(self, request: StartNonContextualRequest) -> StartNonContextualResponse:
        """
        Start a non-contextual reconnaissance process with the Mindgard service

        Args:
            request (StartNonContextualRequest): Info connecting this operation to a target name

        Raises:
            ClientException: Raised if the Mindgard service returns an error

        Returns:
            StartNonContextualResponse: Mindgard service response from the start request
        """
        response = self._session.post(self._recon_noncontextual_url, data=request.model_dump_json())

        if response.status_code != 201:
            logging.debug(f"Failed to start recon: {response.json()} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)
        try:
            return StartNonContextualResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing StartDetectResponse", response.status_code) from e

    def get_non_contextual_result(self, request: GetReconRequest) -> Optional[GetNonContextualResponse]:
        """
        Get the non-contextual reconnaissance result from the Mindgard service

        Args:
            request (GetReconRequest): Info connecting this operation to a reconnaissance session
        Raises:
            ClientException: Raised if the Mindgard service returns an error
        Returns:
            Optional[GetNonContextualResponse]: Mindgard service response from the get request
        """
        get_recon_url = urljoin(self._recon_noncontextual_url + "/", str(request.recon_id))
        response = self._session.get(get_recon_url)

        if response.status_code == 404:
            logging.debug(f"No reconnaissance found for recon_id={request.recon_id}: {response.text}")
            return None

        if response.status_code != 200:
            logging.debug(f"Failed to get recon result: {response.text} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)

        try:
            return GetNonContextualResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing GetNoncontextualResponse", response.status_code) from e
