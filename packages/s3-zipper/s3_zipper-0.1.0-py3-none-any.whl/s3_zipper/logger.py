import sys
import datetime


class Logger:
    def __init__(self, use_timestamp=True, level="INFO"):
        self.use_timestamp = use_timestamp
        self.level = level.upper()

        self.level_order = {
            "DEBUG": 10,
            "INFO": 20,
            "WARN": 30,
            "ERROR": 40,
        }

    def _allowed(self, msg_level):
        return self.level_order[msg_level] >= self.level_order[self.level]

    def _format(self, level, message):
        if self.use_timestamp:
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            return f"[{ts}] [{level}] {message}"
        return f"[{level}] {message}"

    def debug(self, message):
        if self._allowed("DEBUG"):
            print(self._format("DEBUG", message), file=sys.stdout)

    def info(self, message):
        if self._allowed("INFO"):
            print(self._format("INFO", message), file=sys.stdout)

    def warn(self, message):
        if self._allowed("WARN"):
            print(self._format("WARN", message), file=sys.stdout)

    def error(self, message):
        if self._allowed("ERROR"):
            print(self._format("ERROR", message), file=sys.stderr)


# Singleton default logger (optional)
logger = Logger()
