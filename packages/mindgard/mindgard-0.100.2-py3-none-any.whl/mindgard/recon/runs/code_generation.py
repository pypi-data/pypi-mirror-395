# Standard library imports
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.code_generation import (
    GetCodeGenerationResponse,
    ReconCodeGenerationClient,
)
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE
from mindgard.recon.subcommands.code_generation import CodeGenerationReconCommand
from mindgard.utils import CliResponse
from mindgard.wrappers.llm import LLMModelWrapper


def run_code_generation_recon(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    guardrail_recon_service = ReconCodeGenerationClient(API_BASE, access_token)
    code_generation_command = CodeGenerationReconCommand(guardrail_recon_service, model_wrapper)
    result: list[GetCodeGenerationResponse] = []

    def code_generation() -> None:
        recon_id = code_generation_command.start_code_generation(final_args["project_id"])
        code_generation_command.poll_code_generation(recon_id)
        code_generation_results = code_generation_command.fetch_recon_code_generation_result(recon_id)
        result.append(code_generation_results)

    def code_generation_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for code generation…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                guardrail_future = executor.submit(code_generation)

                while not guardrail_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                guardrail_future.result()

    try:
        code_generation_with_spinner()
    except ClientException as ex:
        console.print(f"[red bold]Error: {ex.message}[/red bold]")
        exit(CliResponse(ex.status_code).code())

    if len(result) == 0:
        console.print("Failed to get result from code generation recon session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result[0].result.guardrail_detected

    if not detected:
        # CASE: No guardrail detected
        console.print("\nNo clear signs of target system supporting code generation.", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce outputs that point to code generation support."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print("\nSome signs of code generation support found.\n", style="bold blue")
