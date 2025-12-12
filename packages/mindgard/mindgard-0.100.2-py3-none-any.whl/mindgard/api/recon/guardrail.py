# Standard library imports
import logging
import uuid
from typing import Optional
from urllib.parse import urljoin

# Third party imports
from pydantic import BaseModel

from ..exceptions import ClientException
from .recon_prompt_events import ReconPromptEventsClient


class StartDetectRequest(BaseModel):
    project_id: str


class StartDetectResponse(BaseModel):
    recon_id: uuid.UUID


class StartFingerprintRequest(BaseModel):
    recon_id: uuid.UUID


class StartFingerprintResponse(BaseModel):
    recon_id: uuid.UUID


class GetReconRequest(BaseModel):
    recon_id: uuid.UUID


class ReconResult(BaseModel):
    guardrail_detected: bool
    detected_guardrails: list[str] = []


class GetDetectResponse(BaseModel):
    id: uuid.UUID
    state: str
    result: Optional[ReconResult] = None
    reason: Optional[str] = None
    recommendation: Optional[str] = None
    project_id: str


class GetFingerprintResponse(BaseModel):
    guardrail_name: str
    guardrail_pretty_name: str
    confidence: float
    errors: int


class ReconGuardrailClient(ReconPromptEventsClient):
    def __init__(self, base_url: str, access_token: str):
        super().__init__(base_url, access_token)
        self._reconn_detection_url = urljoin(base_url + "/", "recon/guardrail/detection")
        self._reconn_fingerprint_url = urljoin(base_url + "/", "recon/guardrail/fingerprint")

    def start_detect(self, request: StartDetectRequest) -> StartDetectResponse:
        """
        Start the detection process, will start a new reconnaissance session

        Args:
            request (StartDetectRequest): Info connecting this operation to a target name

        Raises:
            ClientException: Raised if the Mindgard service returns an error

        Returns:
            StartDetectResponse: Mindgard service response from the start request
        """
        response = self._session.post(self._reconn_detection_url, data=request.model_dump_json())

        if response.status_code != 201:
            logging.debug(f"Failed to start recon: {response.json()} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)
        try:
            return StartDetectResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing StartDetectResponse", response.status_code) from e

    def start_fingerprint(self, request: StartFingerprintRequest) -> StartFingerprintResponse:
        """
        Start the fingerprinting process for an existing reconnaissance session

        Args:
            request (StartFingerprintRequest): Info connecting this operation to an existing recon session

        Raises:
            ClientException: Raised if the Mindgard service returns an error

        Returns:
            StartFingerprintResponse: Mindgard service response from the start request
        """
        response = self._session.post(self._reconn_fingerprint_url, data=request.model_dump_json())

        if response.status_code != 201:
            logging.debug(f"Failed to start fingerprinting: {response.json()} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)
        try:
            return StartFingerprintResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing StartFingerprintResponse", response.status_code) from e

    def get_detect_result(self, request: GetReconRequest) -> Optional[GetDetectResponse]:
        """
        Query the Mindgard service for the results of a guardrail detect recon operation

        Args:
            request (GetReconRequest): Request object containing recon_id

        Raises:
            ClientException: Raised if there is a service error fetching the detection results

        Returns:
            Optional[GetDetectResponse], None]: Result for guardrail detection, or None if no results returned
        """
        response = self._session.get(self._reconn_detection_url, params={"recon_id": str(request.recon_id)})

        if response.status_code == 404:
            logging.debug(f"No reconn found for source_id={request.recon_id}: {response.text}")
            return None

        if response.status_code != 200:
            logging.debug(f"Failed to get recon result: {response.text} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)
        try:
            return GetDetectResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing GetDetectResponse", response.status_code) from e

    def get_fingerprint_result(self, request: GetReconRequest) -> Optional[list[GetFingerprintResponse]]:
        """
        Query the Mindgard service for the results of a guardrail fingerprinting recon operation

        Args:
            request (GetReconRequest): Request object containing recon_id

        Raises:
            ClientException: Raised if there is a service error fetching the fingerprint results

        Returns:
            Optional[list[GetFingerprintResponse]]: Results for each guardrail fingerprinted, or None if no results returned
        """
        response = self._session.get(self._reconn_fingerprint_url, params={"recon_id": str(request.recon_id)})

        if response.status_code == 404:
            logging.debug(f"No reconn found for source_id={request.recon_id}: {response.text}")
            return None

        if response.status_code != 200:
            logging.debug(f"Failed to get recon result: {response.text} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)

        resp_json = response.json()

        if not isinstance(resp_json, list):
            logging.debug(f"Expected list in fingerprint result, got: {type(resp_json)}")
            return None
        try:
            return [GetFingerprintResponse.model_validate(item) for item in resp_json]
        except Exception as e:
            raise ClientException("Problem parsing GetFingerprintResponse", response.status_code) from e
