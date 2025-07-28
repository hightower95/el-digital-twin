
try:
    from .connector_part import DBConnector
except ImportError:
    from connector_part import DBConnector
from typing import Callable, List, Optional
from el_analysis.connector_toolkit.connector import Connector
from el_analysis.connector_toolkit.specification import Specification, DefaultSpecification

class ConnectorDatabase:
    """
    A class to manage a database of connectors.
    This class is responsible for loading, saving, and managing connector data.
    """

    def __init__(self):
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "connectors.csv")

        self.db_path: str = db_path
        self.connectors: list[Connector] = []
        self._deserializers: list[type[Specification]] = []
        self._load_connectors()
        print(f"Loaded {len(self.connectors)} connectors from database.")

    def add_connector_deserialization_handler(self, handler: type[Specification]) -> None:
        """
        Add a handler to the database.
        :param handler: A callable that handles connector specifications.
        """
        print(f"Adding handler for specification: {handler.SPECIFICATION_NAME}")

        self._deserializers.append(handler)

    def _load_connectors(self):
        """
        Load connectors from the database file.
        """
        with open(self.db_path, 'r') as file:
            file.readline()  # Skip header line
            connector_lines = file.readlines()
            for line in connector_lines:
                if line.strip():
                    part_code, part_number = line.strip().split(',')
                    # print(f"Loading connector with part type: {part_code} and part number: {part_number.strip()}")
                    # part_code = ConnectorPart.from_part_code_string(part_code)
                    connector = self._deserialize_connector(part_code, part_number.strip())

                    if not connector:
                        raise ValueError(f"Failed to deserialize connector with part type: {part_code} and part number: {part_number.strip()}")
                    self.connectors.append(connector)

    def _deserialize_connector(self, part_code: str, part_number: str) -> Optional[Connector]:
        """
        Deserialize a connector from its part code.
        :param part_code: The part code of the connector.
        :return: The deserialized connector if successful, None otherwise.
        """
        specification_factory = DefaultSpecification
        for deserializer in self._deserializers:
            if deserializer.can_parse_part_code(part_code):
                specification_factory = deserializer
                break

        specification = specification_factory.from_part_code_string(part_code)

        if specification:
            return Connector(component=specification, part_number=part_number)

        return None

    def get_connector_by_part_number(self, part_number: str):
        """
        Get a connector by its part number.
        :param part_number: The part number of the connector.
        :return: The connector if found, None otherwise.
        """
        for connector in self.connectors:
            if connector.part_number == part_number:
                return connector
        return None
    
    def get_connectors_by_part_code(self, part_code: str):
        """
        Get connectors by their part type.
        :param part_code: The part type of the connectors.
        :return: A list of connectors that match the part type.
        """
        return [connector for connector in self.connectors if connector.part_code == part_code or connector.minified_part_code == part_code]

    def get_connector_by_part_code(self, part_code: str) -> Optional[Connector]:
        """
        Get a connector by its part type.
        :param part_code: The part type of the connector.
        :return: The connector if found, None otherwise.
        """
        for connector in self.connectors:
            if connector.part_code == part_code or connector.minified_part_code == part_code:
                return connector
        return None
    
    def get_connectors_by_lambda(self, filter: Callable):
        """
        Get all connectors that match a specific function
        :param filter: A lambda function to filter connectors.
        :return: A list of connectors that match the key.
        """
        return [connector for connector in self.connectors if filter(connector)]

    def get_random_connector(self):
        """
        Get a random connector from the database.
        :return: A random connector.
        """
        import random
        return random.choice(self.connectors) if self.connectors else None
    
    def get_opposite_connector(self, connector: Connector) -> Optional[Connector]:
        """
        Get a connector that is compatible with the given connector.
        :param connector: The connector to find an opposite for.
        :return: A compatible connector.
        """
        opposite_part = connector.component.get_opposite_part()
        opposite_connector = self.get_connector_by_part_code(opposite_part.as_string())
        if opposite_connector:
            return opposite_connector
        return None
    
    
def find_opposite_connectors(connector: Connector, connector_db: ConnectorDatabase) -> list[Connector]:
    """
    Find connectors that are compatible with the given connector.
    :param connector: The connector to find opposites for.
    :param connector_db: The database of connectors to search in.
    :return: A list of compatible connectors.
    """
    compatible_parts = connector.component.get_compatible_parts()
    opposite_connectors = []
    
    for part in compatible_parts:
        db_connector = connector_db.get_connector_by_part_code(part.as_string())
        if db_connector:
            opposite_connectors.append(db_connector)
    
    return opposite_connectors

def find_adjacent_connectors(connector: Connector, connector_db: ConnectorDatabase) -> list[Connector]:
    """
    Find connectors that are adjacent to the given connector.
    :param connector: The connector to find adjacent connectors for.
    :param connector_db: The database of connectors to search in.
    :return: A list of adjacent connectors.
    """

    adjacent_parts = connector.get_adjacent_parts()
    adjacent_connectors = []

    for part in adjacent_parts:
        db_connector = connector_db.get_connector_by_part_code(part.as_string())
        if db_connector:
            adjacent_connectors.append(db_connector)

    return adjacent_connectors

if __name__ == "__main__":
    connector_db = ConnectorDatabase()
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
        print(f"Found connector: {connector.part_code} with part number {connector.part_number}")
    else:
        print("Connector not found.")

    print("Searching for connectors with material 'Z'...")
    connectors = connector_db.get_connectors_by_material("Z")
    if connectors:
        print(f"Found {len(connectors)} connectors with material 'Z':")
        for conn in connectors:
            print(f"- {conn.part_code} with part number {conn.part_number}")

    print("Searching for connectors that are compatible with 'PN-87_51_77_70'...")
    connector = connector_db.get_connector_by_part_number("PN-87_51_77_70")
    if connector:
        compatible_connectors = find_opposite_connectors(connector, connector_db)
        if compatible_connectors:
            print(f"Found {len(compatible_connectors)} compatible connectors for {connector.part_code}:")
            for opp_connector in compatible_connectors:
                print(f"- {opp_connector.part_code} with part number {opp_connector.part_number}")
    else:
        print("Connector not found for compatibility search.")

    print("Searching for connectors that are adjacent to 'PN-87_51_77_70'...")
    if connector:
        adjacent_connectors = find_adjacent_connectors(connector, connector_db)
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