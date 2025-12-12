import sys
from typing import Dict, List, Optional, Any
from ..layouts import TerminalController, DrawingPrimitives, LayoutElement


class CPUCores(LayoutElement):

    def __init__(self, terminal: TerminalController, drawing: DrawingPrimitives,
                 min_width: int = 15, min_height: int = 5, preferred_width: int = 30,
                 preferred_height: int = 8, flexible_width: int = 1, flexible_height: int = 0,
                 anchor: str = "top-left", justification: str = "start"):
        super().__init__(min_width, min_height, preferred_width, preferred_height,
                        flexible_width, flexible_height, anchor, justification)
        self.terminal = terminal
        self.drawing = drawing

    def render(self, x: int, y: int, width: int, height: int, cpu_info: Any):

        width, height = max(15, width), max(5, height)

        self.drawing.draw_box(x, y, width, height, "CPU Cores", "blue")

        if not cpu_info.percent_per_core:
            self.drawing.draw_centered_text(x + width//2, y + height//2, "No core data", "white")
            return



        chart_x = x + 2
        chart_y = y + 2
        chart_width = width - 4
        chart_height = height - 4

        if chart_height <= 0 or chart_width <= 0:
            self.drawing.draw_centered_text(x + width//2, y + height//2, "Too small", "white")
            return

        total_cores = len(cpu_info.percent_per_core)
        max_cores = min(total_cores, chart_width // 3)

        if max_cores == 0:
            self.drawing.draw_centered_text(x + width//2, y + height//2, "Too narrow", "white")
            return

        core_data = {}
        for i in range(max_cores):
            core_data[f"C{i}"] = cpu_info.percent_per_core[i]

        self.drawing.draw_vertical_bars(chart_x, chart_y, chart_width, chart_height, core_data, "blue")

        if height > 5:
            usage_text = f"CPU: {cpu_info.percent:.1f}%" if width > 20 else f"{cpu_info.percent:.0f}%"
            text_y = y + height - 2
            self.drawing.draw_centered_text(x + width//2, text_y, usage_text, "bright_blue")