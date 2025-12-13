from email.message import EmailMessage
from email.utils import localtime
import json
import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
import os
import signal
import smtplib
import socket
import sys
from threading import Timer
from time import time
import traceback

logging_setup = None


def setup_logging(app_name=None, default_level=logging.INFO, signal=None):
    global logging_setup
    logging_setup = LoggingSetup(
        app_name=app_name,
        default_level=default_level,
        signal=signal,
    )
    logging_setup.setup()


class LoggingSetup:
    logger = None
    stdout_logger = None
    stderr_logger = None
    file_logger = None
    syslog_logger = None
    smtp_logger = None

    def __init__(self, app_name=None, default_level=logging.INFO, signal=None):
        self.app_name = app_name

        self.debug = False
        self.systemd_log = False

        self.file_log = None
        self.file_log_count = 14
        self.file_log_when_rotate = "w0"
        self.file_log_rotate_interval = 1
        self.file_log_encoding = "utf-8"

        self.syslog = False
        self.syslog_tag = None
        self.syslog_address = "/dev/log"

        self.smtp_log = False
        self.smtp_log_address = ("localhost", 25)
        self.smtp_log_sender = None
        self.smtp_log_recipient = "root"

        self.default_level = default_level
        self.default_stderr_level = logging.WARNING
        self.default_file_level = self.default_level
        self.default_syslog_level = self.default_level
        self.default_smtp_level = logging.WARNING

        self.formatter = FancyFormatter(
            "%(asctime)s - %(levelname)s - %(name)s: %(message)s",
            "%(asctime)s - %(levelname)s - %(message)s",
        )
        self.formatter_without_timestamp = FancyFormatter(
            "%(levelname)s - %(name)s: %(message)s",
            "%(levelname)s - %(message)s",
        )
        self.formatter_tagged_format = (
            ": %(levelname)s - %(name)s: %(message)s",
            ": %(levelname)s - %(message)s",
        )

        self.toggle_level_signal = signal
        self.toggle_level = self.default_level

    def setup(self):
        if self.app_name is None:
            try:
                # use project root directory name as app_name
                main_file = sys.modules["__main__"].__file__
                self.app_name = str(os.path.realpath(os.path.dirname(main_file)).split(os.sep)[-1])
            except AttributeError:
                self.app_name = os.path.basename(os.getcwd())

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.NOTSET)

        stream_formatter = self.formatter
        if self.systemd_log or "SYSTEMD_LOG" in os.environ:
            stream_formatter = self.formatter_without_timestamp

        self.stderr_logger = StreamHandler(sys.stderr)
        self.stderr_logger.setLevel(self.default_stderr_level)
        self.stderr_logger.setFormatter(stream_formatter)
        self.logger.addHandler(self.stderr_logger)

        self.stdout_logger = StreamHandler(sys.stdout)
        self.stdout_logger.setLevel(self.default_level)
        if self.debug or "DEBUG_LOG" in os.environ:
            self.stdout_logger.setLevel(logging.DEBUG)
        self.stdout_logger.addFilter(LessThanFilter(self.default_stderr_level))
        self.stdout_logger.setFormatter(stream_formatter)
        self.logger.addHandler(self.stdout_logger)

        if self.file_log or "FILE_LOG" in os.environ:
            file = os.environ["FILE_LOG"] if "FILE_LOG" in os.environ else self.file_log
            directory = os.path.dirname(file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            count = int(os.environ["FILE_LOG_COUNT"]) if "FILE_LOG_COUNT" in os.environ else self.file_log_count
            self.file_logger = TimedRotatingFileHandler(
                file,
                when=self.file_log_when_rotate,
                interval=self.file_log_rotate_interval,
                backupCount=count,
                encoding=self.file_log_encoding
            )
            self.file_logger.setFormatter(self.formatter)
            self.file_logger.setLevel(self.default_file_level)
            self.logger.addHandler(self.file_logger)

        if self.syslog or "SYSLOG" in os.environ:
            tag = os.environ["SYSLOG_TAG"] if "SYSLOG_TAG" in os.environ else self.syslog_tag
            if not tag:
                tag = self.app_name
            address = self.syslog_address
            if "SYSLOG_ADDRESS" in os.environ:
                address = os.environ["SYSLOG_ADDRESS"]
                if ":" in address:
                    parts = address.split(":")
                    address = (parts[0], parts[1])
            self.syslog_logger = logging.handlers.SysLogHandler(address)
            self.syslog_logger.setFormatter(FancyFormatter(
                tag + self.formatter_tagged_format[0],
                tag + self.formatter_tagged_format[1]
            ))
            self.syslog_logger.setLevel(self.default_syslog_level)
            self.logger.addHandler(self.syslog_logger)

        if self.smtp_log or "SMTP_LOG" in os.environ:
            address = os.environ["SMTP_LOG_ADDRESS"] if "SMTP_LOG_ADDRESS" in os.environ else self.smtp_log_address
            if isinstance(address, str):
                parts = address.split(":")
                address = (parts[0], parts[1] if len(parts) > 1 else 25)

            sender = os.environ["SMTP_LOG_SENDER"] if "SMTP_LOG_SENDER" in os.environ else self.smtp_log_sender
            if not sender:
                sender = self.app_name + "@"
                if os.name == "nt":
                    sender += socket.gethostname()
                else:
                    sender += socket.getfqdn()

            recipient = os.environ["SMTP_LOG_RECIPIENT"] if "SMTP_LOG_RECIPIENT" in os.environ else None
            if not recipient:
                recipient = self.smtp_log_recipient

            self.smtp_logger = BufferingSMTPHandler(address, sender, recipient, self.app_name)
            self.smtp_logger.setFormatter(self.formatter)
            self.smtp_logger.setLevel(self.default_smtp_level)
            self.logger.addHandler(self.smtp_logger)

        if self.toggle_level_signal:
            signal.signal(self.toggle_level_signal, self.handle_signal_level_toggle)

    def handle_signal_level_toggle(self, signum, frame):
        if self.toggle_level == logging.DEBUG:
            self.toggle_level = logging.INFO
            logging.info("received signal - switched logging to INFO")
        else:
            self.toggle_level = logging.DEBUG
            logging.info("received signal - switched logging to DEBUG")

        for logger in [self.stdout_logger, self.file_logger, self.syslog_logger]:
            if logger:
                logger.setLevel(self.toggle_level)


class FancyFormatter(logging.Formatter):
    formatter_root = None

    # noinspection PyMissingConstructor
    def __init__(self, fmt, fmt_root=None):
        self.formatter = logging.Formatter(fmt)
        if fmt_root is not None:
            self.formatter_root = logging.Formatter(fmt_root)

    def formatTime(self, record, datefmt=None):
        if record.name == "root" and self.formatter_root:
            return self.formatter_root.formatTime(record, datefmt)
        return self.formatter.formatTime(record, datefmt)

    def formatException(self, ei):
        return self.formatter.formatException(ei)

    def usesTime(self):
        return self.formatter.usesTime() or self.formatter_root and self.formatter_root.usesTime()

    def formatMessage(self, record):
        if record.name == "root" and self.formatter_root:
            return self.formatter_root.formatMessage(record)
        return self.formatter.formatMessage(record)

    def formatStack(self, stack_info):
        return self.formatter.formatStack(stack_info)

    def format(self, record):
        if record.name == "root" and self.formatter_root:
            return self.formatter_root.format(record)
        return self.formatter.format(record)


class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name="lessThanFilter"):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        return 1 if record.levelno < self.max_level else 0


