from typing import Tuple, Optional, Dict, List, Any

from .layout_element import LayoutElement


class VerticalLayout:

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

        
        total_preferred_height = 0
        total_flexible_height = 0
        min_widths = []

        for element, _, _, _, _ in self.children:
            pref_w, pref_h = element.get_preferred_size()
            _, flex_h = element.get_flexible_size()
            min_w, min_h = element.get_min_size()

            total_preferred_height += pref_h
            total_flexible_height += flex_h
            min_widths.append(min_w)

        
        total_spacing = self.spacing * (len(self.children) - 1)
        total_preferred_height += total_spacing

        
        remaining_height = available_height - total_preferred_height
        extra_height_per_flexible = remaining_height / total_flexible_height if total_flexible_height > 0 else 0

        current_y = y + self.padding
        max_width = min(available_width, max(min_widths) if min_widths else available_width)

        
        spacing = self.spacing  
        if self.justification == "start":
            current_y = y + self.padding
        elif self.justification == "center":
            total_height = sum(h for _, _, _, _, h in self.children) + total_spacing
            current_y = y + self.padding + (available_height - total_height) // 2
        elif self.justification == "end":
            total_height = sum(h for _, _, _, _, h in self.children) + total_spacing
            current_y = y + height - self.padding - total_height
        elif self.justification == "space-between":
            if len(self.children) > 1:
                total_height = sum(h for _, _, _, _, h in self.children)
                spacing = (available_height - total_height) // (len(self.children) - 1)
                current_y = y + self.padding
            else:
                current_y = y + self.padding
        elif self.justification == "space-around":
            if len(self.children) > 0:
                total_height = sum(h for _, _, _, _, h in self.children)
                total_spacing = (available_height - total_height) // len(self.children)
                spacing = total_spacing
                current_y = y + self.padding + total_spacing // 2
            else:
                current_y = y + self.padding
        elif self.justification == "space-evenly":
            if len(self.children) > 0:
                total_height = sum(h for _, _, _, _, h in self.children)
                total_spacing = (available_height - total_height) // (len(self.children) + 1)
                spacing = total_spacing
                current_y = y + self.padding + total_spacing
            else:
                current_y = y + self.padding
        else:
            current_y = y + self.padding

        
        for i, (element, _, _, _, _) in enumerate(self.children):
            pref_w, pref_h = element.get_preferred_size()
            flex_w, flex_h = element.get_flexible_size()
            min_w, min_h = element.get_min_size()

            
            final_height = pref_h
            if flex_h > 0 and extra_height_per_flexible > 0:
                final_height += int(flex_h * extra_height_per_flexible)
            final_height = max(min_h, min(final_height, available_height))

            
            final_width = min(max_width, max(min_w, pref_w))

            
            child_x, child_y = self._calculate_anchor_position(
                x + self.padding, current_y, final_width, final_height,
                available_width, element.anchor
            )

            
            self.children[i] = (element, child_x, child_y, final_width, final_height)

            
            current_y += final_height + spacing

    def _calculate_anchor_position(self, x: int, y: int, w: int, h: int,
                                  container_width: int, anchor: str) -> Tuple[int, int]:
        if anchor == "top-left":
            return x, y
        elif anchor == "top-center":
            return x + (container_width - w) // 2, y
        elif anchor == "top-right":
            return x + container_width - w, y
        elif anchor == "center-left":
            return x, y
        elif anchor == "center":
            return x + (container_width - w) // 2, y
        elif anchor == "center-right":
            return x + container_width - w, y
        elif anchor == "bottom-left":
            return x, y
        elif anchor == "bottom-center":
            return x + (container_width - w) // 2, y
        elif anchor == "bottom-right":
            return x + container_width - w, y
        else:
            return x, y