import base64
import binascii
from Crypto.Cipher import ARC4

def encrypt_message(message: str, encryption_key: str) -> str:
    """
    Encrypt a message using RC4 with the provided base64-encoded key.

    Args:
        message: The plaintext message to encrypt.
        encryption_key: The base64-encoded RC4 key.

    Returns:
        The base64-encoded encrypted ciphertext.

    Raises:
        ValueError: If the message is not a string, the key is invalid, or encryption fails.
    """
    if not isinstance(message, str):
        raise ValueError("Message must be a string")

    try:
        key_bytes = base64.b64decode(encryption_key)
    except binascii.Error as e:
        raise ValueError(f"Invalid base64-encoded key: {e}")

    try:
        cipher = ARC4.new(key_bytes)
        message_bytes = message.encode('utf-8')
        encrypted_bytes = cipher.encrypt(message_bytes)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Encryption failed: {e}")

def decrypt_message(cipher: str, encryption_key: str) -> bytes:
    """
    Decrypt a ciphertext using RC4 with the provided base64-encoded key.

    Args:
        cipher: The base64-encoded ciphertext to decrypt.
        encryption_key: The base64-encoded RC4 key.

    Returns:
        The decrypted plaintext as bytes.

    Raises:
        ValueError: If the key or ciphertext is invalid, or decryption fails.
    """
    try:
        key_bytes = base64.b64decode(encryption_key)
    except binascii.Error as e:
        raise ValueError(f"Invalid base64-encoded key: {e}")

    try:
        cipher_bytes = base64.b64decode(cipher)
    except binascii.Error as e:
        raise ValueError(f"Invalid base64-encoded ciphertext: {e}")

    try:
        cipher = ARC4.new(key_bytes)
        return cipher.decrypt(cipher_bytes)
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")