class BufferingSMTPHandler(logging.Handler):
    ENCRYPTION_STARTTLS = "starttls"
    ENCRYPTION_TLS = "tls"

    credentials = None
    encryption = None
    secure = False  # = starttls backward compatibility
    timeout = 5.0

    timer = None
    buffer = None
    last_flush = 0
    flush_timeouts = None
    flush_timeout_current = 0
    postpone_flush = False

    def __init__(self, host, sender, recipients, subject_prefix=None):
        logging.Handler.__init__(self)
        self.buffer = []
        self.host = host
        self.sender = sender
        self.recipients = recipients
        self.subject_prefix = subject_prefix
        self.flush_timeouts = [5, 300, 1800, 3600]

        self.flush_on_timeout()

    def should_flush(self):
        if self.postpone_flush:
            return False

        timeout = self.flush_timeouts[self.flush_timeout_current]
        if self.last_flush < time() - timeout:
            if self.last_flush < time() - timeout * 1.1:
                self.flush_timeout_current = 0
            else:
                if self.flush_timeout_current < len(self.flush_timeouts) - 1:
                    self.flush_timeout_current += 1
            return True

        return False

    def flush_on_timeout(self):
        self.timer = Timer(min(self.flush_timeouts), self.flush_on_timeout)
        self.timer.daemon = True
        self.timer.start()

        self.flush_maybe()

    def emit(self, record):
        self.buffer.append(record)

        self.flush_maybe()

    def flush_maybe(self):
        self.acquire()
        try:
            if self.should_flush():
                self.flush()
        except Exception as e:
            stderr = sys.stderr if sys.stderr else sys.stdout
            print("BufferingSMTPHandler failed: " + str(e), file=stderr)
            traceback.print_exc(file=stderr)
            if stderr:
                stderr.flush()
        finally:
            self.release()

    def flush(self):
        if len(self.buffer) > 0:
            self.send_email()
            self.buffer = []
            self.last_flush = time()

    def close(self):
        try:
            self.acquire()
            self.flush()
        finally:
            self.timer.cancel()
            try:
                logging.Handler.close(self)
            finally:
                self.release()

    def send_email(self):
        message = EmailMessage()
        message["From"] = self.sender
        message["To"] = ",".join(self.get_recipients())
        message["Subject"] = self.construct_subject()
        message["Date"] = localtime()

        content = []
        for record in self.buffer:
            try:
                content.append(self.format(record))
            except Exception:
                content.append("FAILED TO FORMAT: %s" % json.dumps(record))
        message.set_content("\n".join(content))

        host, port = self.get_host_port()

        if self.encryption == self.ENCRYPTION_TLS:
            if port is None:
                port = smtplib.SMTP_SSL_PORT
            smtp = smtplib.SMTP_SSL(host, port, timeout=self.timeout)
        else:
            if port is None:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(host, port, timeout=self.timeout)

            if self.encryption == self.ENCRYPTION_STARTTLS or self.secure:
                smtp.starttls()

        username, password = self.get_credentials()
        if username is not None:
            smtp.login(username, password)

        smtp.send_message(message)
        smtp.quit()

    def get_recipients(self):
        recipients = self.recipients
        if isinstance(recipients, str):
            recipients = [recipients]
        return recipients

    def get_host_port(self):
        if isinstance(self.host, (list, tuple)):
            return self.host
        return self.host, None

    def get_credentials(self):
        if isinstance(self.credentials, (list, tuple)):
            return self.credentials
        elif self.credentials is not None:
            raise Exception("unsupported credentials format: " + str(type(self.credentials)))
        return None, None

    def construct_subject(self):
        level = 0
        level_name = None
        override_level = 0
        override_value = None

        for record in self.buffer:
            if level < record.levelno:
                level = record.levelno
                level_name = record.levelname.lower()

            if hasattr(record, "subject"):
                if override_level < record.levelno:
                    override_level = record.levelno
                    override_value = record.subject

        subject = None
        if override_value:
            subject = override_value
        elif level_name:
            subject = level_name

        if self.subject_prefix and subject:
            subject = self.subject_prefix + ": " + subject

        return subject
