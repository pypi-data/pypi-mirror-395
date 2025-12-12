import sys
from typing import Dict, List, Optional, Any
from ..layouts import TerminalController, DrawingPrimitives, LayoutElement


class ProcessList(LayoutElement):

    def __init__(self, terminal: TerminalController, drawing: DrawingPrimitives,
                 min_width: int = 30, min_height: int = 8, preferred_width: int = 80,
                 preferred_height: int = 15, flexible_width: int = 1, flexible_height: int = 1,
                 anchor: str = "top-left", justification: str = "start"):
        super().__init__(min_width, min_height, preferred_width, preferred_height,
                        flexible_width, flexible_height, anchor, justification)
        self.terminal = terminal
        self.drawing = drawing
        self.sort_by = "cpu"

    def render(self, x: int, y: int, width: int, height: int, processes: List[Any]):

        width, height = max(30, width), max(5, height)

        self.drawing.draw_box(x, y, width, height, "Top Processes", "magenta")


        available_lines = height - 3
        limit = max(1, min(available_lines, 20))


        if self.sort_by == "memory":
            procs = sorted(processes, key=lambda p: p.memory_percent, reverse=True)
        else:
            procs = sorted(processes, key=lambda p: p.cpu_percent, reverse=True)


        content_x = x + 2
        content_width = width - 4
        current_y = y + 1


        if width < 40:

            header = "PID PROC  C% M%"
            separator = "=" * min(content_width, len(header))
            if current_y < y + height - 1:
                self.drawing.draw_at(content_x, current_y, header, "white")
                current_y += 1
            if current_y < y + height - 1:
                self.drawing.draw_at(content_x, current_y, separator, "white")
                current_y += 1

            for i, proc in enumerate(procs[:limit]):
                if current_y >= y + height - 1:
                    break
                name = (proc.name[:4] + ".") if len(proc.name) > 5 else proc.name.ljust(5)
                line = f"{proc.pid:<4} {name} {proc.cpu_percent:<2.0f} {proc.memory_percent:<2.0f}"

                if len(line) > content_width:
                    line = line[:content_width]
                self.drawing.draw_at(content_x, current_y, line, "white")
                current_y += 1
        else:

            header = "PID     PROCESS                   CPU%        MEM%"
            separator = "=" * min(content_width, len(header))
            if current_y < y + height - 1:
                self.drawing.draw_at(content_x, current_y, header, "white")
                current_y += 1
            if current_y < y + height - 1:
                self.drawing.draw_at(content_x, current_y, separator, "white")
                current_y += 1

            for i, proc in enumerate(procs[:limit]):
                if current_y >= y + height - 1:
                    break
                name_width = max(10, (content_width - 25) // 2)
                name = (proc.name[:name_width-2] + "..") if len(proc.name) > name_width else proc.name.ljust(name_width)
                line = f"{proc.pid:<6} {name} {proc.cpu_percent:<5.1f} {proc.memory_percent:<5.1f}"

                if len(line) > content_width:
                    line = line[:content_width]
                self.drawing.draw_at(content_x, current_y, line, "white")
                current_y += 1

    def set_sort_method(self, sort_by: str):
        if sort_by in ("cpu", "memory"):
            self.sort_by = sort_by