import sys
from typing import Dict, List, Optional, Any
from ..layouts import TerminalController, DrawingPrimitives, LayoutElement


class SystemOverview(LayoutElement):

    def __init__(self, terminal: TerminalController, drawing: DrawingPrimitives,
                 min_width: int = 20, min_height: int = 5, preferred_width: int = 40,
                 preferred_height: int = 8, flexible_width: int = 1, flexible_height: int = 0,
                 anchor: str = "top-left", justification: str = "start"):
        super().__init__(min_width, min_height, preferred_width, preferred_height,
                        flexible_width, flexible_height, anchor, justification)
        self.terminal = terminal
        self.drawing = drawing

    def render(self, x: int, y: int, width: int, height: int,
                  cpu_info: Any, mem_info: Any, disk_info: Any):

        width, height = max(20, width), max(5, height)


        self.drawing.draw_box(x, y, width, height, "System", "cyan")



        available_width = width - 4
        gauge_width = max(10, available_width // 3)
        spacing = 2
        gauge_y = y + 2

        total_width = 3 * gauge_width + 2 * spacing
        if total_width > available_width:
            gauge_width = max(10, (available_width - 2 * spacing) // 3)
            total_width = 3 * gauge_width + 2 * spacing

        start_x = x + 2 + (available_width - total_width) // 2

        for i in range(3):
            gauge_x = start_x + i * (gauge_width + spacing)
            for line in range(4):
                clear_y = gauge_y + line
                if clear_y < y + height - 1:
                    clear_width = min(gauge_width, x + width - gauge_x - 1)
                    if clear_width > 0:
                        self.terminal.move_cursor(gauge_x, clear_y)
                        sys.stdout.write(" " * clear_width)

        self.drawing.draw_progress_bar(start_x, gauge_y, gauge_width, cpu_info.percent, "CPU", "red")
        self.drawing.draw_progress_bar(start_x + gauge_width + spacing, gauge_y, gauge_width, mem_info.percent, "MEM", "green")
        self.drawing.draw_progress_bar(start_x + 2*(gauge_width + spacing), gauge_y, gauge_width, disk_info.percent, "DSK", "yellow")