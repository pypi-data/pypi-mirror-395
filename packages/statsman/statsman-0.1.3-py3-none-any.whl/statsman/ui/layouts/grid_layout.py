from typing import Tuple, Optional, Dict, List, Any

from .layout_element import LayoutElement


class GridLayout:

    def __init__(self, rows: int = 1, cols: int = 1, spacing: int = 1, padding: int = 0,
                 justification: str = "start", anchor: str = "top-left"):
        self.rows = rows
        self.cols = cols
        self.spacing = spacing
        self.padding = padding
        self.justification = justification
        self.anchor = anchor
        self.children: List[Tuple[LayoutElement, int, int, int, int]] = []

    def add_child(self, element: LayoutElement):
        self.children.append((element, 0, 0, 0, 0))

    def calculate_layout(self, x: int, y: int, width: int, height: int):
        if not self.children:
            return

        
        available_width = width - 2 * self.padding
        available_height = height - 2 * self.padding

        
        cell_width = (available_width - self.spacing * (self.cols - 1)) // self.cols
        cell_height = (available_height - self.spacing * (self.rows - 1)) // self.rows

        
        for i, (element, _, _, _, _) in enumerate(self.children):
            if i >= self.rows * self.cols:
                break

            row = i // self.cols
            col = i % self.cols

            cell_x = x + self.padding + col * (cell_width + self.spacing)
            cell_y = y + self.padding + row * (cell_height + self.spacing)

            
            min_w, min_h = element.get_min_size()
            pref_w, pref_h = element.get_preferred_size()

            
            final_width = min(cell_width, max(min_w, pref_w))
            final_height = min(cell_height, max(min_h, pref_h))

            
            child_x, child_y = self._calculate_anchor_position(
                cell_x, cell_y, final_width, final_height,
                cell_width, cell_height, element.anchor
            )

            
            self.children[i] = (element, child_x, child_y, final_width, final_height)

    def _calculate_anchor_position(self, cell_x: int, cell_y: int, w: int, h: int,
                                  cell_w: int, cell_h: int, anchor: str) -> Tuple[int, int]:
        if anchor == "top-left":
            return cell_x, cell_y
        elif anchor == "top-center":
            return cell_x + (cell_w - w) // 2, cell_y
        elif anchor == "top-right":
            return cell_x + cell_w - w, cell_y
        elif anchor == "center-left":
            return cell_x, cell_y + (cell_h - h) // 2
        elif anchor == "center":
            return cell_x + (cell_w - w) // 2, cell_y + (cell_h - h) // 2
        elif anchor == "center-right":
            return cell_x + cell_w - w, cell_y + (cell_h - h) // 2
        elif anchor == "bottom-left":
            return cell_x, cell_y + cell_h - h
        elif anchor == "bottom-center":
            return cell_x + (cell_w - w) // 2, cell_y + cell_h - h
        elif anchor == "bottom-right":
            return cell_x + cell_w - w, cell_y + cell_h - h
        else:
            return cell_x, cell_y