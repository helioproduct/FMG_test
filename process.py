import subprocess
from enum import Enum


class ProcessStatus(Enum):
    RUNNING = "running"
    KILLED = "killed"
    NOT_STARTED = "not started"


class LinuxProcess:
    def __init__(self, command):
        self.command = command
        self.process = None
        self.status = ProcessStatus.NOT_STARTED

    def start(self):
        if self.status != ProcessStatus.RUNNING:
            self.process = subprocess.Popen(self.command)
        elif self.process:
            self.status = ProcessStatus.RUNNING
        else:
            self.status = ProcessStatus.NOT_STARTED

    def stop(self):
        if self.status == ProcessStatus.RUNNING:
            self.process.kill()
        self.process = None

    def get_status(self):
        return self.status

    def get_result(self):
        if self.process:
            return 'Process is still running'
        return subprocess.check_output(self.command, shell=True).decode("utf-8")

