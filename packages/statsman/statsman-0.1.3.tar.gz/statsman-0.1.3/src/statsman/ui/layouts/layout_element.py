from typing import Tuple, Optional, Dict, List, Any


class LayoutElement:

    def __init__(self, min_width: int = 0, min_height: int = 0, preferred_width: int = 0,
                 preferred_height: int = 0, flexible_width: int = 0, flexible_height: int = 0,
                 anchor: str = "top-left", justification: str = "start"):
        self.min_width = min_width
        self.min_height = min_height
        self.preferred_width = preferred_width
        self.preferred_height = preferred_height
        self.flexible_width = flexible_width
        self.flexible_height = flexible_height
        self.anchor = anchor  
        self.justification = justification  

    def get_preferred_size(self) -> Tuple[int, int]:
        return (self.preferred_width, self.preferred_height)

    def get_min_size(self) -> Tuple[int, int]:
        return (self.min_width, self.min_height)

    def get_flexible_size(self) -> Tuple[int, int]:
        return (self.flexible_width, self.flexible_height)