import base64
from typing import Dict, List, Any
from urllib.parse import quote

from pvml import mcp
from pvml import util, routes
from pvml.agent import Agent
from pvml.agent_session import AgentSession
from pvml.audit import AuditFilter
from pvml.connector.base import BaseConnector
from pvml.datasource import Datasource
from pvml.group import Group
from pvml.llm import LLM
from pvml.mcp import MCP
from pvml.policy import Policy
from pvml.pvml_http_client import PvmlHttpClient
from pvml.view import View
from pvml.workspace_user import WorkspaceUser


class Workspace:
    """
    A Workspace object and client
    Attributes:
        id (str): The workspace id
        name (str): The name of the workspace
        description (str): The description of the workspace
    """

    def __init__(self, http_client: PvmlHttpClient, workspace_info):
        self.__http_client = http_client
        self.id = workspace_info['id']
        self.name = workspace_info['name']
        self.description = workspace_info['description']

    def __str__(self):
        return f"Workspace(workspace_name='{self.name}', workspace_id='{self.id}')"

    def __repr__(self):
        return f"Workspace(workspace_name='{self.name}', workspace_id='{self.id}')"

    @property
    def http_client(self):
        return self.__http_client

    def get_current_user(self) -> WorkspaceUser:
        """
        Fetch a WorkspaceUser client for the current api key
        :return: WorkspaceUser
        :raises Exception: If the API call fails
        """
        return self.get_user(self.http_client.user_id)

    def get_datasources(self) -> Dict[str, Datasource]:
        """
        Fetches all datasources connected to this workspace
        :return: A dictionary of Datasource clients mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCES.format(workspace_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {ds['id']: Datasource(self.http_client, ds) for ds in response_dict['datasources']}

    def get_users(self) -> Dict[str, WorkspaceUser]:
        """
        Fetches all users connected to this workspace
        :return: A dictionary of WorkspaceUser clients mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.USERS.format(workspace_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {wsu['User']['id']: WorkspaceUser(self.http_client, wsu) for wsu in response_dict['workspaceUsers']}

    def get_views(self) -> Dict[str, View]:
        """
        Fetches all views configured on this workspace
        :return: A dictionary of View clients mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.VIEWS.format(workspace_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {view['viewId']: View(self.http_client, view) for view in response_dict['views']}

    def get_groups(self) -> Dict[str, Group]:
        """
        Fetches all groups configured on this workspace
        :return: A dictionary of Group clients mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.GROUPS.format(workspace_id=self.id) + '/?summary=true'
        response_dict = self.http_client.request("GET", url)
        return {group['id']: Group(self.http_client, group) for group in response_dict['groups']}

    def get_policies(self) -> Dict[str, Policy]:
        """
        Fetches all policies configured on this workspace
        :return: A dictionary of Policy clients mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.PERMISSIONS.format(workspace_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {permission['id']: Policy(self.http_client, permission) for permission in response_dict['permissions']}

    def create_llm(self, name: str, description: str, vendor_name: str, model_name: str,
                   token: str, props: dict) -> LLM:
        """
        Configures a new LLM in the workspace
        :param name: The name of the LLM
        :param description: The description of the LLM
        :param vendor_name: The name of the LLM vendor
        :param model_name: The name of the LLM model
        :param token: The token for the LLM
        :param props: The PVML configured properties for the LLM
        :return: An LLM client
        :raises Exception: If the API call fails
        """
        url = routes.LLMS.format(workspace_id=self.id)
        payload = {
            "name": name,
            "description": description,
            "workspaceId": self.id,
            "vendorName": vendor_name,
            "modelName": model_name,
            "token": token,
            "llmProps": props
        }
        response_dict = self.http_client.request("POST", url, json=payload)
        return LLM(self.http_client, response_dict)

    def create_custom_llm(self, name: str, description: str, custom_llm_url: str,
                          token: str, props: dict) -> LLM:
        """
        Configures a new LLM in the workspace
        :param name: The name of the LLM
        :param description: The description of the LLM
        :param custom_llm_url: The URL of the LLM
        :param token: The token for the LLM
        :param props: The PVML configured properties for the LLM
        :return: An LLM client
        :raises Exception: If the API call fails
        """
        url = routes.LLMS.format(workspace_id=self.id)
        payload = {
            "name": name,
            "description": description,
            "workspaceId": self.id,
            "vendorName": "custom",
            "modelName": "custom",
            "url": custom_llm_url,
            "token": token,
            "llmProps": props
        }
        response_dict = self.http_client.request("POST", url, json=payload)
        return LLM(self.http_client, response_dict)

    def get_llm(self, llm_id: str) -> LLM:
        """
        Fetches the details for a specific LLM
        :param llm_id: The ID of the LLM to retrieve details for
        :return: An LLM object containing the LLM details
        :raises Exception: If the API call fail
        """
        url = routes.LLM.format(workspace_id=self.id, llm_id=llm_id)
        response_dict = self.http_client.request("GET", url)
        return LLM(self.http_client, response_dict)

    def get_llms(self) -> Dict[str, LLM]:
        """
        Fetches all llms configured on this workspace
        :return: A dictionary of LLM clients mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.LLMS.format(workspace_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {llm['id']: LLM(self.http_client, llm) for llm in response_dict['workspaceLlms']}

    def delete_llm(self, llm_id: str | None = None, llm: LLM | None = None) -> None:
        """
        Deletes a specific LLM
        :param llm_id: The ID of the LLM to delete
        :param llm: The LLM to delete
        :return: None
        :raises Exception: If the API call fails
        """
        llm_id = util.get_id(llm_id, llm)
        url = routes.LLM.format(workspace_id=self.id, llm_id=llm_id)
        self.http_client.request("DELETE", url)

    def create_adhoc_user(self, name: str) -> WorkspaceUser:
        """
        Creates a new adhoc user in the workspace
        :param name: The name of the adhoc user to create
        :return: WorkspaceUser client
        :raises Exception: If the API call fails
        """
        url = routes.USERS_ADHOC.format(workspace_id=self.id)
        payload = {'name': name}
        response_dict = self.http_client.request("POST", url, json=payload)
        return WorkspaceUser(self.http_client, response_dict)

    def get_user(self, user_id: str) -> WorkspaceUser:
        """
        Fetches a WorkspaceUser client for a specific user
        :param user_id: The ID of the user to retrieve
        :return: WorkspaceUser client
        :raises Exception: If the API call fails
        """
        url = routes.USER.format(workspace_id=self.id, user_id=user_id) + '?enrich=true'
        response_dict = self.http_client.request("GET", url)
        return WorkspaceUser(self.http_client, response_dict)

    def delete_user(self, user_id: str | None = None, user: WorkspaceUser | None = None) -> None:
        """
        Deletes a user from the project_workspace.
        :param user_id: The ID of the user to delete
        :param user: The WorkspaceUser to delete
        :raises Exception: If the API call fails
        """
        user_id = util.get_id(user_id, user)
        url = routes.USER.format(workspace_id=self.id, user_id=user_id)
        self.http_client.request("DELETE", url)

    def connect_datasource(self, connector: BaseConnector) -> Datasource:
        """
        Connects a new datasource to the project_workspace
        :param connector: The datasource configuration details
        :return: The connected Datasource client
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCES.format(workspace_id=self.id)
        response_dict = self.http_client.request("POST", url, json=connector.get_payload())
        return Datasource(self.http_client, response_dict)

    def get_datasource(self, datasource_id: str) -> Datasource:
        """
        Fetches a datasource client with the provided id
        :param datasource_id: The datasource id
        :return: A Datasource client that allows API calls
        :raises Exception: If the API call fails        """
        url = routes.DATASOURCE_DATA.format(workspace_id=self.id, datasource_id=datasource_id)
        response_dict = self.http_client.request("GET", url)
        return Datasource(self.http_client, response_dict)

    def delete_datasource(self, datasource_id: str | None = None, datasource: Datasource | None = None) -> None:
        """
        Deletes a datasource
        :param datasource_id: The ID of the datasource to delete
        :param datasource: The datasource to delete
        :return: None
        :raises Exception: If the API call fails
        """
        datasource_id = util.get_id(datasource_id, datasource)
        url = routes.DATASOURCE.format(workspace_id=self.id, datasource_id=datasource_id)
        self.http_client.request("DELETE", url)

    def create_group(self, name: str, description: str, image: bytes | None = None) -> Group:
        """
        Creates a new group
        :param name: The name of the group
        :param description: The description of the group
        :param image: The image of the group
        :return: The created Group client
        :raises Exception: If the API call fails
        """
        url = routes.GROUPS.format(workspace_id=self.id)
        request_dict = {'name': name, 'description': description}
        body_text, headers = self.http_client.metadata_request(request_dict, image)
        response_dict = self.http_client.request("POST", url, data=body_text, headers=headers)
        return Group(self.http_client, response_dict['group'])

    def get_group(self, group_id: str) -> Group:
        """
        Fetches the details of a specific group
        :param group_id: The ID of the group to retrieve
        :return: A Group client
        :raises Exception: If the API call fails
        """
        url = routes.GROUP.format(workspace_id=self.id, group_id=group_id) + '?enrich=true'
        response_dict = self.http_client.request("GET", url)
        return Group(self.http_client, response_dict['group'])

    def delete_group(self, group_id: str | None = None, group: Group | None = None) -> None:
        """
        Deletes the group
        :param group_id: The ID of the group to delete
        :param group: The group to delete
        :return: None
        :raises Exception: If the API call fails
        """
        group_id = util.get_id(group_id, group)
        url = routes.GROUP.format(workspace_id=self.id, group_id=group_id)
        self.http_client.request("DELETE", url)

    def create_view(self, name: str, description: str,
                    datasource_id: str | None = None, datasource: Datasource | None = None,
                    image: bytes | None = None) -> View:
        """
        Creates a new view for a specific datasource
        :param name: The name of the view
        :param description: A brief description of the view
        :param datasource_id: The datasource ID
        :param datasource: The datasource
        :param image: Binary data for the image to upload
        :return: A View client
        :raises Exception: If the API call fails
        """
        datasource_id = util.get_id(datasource_id, datasource)
        url = routes.VIEWS.format(workspace_id=self.id)
        request_dict = {'name': name, 'description': description, 'datasourceId': datasource_id}
        body_text, headers = self.http_client.metadata_request(request_dict, image_bytes=image)
        response_dict = self.http_client.request("POST", url, headers, data=body_text)
        return View(self.http_client, response_dict['view'])

    def get_view(self, view_id: str) -> View:
        """
        Fetches a view client with the provided id
        :param view_id: The ID of the view to retrieve
        :return: A View client
        :raises Exception: If the API call fails
        """
        url = routes.VIEW.format(workspace_id=self.id, view_id=view_id)
        response_dict = self.http_client.request("GET", url)
        return View(self.http_client, response_dict['view'])

    def delete_view(self, view_id: str | None = None, view: View | None = None) -> None:
        """
        Deletes a specific view
        :param view_id: The ID of the view to delete
        :param view: The view to delete
        :return: None
        :raises Exception: If the API call fails
        """
        view_id = util.get_id(view_id, view)
        url = routes.VIEW.format(workspace_id=self.id, view_id=view_id)
        self.http_client.request("DELETE", url)

    def get_query_audit(
            self,
            page_size: int = 10,
            page_number: int = 1,
            override_projection_columns: List[str] | None = None,
            audit_filters: List[AuditFilter] | None = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetches query audit logs for the project_workspace.

        :param page_size: Number of records per page (default: 10)
        :param page_number: Page number to fetch (default: 1)
        :param override_projection_columns: List of columns to override
        :param audit_filters: List of filters to apply to the audit log
        :return: A list of audit logs
        :raises Exception: If the API call fails
        """
        default_projection_columns = ['id', 'query', 'duration', 'source', 'startTime', 'status', 'endTime',
                                      'userEmail',
                                      'userId', 'datasourceId', 'errorReason', 'traceId', 'errorType', 'datasourceType',
                                      'viewId', 'viewName', 'userQuestion', 'botId']
        projection_columns = (default_projection_columns
                              if (override_projection_columns is None)
                                 or (len(override_projection_columns) == 0)
                              else override_projection_columns)
        str_filter = ""
        if audit_filters is not None:
            filter_pairs = [
                [f"{iter_filter.field_name}",
                 "{\"operator\":" + f"\"{iter_filter.operator.name.lower()}\"" + ",\"value\":" +
                 f"\"{iter_filter.value}\"" + "}"]
                for iter_filter in audit_filters]
            post_filters = [
                f"{filter_pair[0]}={quote(filter_pair[1])}"
                for filter_pair in filter_pairs]

            str_filter = "&".join(post_filters)
            if len(str_filter) > 0:
                str_filter += "&"
        url = (routes.AUDIT.format(workspace_id=self.id) +
               "?" +
               f"{str_filter}%20" +
               f"projectionColumns={','.join(projection_columns)}" +
               f"&pageSize={page_size}&pageNumber={page_number}"
               )
        response_dict = self.http_client.request("GET", url)
        return response_dict['data']

    def create_mcp(self, name: str, description: str, mcp_url: str, auth_data: mcp.McpAuthData,
                   allowed_mcp_tool_names: list[str] | None, image: bytes | None) -> MCP:
        """
        Configure a new MCP to the workspace
        :param name: The desired name of the MCP
        :param description: The desired description of the MCP
        :param mcp_url: The url of the MCP
        :param auth_data: The authentication data of the MCP
        :param allowed_mcp_tool_names: allowed mcp tools name (None means allow all)
        :param image: Icon for easy identification
        :return: An PVML MCP client
        :raises Exception: If the API call fails
        """
        url = routes.MCPS.format(workspace_id=self.id)
        payload = {
            "name": name,
            "description": description,
            "allowedMcpToolNames": allowed_mcp_tool_names,
            "type": "external",
            "url": mcp_url,
            "authType": auth_data.auth_type,
            "baseAuthData": None if auth_data.base_auth_data is None else vars(auth_data.base_auth_data),
            "oauthData": None if auth_data.oauth_data is None else vars(auth_data.oauth_data)
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        body_text, headers = self.http_client.metadata_request(payload, image_bytes=image)
        response_dict = self.http_client.request("POST", url, headers, data=body_text)
        return MCP(self.http_client, response_dict, image)

    def get_mcps(self) -> Dict[str, MCP]:
        """
        Fetches all configured MCPs on this workspace
        :return: A dictionary of MCPs mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.MCPS.format(workspace_id=self.id)
        response_ls = self.http_client.request("GET", url)
        return {_mcp['id']: MCP(self.http_client, _mcp, image=_mcp['image']) for _mcp in response_ls['mcps']}

    def get_mcps_by_ids(self, mcp_ids: List[str]) -> Dict[str, MCP]:
        """
        Fetches configured MCPs on this workspace by the given ids
        :return: A dictionary of MCPs mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.MCPS_IDS.format(workspace_id=self.id)
        payload = {
            "mcpsIds": mcp_ids,
        }
        response_ls = self.http_client.request("POST", url, json=payload)
        return {_mcp['id']: MCP(self.http_client, _mcp, _mcp['image']) for _mcp in response_ls['mcps']}

    def get_permitted_mcps(self) -> Dict[str, MCP]:
        """
        Fetches user permitted MCPs
        :return: A dictionary of MCPs mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.MCPS_PERMITTED.format(workspace_id=self.id)
        response_ls = self.http_client.request("GET", url)
        return {_mcp['id']: MCP(self.http_client, _mcp, _mcp['image']) for _mcp in response_ls['mcps']}

    def get_mcp(self, mcp_id: str) -> MCP:
        """
        Fetches the details for a specific MCP
        :param mcp_id: The ID of the MCP to retrieve details for
        :return: An MCP object containing the MCP details
        :raises Exception: If the API call fail
        """
        url = routes.MCP.format(workspace_id=self.id, mcp_id=mcp_id)
        response_dict = self.http_client.request("GET", url)
        return MCP(self.http_client, response_dict['mcp'], base64.b64decode(response_dict['mcp']['image']))

    def delete_mcp(self, mcp_id: str | None = None, mcp: MCP | None = None) -> None:
        """
        Deletes a specific MCP
        :param mcp_id: The ID of the MCP to delete
        :param mcp: The MCP to delete
        :return: None
        :raises Exception: If the API call fails
        """
        mcp_id = util.get_id(mcp_id, mcp)
        url = routes.MCP.format(workspace_id=self.id, mcp_id=mcp_id)
        self.http_client.request("DELETE", url)

    def create_agent(self, name: str, prompt: str, description: str | None = None,
                     mcp_ids: List[str] | None = None, llm: LLM | None = None,
                     llm_id: str | None = None, image: bytes | None = None) -> Agent:
        """
        Configure a new Agent in the workspace
        :param name: The desired name of the Agent
        :param prompt: The prompt for the Agent
        :param description: The desired description of the Agent
        :param mcp_ids: List of MCP IDs to associate with the Agent
        :param llm: The llm to associate with the Agent (choose one to pass, llm or llm_id)
        :param llm_id: The llm_id to associate with the Agent (choose one to pass, llm or llm_id)
        :param image: The image to associate with the Agent
        :return: A PVML Agent client
        :raises Exception: If the API call fails
        """
        llm_id = util.get_id(llm_id, llm)
        url = routes.AGENTS.format(workspace_id=self.id)
        payload = {
            "name": name,
            "description": description if description is not None else "",
            "prompt": prompt,
            "llmId": llm_id,
            "mcps": mcp_ids if mcp_ids is not None else [],
        }
        body_text, headers = self.http_client.metadata_request(payload, image)
        response_dict = self.http_client.request("POST", url, data=body_text, headers=headers)
        return Agent(self.http_client, response_dict)

    def get_agents(self) -> Dict[str, Agent]:
        """
        Fetches all configured Agents on this workspace
        :return: A dictionary of Agents mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.AGENTS.format(workspace_id=self.id)
        response_ls = self.http_client.request("GET", url)
        return {agent['id']: Agent(self.http_client, agent) for agent in response_ls['workspaceAgents']}

    def get_agent(self, agent_id: str) -> Agent:
        """
        Fetches the details for a specific Agent
        :param agent_id: The ID of the Agent to retrieve details for
        :return: An agent instance
        :raises Exception: If the API call fail
        """
        url = routes.AGENT.format(workspace_id=self.id, agent_id=agent_id)
        response_dict = self.http_client.request("GET", url)
        return Agent(self.http_client, response_dict)

    def delete_agent(self, agent_id: str | None = None, agent: Agent | None = None) -> None:
        """
        Deletes a specific agent
        :param agent_id: The ID of the Agent to delete
        :param agent: The Agent to delete
        :return: None
        :raises Exception: If the API call fails
        """
        agent_id = util.get_id(agent_id, agent)
        url = routes.AGENT.format(workspace_id=self.id, agent_id=agent_id)
        self.http_client.request("DELETE", url)

    def get_permitted_agents(self) -> Dict[str, Agent]:
        """
        Fetches all configured Agents on this workspace that the user has access to
        :return: A dictionary of Agents mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.AGENTS_PERMITTED.format(workspace_id=self.id)
        response_ls = self.http_client.request("GET", url)
        return {agent['id']: Agent(self.http_client, agent) for agent in response_ls['workspaceAgents']}

    def get_permitted_agent_sessions(self) -> Dict[str, AgentSession]:
        """
        Fetches all configured Agents on this workspace
        :return: A dictionary of Agents mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.AGENTS_PERMITTED_SESSIONS.format(workspace_id=self.id)
        response_ls = self.http_client.request("GET", url)
        return {session['sessionId']: AgentSession(self.http_client, session) for session in
                response_ls['userSessions']}

    def clear_permitted_agent_sessions(self) -> None:
        """
        Clears all sessions the user has access to
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.AGENTS_PERMITTED_SESSIONS.format(workspace_id=self.id)
        self.http_client.request("DELETE", url)
