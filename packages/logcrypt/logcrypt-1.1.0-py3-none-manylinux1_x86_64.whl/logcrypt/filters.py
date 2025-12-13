import logging
import uuid
import re

class CorrelationIdFilter(logging.Filter):
    """Add correlation ID to log records."""
    def __init__(self, correlation_id=None):
        super().__init__()
        self.correlation_id = correlation_id or str(uuid.uuid4())

    def filter(self, record):
        record.correlation_id = self.correlation_id
        return True

class RedactionFilter(logging.Filter):
    """Redact sensitive patterns from log messages."""
    def __init__(self, patterns=None):
        super().__init__()
        self.patterns = [re.compile(p) for p in (patterns or [])]

    def filter(self, record):
        if isinstance(record.msg, str):
            for pattern in self.patterns:
                record.msg = pattern.sub('REDACTED', record.msg)
        return True