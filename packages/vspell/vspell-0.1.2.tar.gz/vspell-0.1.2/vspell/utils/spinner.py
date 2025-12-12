import sys
import time
import threading
import itertools

# ---------------------------
# Spinner
# ---------------------------
class Spinner:
    def __init__(self, message="Working"):
        self.message = message
        self._stop_event = threading.Event()
        self._spinner_thread = None

    def _spinner(self):
        frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        for frame in itertools.cycle(frames):
            if self._stop_event.is_set(): break
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(self.message)+2) + "\r")
        sys.stdout.flush()

    def start(self):
        self._stop_event.clear()
        if self._spinner_thread is None or not self._spinner_thread.is_alive():
            self._spinner_thread = threading.Thread(target=self._spinner, daemon=True)
            self._spinner_thread.start()

    def stop(self):
        self._stop_event.set()
        if self._spinner_thread is not None:
            self._spinner_thread.join()
            self._spinner_thread = None
