import sys
import time
import signal
import threading
from typing import Optional

from .renderer import StatsManRenderer


class KeyboardHandler:

    def __init__(self, renderer: StatsManRenderer):
        self.renderer = renderer

    def handle_key(self, char: str) -> bool:
        char_lower = char.lower()

        if char_lower == 'q':
            self.renderer.running = False
            return False
        elif char_lower == 'p':

            pass
        elif char_lower == 'c':
            self.renderer.set_process_sort('cpu')
        elif char_lower == 'm':
            self.renderer.set_process_sort('memory')

        return True

    def start_input_thread(self):
        input_thread = threading.Thread(target=self.renderer.handle_keyboard_input,
                                     args=(self.handle_key,), daemon=True)
        input_thread.start()


class StatsManApp:

    def __init__(self, refresh_rate: float = 1.0, no_color: bool = False, bg_color: str = "black"):
        self.refresh_rate = refresh_rate
        self.no_color = no_color
        self.bg_color = bg_color


        self.renderer = StatsManRenderer(no_color, bg_color)
        self.keyboard_handler = KeyboardHandler(self.renderer)

    def run(self):

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        def on_resize(sig, frame):
            if self.renderer.running:

                self.renderer._handle_resize()

        signal.signal(signal.SIGWINCH, on_resize)


        self.renderer.initialize()
        self.keyboard_handler.start_input_thread()

        try:
            while self.renderer.running:
                self.renderer.render()
                time.sleep(self.refresh_rate)
        except KeyboardInterrupt:
            pass
        finally:
            self.renderer.cleanup()
            print("\n[bold cyan]StatsMan – See you later![/]\n")

    def _signal_handler(self, signum, frame):
        self.renderer.running = False