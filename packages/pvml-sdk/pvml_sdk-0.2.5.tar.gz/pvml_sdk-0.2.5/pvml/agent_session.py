from pvml import routes
from pvml.pvml_http_client import PvmlHttpClient
from pvml.util import convert_string_to_datetime


class AgentSession:
    """
    A bot object and client

    Attributes:
        id (str): id of the agent session
        agent_id (str): id of the agent
        workspace_id (str):  id of the workspace
        user_id (str): the id of the user who created the session
        title (str): the title of the session
        creation_time (str): creation time of the session
        last_modified (str): last modified time of the session
        messages (list): the messages of the session
    """

    def __assign_info(self, session_info: dict) -> None:
        self.id = session_info['sessionId']
        self.agent_id = session_info['agentId']
        self.workspace_id = session_info['workspaceId']
        self.user_id = session_info['userId']
        self.title = session_info['title']
        self.creation_time = convert_string_to_datetime(session_info['createdAt'])
        self.last_modified = convert_string_to_datetime(session_info['last_modified_at'])
        self.messages = session_info[
            'messages']  # TODO: look at real data and understand what is really coming back here

    def __init__(self, http_client: PvmlHttpClient, session_info: dict):
        self.__http_client = http_client
        self.__assign_info(session_info)

    def __str__(self):
        return f"AgentSession(title='{self.title}', id='{self.id}')"

    def __repr__(self):
        return f"AgentSession(title='{self.title}', id='{self.id}')"

    @property
    def http_client(self):
        return self.__http_client

    def update(self, title: str, messages: list) -> None:
        """
        Update a Session with title and messages (replaces previous values)
        :param title: The desired title of the session
        :param messages: A list of user & ai message interactions
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.SESSION.format(workspace_id=self.workspace_id, agent_id=self.agent_id, session_id=self.id)
        payload = {
            "title": title,
            "messages": messages
        }
        response_dict = self.http_client.request("POST", url, json=payload)
        self.__assign_info(response_dict)

    def update_title(self, session_title: str) -> None:
        """
        Update the title of the session
        :param session_title: New title of the session
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.SESSION_TITLE.format(workspace_id=self.workspace_id, agent_id=self.agent_id, session_id=self.id)
        payload = {
            "title": session_title,
        }
        response_dict = self.http_client.request("POST", url, json=payload)
        self.__assign_info(response_dict)

    def add_message(self, message) -> None:
        """
        Adds a new message to the session messages
        :param message: The new message to add
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.SESSION_MESSAGE.format(workspace_id=self.workspace_id, agent_id=self.agent_id, session_id=self.id)
        payload = {
            "message": message,
        }
        self.http_client.request("POST", url, json=payload)

    def generate(self, user_input: str) -> str:
        """
        Generate a response from the underlying AI-agent
        :param user_input: The user input for the agent
        :return: Generated response
        :raises Exception: If the API call fails
        """
        headers = self.http_client.get_text_header(user_input)
        url = routes.SESSION_GENERATE.format(workspace_id=self.workspace_id, agent_id=self.agent_id, session_id=self.id)
        response = self.http_client.request_expect_text("POST", url, headers=headers, data=user_input)
        return response
