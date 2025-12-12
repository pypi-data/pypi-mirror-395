# Standard library imports
from datetime import datetime
from typing import List, Optional

# Third party imports
from rich.progress import Progress
from rich.table import Table

from ..api_service import api_get
from ..constants import DASHBOARD_URL
from ..orchestrator import GetTestListResponse, get_tests
from ..types import (
    type_ui_exception_map,
    type_ui_task_map,
)
from ..utils import print_to_stderr_as_json


def list_test_submit(
    access_token: str,
    ui_exception_map: type_ui_exception_map,
    ui_exception_progress: Progress,
) -> GetTestListResponse:
    tests_res = get_tests(access_token, request_function=api_get)

    return tests_res


def list_test_polling(
    access_token: str,
    tests_response: GetTestListResponse,
    ui_task_map: type_ui_task_map,
    ui_task_progress: Progress,
) -> Optional[GetTestListResponse]:
    return tests_response


def list_test_output(test_list: GetTestListResponse, json_out: bool) -> Optional[Table]:
    if json_out:
        print_to_stderr_as_json([test.model_dump() for test in test_list.items])
        return None
    else:
        table = Table(title=f"Tests run by user")
        table.add_column("Model Name", style="cyan")
        table.add_column("Assessment Date", style="magenta")
        table.add_column("Flagged Events", justify="right", style="green")
        table.add_column("URL", justify="right", style="green")

        for test in test_list.items:
            table.add_row(
                test.project_id,
                datetime.fromisoformat(test.created_at.replace("Z", "+00:00")).strftime("%H:%M, %Y-%m-%d"),
                f"{test.flagged_events} / {test.total_events}",
                f"{DASHBOARD_URL}/r/test/{test.id}/{test.project_id}",
            )
        return table
