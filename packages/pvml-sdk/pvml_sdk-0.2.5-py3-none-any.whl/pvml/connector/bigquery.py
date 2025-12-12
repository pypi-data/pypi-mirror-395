import json

from pvml.connector.base import BaseConnector


class BigQueryConnector(BaseConnector):
    def __init__(self, name: str, description: str, project_id: str, credentials: str, region: str):
        super().__init__()
        self.type = "BigQuery"
        self.name = name
        self.description = description
        self.project_id = project_id
        self.credentials = credentials

    def get_payload(self):
        """Returns the payload with connection data."""
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "data": json.dumps({
                "projectId": self.project_id,
                "credentials": self.credentials
            })
        }
