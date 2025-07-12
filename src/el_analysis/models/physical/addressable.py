from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis import Address

from typing import Optional


class Addressable:
    """Base class for addressable objects in the BW Analysis module."""

    def __init__(self, address: Address, name: str = "Unnamed"):
        self.address = address
        self.name = name

    def search_by_address(self, address: Address, create_if_not_exists: bool) -> Optional[Addressable]:
        raise NotImplementedError("This method should be implemented in subclasses.")