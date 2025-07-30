


# In some circumstances we want to specify a Connector Database to use for the project.
# This is useful now, when there is no built-in connector library for the project
# The connector database is not mandatory, but without it a warning will be displayed when the project is loaded.
# We might do this when we have a format that the library does not support, or if we want to modify the data before adding it to the project.
# from el_analysis.models.physical.connector import Connector
# from el_analysis.models.physical.part import Part
from sample_connector_db.connector_database import ConnectorDatabase
from el_analysis.connector_toolkit import ConnectorDBInterface
from el_analysis.connector_toolkit.connector import Connector
from typing import Callable, Optional

class CustomConnectorDatabaseInterface(ConnectorDBInterface):
    def __init__(self, connector_db: ConnectorDatabase):
        # super().__init__(connector_db)
        self.connector_db = connector_db
        self.connectors = []
        self._connector_cache = {}

    def _db_to_connector(self, connector: Connector) -> Optional[Connector]:
        """
        Convert a database connector to a project connector.
        """
        if not connector:
            return None
        
        # Here we can do some customer logic to manipulate the connector object before returning it, or doing something else with it
        if connector.part_number in self._connector_cache:
            return self._connector_cache[connector.part_number]
        else:
            self._connector_cache[connector.part_number] = connector
            return connector

    def get_connector_by_part_number(self, part_number: str) -> Optional[Connector]:
        connector = self.connector_db.get_connector_by_part_number(part_number)
        return self._db_to_connector(connector) if connector else None

    def get_connectors_by_part_code(self, part_code: str) -> list[Connector]:
        connectors = self.connector_db.get_connectors_by_part_code(part_code)
        # Convert each DBConnector to a Connector
        # using the _db_to_connector method
        if not connectors:
            return []
        _connectors = [self._db_to_connector(connector) for connector in connectors]
        # Filter out None values
        return [connector for connector in _connectors if connector]

    def get_connector_by_part_code(self, part_code: str) -> Optional[Connector]:
        connector = self.connector_db.get_connector_by_part_code(part_code)
        return self._db_to_connector(connector) if connector else None

    def get_connectors_by_lambda(self, filter: Callable) -> list[Connector]:
        connectors = self.connector_db.get_connectors_by_lambda(filter)
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
        
        opposite_connector = self.connector_db.get_opposite_connector(connector)
        if not opposite_connector:
            return None

        return self._db_to_connector(opposite_connector)

connector_database = ConnectorDatabase()

# In this example, we are adding a custom connector deserializer to the database.
# This allows us to handle custom connector specifications that are not part of the default library.
from custom_connector_spec import CustomSpecification
connector_database.add_connector_deserialization_handler(CustomSpecification)

database_interface = CustomConnectorDatabaseInterface(connector_database)
# Note - adding a handler triggers reloading of the connectors from the database file. Which is problematic if you depend
# on the object ID.


if __name__ == "__main__":
    # Example usage
    part_number = "1-W-S-F"
    connector = connector_database.get_connector_by_part_code(part_number)
    if connector:
        print(f"Found connector: {connector} with part number {connector.part_number}")
    else:
        print(f"No connector found for part number {part_number}")


    connector_db = connector_database
    print(f"Loaded {len(connector_db.connectors)} connectors from {connector_db.db_path}")

    print("Searching for connector with part number 'PN-87_51_77_70'...")
    connector = connector_db.get_connector_by_part_number("PN-87_51_77_70")
    if connector:
        print(f"Found connector: {connector.part_code} with part number {connector.part_number}")
    else:
        print("Connector not found.")

    print("Searching for connector with part type '3-W-M-F'...")
    connector = connector_db.get_connector_by_part_code("3-W-M-F")
    if connector:
        print(f"Found connector: {connector} with part number {connector.part_number}")
        print(f"Found connector: {connector.part_code} with part number {connector.part_number}")
    else:
        print("Connector not found.")

    # print("Searching for connectors with material 'Z'...")
    # connectors = connector_db.get_connectors_by_material("Z")
    # if connectors:
    #     print(f"Found {len(connectors)} connectors with material 'Z':")
    #     for conn in connectors:
    #         print(f"- {conn.part_code} with part number {conn.part_number}")

    print("Searching for connectors that are compatible with 'PN-87_51_77_70'...")
    connector = connector_db.get_connector_by_part_number("PN-87_51_77_70")
    if connector:
        compatible_connectors = connector_db.find_opposite_connectors(connector)
        if compatible_connectors:
            print(f"Found {len(compatible_connectors)} compatible connectors for {connector.part_code}:")
            for opp_connector in compatible_connectors:
                print(f"- {opp_connector.part_code} with part number {opp_connector.part_number}")
    else:
        print("Connector not found for compatibility search.")

    print("Searching for connectors that are adjacent to 'PN-87_51_77_70'...")
    if connector:
        adjacent_connectors = connector_db.find_adjacent_connectors(connector)
        if adjacent_connectors:
            print(f"Found {len(adjacent_connectors)} adjacent connectors for {connector.part_code}:")
            for adj_connector in adjacent_connectors:
                print(f"- {adj_connector.part_code} with part number {adj_connector.part_number}")
    else:
        print("Connector not found for adjacency search.")

    print("Getting opposite connector for 'PN-87_51_77_70', part type '3-W-M-F'...")
    if connector:
        opposite_connector = connector_db.get_opposite_connector(connector)
        if opposite_connector:
            print(f"Found opposite connector: {opposite_connector.part_code} with part number {opposite_connector.part_number}")
        else:
            print("No opposite connector found.")
