import json
import logging
from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """
    Formatter for colored console output based on log levels.
    """

    LEVEL_COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.WHITE,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "FAIL": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def __init__(self) -> None:
        super().__init__("%(message)s")

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelname, Fore.WHITE)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


class JsonFormatter(logging.Formatter):
    """
    Formatter for structured JSON log output.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, "%Y/%m/%d %H:%M:%S,%f"),
            "level": record.levelname,
            "correlation_id": getattr(record, "correlation_id", "none"),
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)