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
        elif self.status == ProcessStatus.NOT_STARTED:
            return None
        # process is killed
        out, err = self._process.communicate()
        return out.decode("utf-8")

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time


class LinuxProcessStatistic:
    def __init__(self, linux_process: LinuxProcess):
        self.linux_process = linux_process

    def get_cpu_usage(self):
        if self.linux_process.status == ProcessStatus.RUNNING:
            pid = self.linux_process.pid
            process = psutil.Process(pid)
            return process.cpu_percent()
        return 0

    def get_memory_usage(self):
        if self.linux_process.status == ProcessStatus.RUNNING:
            pid = self.linux_process.pid
            process = psutil.Process(pid)
            memory_info = process.memory_info()
            return memory_info.rss / 1024 / 1024
        return 0

    def get_working_time(self):
        if self.linux_process.status == ProcessStatus.RUNNING:
            return time.time() - self.linux_process.start_time
        if self.linux_process.status == ProcessStatus.NOT_STARTED:
            return 0
        return self.linux_process.end_time - self.linux_process.start_time

    def __str__(self):
        return f"Process info:\n\
            Status: {self.linux_process.status}\n\
            PID: {self.linux_process.pid}\n\
            Working time: {self.get_working_time():.2f} seconds\n\
            CPU usage: {self.get_cpu_usage():.2f}%\n\
            Memory usage: {self.get_memory_usage():.2f} MB"

