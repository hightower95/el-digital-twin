
from abc import ABC, abstractmethod
from el_analysis.models.physical.connector import Connector
from typing import Callable, Optional

class ConnectorDBInterface(ABC):
    def __init__(self, connector_db):
        self.connector_db = connector_db

    @abstractmethod
    def get_connector_by_part_number(self, part_number: str) -> Optional[Connector]:
        pass

    @abstractmethod
    def get_connectors_by_part_type(self, part_type: str) -> list[Connector]:
        pass
    
    @abstractmethod
    def get_connector_by_part_type(self, part_type: str) -> Optional[Connector]:
        pass

    @abstractmethod
    def get_connectors_by_material(self, material: str) -> list[Connector]:
        pass

    @abstractmethod
    def get_connectors_by_gender(self, gender: str) -> list[Connector]:
        pass

    @abstractmethod
    def get_connectors_by_lambda(self, filter: Callable) -> list[Connector]:
        pass
    
    @abstractmethod
    def get_opposite_connector(self, connector: Connector) -> Optional[Connector]:
        pass
  