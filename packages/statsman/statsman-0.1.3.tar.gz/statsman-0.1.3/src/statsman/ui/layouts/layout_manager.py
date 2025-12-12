from typing import Tuple, Optional, Dict, List, Any

from .terminal_controller import TerminalController
from .horizontal_layout import HorizontalLayout
from .vertical_layout import VerticalLayout
from .grid_layout import GridLayout
from .content_size_fitter import ContentSizeFitter


class LayoutManager:

    def __init__(self, terminal: TerminalController):
        self.terminal = terminal
        self.width, self.height = terminal.get_size()
        self.layouts: Dict[str, Any] = {}
        self.size_fitter = ContentSizeFitter()

    def create_horizontal_layout(self, name: str, spacing: int = 1, padding: int = 0,
                                justification: str = "start") -> HorizontalLayout:
        layout = HorizontalLayout(spacing, padding, justification)
        self.layouts[name] = layout
        return layout

    def create_vertical_layout(self, name: str, spacing: int = 1, padding: int = 0,
                              justification: str = "start") -> VerticalLayout:
        layout = VerticalLayout(spacing, padding, justification)
        self.layouts[name] = layout
        return layout

    def create_grid_layout(self, name: str, rows: int = 1, cols: int = 1,
                          spacing: int = 1, padding: int = 0) -> GridLayout:
        layout = GridLayout(rows, cols, spacing, padding)
        self.layouts[name] = layout
        return layout

    def calculate_layout(self, name: str, x: int, y: int, width: int, height: int):
        if name in self.layouts:
            self.layouts[name].calculate_layout(x, y, width, height)

    def get_child_bounds(self, layout_name: str, child_index: int) -> Tuple[int, int, int, int]:
        if layout_name in self.layouts:
            layout = self.layouts[layout_name]
            if child_index < len(layout.children):
                _, x, y, w, h = layout.children[child_index]
                return (x, y, w, h)
        return (0, 0, 0, 0)

    def update_size(self):
        self.width, self.height = self.terminal.get_size()

    def get_size(self) -> Tuple[int, int]:
        return (self.width, self.height)