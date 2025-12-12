import sys
import time
import signal
import threading

import click
from rich.console import Console
from rich.live import Live

from .system_monitor import SystemMonitor
from .ui.dashboard import Dashboard


class StatsManApp:    
    def __init__(self, refresh_rate: float = 1.0, no_color: bool = False):
        self.refresh_rate = refresh_rate
        self.no_color = no_color
        
        self.console = Console(color_system=None if no_color else "auto")
        self.dashboard = Dashboard(self.console, no_color)
        self.live = None
        self.running = False
        self.paused = False
        
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        self.running = False
        if self.live:
            self.live.stop()
    
    def _handle_keyboard_input(self):
        try:
            import select
            import termios
            import tty
            
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            
            while self.running:
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    char = sys.stdin.read(1)
                    
                    if char.lower() == 'q':
                        self.running = False
                        break
                    elif char.lower() == 'p':
                        self.paused = not self.paused
                    elif char.lower() == 'c':
                        self.dashboard.set_process_sort('cpu')
                    elif char.lower() == 'm':
                        self.dashboard.set_process_sort('memory')
                    elif char.lower() == 'r':
                        self.dashboard.set_process_sort('cpu')
                
                time.sleep(0.1)
        
        except (ImportError, OSError):
            pass
        
        finally:
            try:
                if 'old_settings' in locals():
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                pass
    
    def run(self):
        self.running = True
        
        keyboard_thread = threading.Thread(target=self._handle_keyboard_input, daemon=True)
        keyboard_thread.start()
        
        try:
            with Live(
                self.dashboard.render(),
                console=self.console,
                refresh_per_second=1.0 / self.refresh_rate,
                screen=True,
                auto_refresh=True,
            ) as self.live:
                self.live = self.live
                
                while self.running:
                    if not self.paused:
                        layout = self.dashboard.render()
                        self.live.update(layout)
                    
                    time.sleep(self.refresh_rate)
        
        except KeyboardInterrupt:
            pass
        
        finally:
            self.running = False
            if self.live:
                self.live.stop()
            
            self.console.clear()
            self.console.print("StatsMan - Goodbye!", justify="center")