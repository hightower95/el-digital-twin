from typing import TYPE_CHECKING, Optional
from el_analysis.connector_toolkit.specification import Specification as ConnectorSpecification, DefaultSpecification

class Connector:
    """Base class for connector variants."""

    def __init__(self, component: Optional[ConnectorSpecification], part_number: Optional[str] = None):
        if component:
            self.component = component
        else:
            self.component = DefaultSpecification()
        self.component: Optional[ConnectorSpecification] = component
        self.part_number: Optional[str] = part_number
    
    @property
    def part_code(self) -> str:
        """Returns the part code of the connector."""
        return self.component.get_part_code() if self.component else "<No Part Code>"
    
    @property
    def minified_part_code(self) -> str:
        """Returns the minified part code of the connector."""
        return self.component.get_minified_part_code() if self.component else "<No Minified Part Code>"
    
    def get_minified_part_code(self, include_keying: bool = False) -> str:
        """Returns the minified part code, optionally including keying."""
        return self.component.get_minified_part_code(include_keying) if self.component else "<No Minified Part Code>"
    
    def __repr__(self) -> str:
        """Returns a string representation of the connector."""
        return f"Connector(part_code={self.part_code}, part_number={self.part_number}, specification={self.component.SPECIFICATION_NAME if self.component else 'None'})"

