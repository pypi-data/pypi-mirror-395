# Standard library imports
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.input_encoding import GetInputEncodingResponse, ReconInputEncodingClient
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE, DASHBOARD_URL
from mindgard.recon.subcommands.input_encoding import InputEncodingReconCommand
from mindgard.utils import CliResponse
from mindgard.wrappers.llm import LLMModelWrapper


def run_input_encoding_recon(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    input_encoding_recon_service = ReconInputEncodingClient(API_BASE, access_token)
    input_encoding_command = InputEncodingReconCommand(input_encoding_recon_service, model_wrapper)
    result: GetInputEncodingResponse = None

    def input_encoding() -> None:
        nonlocal result
        recon_id = input_encoding_command.start_input_encoding(final_args["project_id"])
        input_encoding_command.poll_input_encoding(recon_id)
        result = input_encoding_command.fetch_recon_input_encoding_result(recon_id)

    def input_encoding_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for input encoding…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                input_encoding_future = executor.submit(input_encoding)

                while not input_encoding_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                input_encoding_future.result()

    try:
        input_encoding_with_spinner()
    except ClientException as ex:
        raise ex

    if result is None:
        console.print("Failed to get result from input encoding recon session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result.result.total_detected > 0

    if not detected:
        console.print("\nNo clear signs of target system supporting input encoding(s).", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce outputs that point to input encoding support."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print(
        f"\nTests indicate the target supports {result.result.total_detected}/{result.result.total} distinct input-encoding capabilties.",
        style="bold blue",
    )
    console.print(
        f"\nFull results can be found here: {DASHBOARD_URL}/results/recon?project_id={result.project_id}&reconType=input\n"
    )
