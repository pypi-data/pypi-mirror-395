import json
from typing import Dict

from pvml import routes, util
from pvml.connector.base import BaseConnector
from pvml.policy import Policy, PolicyType
from pvml.pvml_http_client import PvmlHttpClient
from pvml.schema_relation import DatasourceRelations


class Datasource:
    """
    A datasource object and client.
    Holds the connection information about the connected database

    Attributes:
        workspace_id (str): The associated workspace id
        id (str): id of the datasource
        name (str): name of the datasource
        description (str): description of the datasource
    """

    def __init__(self, http_client: PvmlHttpClient, ds: dict):
        self.__http_client = http_client
        self.id = ds['id']
        self.name = ds['name']
        self.type = ds['type']
        self.description = ds['description']
        self.workspace_id = ds['workspaceId']

    def __str__(self):
        return f"Datasource(name='{self.name}', id='{self.id})"

    def __repr__(self):
        return f"Datasource(name='{self.name}', id='{self.id})"

    @property
    def http_client(self):
        return self.__http_client

    def ping(self) -> str:
        """
        Sends a ping request to a datasource to tests its connectivity
        :return: 'passed' if the ping is successful, otherwise 'failed'
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_PING.format(workspace_id=self.workspace_id, datasource_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return response_dict['result']

    def get_schemas_tree(self) -> Dict:
        """
        Fetch the tree structure for the datasource
        :return: The tree structure as a dictionary
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_TREE.format(workspace_id=self.workspace_id, datasource_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return response_dict['tree']['schemas']

    def get_relations(self) -> DatasourceRelations:
        """
        Fetch all the table relations for the datasource
        :return: The metadata relations as a dictionary
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_RELATIONS.format(workspace_id=self.workspace_id, datasource_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return DatasourceRelations(response_dict['schemaRelations'])

    def get_policies(self) -> dict[str, Policy]:
        """
        Fetch all the policies for the datasource
        :return: Dictionary of policies mapped by their ids
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_PERMISSIONS.format(workspace_id=self.workspace_id, datasource_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return {permission['id']: Policy(self.http_client, permission) for permission in response_dict['permissions']}

    def get_connection_details(self) -> dict:
        """
        Get the datasource connection details (doesn't returns secrets)
        :return: The connection details as a dictionary
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_DATA.format(workspace_id=self.workspace_id, datasource_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return json.loads(response_dict['data'])

    def get_descriptions(self) -> dict:
        """
        Fetch all the schema, table, column descriptions in the datasource
        :return: A dictionary of the datasource descriptions, the schema, table, column path maps to its descriptions
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_DESCRIPTIONS.format(workspace_id=self.workspace_id, datasource_id=self.id)
        response_dict = self.http_client.request("GET", url)
        return response_dict['descriptions']

    def patch_descriptions(self, new_descriptions_arr, remove_coordinates_arr):
        """
        Update the descriptions of the datasource, add new descriptions or remove existing ones
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_DESCRIPTIONS.format(workspace_id=self.workspace_id, datasource_id=self.id)
        payload = {"toAdd": new_descriptions_arr, "toRemove": remove_coordinates_arr}
        self.http_client.request("PATCH", url, json=payload)

    def create_policy(self, name: str, description: str, policy_type: PolicyType, data: str) -> Policy:
        """
        Create a new policy
        :return: A policy object
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_PERMISSIONS.format(workspace_id=self.workspace_id, datasource_id=self.id)
        payload = {
            "name": name,
            "description": description,
            "type": policy_type.value,
            "data": data
        }
        response_dict = self.http_client.request("POST", url, json=payload)
        return Policy(self.http_client, response_dict['permission'])

    def get_policy(self, policy_id: str = None, policy: Policy = None) -> Policy:
        """
        Fetch a policy by its id
        :return: A policy object
        :raises Exception: If the API call fails
        """
        permission_id = util.get_id(policy_id, policy)
        url = routes.DATASOURCE_PERMISSION.format(workspace_id=self.workspace_id, datasource_id=self.id,
                                                  permission_id=permission_id)
        response_dict = self.http_client.request("GET", url)
        return Policy(self.http_client, response_dict['permission'])

    def delete_policy(self, policy_id: str = None, policy: Policy = None):
        """
        Deletes a specific policy
        :param policy_id: The ID of the policy to delete
        :param policy: The policy to delete (prioritizes policy_id if both are provided)
        :return: None
        :raises Exception: If the API call fails
        """
        permission_id = util.get_id(policy_id, policy)
        url = routes.DATASOURCE_PERMISSION.format(workspace_id=self.workspace_id, datasource_id=self.id,
                                                  permission_id=permission_id)
        self.http_client.request("DELETE", url)

    def update(self, name: str = "", description: str = "",
               connector: BaseConnector = None) -> None:
        """
        Update the datasource's name, description or connector details
        :param name: The name of the datasource
        :param description: The description of the datasource
        :param connector: The datasource connection details
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE.format(workspace_id=self.workspace_id, datasource_id=self.id)
        data = connector if connector is None else connector.get_payload()['data']
        payload = {
            "name": name,
            "description": description,
            "type": self.type,
            "data": data
        }
        payload = {k: v for k, v in payload.items() if (v is not None) and (v != "")}
        self.http_client.request("PUT", url, json=payload)

        get_datasource_url = routes.DATASOURCE.format(workspace_id=self.workspace_id, datasource_id=self.id)
        response_dict = self.http_client.request("GET", get_datasource_url)
        self.name = response_dict['name']
        self.description = response_dict['description']
