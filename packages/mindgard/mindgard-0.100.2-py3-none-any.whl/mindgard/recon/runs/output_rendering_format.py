# Standard library imports
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.output_rendering_format import (
    GetOutputRenderingFormatResponse,
    ReconOutputRenderingFormatClient,
)
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE
from mindgard.recon.subcommands.output_rendering_format import OutputRenderingFormatReconCommand
from mindgard.utils import CliResponse
from mindgard.wrappers.llm import LLMModelWrapper


def run_output_rendering_format_recon(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    guardrail_recon_service = ReconOutputRenderingFormatClient(API_BASE, access_token)
    output_rendering_format_command = OutputRenderingFormatReconCommand(guardrail_recon_service, model_wrapper)
    result: list[GetOutputRenderingFormatResponse] = []

    def output_rendering_format() -> None:
        recon_id = output_rendering_format_command.start_output_rendering_format(final_args["project_id"])
        output_rendering_format_command.poll_output_rendering_format(recon_id)
        output_rendering_format_results = output_rendering_format_command.fetch_recon_output_rendering_format_result(
            recon_id
        )
        result.append(output_rendering_format_results)

    def output_rendering_format_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for output rendering format…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                guardrail_future = executor.submit(output_rendering_format)

                while not guardrail_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                guardrail_future.result()

    try:
        output_rendering_format_with_spinner()
    except ClientException as ex:
        raise ex

    if len(result) == 0:
        console.print("Failed to get result from output rendering format recon session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result[0].result.guardrail_detected

    if not detected:
        # CASE: No guardrail detected
        console.print("\nNo clear signs of target system supporting output rendering format(s).", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce outputs that point to output rendering format support."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print("\nSome signs of output rendering format support found.\n", style="bold blue")
