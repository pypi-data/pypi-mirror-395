import os
import re
import subprocess
import sys
import threading
from time import sleep
from typing import Any

os_win = os.name == "nt"


def hidden_startupinfo():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    return startupinfo


class Process:
    encoding = "utf-8"
    encoding_errors = "strict"
    process = None
    thread = None
    data = None
    data_raw = None
    stderr = None
    stderr_raw = None
    raw_lines = None
    shell = True
    hidden = True
    exception = None
    kill_children = True

    def __init__(self, command, timeout=3600, block=True, encoding=None, popen_override=None, shell=True, hidden=True):
        self.command = command
        self.popen_override = popen_override
        self.timeout = timeout
        self.block = block
        if encoding is not None:
            self.encoding = encoding
        self.shell = shell
        self.hidden = hidden

    def execute(self, input=None, callback=None):
        self.thread = threading.Thread(target=self.target, args=(input, callback), daemon=True)
        self.thread.start()

        if self.timeout > 0:
            threading.Thread(target=self.killer, daemon=True).start()

        if self.block:
            while self.thread.is_alive():
                self.thread.join(1)
        else:
            while self.process is None and self.exception is None:
                sleep(0.010)

        if self.exception:
            raise self.exception

        return self

    def target(self, input, callback):
        try:
            parameters = {
                "args": self.command,
                "stdin": subprocess.PIPE,
                "stdout": subprocess.PIPE,
                "stderr": subprocess.STDOUT,
                "shell": self.shell,
            }

            if os_win:
                if self.hidden and "startupinfo" not in parameters:
                    parameters["startupinfo"] = hidden_startupinfo()

            if self.popen_override:
                if "shell" in self.popen_override:
                    self.shell = self.popen_override["shell"]
                parameters.update(self.popen_override)

            self.process = subprocess.Popen(**parameters)

            if self.block:
                if self.data is None:
                    self.data = ""

                if callback:
                    self.raw_lines = []
                    while self.process.poll() is None:
                        for line in self.process.stdout:
                            if self.encoding:
                                line = line.decode(self.encoding, errors=self.encoding_errors)
                                line = line.rstrip("\r\n")
                                self.data += line + "\n"
                                callback(line)
                            else:
                                self.data_raw += line
                                self.raw_lines.append(line)
                                callback(line)
                else:
                    stdout: Any
                    (stdout, stderr) = self.process.communicate(input)
                    if stdout is not None:
                        if self.encoding:
                            self.data = stdout.decode(self.encoding, errors=self.encoding_errors)
                        self.data_raw = stdout

                    if stderr is not None:
                        self.stderr_raw = stderr

                self.data = self.data.rstrip("\r\n")
            else:
                self.process.wait()

        except:
            self.exception = sys.exc_info()[1]

    def killer(self):
        self.thread.join(self.timeout)
        if self.thread.is_alive():
            self.kill()

    def read_lines(self):
        source: Any
        if self.data_raw is None and self.block is False:
            source = self.process.stdout.read()
        else:
            source = self.data_raw

        if self.encoding:
            if self.data is not None:
                decoded = self.data
            else:
                decoded = source.decode(self.encoding, errors=self.encoding_errors)
            lines = []
            for line in decoded.split("\n"):
                line = line.rstrip("\r")
                lines.append(line)
            return lines

        else:
            if self.raw_lines is not None:
                return self.raw_lines

            lines = []
            for line in source.split(b"\n"):
                line = line.rstrip(b"\r")
                lines.append(line)
            return lines

    def read(self):
        if self.encoding:
            return "\n".join(self.read_lines()).rstrip("\r\n")
        else:
            return self.data_raw

    def read_stderr(self):
        source: Any
        if self.stderr_raw is None and self.block is False:
            source = self.process.stderr.read()
        else:
            source = self.stderr_raw

        if self.encoding:
            return source.decode(encoding=self.encoding, errors=self.encoding_errors)
        return source

    def return_code(self):
        if not self.process:
            return None
        return self.process.returncode

    def pid(self):
        if not self.process:
            return None
        return self.process.pid

    def kill(self, block=True):
        if not self.process:
            return

        if self.kill_children:
            self.kill_tree()
        else:
            self.process.kill()

        if block:
            self.thread.join()

    def kill_tree(self):
        try:
            if os_win:
                subprocess.check_output(
                    "taskkill /t /f /pid " + str(self.process.pid), startupinfo=hidden_startupinfo()
                )
            else:
                subprocess.check_output(
                    "pkill -P %s" % self.process.pid, shell=True
                )
            return True
        except subprocess.CalledProcessError:
            return False


_detected_encoding = None


def detect_encoding():
    global _detected_encoding

    if _detected_encoding is None:
        if os_win:
            output = subprocess.check_output("C:\\Windows\\System32\\chcp.com", startupinfo=hidden_startupinfo())
            output = output.decode("ascii", errors="ignore").strip()

            match = re.search(r":\s*([0-9]+)$", output, flags=re.I | re.M)
            if not match:
                raise ProcessException("unexpected response from chcp while detecting encoding: " + output)

            _detected_encoding = "cp" + match.group(1)
        else:
            _detected_encoding = "utf-8"

    return _detected_encoding


def execute_command(command, timeout=60, valid_codes=0, encoding=None, popen_override=None, shell=True,
                    setup: callable = None, any_code_valid=False, **kwargs):

    if encoding is None:
        encoding = detect_encoding()

    process = Process(
        command, timeout=timeout, encoding=encoding, popen_override=popen_override, shell=shell, **kwargs
    )
    if setup is not None:
        setup(process)
    process.execute()

    if not any_code_valid:
        if not isinstance(valid_codes, list):
            valid_codes = [valid_codes]

        if process.return_code() not in valid_codes:
            raise ProcessException("command %s failed with code %s, output: %s" % (
                command, process.return_code(), process.read()
            ))

    return process


class ProcessException(Exception):
    pass
