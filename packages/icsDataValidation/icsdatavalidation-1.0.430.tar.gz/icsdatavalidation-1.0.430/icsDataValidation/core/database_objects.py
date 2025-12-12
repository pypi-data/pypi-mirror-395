from enum import Enum

class DatabaseObjectType(Enum):
    """
    Enum for valid database object types
    """

    TABLE = "table"
    VIEW = "view"

class DatabaseObject():
    def __init__(self, object_identifier: str, object_type: DatabaseObjectType):
        self.identifier = object_identifier
        self.database   = object_identifier.split(".",2)[0]
        self.schema     = object_identifier.split(".",2)[1]
        self.name       = object_identifier.split(".",2)[2]
        self.type       = object_type
    