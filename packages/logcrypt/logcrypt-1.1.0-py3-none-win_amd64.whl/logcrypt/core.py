import logging
import hashlib
from queue import Queue
from logging.handlers import QueueHandler, QueueListener
from .formatters import ColoredFormatter, JsonFormatter
from .filters import CorrelationIdFilter, RedactionFilter
from .key_manager import generate_key
from .cryptography import encrypt_message

# ----- Custom file handler for encrypted logs -----
class EncryptedFileHandler(logging.FileHandler):
    def __init__(self, filename, encryption_key, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self.encryption_key = encryption_key

    def emit(self, record):
        try:
            # Format the record first (handles text or JSON)
            formatted = self.format(record)
            checksum = hashlib.sha256(formatted.encode('utf-8')).hexdigest()
            encrypted = encrypt_message(formatted, self.encryption_key)
            msg_to_write = f"{checksum}:{encrypted}"
            self.stream.write(msg_to_write + self.terminator)
            self.flush()
        except Exception as e:
            self.handleError(record)

# ----- Custom logger -----
class Logger:
    def __init__(
        self,
        file_name=None,
        log_level="INFO",
        correlation_id=None,
        encrypt_file=False,
        encryption_key=None,
        key_file=None,
        file_format='text',  # New: 'text' or 'json'
        async_logging=False,  # New: Enable asynchronous logging
        redact_patterns=None  # New: List of regex patterns for redaction
    ):
        # Create logger
        self.logger = logging.getLogger("custom_logger")
        self.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        self.encryption_key = None
        self.file_handler = None
        self.encrypt_file = encrypt_file
        self.async_logging = async_logging
        self.listener = None

        # Clear existing handlers
        self.logger.handlers.clear()

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter())
        self.logger.addHandler(console_handler)
        self.logger.addFilter(CorrelationIdFilter(correlation_id))
        # Add correlation ID filter if provided
        if correlation_id:
            self.logger.addFilter(CorrelationIdFilter(correlation_id))

        # Add redaction filter if patterns provided
        if redact_patterns:
            self.logger.addFilter(RedactionFilter(redact_patterns))

        # Handle encryption key first
        if encrypt_file:
            self.encryption_key = generate_key(encryption_key, key_file)
            self.logger.info(f"Encryption enabled with key from {key_file or 'provided key'}")

        # Add file handler if needed
        if file_name:
            if encrypt_file and self.encryption_key:
                self.file_handler = EncryptedFileHandler(file_name, self.encryption_key)
            else:
                self.file_handler = logging.FileHandler(file_name)

            # Set formatter based on file_format
            if file_format == 'json':
                self.file_handler.setFormatter(JsonFormatter())
            else:
                self.file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s>%(levelname)s>%(correlation_id)s>%(message)s'
                ))

            # Handle async logging
            if async_logging:
                self.queue = Queue(-1)
                queue_handler = QueueHandler(self.queue)
                self.listener = QueueListener(self.queue, self.file_handler)
                self.listener.start()
                self.logger.addHandler(queue_handler)
            else:
                self.logger.addHandler(self.file_handler)

    # ----- Internal logging method -----
    def _log(self, level, message, extra=None):
        self.logger.log(level, message, extra=extra)

    # ----- Convenience methods -----
    def debug(self, message, extra=None):
        self._log(logging.DEBUG, message, extra)

    def info(self, message, extra=None):
        self._log(logging.INFO, message, extra)

    def warning(self, message, extra=None):
        self._log(logging.WARNING, message, extra)

    def error(self, message, extra=None):
        self._log(logging.ERROR, message, extra)

    def critical(self, message, extra=None):
        self._log(logging.CRITICAL, message, extra)

    def success(self, message, extra=None):
        self._log(logging.SUCCESS, message, extra)

    def fail(self, message, extra=None):
        self._log(logging.FAIL, message, extra)

    # ----- Cleanup method -----
    def close(self):
        if self.listener:
            self.listener.stop()
        if self.file_handler:
            self.file_handler.close()
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)