from enum import Enum
from typing import Dict, Any

from pvml import routes, util
from pvml.pvml_http_client import PvmlHttpClient


class PolicyType(Enum):
    DATA_VALIDATION = "data_validation"
    DATA_ACCESS = "data_access"
    DATA_FILTER = "data_filter"
    DATA_PRIVACY = "data_privacy"
    DATA_MASKING = "data_masking"


class Policy:
    """
        Data Validation Policy:
            - Purpose: Specifies validation rules, such as schemas or data sources.
            - Fully qualified format: "catalog"."schema"."table"."column".

        Example:
            policy_data = {
                "type": "data_validation",
                "data": {
                    "header": "Agg only databricks",
                    "aggregationPermission": {"schemas": ['"catalog"."schema"']}
                }
            }

        -------------------------------------------------------------------------------------

        Data Access Policy:
            - Purpose: Grants access to specific tables, columns, and schemas.
            - Fully qualified format: "catalog"."schema"."table"."column".

        Example:
            policy_data = {
                "type": "data_access",
                "data": [
                    {"table": '"accounts"', "column": '"income"', "schema": '"catalog"."schema"'}
                ]
            }

        -------------------------------------------------------------------------------------

        Data Filter Policy:
            - Purpose: Applies filters to the data for access control or privacy.
            - Fully qualified format: "catalog"."schema"."table"."column".

        Example:
            policy_data = {
                "type": "data_filter",
                "data": "filters": [
                    {"basic": {"type": "character varying", "value": "London",
                     "column": '"catalog"."schema"."table"."column"', "compOperator": "="}}
                ]
            }

        -------------------------------------------------------------------------------------

        Data Privacy Policy:
            - Purpose: Defines privacy rules, such as allowed schemas.
            - Fully qualified format: "catalog"."schema"."table"."column".

        Example:
            policy_data = {
                "type": "data_privacy",
                "data": {"schemas": ['"catalog"."schema"']}
            }

        -------------------------------------------------------------------------------------

        Data Masking Policy:
            - Purpose: Masks sensitive columns for privacy compliance.
            - Fully qualified format: "catalog"."schema"."table"."column".

        Example:
            policy_data = {
                "type": "data_masking",
                "data": [
                    {"column": '"catalog"."schema"."table"."column"', "unmaskLeft": 0, "unmaskRight": 0}
                ]
            }
    """

    def __init__(self, http_client: PvmlHttpClient, policy_data: Dict[str, Any]):
        self.__http_client = http_client

        self.id = policy_data["id"]
        self.type = PolicyType(policy_data["type"])
        self.name = policy_data["name"]
        self.description = policy_data["description"]
        self.workspace_id = policy_data["workspaceId"]
        self.created_at = util.convert_string_to_datetime(policy_data["createdAt"])
        self.last_modified_at = util.convert_string_to_datetime(policy_data["lastModifiedAt"])
        self.datasource_id = policy_data["datasourceId"]
        self.datasource_name = policy_data["datasourceName"]
        self.datasource_type = policy_data["datasourceType"]
        self.data = policy_data["data"]

    @property
    def http_client(self):
        return self.__http_client

    def __repr__(self):
        return f"Policy(id={self.id}, type={self.type}, name={self.name}, description={self.description})"

    def update(self, name: str, description: str, policy_type: PolicyType, data: str) -> None:
        """
        Updates the policy
        :param name: name of the policy
        :param description: description of the policy
        :param policy_type: type of the policy
        :param data: data of the policy
        :return: None
        :raises Exception: If the API call fails
        """
        url = routes.DATASOURCE_PERMISSION.format(workspace_id=self.workspace_id, datasource_id=self.datasource_id,
                                                  permission_id=self.id)
        payload = {
            "name": name,
            "description": description,
            "type": policy_type.value,
            "data": data
        }
        response_dict = self.http_client.request('PUT', url, json=payload)
        updated_policy = response_dict['permission']
        self.type = PolicyType(updated_policy["type"])
        self.name = updated_policy["name"]
        self.description = updated_policy["description"]
        self.data = updated_policy["data"]
