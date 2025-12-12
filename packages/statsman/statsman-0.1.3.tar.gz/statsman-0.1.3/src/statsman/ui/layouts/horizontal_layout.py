from typing import Tuple, Optional, Dict, List, Any

from .layout_element import LayoutElement


class HorizontalLayout:

    def __init__(self, spacing: int = 1, padding: int = 0, justification: str = "start"):
        self.spacing = spacing
        self.padding = padding
        self.justification = justification
        self.children: List[Tuple[LayoutElement, int, int, int, int]] = []  

    def add_child(self, element: LayoutElement):
        self.children.append((element, 0, 0, 0, 0))

    def calculate_layout(self, x: int, y: int, width: int, height: int):
        if not self.children:
            return

        
        available_width = width - 2 * self.padding
        available_height = height - 2 * self.padding

        
        total_preferred_width = 0
        total_flexible_width = 0
        min_heights = []

        for element, _, _, _, _ in self.children:
            pref_w, pref_h = element.get_preferred_size()
            flex_w, _ = element.get_flexible_size()
            min_w, min_h = element.get_min_size()

            total_preferred_width += pref_w
            total_flexible_width += flex_w
            min_heights.append(min_h)

        
        total_spacing = self.spacing * (len(self.children) - 1)
        total_preferred_width += total_spacing

        
        remaining_width = available_width - total_preferred_width
        extra_width_per_flexible = remaining_width / total_flexible_width if total_flexible_width > 0 else 0

        current_x = x + self.padding
        max_height = min(available_height, max(min_heights) if min_heights else available_height)

        
        spacing = self.spacing  
        if self.justification == "start":
            current_x = x + self.padding
        elif self.justification == "center":
            total_width = sum(w for _, _, _, w, _ in self.children) + total_spacing
            current_x = x + self.padding + (available_width - total_width) // 2
        elif self.justification == "end":
            total_width = sum(w for _, _, _, w, _ in self.children) + total_spacing
            current_x = x + width - self.padding - total_width
        elif self.justification == "space-between":
            if len(self.children) > 1:
                total_width = sum(w for _, _, _, w, _ in self.children)
                spacing = (available_width - total_width) // (len(self.children) - 1)
                current_x = x + self.padding
            else:
                current_x = x + self.padding
        elif self.justification == "space-around":
            if len(self.children) > 0:
                total_width = sum(w for _, _, _, w, _ in self.children)
                total_spacing = (available_width - total_width) // len(self.children)
                spacing = total_spacing
                current_x = x + self.padding + total_spacing // 2
            else:
                current_x = x + self.padding
        elif self.justification == "space-evenly":
            if len(self.children) > 0:
                total_width = sum(w for _, _, _, w, _ in self.children)
                total_spacing = (available_width - total_width) // (len(self.children) + 1)
                spacing = total_spacing
                current_x = x + self.padding + total_spacing
            else:
                current_x = x + self.padding
        else:
            current_x = x + self.padding

        
        for i, (element, _, _, _, _) in enumerate(self.children):
            pref_w, pref_h = element.get_preferred_size()
            flex_w, flex_h = element.get_flexible_size()
            min_w, min_h = element.get_min_size()

            
            final_width = pref_w
            if flex_w > 0 and extra_width_per_flexible > 0:
                final_width += int(flex_w * extra_width_per_flexible)
            final_width = max(min_w, min(final_width, available_width))

            
            final_height = min(max_height, max(min_h, pref_h))

            
            child_x, child_y = self._calculate_anchor_position(
                current_x, y + self.padding, final_width, final_height,
                available_height, element.anchor
            )

            
            self.children[i] = (element, child_x, child_y, final_width, final_height)

            
            current_x += final_width + spacing

    def _calculate_anchor_position(self, x: int, y: int, w: int, h: int,
                                  container_height: int, anchor: str) -> Tuple[int, int]:
        if anchor == "top-left":
            return x, y
        elif anchor == "top-center":
            return x, y
        elif anchor == "top-right":
            return x, y
        elif anchor == "center-left":
            return x, y + (container_height - h) // 2
        elif anchor == "center":
            return x, y + (container_height - h) // 2
        elif anchor == "center-right":
            return x, y + (container_height - h) // 2
        elif anchor == "bottom-left":
            return x, y + container_height - h
        elif anchor == "bottom-center":
            return x, y + container_height - h
        elif anchor == "bottom-right":
            return x, y + container_height - h
        else:
            return x, y