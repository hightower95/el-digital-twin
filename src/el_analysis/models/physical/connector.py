from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from el_analysis.models.physical.part import Part 

from typing import Optional



class Connector:
    def __init__(self, part: Optional[Part]=None):
        from el_analysis.models.physical.part import Part
        self.part = part if part else Part("","")

    @property
    def part_number(self) -> Optional[str]:
        return self.part.part_number if self.part else None
    
    @property
    def part_type(self) -> Optional[str]:
        return self.part.part_type if self.part else None
    
    @staticmethod
    def minify_part_type(part_type: str, minify_keying: bool = False) -> str:
        """Minify part type by removing spaces and converting to lowercase."""
        return part_type
    
    def get_minified_part_type(self, include_keying: bool = False) -> Optional[str]:
        return Connector.minify_part_type(self.part_type, include_keying) if self.part and self.part_type else None