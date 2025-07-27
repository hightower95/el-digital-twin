import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Now we can import from the adjacent folder
from sample_connector_db.connector_database import ConnectorDatabase, Connector
from sample_connector_db.connector_part import Variants, Materials, Sizes, Genders

connector_db = ConnectorDatabase()

def get_connectors(quantity=5) -> list[Connector]:
    """Returns a list of all connectors."""
    if quantity is None or quantity <= 0:
        return connector_db.connectors
    
    connectors_selected = []

    # max loops
    max_loops = 1000

    while len(connectors_selected) < quantity:
        if max_loops <= 0:
            raise ValueError("Could not find enough connectors that are not mateable with existing connectors.")
        max_loops -= 1
        # Get a random connector
        connector = connector_db.get_random_connector()
        # check connector not in connectors_selected
        if connector in connectors_selected:
            continue

        if not connector:
            continue

        # connector should not be mateable with any existing connector
        if any(connector.can_connect_to(existing_connector) or connector.minified_part_type == existing_connector.minified_part_type for existing_connector in connectors_selected):
            continue


        
        connectors_selected.append(connector)

    return connectors_selected

chosen_connectors = get_connectors(7)
for connector in chosen_connectors:
    print(f"Connector Part Type: {connector.part_type}, Connector Part Number: {connector.part_number}")
