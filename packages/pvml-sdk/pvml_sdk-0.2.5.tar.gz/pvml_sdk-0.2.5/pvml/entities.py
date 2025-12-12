from enum import Enum


class EntityType(Enum):
    GROUP = "group"
    USER = "user"


class Entity:
    """
    An object for entities, returned from View client or Agent client.

    Attributes:
        id (str): id of the object
        entity_type (EntityType): The type of the object (group or user)
    """

    def __init__(self, id: str, entity_type: EntityType):
        if not isinstance(entity_type, EntityType):
            raise ValueError(f"type must be one of {list(EntityType)}")

        self.id = id
        self.__entity_type = entity_type

    def get_payload(self):
        return {f"id": self.id, "type": self.entity_type.value}

    @property
    def entity_type(self):
        return self.__entity_type
