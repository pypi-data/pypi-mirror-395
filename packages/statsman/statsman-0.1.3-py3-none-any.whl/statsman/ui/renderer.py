import sys
import time
import signal
import threading
from typing import Optional
import threading

from .layouts import (TerminalController, LayoutManager, DrawingPrimitives,
                       HorizontalLayout, VerticalLayout, GridLayout, ContentSizeFitter)
from .components import SystemOverview, CPUCores, MemoryDisplay, NetworkDisplay, ProcessList, HeaderFooter


class StatsManRenderer:

    def __init__(self, no_color: bool = False, bg_color: str = "black"):
        self.terminal = TerminalController(no_color)
        self.layout_manager = LayoutManager(self.terminal)
        self.bg_color = bg_color
        self.sort_processes_by = "cpu"
        self.running = False
        self._needs_full_redraw = False

        self.drawing = DrawingPrimitives(self.terminal)

        
        self.system_overview = SystemOverview(self.terminal, self.drawing)
        self.cpu_cores = CPUCores(self.terminal, self.drawing)
        self.memory_display = MemoryDisplay(self.terminal, self.drawing)
        self.network_display = NetworkDisplay(self.terminal, self.drawing)
        self.process_list = ProcessList(self.terminal, self.drawing)
        self.header_footer = HeaderFooter(self.terminal, self.drawing)



        
        try:
            from ..system_monitor import SystemMonitor
            self.monitor = SystemMonitor(history_size=120)
        except:
            self.monitor = None
    
    def initialize(self):
        self.terminal.initialize(self.bg_color)
        
        import time
        time.sleep(0.01)  
        self.layout_manager.update_size()
        
        width, height = self.layout_manager.get_size()
        self._last_width, self._last_height = width, height
        self.running = True

    def cleanup(self):
        self.running = False
        self.terminal.cleanup()

    def render(self):
        
        self.layout_manager.update_size()
        width, height = self.layout_manager.get_size()

        
        if not hasattr(self, '_last_width'):
            self._last_width, self._last_height = width, height
            self._needs_full_redraw = False

        
        size_changed = (width != self._last_width or height != self._last_height)

        if size_changed:
            
            self._last_width, self._last_height = width, height
            
            self._needs_full_redraw = True
        elif self._needs_full_redraw:
            
            pass

        
        if self._needs_full_redraw or not hasattr(self, '_rendered_once'):
            self.terminal.clear()
            
            time.sleep(0.01)
            self._rendered_once = True
            self._needs_full_redraw = False

        
        if width < 70 or height < 20:
            
            self.drawing.draw_centered_text(width // 2, height // 2,
                                           "Terminal too small. Please resize to at least 70x20.",
                                           "red")
            sys.stdout.flush()
            return

        
        aspect_ratio = width / height
        if aspect_ratio < 1.5 or aspect_ratio > 4.0:
            
            self.drawing.draw_centered_text(width // 2, height // 2,
                                           "Terminal aspect ratio too extreme. Please resize for better proportions.",
                                           "red")
            sys.stdout.flush()
            return

        
        if self.monitor:
            self.monitor.update_history()

        
        header_h, footer_h = 3, 3
        content_h = height - header_h - footer_h - 1

        
        self.header_footer.render_header(1, 1, width, header_h)

        
        content_y = header_h + 1

        
        section_padding = 1

        
        if height < 20:
            
            grid_rows = 1
            grid_cols = 2
            show_processes = True
            panels = ["system", "cpu"]
        else:
            
            grid_rows = 2
            grid_cols = 2
            show_processes = True
            panels = ["system", "cpu", "memory", "network"]

        
        grid_width = width - 2  
        grid_height = content_h - section_padding  

        if show_processes:
            
            processes_height = max(5, grid_height // 5)  
            grid_height = grid_height - processes_height - section_padding

        
        total_spacing_width = (grid_cols - 1) * section_padding
        total_spacing_height = (grid_rows - 1) * section_padding
        cell_width = (grid_width - total_spacing_width) // grid_cols
        cell_height = (grid_height - total_spacing_height) // grid_rows

        

        
        panel_grid = {
            "system": (0, 0),
            "cpu": (0, 1),
            "memory": (1, 0),
            "network": (1, 1)
        }

        
        if self.monitor:
            for panel_name in panels:
                if panel_name in panel_grid:
                    row, col = panel_grid[panel_name]

                    
                    panel_x = 1 + col * (cell_width + section_padding)
                    panel_y = content_y + section_padding + row * (cell_height + section_padding)
                    panel_w = cell_width
                    panel_h = cell_height

                    
                    if panel_y + panel_h > height - footer_h:
                        panel_h = max(5, height - footer_h - panel_y)

                    
                    if panel_name == "system":
                        cpu_info = self.monitor.get_cpu_info()
                        mem_info = self.monitor.get_memory_info()
                        disk_info = self.monitor.get_disk_info()
                        self.system_overview.render(panel_x, panel_y, panel_w, panel_h, cpu_info, mem_info, disk_info)
                    elif panel_name == "cpu":
                        cpu_info = self.monitor.get_cpu_info()
                        self.cpu_cores.render(panel_x, panel_y, panel_w, panel_h, cpu_info)
                    elif panel_name == "memory":
                        mem_info = self.monitor.get_memory_info()
                        self.memory_display.render(panel_x, panel_y, panel_w, panel_h, mem_info)
                    elif panel_name == "network":
                        net_info = self.monitor.get_network_info()
                        self.network_display.render(panel_x, panel_y, panel_w, panel_h, net_info)

        
        if show_processes and self.monitor:
            
            
            grid_end_y = content_y + section_padding + (grid_rows * (cell_height + section_padding)) - section_padding
            proc_y = grid_end_y + section_padding
            proc_h = max(6, height - proc_y - footer_h - 1)
            processes = self.monitor.get_process_info(limit=min(20, proc_h - 2))
            self.process_list.set_sort_method(self.sort_processes_by)
            self.process_list.render(1, proc_y, width, proc_h, processes)



        
        separator_y = height - footer_h
        if separator_y >= 1:
            self.drawing.draw_at(1, separator_y, "═" * width, "cyan")

        
        footer_y = height - footer_h + 1
        if footer_y >= 1:
            
            sep_y = footer_y - 1
            if sep_y >= 1:
                self.drawing.draw_at(1, sep_y, "─" * width, "blue")

        self.header_footer.render_footer(1, footer_y, width, footer_h)

        
        sys.stdout.flush()

    def _handle_resize(self):
        
        self.layout_manager.update_size()
        new_width, new_height = self.layout_manager.get_size()

        
        if new_width != getattr(self, '_last_width', 0) or new_height != getattr(self, '_last_height', 0):
            
            self._needs_full_redraw = True
            
            self._last_width, self._last_height = new_width, new_height


    
    def set_process_sort(self, sort_by: str):
        if sort_by in ("cpu", "memory"):
            self.sort_processes_by = sort_by
    
    def handle_keyboard_input(self, key_handler):
        try:
            import select
            while self.running:
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    char = sys.stdin.read(1)
                    if not key_handler(char):
                        break
                time.sleep(0.01)
        except (ImportError, OSError, KeyboardInterrupt):
            pass