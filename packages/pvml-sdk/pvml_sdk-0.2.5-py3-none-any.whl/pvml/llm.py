from pvml import routes
from pvml.pvml_http_client import PvmlHttpClient
from pvml.util import convert_timestamp_to_datetime


class LLM:
    """
    Represent a connected LLM in PVML
    Attributes:
         id (int): the llm id
         workspace_id (int): the workspace id
         name (str): the llm name
         description (str): the llm description
         vendor_name (str): the llm vendor name
         model_name (str): the llm model name
         llm_props (dict): the llm connection properties (temperature, host, etc..)
         created_at (datetime): the llm creation time
         last_modified_at (datetime): the last time the llm was modified
    """

    def __init__(self, http_client: PvmlHttpClient, llm_info: dict):
        self.__http_client = http_client
        self.id = llm_info['id']
        self.name = llm_info['name']
        self.description = llm_info['description']
        self.vendor_name = llm_info['vendorName']
        self.model_name = llm_info['modelName']
        self.workspace_id = llm_info['workspaceId']
        self.llm_props = llm_info['llmProps']
        self.created_at = convert_timestamp_to_datetime(llm_info.get('createdAt'))
        self.last_modified_at = convert_timestamp_to_datetime(llm_info.get('lastModifiedAt'))

    def __str__(self):
        return f"LLM(name='{self.name}', id='{self.id}')"

    def __repr__(self):
        return f"LLM(name='{self.name}', id='{self.id}')"

    @property
    def http_client(self):
        return self.__http_client

    @property
    def props(self) -> dict:
        for key, prop in self.llm_props.items():
            if prop is not None:
                return self.llm_props[key]
        raise ValueError("LLM uninitialized missing props")

    def update(self, name: str, description: str, vendor_name: str, model_name: str, llm_props: dict):
        """
        Updates the LLM info on the platform
        :return: Response from the API.
        :raises Exception: If the API call fails
        """
        url = routes.LLM.format(workspace_id=self.workspace_id, llm_id=self.id)
        payload = {
            "name": name,
            "description": description,
            "vendorName": vendor_name,
            "modelName": model_name,
            "llmProps": llm_props,
        }
        payload = {k: v for k, v in payload.items() if (v != '') and (llm_props is not None)}
        response_dict = self.http_client.request("POST", url, json=payload)

        self.name = response_dict['name']
        self.description = response_dict['description']
        self.vendor_name = response_dict['vendorName']
        self.model_name = response_dict['modelName']
        self.llm_props = response_dict['llmProps']

    @staticmethod
    def create_basic_props(temperature: float) -> dict:
        return {'temperature': temperature, "maxTokens": None}

    @staticmethod
    def create_custom_props(input_dict: dict) -> dict:
        if input_dict is None:
            raise ValueError('input_dict cannot be None')
        return input_dict

    @staticmethod
    def create_azure_props(azure_endpoint: str, azure_deployment_name: str,
                           open_ai_api_version: str, temperature: float) -> dict:
        return {'azureEndpoint': azure_endpoint, 'azureDeploymentName': azure_deployment_name,
                'openAiApiVersion': open_ai_api_version, 'temperature': temperature}

    @staticmethod
    def create_databricks_props(host: str, temperature: float) -> dict:
        return {'host': host, 'temperature': temperature}

    @staticmethod
    def create_databricks_genie_props(host: str, space_id: str, temperature: float) -> dict:
        return {'host': host, 'space_id': space_id, 'temperature': temperature}

    @staticmethod
    def create_nim_props(model_name: str, base_url: str) -> dict:
        return {'modelName': model_name, "baseUrl": base_url}
