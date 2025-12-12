# Standard library imports
import logging
import uuid
from typing import Optional
from urllib.parse import urljoin

# Third party imports
from pydantic import BaseModel

from ..exceptions import ClientException
from .recon_prompt_events import ReconPromptEventsClient


class StartCodeGenerationRequest(BaseModel):
    project_id: str


class StartCodeGenerationResponse(BaseModel):
    recon_id: uuid.UUID


class GetReconRequest(BaseModel):
    recon_id: uuid.UUID


class ReconResult(BaseModel):
    guardrail_detected: bool
    detected_guardrails: list[str] = []


class GetCodeGenerationResponse(BaseModel):
    id: uuid.UUID
    state: str
    result: Optional[ReconResult] = None
    reason: Optional[str] = None
    recommendation: Optional[str] = None
    project_id: str


class ReconCodeGenerationClient(ReconPromptEventsClient):
    def __init__(self, base_url: str, access_token: str):
        super().__init__(base_url, access_token)
        self._recon_code_generation_url = urljoin(base_url + "/", "recon/code_generation")

    def start_code_generation(self, request: StartCodeGenerationRequest) -> StartCodeGenerationResponse:
        """
        Start a code generation reconnaissance process with the Mindgard service

        Args:
            request (StartCodeGenerationRequest): Info connecting this operation to a target name

        Raises:
            ClientException: Raised if the Mindgard service returns an error

        Returns:
            StartCodeGenerationResponse: Mindgard service response from the start request
        """
        response = self._session.post(self._recon_code_generation_url, data=request.model_dump_json())

        if response.status_code != 201:
            logging.debug(f"Failed to start recon: {response.json()} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)
        try:
            return StartCodeGenerationResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing StartDetectResponse", response.status_code) from e

    def get_code_generation_result(self, request: GetReconRequest) -> Optional[GetCodeGenerationResponse]:
        """
        Get the code generation reconnaissance result from the Mindgard service

        Args:
            request (GetReconRequest): Info connecting this operation to a reconnaissance session
        Raises:
            ClientException: Raised if the Mindgard service returns an error
        Returns:
            Optional[GetCodeGenerationResponse]: Mindgard service response from the get request
        """
        get_recon_url = urljoin(self._recon_code_generation_url + "/", str(request.recon_id))
        response = self._session.get(get_recon_url)

        if response.status_code == 404:
            logging.debug(f"No reconnaissance found for recon_id={request.recon_id}: {response.text}")
            return None

        if response.status_code != 200:
            logging.debug(f"Failed to get recon result: {response.text} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)

        try:
            return GetCodeGenerationResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing GetCodeGenerationResponse", response.status_code) from e
