import sys
from typing import Dict, List, Optional, Any
from ..layouts import TerminalController, DrawingPrimitives, LayoutElement


class NetworkDisplay(LayoutElement):

    def __init__(self, terminal: TerminalController, drawing: DrawingPrimitives,
                 min_width: int = 20, min_height: int = 5, preferred_width: int = 30,
                 preferred_height: int = 8, flexible_width: int = 1, flexible_height: int = 0,
                 anchor: str = "top-left", justification: str = "start"):
        super().__init__(min_width, min_height, preferred_width, preferred_height,
                        flexible_width, flexible_height, anchor, justification)
        self.terminal = terminal
        self.drawing = drawing

    def render(self, x: int, y: int, width: int, height: int, net_info: Any):

        width, height = max(20, width), max(5, height)

        self.drawing.draw_box(x, y, width, height, "Network", "yellow")

        sent_mb = net_info.bytes_sent / (1024 * 1024)
        recv_mb = net_info.bytes_recv / (1024 * 1024)


        content_width = width - 4
        content_height = height - 2
        current_y = y + 1



        if height < 6:

            self.drawing.draw_at(x + 2, y + 1, f"↑{sent_mb:.1f}M ↓{recv_mb:.1f}M", "yellow")
            return


        available_height = height - 2

        if available_height >= 8:

            text_y = y + 1
            upload_bar_y = y + 3
            download_bar_y = y + 7


            if width < 25:
                self.drawing.draw_at(x + 2, text_y, f"↑{sent_mb:.1f}M ↓{recv_mb:.1f}M", "yellow")
            else:
                self.drawing.draw_at(x + 2, text_y, f"Upload: {self._format_bytes(net_info.bytes_sent)}", "green")
                self.drawing.draw_at(x + 2, text_y + 1, f"Download: {self._format_bytes(net_info.bytes_recv)}", "blue")


            bar_text = "UP" if width < 25 else "UPLOAD"
            self.drawing.draw_progress_bar(x + 2, upload_bar_y, content_width, min(sent_mb * 10, 100), bar_text, "green")

            bar_text = "DOWN" if width < 25 else "DOWNLOAD"
            self.drawing.draw_progress_bar(x + 2, download_bar_y, content_width, min(recv_mb * 10, 100), bar_text, "blue")

        elif available_height >= 5:

            text_y = y + 1
            bar_y = y + 3


            if width < 25:
                self.drawing.draw_at(x + 2, text_y, f"↑{sent_mb:.1f}M ↓{recv_mb:.1f}M", "yellow")
            else:
                self.drawing.draw_at(x + 2, text_y, f"UL: {self._format_bytes(net_info.bytes_sent)}", "green")
                self.drawing.draw_at(x + 2, text_y + 1, f"DL: {self._format_bytes(net_info.bytes_recv)}", "blue")


            combined_rate = (sent_mb + recv_mb) / 2
            self.drawing.draw_progress_bar(x + 2, bar_y, content_width, min(combined_rate * 10, 100), "NET", "cyan")

        else:

            self.drawing.draw_at(x + 2, y + 1, f"↑{sent_mb:.1f} ↓{recv_mb:.1f}", "yellow")

    def _format_bytes(self, bytes_value: int) -> str:
        bytes_float = float(bytes_value)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_float < 1024.0:
                return f"{bytes_float:.1f} {unit}"
            bytes_float /= 1024.0
        return f"{bytes_float:.1f} PB"