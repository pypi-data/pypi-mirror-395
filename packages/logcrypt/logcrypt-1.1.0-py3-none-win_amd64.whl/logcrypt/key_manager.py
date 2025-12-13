import os
import logging
import base64
import binascii

def _setup_console_logger():
    """Configure a console-only logger for key management messages."""
    console_logger = logging.getLogger("key_manager")
    console_logger.setLevel(logging.INFO)
    console_logger.handlers = []  # Clear any existing handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    console_logger.addHandler(console_handler)
    return console_logger

def _validate_key_bytes(key_bytes):
    """Validate the decoded key bytes for RC4 compatibility."""
    if len(key_bytes) not in range(5, 257):
        raise ValueError("RC4 key must be 5-256 bytes in length")

def _load_key_from_file(key_file, logger):
    """Attempt to load and validate a base64-encoded key from a file."""
    try:
        with open(key_file, "r", encoding='utf-8') as f:
            key = f.read().strip()
        key_bytes = base64.b64decode(key)
        _validate_key_bytes(key_bytes)
        logger.info(f"Loaded valid base64-encoded encryption key from {key_file}")
        return key
    except (OSError, binascii.Error, ValueError) as e:
        logger.error(f"Invalid base64-encoded key in {key_file}: {e}; generating a new one")
        raise

def _generate_and_save_key(key_file, logger):
    """Generate a new 16-byte key, encode it, and save to file."""
    try:
        new_key_bytes = os.urandom(16)
        new_key = base64.b64encode(new_key_bytes).decode('utf-8')
        with open(key_file, "w", encoding='utf-8') as f:
            f.write(new_key)
        logger.info(f"Generated and saved new base64-encoded encryption key to {key_file}")
        return new_key
    except OSError as e:
        logger.error(f"Failed to save base64-encoded encryption key to {key_file}: {e}")
        raise

def generate_key(encryption_key, key_file):
    """
    Load or generate an RC4 encryption key as a base64-encoded string.

    Prioritizes a provided key, then an existing file, and generates a new one if necessary.
    """
    logger = _setup_console_logger()

    if encryption_key:
        try:
            key_bytes = base64.b64decode(encryption_key)
            _validate_key_bytes(key_bytes)
            logger.info("Using provided base64-encoded encryption key")
            return encryption_key
        except (binascii.Error, ValueError) as e:
            logger.error(f"Provided base64-encoded key is invalid: {e}; generating a new one")

    if os.path.exists(key_file):
        try:
            return _load_key_from_file(key_file, logger)
        except Exception:
            pass  # Proceed to generation on failure

    return _generate_and_save_key(key_file, logger)