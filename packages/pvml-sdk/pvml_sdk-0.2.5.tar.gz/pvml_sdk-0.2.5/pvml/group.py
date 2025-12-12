from typing import List, Dict

from pvml import routes, util
from pvml.entities import EntityType
from pvml.pvml_http_client import PvmlHttpClient


class Group(util.Identifiable):
    """
    Represent a user group in PVML
    Attributes:
         id (int): the group id
         workspace_id (int): the workspace id
         name (str): the group name
         description (str): the group description
         created_at (datetime): the group creation time
         last_modified_at (datetime): the last time the group info was modified
         image (bytes): the group image
    """

    def __init__(self, http_client: PvmlHttpClient, data: dict):
        self.__http_client = http_client
        self.id = data['id']
        self.workspace_id = data['workspaceId']
        self.__entity_type = EntityType.GROUP
        self.name = data['name']
        self.description = data['description']
        self.created_at = util.convert_string_to_datetime(data['createdAt'])
        self.last_modified_at = util.convert_string_to_datetime(data['lastModifiedAt'])
        self.image = data['image']

    def __str__(self):
        return f"Group(group_id='{self.id}', name={self.name})"

    def __repr__(self):
        return f"Group(group_id='{self.id}', name={self.name})"

    @property
    def entity_type(self):
        return self.__entity_type

    @property
    def http_client(self):
        return self.__http_client

    def _create_user(self, user_data):
        from pvml.workspace_user import WorkspaceUser
        return WorkspaceUser(self.http_client, user_data)

    def get_users(self) -> Dict[str, 'WorkspaceUser']:
        """
        Fetches users associated with this group.
        :return: A dictionary of WorkspaceUsers mapped by their id
        :raises Exception: If the API call fails
        """
        url = routes.GROUP_USERS.format(workspace_id=self.workspace_id, group_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {user_data['User']['id']: self._create_user(user_data) for user_data in
                response_dict["users"]}

    def update_users(self, user_ids_to_add: List[str] = None, user_ids_to_remove: List[str] = None):
        """
        Updates the users in the group by adding or removing users.
        :param user_ids_to_add: A list of user ids to add to the group
        :param user_ids_to_remove: A list of user ids to remove from the group
        :return: None
        :raises Exception: If the API call fails
        """
        _users_to_add = [] if user_ids_to_add is None else list(set(user_ids_to_add))
        _users_to_remove = [] if user_ids_to_remove is None else list(set(user_ids_to_remove))
        url = routes.GROUP_USERS.format(workspace_id=self.workspace_id, group_id=self.id)
        payload = {
            "usersToAdd": _users_to_add,
            "usersToRemove": _users_to_remove
        }
        self.http_client.request("PATCH", url, json=payload)
