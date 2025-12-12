from typing import Dict

from pvml import routes
from pvml.pvml_http_client import PvmlHttpClient
from pvml.workspace import Workspace


class Client:
    """
    The PVML client class, the entry point for interacting with PVML.

    Attributes:
        http_client (PvmlHttpClient): The PVML http client initiated by the provided api_key
    """

    def __init__(self, api_key, event_loop=None):
        self.__http_client = PvmlHttpClient(api_key, event_loop)

    def __str__(self):
        return f"PVML Client"

    def __repr__(self):
        return f"PVML Client"

    @property
    def http_client(self) -> PvmlHttpClient:
        return self.__http_client

    async def close(self) -> None:
        """
        Close the PVML http client
        :raises Exception: If the API call fails
        """
        await self.http_client.close()

    def get_workspaces(self) -> Dict[str, Workspace]:
        """
        Get all workspaces associated with the user
        :return: A dictionary mapping ids to their workspaces
        :raises Exception: If the API call fails
        """
        url = routes.USER_WORKSPACES.format(user_id=self.http_client.user_id)
        response_dict = self.http_client.request('GET', url)
        return {workspace['id']: Workspace(self.http_client, workspace) for workspace in response_dict['workspaces']}

    def get_workspace(self, workspace_id: str) -> Workspace:
        """
        Get a specific workspace
        :param workspace_id: the workspace identifier
        :return: The workspace associated with the provided workspace id
        :raises Exception: If the API call fails
        """
        url = routes.WORKSPACE.format(workspace_id=workspace_id)
        response_dict = self.http_client.request('GET', url)
        return Workspace(self.http_client, response_dict)

    def get_supported_llms(self) -> Dict[str, list[str]]:
        """
        Get all llms supported by PVML
        :return: A dictionary mapping llm vendor to all their PVML supported llms
        :raises Exception: If the API call fails
        """
        url = routes.AVAILABLE_LLMS
        response_dict = self.http_client.request("GET", url)
        return response_dict

    def get_default_prompts(self) -> Dict[str, str]:
        """
        Get all llms supported by PVML
        :return: A dictionary mapping llm vendor to all their PVML supported llms
        :raises Exception: If the API call fails
        """
        url = routes.DEFAULT_PROMPTS
        response_dict = self.http_client.request("GET", url)
        return response_dict['agentPromptDefault']
