# Standard library imports
import uuid
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

# Third party imports
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.recon.guardrail import GetDetectResponse, ReconGuardrailClient
from mindgard.auth import load_access_token
from mindgard.constants import API_BASE
from mindgard.recon.subcommands.guardrail import GuardrailReconCommand
from mindgard.utils import CliResponse, request_user_input
from mindgard.wrappers.llm import LLMModelWrapper


def run_guardrail_recon(console: Console, model_wrapper: LLMModelWrapper, final_args: dict[str, Any]):
    access_token = load_access_token()
    guardrail_recon_service = ReconGuardrailClient(API_BASE, access_token)
    guardrail_command = GuardrailReconCommand(guardrail_recon_service, model_wrapper)
    result: list[GetDetectResponse] = []

    def guardrail() -> None:
        recon_id = guardrail_command.start_detect(final_args["project_id"])
        guardrail_command.poll_detect(recon_id)
        detect_results = guardrail_command.fetch_recon_detect_result(recon_id)
        result.append(detect_results)

    def guardrail_fingerprint(recon_id: uuid.UUID) -> None:
        fp_recon_id = guardrail_command.start_fingerprint(recon_id)
        if fp_recon_id != recon_id:
            print(fp_recon_id, type(fp_recon_id))
            print(recon_id, type(recon_id))
            console.print(f"[red bold]Error: Fingerprinting session did not initialise correctly.[/red bold]")
            exit(CliResponse(1).code())
        guardrail_command.poll_fingerprint(fp_recon_id)
        fp_results = guardrail_command.fetch_recon_fingerprint_result(fp_recon_id)
        result.append(fp_results)

    def guardrail_with_spinner() -> None:
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Probing for guardrails…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("probing", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                guardrail_future = executor.submit(guardrail)

                while not guardrail_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                guardrail_future.result()

    def fingerprint_with_spinner() -> None:
        """
        Start fingerprinting session worker(s) and display a spinner to the user
        """
        with Progress(
            SpinnerColumn(style="bold yellow"),
            TextColumn("[bold yellow]Fingerprinting guardrails…"),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("fingerprinting", total=None)

            with ThreadPoolExecutor(max_workers=1) as executor:
                guardrail_future = executor.submit(guardrail_fingerprint, result[0].id)

                while not guardrail_future.done():
                    sleep(0.15)

                progress.update(task_id, completed=100)
                guardrail_future.result()

    # Perform initial guardrail recon
    try:
        guardrail_with_spinner()
    except ClientException as ex:
        raise ex

    if len(result) == 0:
        console.print("Failed to get result from guardrail detection session")
        exit(CliResponse(1).code())

    console.print("\nProbing completed!", style="bold green")
    detected = result[0].result.guardrail_detected

    if not detected:
        # CASE: No guardrail detected
        console.print("\nNo clear signs of guardrail(s).", style="bold red")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target didn't produce outputs that point to guardrail behavior."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Run the complete mindgard test suite for open-ended probing to uncover any additional risks. See [yellow]mindgard test --help[/yellow] to learn more.\n"
        )
        exit(CliResponse(0).code())

    console.print("\nSome signs of guardrail(s) found.\n", style="bold blue")

    # Perform guardrail fingerprinting if guardrail detected
    guardrails_detected = None
    console.print(
        "Continue with fingerprinting to identify enabled guardrails?\nDisclaimer: this action will fire [underline]~120[/underline] prompts at the target system"
    )
    if request_user_input(console, "(y/n): ", ["y", "n"]) == "n":
        # CASE: Guardrail detected but user chose not to continue with fingerprinting
        console.rule(style="bold white")
        console.print(f"Guardrail reconnaissance results:")
        console.print("\nSome signs of guardrail(s) found.", style="bold blue")
        console.print(
            f"\n[underline]Reasoning[/underline]: The target produced outputs that point to guardrail presence."
        )
        console.print(
            f"[underline]Recommendation[/underline]: Shift from discovery to evasion. Run tests with different guardrail bypass domains using [yellow]mindgard test --domain bypass.\\[guardrail_name][yellow]\n"
        )
        exit(CliResponse(0).code())

    try:
        # Perform fingerprinting prompt request-response
        fingerprint_with_spinner()

        # Compile results
        guardrails_result = result[1]
        highest_confidence = max(getattr(x, "confidence", 0) for x in guardrails_result)
        guardrails_detected = [x for x in guardrails_result if getattr(x, "confidence", 0) == highest_confidence]
        names = " / ".join(getattr(x, "guardrail_pretty_name", "N/A") for x in guardrails_detected)

        console.rule(style="bold white")
        console.print(f"Guardrail reconnaissance results:\n")

        if highest_confidence == 0:
            # CASE: Guardrail responses matched no known fingerprints
            console.print(f"Response behaviour could not be matched to a known guardrail.", style="bold blue")
            console.print(
                f"\n[underline]Reasoning[/underline]: Responses to fingerprinting prompts did not match the patterns of known guardrails."
            )
            console.print(
                f"[underline]Recommendation[/underline]: We recommend re-running the recon process to try different prompts.\n"
            )
        else:
            # CASE: One or more guardrails matched known fingerprints
            console.print(f"The guardrail exhibits behaviours similar to {names}.", style="bold blue")
            console.print(
                f"\n[underline]Reasoning[/underline]: Custom inputs for {'these guardrails' if '/' in names else 'this guardrail'} were the most successful."
            )
            console.print(
                f"[underline]Recommendation[/underline]: Use the relevant Mindgard guardrail bypass domain to further validate and attempt evasion. Run [yellow]mindgard test --domain bypass.\\[guardrail_name][/yellow] with the selected domain.\n"
            )
        exit(CliResponse(0).code())

    except ClientException as ex:
        console.print(f"[red bold]Error: {ex.message}[/red bold]")
        exit(CliResponse(ex.status_code).code())
