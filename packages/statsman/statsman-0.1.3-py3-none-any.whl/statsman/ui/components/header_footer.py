import sys
from typing import Dict, List, Optional, Any
from ..layouts import TerminalController, DrawingPrimitives, LayoutElement


class HeaderFooter(LayoutElement):

    def __init__(self, terminal: TerminalController, drawing: DrawingPrimitives,
                 min_width: int = 20, min_height: int = 3, preferred_width: int = 80,
                 preferred_height: int = 3, flexible_width: int = 1, flexible_height: int = 0,
                 anchor: str = "top-left", justification: str = "start"):
        super().__init__(min_width, min_height, preferred_width, preferred_height,
                        flexible_width, flexible_height, anchor, justification)
        self.terminal = terminal
        self.drawing = drawing

    def render_header(self, x: int, y: int, width: int, height: int):

        if width < 30:
            title = "SM"
        elif width < 50:
            title = "StatsMan"
        else:
            title = "StatsMan - System Monitor"

        self.drawing.draw_box(x, y, width, height, title, "bright_blue")

        panel_text = "Real-time System Metrics"
        self.drawing.draw_centered_text(x + width//2, y + height//2, panel_text, "bright_blue")

    def render_footer(self, x: int, y: int, width: int, height: int):

        if width < 25:
            help_text = "q:quit p:pause"
        elif width < 40:
            help_text = "q:quit p:pause c:cpu m:mem"
        elif width < 60:
            help_text = "q:quit │ p:pause │ c:cpu │ m:mem"
        else:
            help_text = "q:quit │ p:pause │ c:sort CPU │ m:sort MEM"

        self.drawing.draw_box(x, y, width, height, "", "bright_black")
        self.drawing.draw_centered_text(x + width//2, y + height//2, help_text, "bright_cyan")