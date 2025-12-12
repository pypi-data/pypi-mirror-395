# Third party imports
from rich.console import Console
from rich.table import Table

# Project imports
from mindgard.api.exceptions import ClientException
from mindgard.api.project.project import CreateProjectRequest, ProjectClient
from mindgard.auth import require_auth
from mindgard.constants import API_BASE, DASHBOARD_URL
from mindgard.utils import CliResponse

console = Console()


class CreateProjectCLIArgs:
    name: str


@require_auth
def create_project(create_project_args: CreateProjectCLIArgs, access_token: str):
    """
    Create a new project with the given name.
    """
    project_service = ProjectClient(API_BASE, access_token)

    try:
        with console.status("Creating project...", spinner="dots"):
            response = project_service.create(CreateProjectRequest(project_name=create_project_args.name))
    except ClientException as ex:
        console.print(f"[red bold]Error: {ex.message}[/red bold]")
        exit(CliResponse(ex.status_code).code())

    console.print(f"\nProject created successfully!\n", style="bold green")
    console.print(f"Project name: {response.name}")
    console.print(f"Project ID: {response.id}\n")
    console.print(
        f"Add the project ID to your config file or pass it with the command (e.g., --project-id {response.id} )."
    )
    console.print("Visit https://docs.mindgard.ai/user-guide/projects for more details.\n")


@require_auth
def list_projects(access_token: str):
    """
    Create a new project with the given name.
    """
    project_service = ProjectClient(API_BASE, access_token)

    try:
        with console.status("Fetching all your projects...", spinner="dots"):
            response = project_service.list()
    except ClientException as ex:
        console.print(f"[red bold]Error: {ex.message}[/red bold]")
        exit(CliResponse(ex.status_code).code())

    if len(response.items) == 0:
        console.print(
            "\nNo projects available. Run `mindgard create project --name <New Project Name>` to create a project"
        )
        return

    table = Table(title="Projects")
    table.add_column("Project ID", style="blue")
    table.add_column("Project Name", style="white")
    table.add_column("Project URL", style="white")

    for _, item in enumerate(response.items, start=1):
        table.add_row(item.id, item.name, f"{DASHBOARD_URL}/results/tests?project_id={item.id}")

    console.print(table)
