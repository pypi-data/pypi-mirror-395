# Standard library imports
import logging
import time
import uuid
from typing import Optional

from ..api import attack_multiturn, attack_prompt_events
from ..api.exceptions import ClientException
from ..exceptions import MGException
from ..wrappers.llm import LLMModelWrapper, PromptResponse

logger = logging.getLogger(__name__)

VALID_MULTI_TURNS = ("actor_attack", "crescendo", "skeleton_key")


class MultiturnAttack:
    def __init__(
        self,
        call_system_under_test: LLMModelWrapper,
        ma_client: attack_multiturn.AttackMultiturnClient,
        project_id: str,
        goal: str,
        attack_name: str,
    ):
        self._attack_name = attack_name
        self._goal = goal
        self._project_id = project_id
        self._maClient = ma_client
        self._call_system_under_test = call_system_under_test

    def start(self) -> attack_multiturn.StartResponse:
        logger.debug(f"Starting multi-turn {self._attack_name} for project: {self._project_id}")
        return self._maClient.start(
            attack_multiturn.StartRequest(project_id=self._project_id, goal=self._goal, attack_name=self._attack_name)
        )

    def poll(self, request_uuid: uuid.UUID) -> None:
        completed = False
        event: Optional[attack_prompt_events.Event] = None

        logger.debug(f"Polling for prompt requests to process: {request_uuid}")
        while not completed:
            rt = time.monotonic()
            event, completed = self.__poll_inner(request_uuid)
            if completed:
                break
            # sleep if last request < 0.5s
            wait_time = max(0, (rt + 0.5) - time.monotonic())
            time.sleep(wait_time)

        logger.debug(f"All prompt requests processed for id: {request_uuid}")
        logger.debug(f"Fetching multi-turn {self._attack_name} result...")

    def __poll_inner(self, request_uuid: uuid.UUID) -> tuple[Optional[attack_prompt_events.Event], bool]:
        request = attack_prompt_events.PopRequest(runId=request_uuid)

        event = self._maClient.pop(request)
        if event is None:
            return None, False

        if event.runStatus == "COMPLETED":
            logger.debug(f"Attack completed for id: {request_uuid}")
            return event, True

        logger.debug(f"Processing prompt request")
        response: Optional[PromptResponse] = None
        error_code = None
        error_message = None
        duration_ms = 0
        content = ""
        try:
            response = self._call_system_under_test(event.event.query)
            content = response.response
            duration_ms = response.duration_ms
            logger.debug(f"{content=}")
        except MGException as e:
            logger.debug(f"Error communicating with target application: {e}")
            error_code = getattr(e, "status_code", None)
            error_message = str(e)
            logger.debug(f"{error_code=} {error_message=}")

        logger.debug("Pushing prompt result for request")
        result_push_request = attack_prompt_events.ResultPushRequest(
            requestEventID=event.event.id,
            sessionID=event.event.sessionID,
            referrerID=event.event.referrerID,
            attackName=event.event.attackName,
            turnIndex=event.event.turnIndex,
            durationMs=duration_ms,
            response=content,
            errorCode=error_code,
            errorMessage=error_message,
        )
        try:
            self._maClient.push(result_push_request)
        except ClientException:
            logger.debug("Failed to push response from target")
            result_push_request.response = ""
            result_push_request.errorCode = -1
            result_push_request.errorMessage = "Failed to contact Mindgard"
            self._maClient.push(result_push_request)

        return event, False

    def get_results(self, run_uuid: uuid.UUID) -> attack_multiturn.ResultsResponse:
        return self._maClient.get_results(attack_multiturn.ResultsRequest(run_id=run_uuid))
