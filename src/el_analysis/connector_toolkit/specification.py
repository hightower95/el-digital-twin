from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Optional
if TYPE_CHECKING:
    from el_analysis.connector_toolkit.property import PropertyValue, ConnectorProperty
from abc import ABC, abstractmethod

class Specification(ABC):

    def __init__(self, specification_name: str):
        self._name = specification_name

    @property
    def connector_type(self) -> str:
        """Returns the type (or specification) of the connector."""
        return self._name
    
    @property
    def connector_family(self) -> str:
        """Alias for connector type."""
        return self.connector_type

    @property
    def aspects(self) -> Dict[str, type[ConnectorProperty]]:
        """Returns the aspects of the specification."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    @property
    def values(self) -> Dict[str, PropertyValue]:
        """Returns the values of the specification aspects."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    @property
    def has_part_code(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")

    @staticmethod
    @abstractmethod
    def can_parse_part_code(part_code: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def get_part_code(self) -> str:
        """
        Abstract method to get the part code.
        This should be implemented in subclasses to provide specific part code logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def get_minified_part_code(self, minify_keying: bool = False) -> str:
        """
        Abstract method to get the minified part code.
        This should be implemented in subclasses to provide specific minification logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def can_connect_to(self, other: 'Specification') -> bool:
        """
        Checks if this specification can connect to another specification.
        This should be implemented in subclasses to define specific connection logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @classmethod
    @abstractmethod
    def from_part_code_string(cls, part_code: str) -> 'Specification':
        raise NotImplementedError("Subclasses must implement this method.")
    

class DefaultSpecification(Specification):
    """
    Default specification for connectors.
    This class can be extended to define specific aspects of the connector.
    """
    def __init__(self, part_code: Optional[str] = None):
        """ Initializes the DefaultSpecification with an optional part code.
        If no part code is provided, it defaults to None.
        """
        super().__init__("DefaultSpecification")
        self._part_code = part_code

    @property
    def aspects(self) -> Dict[str, type[ConnectorProperty]]:
        """Returns the aspects of the specification."""
        return {}

    @property
    def values(self) -> Dict[str, PropertyValue]:
        """Returns the values of the specification aspects."""
        return {}
    
    @property
    def has_part_code(self) -> bool:
        """Returns True if the specification has a part code."""
        return self._part_code is not None

    @staticmethod
    def can_parse_part_code(part_code: str) -> bool:
        return False  # Default implementation, can be overridden in subclasses
    
    
    def get_part_code(self) -> str:
        """
        Returns the part code of the connector.
        This should be implemented in subclasses to provide specific part code logic.
        """
        return self._part_code if self._part_code else "<No Part Code>"
    
    def get_minified_part_code(self, minify_keying: bool = False) -> str:
        """
        Returns the minified part code of the connector.
        This should be implemented in subclasses to provide specific minification logic.
        """
        return self._part_code if self._part_code else "<No Part Code>"

    def can_connect_to(self, other: 'Specification') -> bool:
        """
        Checks if this specification can connect to another specification.
        This should be implemented in subclasses to define specific connection logic.
        """
        return False
    

    @classmethod
    def from_part_code_string(cls, part_code: str) -> 'DefaultSpecification':
        """
        Creates a DefaultSpecification from a part code string.
        This should be implemented in subclasses to provide specific parsing logic.
        """
        return cls(part_code=part_code)