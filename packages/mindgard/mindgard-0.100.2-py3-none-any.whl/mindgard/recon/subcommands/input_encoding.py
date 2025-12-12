# Standard library imports
import logging
import uuid
from time import sleep
from typing import Optional

from ...api.recon.input_encoding import (
    GetInputEncodingResponse,
    GetReconRequest,
    ReconInputEncodingClient,
    StartInputEncodingRequest,
)
from ...api.recon.recon_prompt_events import (
    ALLOWED_EVENT_SUBJECTS,
    PopEventRequest,
    PopEventResponse,
    PromptResult,
    PushEventRequest,
)
from ...exceptions import MGException
from ...wrappers.llm import LLMModelWrapper


class InputEncodingReconCommand:
    def __init__(self, service: ReconInputEncodingClient, call_system_under_test: LLMModelWrapper):
        self.call_system_under_test = call_system_under_test
        self.service = service

    def start_input_encoding(self, project_id: str) -> uuid.UUID:
        f"Starting input encoding recon for target: {str(project_id)}"
        response = self.service.start_input_encoding(StartInputEncodingRequest(project_id=project_id))
        return response.recon_id

    def poll_input_encoding(self, recon_id: uuid.UUID) -> None:
        return self.poll(recon_id, "INPUT_ENCODING")

    def poll(self, recon_id: uuid.UUID, event_subject: ALLOWED_EVENT_SUBJECTS) -> None:
        completed = False
        event: Optional[PopEventResponse] = None

        logging.debug(f"Polling for prompt requests to process: {str(recon_id)}")
        while not completed:
            completed, event = self._poll_inner(recon_id, event_subject)
            if completed:
                break  # dont sleep again if completed
            sleep(0.5)

        logging.debug(f"All prompt requests processed for recon_id: {str(recon_id)}")
        logging.debug("Fetching reconnaissance result...")

    def _poll_inner(
        self, recon_id: uuid.UUID, event_subject: ALLOWED_EVENT_SUBJECTS
    ) -> tuple[bool, Optional[PopEventResponse]]:
        request = PopEventRequest(
            source_id=recon_id,
            event_type=["prompt_request", "complete"],
            event_subject=event_subject,
        )

        event = self.service.pop(request)

        if event is not None:
            if event.event_type == "complete":
                logging.debug(f"Reconnaissance completed for recon_id: {str(recon_id)}")
                return True, event

            if event.event_type == "prompt_request" and len(event.prompt_request) > 0:
                logging.debug(f"Processing prompt request for input encoding recon: {str(recon_id)}")
                for request in event.prompt_request:
                    response = None
                    exception = None
                    try:
                        response = self.call_system_under_test(request.prompt)
                    except MGException as e:
                        logging.debug(f"Error communicating with target application: {e}")
                        exception = e

                    content = response.response if response else None
                    duration_ms = response.duration_ms if response else None
                    error_code = None if exception is None else getattr(exception, "status_code", None)
                    error_message = None if exception is None else str(exception)

                    logging.debug(f"Pushing prompt result for request")
                    push_event = PushEventRequest(
                        source_id=event.source_id,
                        event_type="prompt_result",
                        event_subject=event_subject,
                        prompt_result=[
                            PromptResult(
                                id=request.id,
                                content=content,
                                duration_ms=duration_ms,
                                prompt_request=request,
                                error_code=error_code,
                                error_message=error_message,
                            )
                        ],
                    )

                    self.service.push(push_event)
                return False, event

        return False, None

    def fetch_recon_input_encoding_result(self, recon_id: uuid.UUID) -> GetInputEncodingResponse | None:
        return self.service.get_input_encoding_result(GetReconRequest(recon_id=recon_id))
