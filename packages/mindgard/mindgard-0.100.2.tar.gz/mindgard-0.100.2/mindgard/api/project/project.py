# Standard library imports
import logging
from typing import List

# Third party imports
import requests
from pydantic import BaseModel

# Project imports
from mindgard.api.exceptions import ClientException


class CreateProjectRequest(BaseModel):
    """
    Request model for creating a project.

    Attributes:
        project_name (str): The name of the project to create.
    """

    project_name: str


class CreateProjectResponse(BaseModel):
    """
    Response model for creating a project.

    Attributes:
        id (str): Alphanumeric identifier for the created project.
    """

    id: str
    name: str


class ProjectItem(BaseModel):
    """
    Model representing a single project item.
    """

    id: str
    name: str


class ListProjectsResponse(BaseModel):
    """
    Response model for listing projects.

    Attributes:
        items (List[ProjectItem]): List of project items.
    """

    items: List[ProjectItem]


class ProjectClient:
    """
    Client for managing multiturn attack sessions via the API.

    Inherits from AttackPromptEventsClient and provides methods to start and interact
    with multiturn attack sessions, handling authentication and request formatting.

    Args:
        base_url (str): The base URL of the API endpoint.
        access_token (str): Bearer token for authentication.
    """

    def __init__(self, base_url: str, access_token: str):
        """
        Initialize the AttackMultiturnClient.

        Args:
            base_url (str): The base URL of the API endpoint.
            access_token (str): Bearer token for authentication.
        """
        self._base_url = base_url
        self._projects_url = f"{base_url.rstrip('/')}/projects"
        self._access_token = access_token
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._access_token}",
                "Content-Type": "application/json",
            }
        )

    def create(self, req: CreateProjectRequest) -> CreateProjectResponse:
        """
        Creates a new project.

        Args:
            req (CreateProjectRequest): The request containing project name.

        Returns:
            CreateProjectResponse: The response containing the ID of the created project.

        Raises:
            ClientException: If the request fails or response validation fails.
        """
        response = self._session.post(self._projects_url, data=req.model_dump_json())

        if response.status_code != 201:
            logging.debug(f"Failed to create project: {response.json()} - {response.status_code}")
            raise ClientException(response.text, response.status_code)

        try:
            return CreateProjectResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing CreateProjectResponse", response.status_code) from e

    def list(self) -> ListProjectsResponse:
        """
        Lists all projects.

        Returns:
            ListProjectsResponse: The response containing the list of projects.

        Raises:
            ClientException: If the request fails or response validation fails.
        """
        response = self._session.get(self._projects_url)

        if response.status_code != 200:
            logging.debug(f"Failed to get projects: {response.json()} - {response.status_code}")
            raise ClientException(response.text, response.status_code)

        try:
            return ListProjectsResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing CreateProjectResponse", response.status_code) from e
