from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.align import Align
from typing import Optional
import time

from ..system_monitor import SystemMonitor
from .charts import ChartRenderer


class Dashboard:
    def __init__(self, console: Optional[Console] = None, no_color: bool = False):
        self.console = console or Console(color_system=None if no_color else "auto")
        self.monitor = SystemMonitor()
        self.charts = ChartRenderer(self.console)
        self.layout = Layout()
        self.sort_processes_by = "cpu"
        
        self._setup_visual_layout()
    
    def _setup_visual_layout(self) -> None:
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3),
        )
        
        self.layout["main"].split_column(
            Layout(name="top", size=16),
            Layout(name="middle", size=14),
            Layout(name="bottom", ratio=1),
        )
        
        self.layout["top"].split_row(
            Layout(name="gauges", ratio=1),
            Layout(name="cores", ratio=1),
        )
        
        self.layout["middle"].split_row(
            Layout(name="memory", ratio=1),
            Layout(name="network", ratio=1),
        )
        
        self.layout["bottom"].split_row(
            Layout(name="processes"),
        )
    
    def _create_header(self) -> Panel:
        header_text = Text.from_markup(
            "[bold blue]StatsMan[/bold blue] - System Monitor",
            justify="center"
        )
        return Panel(
            Align.center(header_text),
            border_style="blue"
        )
    
    def _create_footer(self) -> Panel:
        controls = Text.from_markup(
            "[cyan]q:quit p:pause c:cpu m:mem r:reset[/cyan]",
            justify="center"
        )
        return Panel(
            Align.center(controls),
            border_style="cyan"
        )
    
    def _create_system_gauges(self) -> Panel:
        cpu_info = self.monitor.get_cpu_info()
        memory_info = self.monitor.get_memory_info()
        disk_info = self.monitor.get_disk_info()
        
        return self.charts.create_system_gauges(cpu_info, memory_info, disk_info)
    
    def _create_cpu_cores(self) -> Panel:
        cpu_info = self.monitor.get_cpu_info()
        cpu_history = self.monitor.get_cpu_history()
        
        sparkline = self.charts.create_sparkline(cpu_history, width=60, height=8)
        sparkline_text = Text.from_markup(f"[cyan]CPU History:[/cyan] {sparkline}")
        
        cores_panel = self.charts.create_cpu_core_visualization(cpu_info)
        
        return Panel(
            Group(sparkline_text, cores_panel),
            title=f"CPU: {cpu_info.percent:.1f}%",
            border_style="red"
        )
    
    def _create_memory_visual(self) -> Panel:
        memory_info = self.monitor.get_memory_info()
        memory_history = self.monitor.get_memory_history()
        
        sparkline = self.charts.create_sparkline(memory_history, width=50, height=6)
        sparkline_text = Text.from_markup(f"[green]Memory History:[/green] {sparkline}")
        
        breakdown_panel = self.charts.create_memory_breakdown(memory_info)
        
        return Panel(
            Group(sparkline_text, breakdown_panel),
            title=f"Memory: {memory_info.percent:.1f}%",
            border_style="green"
        )
    
    def _create_network_visual(self) -> Panel:
        network_info = self.monitor.get_network_info()
        return self.charts.create_network_visualization(network_info)
    
    def _create_processes_visual(self) -> Panel:
        processes = self.monitor.get_process_info(limit=20)
        return self.charts.create_mini_process_table(processes, limit=16)
    
    def update_layout(self) -> None:
        self.layout["header"].update(self._create_header())
        self.layout["footer"].update(self._create_footer())
        
        self.layout["top"]["gauges"].update(self._create_system_gauges())
        self.layout["top"]["cores"].update(self._create_cpu_cores())
        self.layout["middle"]["memory"].update(self._create_memory_visual())
        self.layout["middle"]["network"].update(self._create_network_visual())
        self.layout["bottom"]["processes"].update(self._create_processes_visual())
    
    def render(self) -> Layout:
        self.monitor.update_history()
        self.update_layout()
        return self.layout
    
    def set_process_sort(self, sort_by: str) -> None:
        if sort_by in ['cpu', 'memory']:
            self.sort_processes_by = sort_by