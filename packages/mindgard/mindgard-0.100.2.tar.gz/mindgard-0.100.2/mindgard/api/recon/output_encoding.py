# Standard library imports
import logging
import uuid
from typing import Optional
from urllib.parse import urljoin

# Third party imports
from pydantic import BaseModel

from ..exceptions import ClientException
from .recon_prompt_events import ReconPromptEventsClient


class StartOutputEncodingRequest(BaseModel):
    project_id: str


class StartOutputEncodingResponse(BaseModel):
    recon_id: uuid.UUID


class GetReconRequest(BaseModel):
    recon_id: uuid.UUID


class ReconResult(BaseModel):
    total: int
    total_detected: int
    results: dict[str, int]


class GetOutputEncodingResponse(BaseModel):
    id: uuid.UUID
    state: str
    result: Optional[ReconResult] = None
    reason: Optional[str] = None
    recommendation: Optional[str] = None
    project_id: str


class ReconOutputEncodingClient(ReconPromptEventsClient):
    def __init__(self, base_url: str, access_token: str):
        super().__init__(base_url, access_token)
        self._recon_output_encoding_url = urljoin(base_url + "/", "recon/output_encoding")

    def start_output_encoding(self, request: StartOutputEncodingRequest) -> StartOutputEncodingResponse:
        """
        Start an output encoding reconnaissance process with the Mindgard service

        Args:
            request (StartOutputEncodingRequest): Info connecting this operation to a target name

        Raises:
            ClientException: Raised if the Mindgard service returns an error

        Returns:
            StartOutputEncodingResponse: Mindgard service response from the start request
        """
        response = self._session.post(self._recon_output_encoding_url, data=request.model_dump_json())

        if response.status_code != 201:
            logging.debug(f"Failed to start recon: {response.json()} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)
        try:
            return StartOutputEncodingResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing StartDetectResponse", response.status_code) from e

    def get_output_encoding_result(self, request: GetReconRequest) -> Optional[GetOutputEncodingResponse]:
        """
        Get the output encoding reconnaissance result from the Mindgard service

        Args:
            request (GetReconRequest): Info connecting this operation to a reconnaissance session
        Raises:
            ClientException: Raised if the Mindgard service returns an error
        Returns:
            Optional[GetOutputEncodingResponse]: Mindgard service response from the get request
        """
        response = self._session.get(self._recon_output_encoding_url, params={"recon_id": str(request.recon_id)})

        if response.status_code == 404:
            logging.debug(f"No reconnaissance found for recon_id={request.recon_id}: {response.text}")
            return None

        if response.status_code != 200:
            logging.debug(f"Failed to get recon result: {response.text} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)

        try:
            return GetOutputEncodingResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing GetOutputEncodingResponse", response.status_code) from e
