# Standard library imports
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.output_format_generation import (
    GetOutputFormatGenerationResponse,
    ReconOutputFormatGenerationClient,
)
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE
from mindgard.recon.subcommands.output_format_generation import OutputFormatGenerationReconCommand
from mindgard.utils import CliResponse
from mindgard.wrappers.llm import LLMModelWrapper


def run_output_format_generation_recon(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    guardrail_recon_service = ReconOutputFormatGenerationClient(API_BASE, access_token)
    output_format_generation_command = OutputFormatGenerationReconCommand(guardrail_recon_service, model_wrapper)
    result: list[GetOutputFormatGenerationResponse] = []

    def output_format_generation() -> None:
        recon_id = output_format_generation_command.start_output_format_generation(final_args["project_id"])
        output_format_generation_command.poll_output_format_generation(recon_id)
        output_format_generation_results = output_format_generation_command.fetch_recon_output_format_generation_result(
            recon_id
        )
        result.append(output_format_generation_results)

    def output_format_generation_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for output format generation…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                guardrail_future = executor.submit(output_format_generation)

                while not guardrail_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                guardrail_future.result()

    try:
        output_format_generation_with_spinner()
    except ClientException as ex:
        raise ex

    if len(result) == 0:
        console.print("Failed to get result from output format generation recon session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result[0].result.guardrail_detected

    if not detected:
        # CASE: No guardrail detected
        console.print("\nNo clear signs of target system supporting output format generation(s).", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce outputs that point to output format generation support."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print("\nSome signs of output format generation support found.\n", style="bold blue")
