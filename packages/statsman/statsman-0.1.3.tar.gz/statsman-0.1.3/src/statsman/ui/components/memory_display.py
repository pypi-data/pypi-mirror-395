import sys
from typing import Dict, List, Optional, Any
from ..layouts import TerminalController, DrawingPrimitives, LayoutElement


class MemoryDisplay(LayoutElement):

    def __init__(self, terminal: TerminalController, drawing: DrawingPrimitives,
                 min_width: int = 20, min_height: int = 5, preferred_width: int = 30,
                 preferred_height: int = 8, flexible_width: int = 1, flexible_height: int = 0,
                 anchor: str = "top-left", justification: str = "start"):
        super().__init__(min_width, min_height, preferred_width, preferred_height,
                        flexible_width, flexible_height, anchor, justification)
        self.terminal = terminal
        self.drawing = drawing

    def render(self, x: int, y: int, width: int, height: int, mem_info: Any):

        width, height = max(20, width), max(5, height)

        self.drawing.draw_box(x, y, width, height, "Memory", "green")

        used_gb = mem_info.used / (1024**3)
        total_gb = mem_info.total / (1024**3)
        available_gb = mem_info.available / (1024**3)


        content_width = width - 4
        content_height = height - 2
        current_y = y + 1



        elements_count = 3 if width < 25 or height < 10 else 4
        available_lines = height - 2

        progress_bar_lines = 4 if elements_count > 3 else 0
        effective_lines = available_lines - progress_bar_lines
        spacing = max(1, effective_lines // (elements_count - 1)) if elements_count > 1 else available_lines

        if width < 25 or height < 6:

            elements = [
                (f"U:{used_gb:.1f}G", "red"),
                (f"A:{available_gb:.1f}G", "green"),
                ("", "green")
            ]
        else:

            elements = [
                (f"Used: {used_gb:.1f}GB", "red"),
                (f"Available: {available_gb:.1f}GB", "green"),
                (f"Total: {total_gb:.1f}GB", "blue"),
                ("", "green")
            ]

        for i, (text, color) in enumerate(elements):
            element_y = y + 1 + (i * spacing)
            if element_y >= y + height - 1:
                break

            if text:
                self.drawing.draw_at(x + 2, element_y, text, color)
            else:
                bar_text = "Memory" if len(elements) > 3 else ""
                self.drawing.draw_progress_bar(x + 2, element_y, content_width, mem_info.percent, bar_text, "green")