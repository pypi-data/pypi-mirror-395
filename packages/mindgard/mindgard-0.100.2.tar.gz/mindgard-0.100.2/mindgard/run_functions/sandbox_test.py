# Standard library imports
from typing import Optional

# Third party imports
from rich.progress import Progress

from ..orchestrator import OrchestratorTestResponse, submit_sandbox_test
from ..types import (
    type_submit_func,
    type_ui_exception_map,
    type_ui_task_map,
)
from ..ui_prefabs import poll_and_display_test

POLL_INTERVAL_SECONDS = 3


def submit_sandbox_submit_factory() -> type_submit_func:

    def submit_sandbox_submit(
        access_token: str,
        ui_exception_map: type_ui_exception_map,
        ui_exception_progress: Progress,
    ) -> OrchestratorTestResponse:
        return submit_sandbox_test(
            access_token=access_token, mindgard_model_name="sandbox-openai-gpt4o-mini"
        )  # NOTE: model choice is currently hardcoded in orchestrator

    return submit_sandbox_submit


def submit_sandbox_polling(
    access_token: str,
    initial_test: OrchestratorTestResponse,
    ui_task_map: type_ui_task_map,
    ui_task_progress: Progress,
) -> Optional[OrchestratorTestResponse]:
    return poll_and_display_test(access_token, ui_task_map, ui_task_progress, initial_test)
