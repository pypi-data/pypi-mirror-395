from typing import List, Dict, AsyncIterator

from pvml import routes, util
from pvml.datasource import Datasource
from pvml.entities import Entity, EntityType
from pvml.group import Group
from pvml.policy import Policy
from pvml.pvml_http_client import PvmlHttpClient
from pvml.util import convert_timestamp_to_datetime
from pvml.workspace_user import WorkspaceUser


class View:
    """
    A view client that allows to call its APIs

    Attributes:
        id (str): id of the view
        workspace_id (str): The associated workspace id
        name (str): name of the view
        description (str): description of the view
        datasource_id (str): the id of the datasource the view belongs to
        created_at (datetime): the timestamp the view was created at
        last_modified_at (datetime): the timestamp the view was last modified at
    """

    def __init__(self, http_client: PvmlHttpClient, data: dict):
        self.__http_client = http_client
        self.id = data['viewId']
        self.datasource_id = data['datasourceId']
        self.datasource_type = data['datasourceType']
        self.workspace_id = data['workspaceId']
        self.name = data['name']
        self.description = data['description']
        self.created_at = convert_timestamp_to_datetime(data['createdAt'])
        self.last_modified_at = convert_timestamp_to_datetime(data['lastModifiedAt'])
        self.permissions_last_modified_at = convert_timestamp_to_datetime(data['permissionsLastModifiedAt'])

    def __repr__(self):
        return f"View(name={self.name}, view_id={self.id})"

    @property
    def http_client(self):
        return self.__http_client

    def get_datasource(self) -> Datasource:
        """
        Fetches the datasource client for this view
        :return: A Datasource client that allows API calls
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_DATA.format(workspace_id=self.workspace_id, datasource_id=self.datasource_id)
        response_dict = self.http_client.request('GET', url)
        return Datasource(self.http_client, response_dict)

    def get_entities(self) -> Dict[str, Entity]:
        """
        Fetches the entities (users and groups) associated with the view
        :return: A dictionary of Entity objects mapped by id
        :raises Exception: If the API call fails
        """
        url = routes.VIEW_ENTITIES.format(workspace_id=self.workspace_id, view_id=self.id)
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

    def get_policies(self) -> Dict[str, Policy]:
        """
        Fetches the policies associated with the view
        :return: A dictionary of Policy objects mapped by id
        :raises Exception: If the API call fails
        """
        url = routes.VIEW_PERMISSIONS.format(workspace_id=self.workspace_id,
                                             view_id=self.id)
        response_dict = self.http_client.request('GET', url)
        return {permission['id']: Policy(self.http_client, permission) for permission in response_dict['permissions']}

    def update_policies(self, policy_ids_to_add: List[str] = None,
                        policy_ids_to_remove: List[str] = None) -> None:
        """
        Updates the policies associated with the view
        :param policy_ids_to_add: A list of policy ids to add to the view
        :param policy_ids_to_remove: A list of policy ids to remove from the view
        :return: None
        :raises Exception: If the API call fails
        """
        policy_ids_to_add = [] if policy_ids_to_add is None else list(set(policy_ids_to_add))
        policy_ids_to_remove = [] if policy_ids_to_remove is None else list(set(policy_ids_to_remove))
        url = routes.VIEW_PERMISSIONS.format(workspace_id=self.workspace_id, view_id=self.id)
        payload = {
            "permissionsToAdd": policy_ids_to_add,
            "permissionsToRemove": policy_ids_to_remove
        }
        self.http_client.request('PATCH', url, json=payload)

    def update_entities(self, entities_to_add: List[Entity | WorkspaceUser | Group] = None,
                        entities_to_remove: List[Entity | WorkspaceUser | Group] = None) -> None:
        """
        Updates the entities assigned to the view
        :param entities_to_add: A list of entity ids to add to the view
        :param entities_to_remove: A list of entity ids to remove from the view
        :return: None
        :raises Exception: If the API call fails
        """
        e_to_add = [Entity(e.id, e.entity_type).get_payload() for e in
                    entities_to_add] if entities_to_add is not None else []
        e_to_remove = [Entity(e.id, e.entity_type).get_payload() for e in
                       entities_to_remove] if entities_to_remove is not None else []
        url = routes.VIEW_ENTITIES.format(workspace_id=self.workspace_id, view_id=self.id)
        payload = {
            "entitiesToAdd": e_to_add,
            "entitiesToRemove": e_to_remove
        }
        self.http_client.request('PATCH', url, json=payload)

    async def execute(self, sql: str) -> AsyncIterator[bytes]:
        """
        Run an SQL query with the view policies
        :param sql: The SQL query to run
        :return: The results of the SQL query
        :raises Exception: If the API call fails
        """
        url = routes.VIEW_EXECUTE.format(workspace_id=self.workspace_id, view_id=self.id)
        payload = {'query': sql}
        async for chunk in self.http_client.request_stream('POST', url, json=payload):
            yield chunk


    def available_policies(self) -> Dict[str, Policy]:
        """
        Fetch all policies associated with the views' **datasource**
        :return: A dictionary of Policy objects mapped by id
        :raises Exception: If the API call fails
        """
        return self.get_datasource().get_policies()

    def get_view_tree(self) -> Dict:
        """
        Fetch the accessible datasource structure under the view policies
        :return: A dictionary describing the datasource structure
        :raises Exception: If the API call fails
        """
        url = routes.VIEW_TREE_DISPLAY.format(workspace_id=self.workspace_id,
                                              view_id=self.id)
        response_dict = self.http_client.request('GET', url)
        return response_dict['tree']

    def get_connection_string(self, name: str, description: str, days_until_expiration: int,
                              user_id: str = None, user: WorkspaceUser = None) -> Dict:
        """
        Get the PVML ODBC/JDBC connector.
        :param name: The name of the connection
        :param description: The description of the connection
        :param days_until_expiration: Number of days until access token expiration
        :param user_id: The user id for which to create the connection string
        :param user: The user for which to create the connection string
        :return: A dictionary containing the connection string details consisting of hostname, http path and access token.
        :raises Exception: If the API call fails
        """
        user_id = util.get_id(user_id, user)
        timestamp = util.get_epoch(days_until_expiration)
        url = routes.VIEW_CONNECTION_STRING.format(workspace_id=self.workspace_id, view_id=self.id, user_id=user_id)
        payload = {
            "name": name,
            "description": description,
            "expiration": timestamp,
        }
        return self.http_client.request('POST', url, json=payload)

    def get_mcp_id(self) -> str:
        """
        Get the MCP id associated with this view
        Returns:
            str: The MCP id
        """

        url = routes.VIEW_MCP.format(workspace_id=self.workspace_id, view_id=self.id)
        response_dict = self.http_client.request('GET', url)
        return response_dict['mcpId']