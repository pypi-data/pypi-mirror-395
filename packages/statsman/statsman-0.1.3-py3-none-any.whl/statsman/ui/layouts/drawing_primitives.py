import sys
from typing import Tuple, Optional, Dict, List, Any

from .terminal_controller import TerminalController


class DrawingPrimitives:
    
    def __init__(self, terminal: TerminalController):
        self.terminal = terminal
    
    def draw_box(self, x: int, y: int, width: int, height: int,
                  title: Optional[str] = None, border_color: str = "white"):
        width, height = max(3, width), max(3, height)

        
        corners = {'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯'}
        horizontal = '─'
        vertical = '│'

        
        output = []
        color_code = ""
        reset_code = ""

        if not self.terminal.no_color:
            color_codes = {
                'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
                'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
                'bright_black': '90', 'bright_red': '91', 'bright_green': '92',
                'bright_yellow': '93', 'bright_blue': '94', 'bright_magenta': '95',
                'bright_cyan': '96', 'bright_white': '97'
            }
            color_code = f"\033[{color_codes.get(border_color, '37')}m"
            reset_code = "\033[0m"

        
        top_border = f"{corners['tl']}{horizontal * (width - 2)}{corners['tr']}"
        output.append(f"\033[{y};{x}H{color_code}{top_border}")

        
        for i in range(1, height - 1):
            output.append(f"\033[{y+i};{x}H{color_code}{vertical}\033[{y+i};{x+width-1}H{vertical}")

        
        bottom_border = f"{corners['bl']}{horizontal * (width - 2)}{corners['br']}"
        output.append(f"\033[{y+height-1};{x}H{color_code}{bottom_border}")

        
        if title and width > len(title) + 4:
            title_pos = x + (width - len(title)) // 2
            output.append(f"\033[{y};{title_pos-2}H{color_code}[ {title} ]")

        
        if reset_code:
            output.append(reset_code)

        sys.stdout.write("".join(output))
    
    def draw_at(self, x: int, y: int, text: str, color: str = "white"):
        if self.terminal.no_color:
            sys.stdout.write(f"\033[{y};{x}H{text}")
        else:
            color_codes = {
                'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
                'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
                'bright_black': '90', 'bright_red': '91', 'bright_green': '92',
                'bright_yellow': '93', 'bright_blue': '94', 'bright_magenta': '95',
                'bright_cyan': '96', 'bright_white': '97'
            }
            color_code = color_codes.get(color, '37')
            sys.stdout.write(f"\033[{y};{x}H\033[{color_code}m{text}\033[0m")
    
    def draw_centered_text(self, x: int, y: int, text: str, color: str = "white", 
                           max_width: Optional[int] = None):
        if max_width and len(text) > max_width:
            text = text[:max_width-3] + "..."
        
        centered_x = max(1, x - len(text) // 2)
        self.terminal.write_at(centered_x, y, text, color)
    
    def draw_progress_bar(self, x: int, y: int, width: int, percentage: float,
                          label: Optional[str] = None, color: str = "green"):
        if width < 8:
            return

        filled_width = int((percentage / 100.0) * (width - 6))  
        filled_width = max(0, min(width - 6, filled_width))

        
        self.terminal.move_cursor(x, y)
        self.terminal.set_text_color("cyan")
        sys.stdout.write("╭" + "─" * (width - 2) + "╮")

        
        for i in range(1, 3):  
            self.terminal.move_cursor(x, y + i)
            self.terminal.set_text_color("cyan")
            sys.stdout.write("│")
            self.terminal.move_cursor(x + width - 1, y + i)
            sys.stdout.write("│")

            
            self.terminal.move_cursor(x + 1, y + i)
            self.terminal.set_text_color("white")
            sys.stdout.write("░" * (width - 2))

        
        if filled_width > 0:
            for i in range(1, 3):  
                self.terminal.move_cursor(x + 1, y + i)
                self.terminal.set_text_color(color)
                sys.stdout.write("█" * filled_width)

        
        self.terminal.move_cursor(x, y + 2)
        self.terminal.set_text_color("cyan")
        sys.stdout.write("╰" + "─" * (width - 2) + "╯")

        
        if label:
            label_text = f"{label}: {percentage:.1f}%"
            self.terminal.write_at(x, y + 3, label_text, color)
        else:
            percent_text = f"{percentage:.1f}%"
            percent_x = x + (width - len(percent_text)) // 2
            self.terminal.write_at(percent_x, y + 3, percent_text, color)

        self.terminal.reset_text_color()
    
    def draw_vertical_bars(self, x: int, y: int, width: int, height: int,
                           data: Optional[Dict[str, float]], color: str = "blue"):
        if not data:
            return

        num_bars = len(data)
        if num_bars == 0:
            return

        max_val = max(data.values()) if data.values() else 1
        if max_val == 0:
            max_val = 1
        
        max_val = max(max_val, 1)

        
        bar_width = max(1, width // num_bars)
        spacing = max(0, (width - bar_width * num_bars) // max(1, num_bars - 1))


        chart_height = height - 2

        
        for clear_y in range(y, y + height):
            for clear_x in range(x, x + width):
                self.terminal.move_cursor(clear_x, clear_y)
                sys.stdout.write(" ")

        for i, (label, value) in enumerate(data.items()):
            
            bar_x = x + i * (bar_width + spacing)
            bar_height = int((value / max_val) * chart_height)


            bar_height = max(0, min(bar_height, chart_height))
            
            if value > 0 and bar_height == 0:
                bar_height = 1

            for j in range(bar_height):
                bar_y = y + height - 2 - j  
                if bar_y >= y and bar_y < y + height:
                    self.terminal.move_cursor(bar_x, bar_y)
                    self.terminal.set_text_color(color)
                    sys.stdout.write("█")

            
            label_y = y + height - 1
            if label_y >= y and label_y < y + height:
                self.terminal.move_cursor(bar_x, label_y)
                self.terminal.set_text_color("white")
                
                display_label = label
                if len(display_label) > bar_width:
                    display_label = display_label[:bar_width]
                elif len(display_label) < bar_width:
                    
                    padding = (bar_width - len(display_label)) // 2
                    display_label = " " * padding + display_label
                    display_label = display_label.ljust(bar_width)
                sys.stdout.write(display_label)

        self.terminal.reset_text_color()
    
    def draw_sparkline(self, x: int, y: int, width: int, height: int, 
                       data: Optional[List[float]], color: str = "cyan"):
        if not data:
            return
        
        
        
        recent_data = data[-width:] if len(data) > width else data
        
        min_val = min(recent_data)
        max_val = max(recent_data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        
        
        if height <= 2:
            spark_chars = [' ', '█']
        elif height <= 4:
            spark_chars = [' ', '▄', '█']
        else:
            spark_chars = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        
        
        self.terminal.move_cursor(x, y)
        self.terminal.set_text_color(color)
        
        for value in recent_data:
            normalized = (value - min_val) / range_val
            char_index = min(int(normalized * len(spark_chars)), len(spark_chars) - 1)
            sys.stdout.write(spark_chars[max(0, char_index)])
        
        self.terminal.reset_text_color()