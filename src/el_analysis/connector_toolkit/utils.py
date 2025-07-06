
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from el_analysis.models.physical.connector import Connector

from el_analysis import config, logging
from typing import Dict

__connector_cache: Dict[str, Connector] = {}

def get_connector_from_part_number(part_number: str):
    """
    Retrieves a connector by its part number.
    
    Args:
        part_number (str): The part number of the connector to retrieve.
    
    Returns:
        Connector: The connector with the specified part number.
    
    Raises:
        ValueError: If no connector with the specified part number exists.
    """
    from el_analysis.models.physical.connector import Connector

    if not part_number:
        raise ValueError("Part number cannot be empty.")
    
    connector = __connector_cache.get(part_number)
    if connector:
        return connector

    connector = Connector()
    connector.part.part_number = part_number    

    if not connector:
        logging.error(f"Connector with part number {part_number} not found.")
        raise ValueError(f"Connector with part number {part_number} not found.")
    
    return connector