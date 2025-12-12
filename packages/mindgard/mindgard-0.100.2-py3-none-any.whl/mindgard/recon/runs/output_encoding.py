# Standard library imports
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.output_encoding import GetOutputEncodingResponse, ReconOutputEncodingClient
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE, DASHBOARD_URL
from mindgard.recon.subcommands.output_encoding import OutputEncodingReconCommand
from mindgard.utils import CliResponse
from mindgard.wrappers.llm import LLMModelWrapper


def run_output_encoding_recon(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    output_encoding_recon_service = ReconOutputEncodingClient(API_BASE, access_token)
    output_encoding_command = OutputEncodingReconCommand(output_encoding_recon_service, model_wrapper)
    result: GetOutputEncodingResponse = None

    def output_encoding() -> None:
        nonlocal result
        recon_id = output_encoding_command.start_output_encoding(final_args["project_id"])
        output_encoding_command.poll_output_encoding(recon_id)
        result = output_encoding_command.fetch_recon_output_encoding_result(recon_id)

    def output_encoding_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for output encoding…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                output_encoding_future = executor.submit(output_encoding)

                while not output_encoding_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                output_encoding_future.result()

    try:
        output_encoding_with_spinner()
    except ClientException as ex:
        raise ex

    if result is None:
        console.print("Failed to get result from output encoding recon session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result.result.total_detected > 0

    if not detected:
        console.print("\nNo clear signs of target system supporting output encoding(s).", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce outputs that point to output encoding support."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print(
        f"\nTests indicate the target supports {result.result.total_detected}/{result.result.total} distinct output-encoding capabilties.",
        style="bold blue",
    )
    console.print(
        f"\nFull results can be found here: {DASHBOARD_URL}/results/recon?project_id={result.project_id}&reconType=output\n"
    )
