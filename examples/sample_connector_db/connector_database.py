
from connector_part import Connector, ConnectorPart

class ConnectorDatabase:
    """
    A class to manage a database of connectors.
    This class is responsible for loading, saving, and managing connector data.
    """

    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.connectors: list[Connector] = []
        self._load_connectors()

    def _load_connectors(self):
        """
        Load connectors from the database file.
        """
        try:
            with open(self.db_path, 'r') as file:
                file.readline()  # Skip header line
                connector_lines = file.readlines()
                for line in connector_lines:
                    if line.strip():
                        part_type, part_number = line.strip().split(',')
                        # print(f"Loading connector with part type: {part_type} and part number: {part_number.strip()}")
                        part = ConnectorPart.from_part_code_string(part_type)
                        connector = Connector(part=part, part_number=part_number.strip())
                        self.connectors.append(connector)
        except FileNotFoundError:
            self.connectors = []

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
    
    def get_connectors_by_part_type(self, part_type: str):
        """
        Get connectors by their part type.
        :param part_type: The part type of the connectors.
        :return: A list of connectors that match the part type.
        """
        return [connector for connector in self.connectors if connector.part_type == part_type or connector.part.minified_part_type == part_type]
    
    def get_connector_by_part_type(self, part_type: str):
        """
        Get a connector by its part type.
        :param part_type: The part type of the connector.
        :return: The connector if found, None otherwise.
        """
        for connector in self.connectors:
            if connector.part_type == part_type or connector.part.minified_part_type == part_type:
                return connector
        return None
    
    def get_connectors_by_material(self, material: str):
        """
        Get all connectors that match a specific material.
        :param material: The material to filter connectors by.
        :return: A list of connectors that match the material.
        """
        return [connector for connector in self.connectors if connector.part.material.short_name == material]
    
    
def find_opposite_connectors(connector: Connector, connector_db: ConnectorDatabase) -> list[Connector]:
    """
    Find connectors that are compatible with the given connector.
    :param connector: The connector to find opposites for.
    :param connector_db: The database of connectors to search in.
    :return: A list of compatible connectors.
    """
    compatible_parts = connector.get_compatible_parts()
    opposite_connectors = []
    
    for part in compatible_parts:
        db_connector = connector_db.get_connector_by_part_type(part.as_string())
        if db_connector:
            opposite_connectors.append(db_connector)
    
    return opposite_connectors
    
    

if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "connectors.csv")
    connector_db = ConnectorDatabase(db_path)
    print(f"Loaded {len(connector_db.connectors)} connectors from {db_path}")

    print("Searching for connector with part number 'PN-87_51_77_70'...")
    connector = connector_db.get_connector_by_part_number("PN-87_51_77_70")
    if connector:
        print(f"Found connector: {connector.part_type} with part number {connector.part_number}")
    else:
        print("Connector not found.")

    print("Searching for connector with part type '3-W-M-F'...")
    connector = connector_db.get_connector_by_part_type("3-W-M-F")
    if connector:
        print(f"Found connector: {connector.part_type} with part number {connector.part_number}")
    else:
        print("Connector not found.")

    print("Searching for connectors with material 'Z'...")
    connectors = connector_db.get_connectors_by_material("Z")
    if connectors:
        print(f"Found {len(connectors)} connectors with material 'Z':")
        for conn in connectors:
            print(f"- {conn.part_type} with part number {conn.part_number}")


    connector = connector_db.get_connector_by_part_number("PN-87_51_77_70")
    if connector:
        compatible_connectors = find_opposite_connectors(connector, connector_db)
        if compatible_connectors:
            print(f"Found {len(compatible_connectors)} compatible connectors for {connector.part_type}:")
            for opp_connector in compatible_connectors:
                print(f"- {opp_connector.part_type} with part number {opp_connector.part_number}")
