# Standard library imports
import logging
import os
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import cast

# Third party imports
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

# Project imports
from mindgard.auth import load_access_token, login, logout
from mindgard.constants import API_BASE, DASHBOARD_URL
from mindgard.dataset_generation import create_custom_dataset
from mindgard.exceptions import MGException
from mindgard.external_model_handlers.llm_model import llm_message_handler
from mindgard.orchestrator import OrchestratorSetupRequest
from mindgard.preflight import preflight_llm
from mindgard.run_functions.external_models import (
    model_test_output_factory,
    model_test_polling,
    model_test_submit_factory,
)
from mindgard.run_functions.list_tests import list_test_output, list_test_polling, list_test_submit
from mindgard.run_functions.sandbox_test import submit_sandbox_polling, submit_sandbox_submit_factory
from mindgard.run_poll_display import cli_run
from mindgard.utils import (
    CliResponse,
    ConflictError,
    conflicting_args_error,
    convert_test_to_cli_response,
    invalid_project_id_error,
    is_version_outdated,
    parse_toml_and_args_into_final_args,
    print_to_stderr,
    unspecified_project_id_error,
)
from mindgard.wrappers.llm import LLMModelWrapper
from mindgard.wrappers.utils import parse_args_into_model

from .api.attack_multiturn import AttackMultiturnClient
from .api.exceptions import ClientException
from .cli_args import parse_args
from .multiturn.attack import MultiturnAttack
from .project.project import create_project, list_projects
from .recon.constants import recon_constants
from .recon.runs.guardrail import run_guardrail_recon
from .recon.runs.input_encoding import run_input_encoding_recon
from .recon.runs.output_encoding import run_output_encoding_recon

debug_help = lambda: print(
    "\033[93mTry running with `mindgard --log-level=debug ...` for more information, and ` 2> >(tee output.log >&2)` after your command to save output to disk.\033[0m"
)


