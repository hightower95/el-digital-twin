


# In some circumstances we want to specify a Connector Database to use for the project.
# This is useful now, when there is no built-in connector library for the project
# The connector database is not mandatory, but without it a warning will be displayed when the project is loaded.
# We might do this when we have a format that the library does not support, or if we want to modify the data before adding it to the project.
from el_analysis.models.physical.connector import Connector
from el_analysis.models.physical.part import Part
from sample_connector_db.connector_database import ConnectorDatabase, Connector as DBConnector
from el_analysis.connector_toolkit import ConnectorDBInterface
from typing import Callable, Optional

class CustomConnectorDatabaseInterface(ConnectorDBInterface):
    from el_analysis.models.physical.connector import Connector
    def __init__(self, connector_db: ConnectorDatabase):
        # super().__init__(connector_db)
        self.connector_db = connector_db
        self.connectors = []
        self._connector_cache = {}

    def _db_to_connector(self, connector: DBConnector) -> Optional[Connector]:
        """
        Convert a database connector to a project connector.
        """
        if not connector:
            return None

        if connector.part_number in self._connector_cache:
            return self._connector_cache[connector.part_number]
        
        else:
            part = Part(connector.part_number, connector.part_type)
            new_connector = Connector(part=part)
            self._connector_cache[connector.part_number] = new_connector

            return new_connector

    @staticmethod
    def _connector_to_db(connector: Connector) -> Optional[DBConnector]:
        """
        Convert a project connector to a database connector.
        """
        if not connector or not connector.part:
            return None
        
        if connector.part.part_number is None or connector.part.part_type is None:
            return None
        # Here we would typically convert the Connector to a DBConnector
        # For now, we assume the Connector is already in the correct format
        from sample_connector_db.connector_part import ConnectorPart
        
        connector_part = ConnectorPart.from_part_code_string(connector.part.part_type)
        return DBConnector(part=connector_part, part_number=connector.part.part_number or "")

    def get_connector_by_part_number(self, part_number: str) -> Optional[Connector]:
        connector = self.connector_db.get_connector_by_part_number(part_number)
        return self._db_to_connector(connector) if connector else None

    def get_connectors_by_part_type(self, part_type: str) -> list[Connector]:
        connectors = self.connector_db.get_connectors_by_part_type(part_type)
        # Convert each DBConnector to a Connector
        # using the _db_to_connector method
        if not connectors:
            return []
        _connectors = [self._db_to_connector(connector) for connector in connectors]
        # Filter out None values
        return [connector for connector in _connectors if connector]

    def get_connector_by_part_type(self, part_type: str) -> Optional[Connector]:
        connector = self.connector_db.get_connector_by_part_type(part_type)
        return self._db_to_connector(connector) if connector else None

    def get_connectors_by_material(self, material: str) -> list[Connector]:
        connectors = self.connector_db.get_connectors_by_material(material)
        if not connectors:
            return []
        _connectors = [self._db_to_connector(connector) for connector in connectors]
        # Filter out None values
        return [connector for connector in _connectors if connector]

    def get_connectors_by_lambda(self, filter: Callable) -> list[Connector]:
        connectors = self.connector_db.get_connectors_by_lambda(filter)
        if not connectors:
            return []
        _connectors = [self._db_to_connector(connector) for connector in connectors]
        # Filter out None values
        return [connector for connector in _connectors if connector]
    
    def get_connectors_by_gender(self, gender: str) -> list[Connector]:
        connectors = self.connector_db.get_connectors_by_gender(gender)
        if not connectors:
            return []
        _connectors = [self._db_to_connector(connector) for connector in connectors]
        # Filter out None values
        return [connector for connector in _connectors if connector]
    
    def get_opposite_connector(self, connector: Connector) -> Optional[Connector]:
        """
        Get the opposite connector for a given connector.
        :param connector: The connector to find the opposite for.
        :return: The opposite connector if found, None otherwise.
        """
        db_connector = self._connector_to_db(connector)
        if not db_connector:
            return None
        
        opposite_connector = self.connector_db.get_opposite_connector(db_connector)
        if not opposite_connector:
            return None

        return self._db_to_connector(opposite_connector)

connector_database = CustomConnectorDatabaseInterface(ConnectorDatabase())