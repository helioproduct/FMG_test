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
    def __init__(self, command: List[str], output_file: str):
        self._start_time = None
        self._end_time = None
        self._command = command
        self._status = ProcessStatus.NOT_STARTED
        self._process = None
        self._output_file = output_file

    def start(self):
        if self.status != ProcessStatus.RUNNING:
            with open(self._output_file, "w") as output:
                self._process = subprocess.Popen(self._command, stdout=output)
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
            return 'Process not started'

        # process is killed
        with open(self._output_file, "r") as output:
            return output.read()

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time


class LinuxProcessStatistic:
    def __init__(self, linux_process: LinuxProcess):
        self.linux_process = linux_process

    # Returns CPU usage in percentages
    def get_cpu_usage(self):
        if self.linux_process.status == ProcessStatus.RUNNING:
            pid = self.linux_process.pid
            process = psutil.Process(pid)
            return process.cpu_percent()
        return 0
    
    # Returns memory usage in MB
    def get_memory_usage(self):
        if self.linux_process.status == ProcessStatus.RUNNING:
            pid = self.linux_process.pid
            process = psutil.Process(pid)
            memory_info = process.memory_info()
            return memory_info.rss / 1024 / 1024
        return 0

    # Returns execution time of process in seconds
    def get_working_time(self):
        if self.linux_process.status == ProcessStatus.RUNNING:
            return time.time() - self.linux_process.start_time
        if self.linux_process.status == ProcessStatus.NOT_STARTED:
            return 0
        return self.linux_process.end_time - self.linux_process.start_time

    def __str__(self):
        return f"Status: {self.linux_process.status} \
            PID: {self.linux_process.pid} \
            Working time: {self.get_working_time():.2f} seconds \
            CPU usage: {self.get_cpu_usage():.2f}% \
            Memory usage: {self.get_memory_usage():.2f} MB"

    def to_dict(self):
        return {
            "Status": f"{self.linux_process.status}",
            "PID": f"{self.linux_process.pid}",
            "Working time": f"{self.get_working_time()} seconds",
            "CPU usage": f"{self.get_cpu_usage()} %",
            "Memory usage": f"{self.get_memory_usage()} MB",
        }

