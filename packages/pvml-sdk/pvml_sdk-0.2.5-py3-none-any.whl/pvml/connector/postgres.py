import json

from pvml.connector.base import BaseConnector


class PostgresConnector(BaseConnector):
    def __init__(self, name: str, description: str, hostname: str, username: str, password: str, port: int,
                 database_name: str, ssl: bool = True):
        super().__init__()
        self.type = 'Postgres'
        self.name = name
        self.description = description
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.database_name = database_name
        self.ssl = ssl

    def get_payload(self):
        """Returns the payload with connection data."""
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "data": json.dumps({
                "hostName": self.hostname,
                "username": self.username,
                "password": self.password,
                "port": self.port,
                "databaseName": self.database_name,
                "ssl": self.ssl
            })
        }
