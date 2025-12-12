import sys
import os
import signal
from typing import Tuple, Optional, Dict, List, Any


class TerminalController:
    
    def __init__(self, no_color: bool = False):
        self.no_color = no_color
        self.original_settings = None
        self.size = (80, 24)
        
    def initialize(self, bg_color: str = "black"):
        if not self.no_color:
            
            sys.stdout.write("\033[?1049h")
            
            sys.stdout.write("\033[?25l")
            
            sys.stdout.write("\033[2J")
            
            sys.stdout.write("\033[H")
            
            self._set_background(bg_color)
            
            self._enable_raw_mode()
        
        sys.stdout.flush()
        self._update_size()
    
    def cleanup(self):
        
        if self.original_settings:
            try:
                import termios
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_settings)
            except:
                pass
        
        
        sys.stdout.write("\033[?25h")
        
        sys.stdout.write("\033[?1049l")
        
        sys.stdout.write("\033]111\007")
        sys.stdout.flush()
    
    def _enable_raw_mode(self):
        try:
            import termios
            import tty
            if sys.stdin.isatty():
                self.original_settings = termios.tcgetattr(sys.stdin)
                tty.setraw(sys.stdin.fileno())
        except:
            pass
    
    def _set_background(self, color: str):
        if self.no_color:
            return
            
        color_map = {
            'black': '#000000', 'blue': '#000080', 'dark_blue': '#00008B',
            'purple': '#800080', 'cyan': '#008080', 'green': '#006400',
            'red': '#8B0000', 'white': '#FFFFFF', 'yellow': '#FFFF00',
            'magenta': '#FF00FF',
        }
        
        hex_color = color_map.get(color.lower(), '#000000')
        sys.stdout.write(f"\033]11;{hex_color}\007")
    
    def _update_size(self):
        try:
            import shutil
            self.size = shutil.get_terminal_size()
        except:
            self.size = (
                int(os.environ.get('COLUMNS', 80)),
                int(os.environ.get('LINES', 24))
            )
    
    def get_size(self) -> Tuple[int, int]:
        self._update_size()
        return self.size
    
    def clear(self):
        
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    
    def move_cursor(self, x: int, y: int):
        sys.stdout.write(f"\033[{y};{x}H")
    
    def set_text_color(self, color: str):
        if self.no_color:
            return
        color_codes = {
            'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
            'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
            'bright_black': '90', 'bright_red': '91', 'bright_green': '92',
            'bright_yellow': '93', 'bright_blue': '94', 'bright_magenta': '95',
            'bright_cyan': '96', 'bright_white': '97'
        }
        code = color_codes.get(color, '37')
        sys.stdout.write(f"\033[{code}m")
    
    def reset_text_color(self):
        if not self.no_color:
            sys.stdout.write("\033[0m")
    
    def write_at(self, x: int, y: int, text: str, color: str = "white"):
        self.move_cursor(x, y)
        self.set_text_color(color)
        sys.stdout.write(text)
        self.reset_text_color()