def run_cli() -> None:
    args = parse_args(sys.argv[1:])

    FORMAT = "%(asctime)s.%(msecs)02d; %(message)s"
    logging.basicConfig(
        level=args.log_level.upper(),
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True), locals_max_string=None, locals_max_length=None)],
    )

    if not (sys.version_info.major == 3 and sys.version_info.minor >= 10):
        print_to_stderr("Python 3.10 or later is required to run the Mindgard CLI.")
        sys.exit(2)

    if new_version := is_version_outdated():
        print_to_stderr(
            f"New version available: {new_version}. Please upgrade as older versions of the CLI may not be actively maintained."
        )

    if args.command == "login":
        login(instance=args.instance)
    elif args.command == "logout":
        logout()
    elif args.command == "list":
        if args.list_command == "tests":
            cli_run(
                submit_func=list_test_submit,
                polling_func=list_test_polling,
                output_func=list_test_output,
                json_out=args.json,
                submitting_text="Fetching tests...",
            )
            exit(CliResponse(0).code())

        if args.list_command == "projects":
            list_projects()
            exit(CliResponse(0).code())
        else:
            print_to_stderr("Provide a resource to list. Eg `list tests`.")
    elif args.command == "sandbox":
        submit_sandbox_submit = submit_sandbox_submit_factory()
        submit_sandbox_output = model_test_output_factory(risk_threshold=100)

        cli_response = cli_run(
            submit_func=submit_sandbox_submit,
            polling_func=submit_sandbox_polling,
            output_func=submit_sandbox_output,
            json_out=args.json,
        )
        exit(convert_test_to_cli_response(test=cli_response, risk_threshold=100).code())
    elif args.command == "create":
        if args.create_command == "dataset":
            create_custom_dataset(args)
        elif args.create_command == "project":
            create_project(args)

        else:
            print("Unknown create command. Please see `mindgard create --help` for more information.")

    elif args.command in ["validate", "test", "recon", "run"]:
        console = Console(highlight=False)  # Disabled highlighting to avoid styling issues with certain terminals
        final_args = {}
        try:
            final_args = parse_toml_and_args_into_final_args(args.config_file, args)
        except ConflictError as e:
            conflicting_args_error(console, e)
            exit(CliResponse(1).code())
        except ValueError as e:
            console.print(f"[red bold]{e}")
            exit(CliResponse(1).code())

        if not final_args["project_id"]:
            unspecified_project_id_error(console)
            exit(CliResponse(1).code())

        model_wrapper = parse_args_into_model(final_args)
        passed_preflight = preflight_llm(model_wrapper, console=console, json_out=final_args["json"])

        if not final_args["json"]:
            console.print(
                f"{'[green bold]Target contactable!' if passed_preflight else '[red bold]Target not contactable!'}"
            )

        if passed_preflight:
            match args.command:
                # Test command
                case "test":
                    if os.getenv("MINDGARD_TOGGLE_USE_LIB") == "true":
                        # Project imports
                        from mindgard.main_lib import run_test

                        run_test(final_args, model_wrapper)
                    else:
                        request = OrchestratorSetupRequest(
                            projectID=final_args["project_id"],
                            parallelism=final_args["parallelism"],
                            system_prompt=final_args["system_prompt"],
                            dataset=final_args.get("custom_dataset", final_args["dataset"]),
                            custom_dataset=final_args.get("custom_dataset", None),
                            modelType="llm",
                            attackSource="user",
                            attackPack=final_args["attack_pack"],
                            exclude=final_args["exclude"],
                            include=final_args["include"],
                            prompt_repeats=final_args["prompt_repeats"],
                        )
                        submit = model_test_submit_factory(
                            request=request,
                            model_wrapper=cast(LLMModelWrapper, model_wrapper),
                            message_handler=llm_message_handler,
                        )

                        output = model_test_output_factory(risk_threshold=int(final_args["risk_threshold"]))
                        cli_response = cli_run(
                            submit, model_test_polling, output_func=output, json_out=final_args["json"]
                        )
                        exit(
                            convert_test_to_cli_response(
                                test=cli_response, risk_threshold=int(final_args["risk_threshold"])
                            ).code()
                        )  # type: ignore

                # Reconnaissance commands
                case recon_constants.recon:
                    if args.recon_subcommand == recon_constants.guardrail:
                        run_guardrail_recon(console, model_wrapper, final_args)
                    elif args.recon_subcommand == recon_constants.input_encoding:
                        run_input_encoding_recon(console, model_wrapper, final_args)
                    elif args.recon_subcommand == recon_constants.output_encoding:
                        run_output_encoding_recon(console, model_wrapper, final_args)
                    elif args.recon_subcommand == recon_constants.non_contextual:
                        print_to_stderr("Non-contextual is not yet implemented.")
                    elif args.recon_subcommand == recon_constants.output_format_generation:
                        print_to_stderr("Output format generation is not yet implemented.")
                    elif args.recon_subcommand == recon_constants.output_rendering_format:
                        print_to_stderr("Output rendering format is not yet implemented.")
                    elif args.recon_subcommand == recon_constants.code_generation:
                        print_to_stderr("Code generation is not yet implemented.")
                    else:
                        print_to_stderr("Provide a recon sub-command. See: $ mindgard recon --help")

                # Run commands
                case "run":
                    if args.run_subcommands == "multiturn":
                        if len(final_args["include"]) != 1:
                            console.print("--include currently only supports one element")
                            exit(CliResponse(1).code())
                        access_token = load_access_token()
                        mt_attack_client = AttackMultiturnClient(API_BASE, access_token)
                        goal = final_args["goal"]
                        project_id = final_args["project_id"]
                        attack_name = final_args["include"][0]
                        multiturn_attack = MultiturnAttack(
                            call_system_under_test=model_wrapper,
                            ma_client=mt_attack_client,
                            project_id=project_id,
                            goal=goal,
                            attack_name=attack_name,
                        )

                        def run_attack():
                            start_response = multiturn_attack.start()
                            multiturn_attack.poll(start_response.run_id)
                            attack_results = multiturn_attack.get_results(start_response.run_id)
                            url = f"{DASHBOARD_URL}/results/multiturns/{attack_results.attack_session_ids[0]}?project_id={project_id}"
                            return url

                        url = None
                        with Progress(
                            SpinnerColumn(style="bold yellow"),
                            TextColumn(f"[bold yellow]Running Multiturn Attack: {attack_name}"),
                            transient=True,
                            console=console,
                        ) as progress:
                            task_id = progress.add_task("running", total=None)

                            with ThreadPoolExecutor(max_workers=1) as executor:
                                future = executor.submit(run_attack)

                                try:
                                    url = future.result()
                                except ClientException as e:
                                    raise e
                                except Exception as e:
                                    console.print(f"Error trying to run multiturn attack, {e}")
                                    exit(CliResponse(1).code())
                                progress.update(task_id, completed=100)
                        if not url:
                            console.print(f"Error did not get results url")
                            exit(CliResponse(1).code())
                        console.print(f"Multiturn Attack complete: {url}")
                        exit(CliResponse(0).code())
                case _:
                    print_to_stderr("Which command are you looking for? See: $ mindgard --help")

        else:
            exit(CliResponse(1).code())

    else:
        print_to_stderr("Which command are you looking for? See: $ mindgard --help")


def main() -> None:
    console = Console(stderr=True)
    try:
        run_cli()
    except ValueError as e:
        console.print(f"[red bold]{e}")
        invalid_project_id_error(console, str(e))
        exit(2)
    except MGException:
        debug_help()
        exit(2)
    except ClientException as e:
        console.print(f"[red bold]Error: {e.message}")
        invalid_project_id_error(console, str(e))
        exit(2)
    except Exception:
        traceback.print_exc()
        debug_help()
        exit(2)
