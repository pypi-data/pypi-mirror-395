# Standard library imports
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.non_contextual import GetNonContextualResponse, ReconNonContextualClient
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE
from mindgard.recon.subcommands.non_contextual import NonContextualReconCommand
from mindgard.utils import CliResponse
from mindgard.wrappers.llm import LLMModelWrapper


def run_noncontextual_recon(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    guardrail_recon_service = ReconNonContextualClient(API_BASE, access_token)
    non_contextual_command = NonContextualReconCommand(guardrail_recon_service, model_wrapper)
    result: list[GetNonContextualResponse] = []

    def non_contextual() -> None:
        recon_id = non_contextual_command.start_non_contextual(final_args["project_id"])
        non_contextual_command.poll_non_contextual(recon_id)
        non_contextual_results = non_contextual_command.fetch_recon_non_contextual_result(recon_id)
        result.append(non_contextual_results)

    def non_contextual_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for non-contextual encoding…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                guardrail_future = executor.submit(non_contextual)

                while not guardrail_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                guardrail_future.result()

    try:
        non_contextual_with_spinner()
    except ClientException as ex:
        raise ex

    if len(result) == 0:
        console.print("Failed to get result from non-contextual encoding recon session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result[0].result.guardrail_detected

    if not detected:
        console.print("\nNo clear signs of target system supporting non contextual(s).", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce responses that point to non-contextual support."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print("\nSome signs of non-contextual support found.\n", style="bold blue")
