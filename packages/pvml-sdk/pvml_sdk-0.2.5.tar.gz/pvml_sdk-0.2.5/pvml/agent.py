from typing import Dict
from typing import List
from typing import TYPE_CHECKING

from pvml import routes, util
from pvml.agent_session import AgentSession
from pvml.entities import Entity, EntityType
from pvml.group import Group
from pvml.pvml_http_client import PvmlHttpClient
from pvml.util import convert_string_to_datetime
from pvml.workspace_user import WorkspaceUser

if TYPE_CHECKING:
    pass


class Agent:
    """
    An Agent object and client

    Attributes:
        id (str): id of the agent
        workspace_id (str):  id of the workspace
        name (str): name of the agent
        description (str): description of the agent
        creation_time (str): creation time of the agent
        created_by (str): the user_id who created the agent
        prompt (str): the prompt of the agent
        llm_id (str): the id of the llm powering the agent
        mcp_ids (str): the mcp(ids) the agent has access to
    """

    def __assign_info(self, agent_info: dict) -> None:
        self.id = agent_info['id']
        self.workspace_id = agent_info['workspaceId']
        self.name = agent_info['name']
        self.description = agent_info['description']
        self.creation_time = convert_string_to_datetime(agent_info['creationTime'])
        self.created_by = agent_info['createdBy']
        self.prompt = agent_info['prompt']
        self.llm_id = agent_info['llmId']
        self.mcp_ids = agent_info['mcps']

    def __init__(self, http_client: PvmlHttpClient, agent_info: dict):
        self.__http_client = http_client
        self.__assign_info(agent_info)

    def __str__(self):
        return f"Agent(name='{self.name}', id='{self.id}')"

    def __repr__(self):
        return f"Agent(name='{self.name}', id='{self.id}')"

    @property
    def http_client(self):
        return self.__http_client

    def get_prompt(self) -> str:
        return self.prompt

    def get_llm_id(self) -> str:
        return self.llm_id

    def update(self, name: str, prompt: str, description: str = None,
               mcp_ids: list[str] = None, llm: "LLM" = None,
               llm_id: str = None, image: bytes = None):
        """
        Update a configured Agent
        :param name: The desired name of the Agent
        :param prompt: The prompt for the Agent
        :param description: The desired description of the Agent
        :param mcp_ids: List of MCP IDs to associate with the Agent
        :param llm: The llm to associate with the Agent (choose one to pass, llm or llm_id)
        :param llm_id: The llm_id to associate with the Agent (choose one to pass, llm or llm_id)
        :param image: The image to associate with the Agent
        :return: None
        :raises Exception: If the API call fails
        """
        llm_id = util.get_id(llm_id, llm)
        url = routes.AGENT.format(workspace_id=self.workspace_id, agent_id=self.id)
        payload = {
            "name": name,
            "description": description if description is not None else "",
            "prompt": prompt,
            "llmId": llm_id,
            "mcps": mcp_ids if mcp_ids is not None else [],
        }
        body_text, headers = self.http_client.metadata_request(payload, image)
        response_dict = self.http_client.request("POST", url, data=body_text, headers=headers)
        self.__assign_info(response_dict)

    def generate(self, user_input: str):
        """
        Stream responses from the agent via SSE (Server-Sent Events).
        Yields one event at a time.
        :param user_input: User input for the agent
        :yield: Individual SSE event data
        :raises Exception: If the API call fails
        """

        headers = self.http_client.get_text_header(user_input)
        url = routes.AGENT_GENERATE.format(workspace_id=self.workspace_id, agent_id=self.id)

        yield from self.http_client.request_sse_stream_sync("POST", url, headers=headers, data=user_input)

    def start_session(self, session_title: str) -> AgentSession:
        """
        Start a new session with history
        :param session_title: The title of the session
        :return: An AgentSession instance
        :raises Exception: If the API call fails
        """
        url = routes.AGENT_SESSIONS.format(workspace_id=self.workspace_id, agent_id=self.id)
        payload = {
            "title": session_title,
        }
        response_dict = self.http_client.request("POST", url, json=payload)
        return AgentSession(self.http_client, response_dict)

    def get_session(self, session_id: str) -> AgentSession:
        """
        Get an AgentSession instance
        :param session_id: The session id
        :return: An AgentSession instance
        :raises Exception: If the API call fails
        """
        url = routes.SESSION.format(workspace_id=self.workspace_id, agent_id=self.id, session_id=session_id)
        response = self.http_client.request("GET", url)
        return AgentSession(self.http_client, response)

    def get_sessions(self) -> Dict[str, AgentSession]:
        """
        Get all session instances that the user has access to
        :return:  A dictionary of AgentSessions mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.AGENT_PERMITTED_SESSIONS.format(workspace_id=self.workspace_id, agent_id=self.id)
        response_ls = self.http_client.request("GET", url)
        return {session['sessionId']: AgentSession(self.http_client, session) for session in
                response_ls['agentSessions']}

    def clear_sessions(self) -> None:
        """
        Clear all sessions that the user has access to under the agent
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.AGENT_PERMITTED_SESSIONS.format(workspace_id=self.workspace_id, agent_id=self.id)
        self.http_client.request("DELETE", url)

    def delete_session(self, session_id: str = None, session: AgentSession = None):
        """
        Delete a specific session
        :param session_id: The ID of the LLM to delete
        :param session: The LLM to delete
        :return: None
        :raises Exception: If the API call fails
        """
        session_id = util.get_id(session_id, session)
        url = routes.SESSION.format(workspace_id=self.workspace_id, agent_id=self.id, session_id=session_id)
        self.http_client.request("DELETE", url)

    def get_entities(self) -> Dict[str, Entity]:
        """
        Fetches the entities (users and groups) associated with the agent
        :return: A dictionary of Entity objects mapped by id
        :raises Exception: If the API call fails
        """
        url = routes.AGENT_ENTITIES.format(workspace_id=self.workspace_id, agent_id=self.id)
        entities_data = self.http_client.request('GET', url)['entities']

        entities = {entity['user']['id']: Entity(entity['user']['id'], EntityType.USER)
                    for entity in entities_data
                    if entity['type'] == 'user'}
        entities.update(
            {entity['group']['id']: Entity(entity['group']['id'], EntityType.GROUP)
             for entity in entities_data
             if entity['type'] == 'group'}
        )
        return entities

    def update_entities(self, entities_to_add: List[Entity | WorkspaceUser | Group] = None,
                        entities_to_remove: List[Entity | WorkspaceUser | Group] = None) -> None:
        """
        Updates the entities assigned to the agent
        :param entities_to_add: A list of entity ids to add to the agent
        :param entities_to_remove: A list of entity ids to remove from the agent
        :return: None
        :raises Exception: If the API call fails
        """
        e_to_add = [Entity(e.id, e.entity_type).get_payload() for e in
                    entities_to_add] if entities_to_add is not None else []
        e_to_remove = [Entity(e.id, e.entity_type).get_payload() for e in
                       entities_to_remove] if entities_to_remove is not None else []
        url = routes.AGENT_ENTITIES.format(workspace_id=self.workspace_id, agent_id=self.id)
        payload = {
            "entitiesToAdd": e_to_add,
            "entitiesToRemove": e_to_remove
        }
        self.http_client.request('PATCH', url, json=payload)