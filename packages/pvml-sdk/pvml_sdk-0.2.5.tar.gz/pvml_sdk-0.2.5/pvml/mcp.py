import base64
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

from pvml import routes
from pvml.pvml_http_client import PvmlHttpClient
from pvml.util import convert_string_to_datetime


class AuthType(str, Enum):
    NONE = "none"
    BASE = "base"
    OAUTH = "oauth"
    DYNAMIC_OAUTH = "dynamic_oauth"


@dataclass
class McpOauthData:
    auth_url: Optional[str] = None
    token_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    scopes: Optional[str] = None

    def to_dict(self):
        dict_obj = {
            'authUrl': self.auth_url,
            'tokenUrl': self.token_url,
            'clientId': self.client_id,
            'clientSecret': self.client_secret,
            'scopes': self.scopes
        }
        return {k: v for k, v in dict_obj if v is not None}


@dataclass
class McpBaseAuthData:
    access_token: Optional[str] = None

    def to_dict(self):
        dict_obj = {
            'accessToken': self.access_token,
        }
        return {k: v for k, v in dict_obj if v is not None}


@dataclass
class McpAuthData:
    auth_type: AuthType
    oauth_data: Optional[McpOauthData] = None
    base_auth_data: Optional[McpBaseAuthData] = None



class MCP:
    """
    Represent a configured MCP in PVML
    Attributes:
         id (int): the mcp id
         workspace_id (int): the workspace id
         name (str): the mcp name in pvml
         description (str): the mcp description
         type (str): the type of the mcp in pvml
         url (str): the url of the mcp
         created_by (str): the user that created the mcp in pvml
         created_at (datetime): the mcp creation time
    """

    def __init__(self, http_client: PvmlHttpClient, mcp_info: dict, image: bytes):
        self.image: bytes = image
        self.__http_client = http_client
        self.id = mcp_info['id']
        self.workspace_id = mcp_info['workspaceId']
        self.name = mcp_info['name']
        self.description = mcp_info.get('description', "")
        self.type = mcp_info['type']
        self.url = mcp_info['url']
        self.allowed_mcp_tool_names = mcp_info['allowedMcpToolNames']
        self.created_by = mcp_info['createdBy']
        self.created_at = convert_string_to_datetime(mcp_info.get('createdAt'))

    def __str__(self):
        return f"MCP(id={self.id}, name={self.name}, url={self.url})"

    def __repr__(self):
        return f"MCP(name='{self.name}', id='{self.id}, url='{self.url}')"

    @property
    def http_client(self):
        return self.__http_client

    def update(self, name: str, description: str, mcp_url: str, auth_data: McpAuthData,
               allowed_mcp_tool_names: list[str] | None, image: bytes) -> None:
        """
        Updates the MCP info on the platform
        :param image: 
        :param name: name of the mcp
        :param description: description of the mcp
        :param mcp_url: url of the mcp
        :param auth_data: authentication configuration for the MCP, containing auth type and corresponding auth data
        :param allowed_mcp_tool_names: allowed mcp tools name (None means allow all)
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.MCP.format(workspace_id=self.workspace_id, mcp_id=self.id)
        payload = {
            "name": name,
            "description": description,
            "url": mcp_url,
            "allowedMcpToolNames": allowed_mcp_tool_names,
            "authType": auth_data.auth_type,
            "baseAuthData": None if auth_data.base_auth_data is None else auth_data.base_auth_data.to_dict(),
            "oauthData": None if auth_data.oauth_data is None else auth_data.oauth_data.to_dict(),
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        body_text, headers = self.http_client.metadata_request(payload, image_bytes=image)
        self.http_client.request("PUT", url, headers, data=body_text)

        self.name = name
        self.description = description
        self.url = mcp_url
        self.image = image

    def get_tools(self) -> List[dict]:
        """
        Updates the MCP info on the platform
        :return: List of tools info
        :raises Exception: If the API call fails
        """
        url = routes.MCP_TOOLS.format(workspace_id=self.workspace_id, mcp_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return response_dict.get('mcpTools')

    def get_view_id(self) -> str:
        """
        Get the View id associated with this MCP
        Returns:
            str: The View id
        """

        url = routes.MCP_VIEW.format(workspace_id=self.workspace_id, mcp_id=self.id)
        response_dict = self.http_client.request('GET', url)
        return response_dict['viewId']
