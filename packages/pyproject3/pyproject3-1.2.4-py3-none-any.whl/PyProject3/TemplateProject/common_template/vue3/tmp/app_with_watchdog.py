# coding: utf-8
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, process_args=['python', '-m', 'http.server', '8099']):
        self.process_args = process_args
        self.process = self.start_server()

    def start_server(self):
        return subprocess.Popen(self.process_args)

    def on_modified(self, event):
        # 杀死旧进程并重启
        self.process.terminate()
        self.process = self.start_server()
        print("Server reloaded due to file change")


if __name__ == "__main__":
    process_args = ['/Users/jiangbin/venvs/py38_xingyun/bin/python', 'app.py']
    event_handler = ReloadHandler(process_args=process_args)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
