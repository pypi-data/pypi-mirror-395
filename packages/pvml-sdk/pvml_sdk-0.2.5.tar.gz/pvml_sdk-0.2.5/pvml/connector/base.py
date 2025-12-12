from abc import ABC, abstractmethod


class BaseConnector(ABC):
    def __init__(self):
        self.type = 'Base'
        self.name = None
        self.description = None

    def get_payload(self):
        pass
