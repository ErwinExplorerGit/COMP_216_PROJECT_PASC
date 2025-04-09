import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen(["python3", self.script])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"🔄 Restarting due to changes in {event.src_path}")
            self.start_process()


script_to_run = "gui.py"  # change to your script name
event_handler = ChangeHandler(script_to_run)
observer = Observer()
observer.schedule(event_handler, ".", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
