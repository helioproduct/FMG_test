import subprocess
import psutil
import time
from enum import Enum
from typing import List


class ProcessStatus(Enum):
    RUNNING = "running"
    KILLED = "killed"
    NOT_STARTED = "not started"


class LinuxProcess:
    def __init__(self, command: List[str]):
        self._start_time = None
        self._end_time = None
        self._command = command
        self._status = ProcessStatus.NOT_STARTED
        self._process = None

    def start(self):
        if self.status != ProcessStatus.RUNNING:
            self._process = subprocess.Popen(self._command, stdout=subprocess.PIPE)
            self._start_time = time.time()
        if self._process:
            self._status = ProcessStatus.RUNNING

    def stop(self):
        if self.status == ProcessStatus.RUNNING:
            self._process.kill()
            self._end_time = time.time()
            self._status = ProcessStatus.KILLED

    @property
    def status(self):
        return self._status

    @property
    def pid(self):
        if self.status == ProcessStatus.NOT_STARTED:
            return -1
        return self._process.pid

    def get_result(self):
        if self.status == ProcessStatus.RUNNING:
            return 'Process is still running'
        return subprocess.check_output(self.command, shell=True).decode("utf-8")

