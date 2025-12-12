from enum import Enum
from typing import Dict, List, Tuple

from pvml import routes, util
from pvml.entities import EntityType
from pvml.pvml_http_client import PvmlHttpClient


class UserAttributeType(Enum):
    NUMERIC = "numeric"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    TEXT = "text"
    DATE = "date"

class WorkspaceUser(util.Identifiable):
    """
    A WorkspaceUser client
    Attributes:
        id (str): The User id
        workspace_id (str): The identifier of the workspace
        email (str): The email of the user
        created_at (datetime): The time the user was created
        joined_at (datetime): The time the user joined the workspace
        role (str): The role of the user
        user_type (str): The type of the user
    """

    def __init__(self, http_client: PvmlHttpClient, wsu):
        self.__http_client = http_client
        self.id = wsu['User']['id']
        self.__entity_type = EntityType.USER
        self.email = wsu['User']['email']
        self.created_at = wsu['User']['created_at']
        self.workspace_id = wsu['workspaceId']
        self.joined_at = wsu['joined_at']
        self.role = wsu['role']
        self.user_type = wsu['type']

    def __str__(self):
        return f"WorkspaceUser(id='{self.id}', email={self.email} ,workspace_id={self.workspace_id})"

    def __repr__(self):
        return f"WorkspaceUser(id='{self.id}', email={self.email} ,workspace_id={self.workspace_id})"

    @property
    def entity_type(self):
        return self.__entity_type

    @property
    def http_client(self):
        return self.__http_client

    def _create_group(self, user_data):
        from pvml.group import Group
        return Group(self.http_client, user_data)

    def _create_view(self, view_data) -> 'View':
        from pvml.view import View
        return View(self.http_client, view_data)

    def create_token(self, days_until_expiration: int) -> str:
        """
        Create a managed API user token
        :param days_until_expiration: Number of days the token is valid for
        :return: A managed API user token string
        :raises Exception: If the API call fails
        """
        timestamp = util.get_epoch(days_until_expiration)
        url = routes.USER_TOKEN.format(workspace_id=self.workspace_id, user_id=self.id)
        payload = {"expiration": timestamp}
        response_dict = self.http_client.request("POST", url, json=payload)
        return response_dict['token']

    def get_user_views(self) -> Dict[str, 'View']:
        """
        Fetches all views associated with a specific user
        :return: A dictionary of View clients mapped by their id
        :raises Exception: If the API call fails
        """
        url = routes.USER_VIEWS.format(workspace_id=self.workspace_id, user_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {view['viewId']: self._create_view(view) for view in response_dict['views']}

    def get_user_groups(self) -> Dict[str, 'Group']:
        """
        Fetches all groups that the user is a part of
        :return: A dictionary of Group clients mapped by their id
        :raises Exception: If the API call fails
        """
        url = routes.USER_GROUPS.format(workspace_id=self.workspace_id, user_id=self.id) + '?enrich=true&summary=true'
        response_dict = self.http_client.request("GET", url)
        return {group['id']: self._create_group(group) for group in response_dict['groups']}

    def change_user_role(self, role: str) -> None:
        """
        Change the user role
        :param role: The new role
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.USER_ROLE.format(workspace_id=self.workspace_id, user_id=self.id)
        payload = {"role": role}
        self.http_client.request("PUT", url, json=payload)
        self.role = role

    def get_attributes(self) -> Dict:
        """
        Fetches all the user attributes
        :return: A dictionary of user attributes mapped by their key
        :raises Exception: If the API call fails
        """
        url = routes.USER_ATTRIBUTES.format(workspace_id=self.workspace_id, user_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {att['key']: att['value'] for att in response_dict['attributes']}

    def set_attributes(self, attributes: List[Tuple[str, any, UserAttributeType]]) -> Dict:
        """
        Set additional user attributes
        :param attributes: User attributes (key, value, type)
        :return: All the user attributes
        :raises Exception: If the API call fails
        """
        url = routes.USER_ATTRIBUTES.format(workspace_id=self.workspace_id, user_id=self.id)
        payload = {
            "attributes": [
                {"key": key, "value": str(value), "type": data_type.value}
                for key, value, data_type in attributes
            ]
        }
        response_dict = self.http_client.request("PATCH", url, json=payload)
        return {att['key']: att['value'] for att in response_dict['attributes']}
