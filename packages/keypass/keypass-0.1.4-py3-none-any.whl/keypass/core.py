import base64
import hashlib
import json
import platform
import socket
import uuid
from getpass import getpass

from cryptography.fernet import Fernet


def key32_from_string_sha256(phrase: str) -> bytes:
    raw32 = hashlib.sha256(phrase.encode("utf-8")).digest()
    return raw32


def fernet_key_from_string_sha256(phrase: str) -> bytes:
    raw32 = key32_from_string_sha256(phrase)
    return base64.urlsafe_b64encode(raw32)


def generate_key(phrase: str = None, bind_to_system: bool = False) -> bytes:
    """
    Generate a Fernet-compatible encryption key.

    Args:
        phrase (str): Optional user-provided key for personalization.
        bind_to_system (bool): If True, bind the key to system-specific information.

    Returns:
        bytes: A 32-byte Fernet-compatible key (urlsafe base64 encoded).
    """
    if phrase is None:
        phrase = ""

    if bind_to_system:
        system_name = platform.system()
        hostname = socket.gethostname()
        architecture = platform.machine()
        mac_address = str(uuid.getnode())
        system_info = f"{phrase}{system_name}{hostname}{mac_address}{architecture}"
        hashed_info = hashlib.sha256(system_info.encode()).digest()
        key = base64.urlsafe_b64encode(hashed_info[:32])
    else:
        key = fernet_key_from_string_sha256(phrase)

    return key


def pass_account() -> dict:
    """
    Prompt user for username and password via terminal.

    Returns:
        dict: Dictionary with 'username' and 'password' keys.
    """
    username = input("Username: ")
    password = getpass()
    return {"username": username, "password": password}


def encrypt(content: str | bytes | dict, key: str | bytes = None, bind_to_system: bool = False) -> bytes:
    """
    Encrypt the given content using a Fernet key.

    Args:
        content (str | bytes | dict): The content to encrypt.
        key (str | bytes): Encryption key (if None, auto-generated).
        bind_to_system (bool): If True, bind the key to system-specific information.

    Returns:
        bytes: The encrypted content.
    """
    if content is None:
        content = {}
    if isinstance(content, dict):
        content = json.dumps(content)
    if isinstance(content, str):
        content = content.encode()

    if not isinstance(key, bytes):
        key = generate_key(phrase=key, bind_to_system=bind_to_system)
    cipher = Fernet(key)

    return cipher.encrypt(content)


def decrypt(
    content: str | bytes, key: str | bytes = None, to_dict: bool = False, bind_to_system: bool = False
) -> bytes | dict:
    """
    Decrypt encrypted content using a Fernet key.

    Args:
        content (str | bytes): Encrypted content.
        key (str | bytes): Encryption key (if None, auto-generated).
        to_dict (bool): Whether to parse decrypted content as JSON.
        bind_to_system (bool): If True, bind the key to system-specific information.

    Returns:
        bytes | dict: Decrypted raw bytes or dict.
    """
    if isinstance(content, str):
        content = content.encode()

    if not isinstance(key, bytes):
        key = generate_key(phrase=key, bind_to_system=bind_to_system)
    cipher = Fernet(key)

    decrypted_content = cipher.decrypt(content)
    if to_dict:
        decrypted_content = json.loads(decrypted_content)

    return decrypted_content


def save(content: str | bytes | dict, file: str = None, key: str | bytes = None, bind_to_system: bool = True) -> bytes:
    """
    Encrypt and save content to a file.

    Args:
        content (str | bytes | dict): The content to encrypt and save.
        file (str): File path.
        key (str | bytes): Optional encryption key.
        bind_to_system (bool): If True, bind the key to system-specific information.

    Returns:
        bytes: Encrypted content.
    """
    if file is None:
        file = "./account.key"

    encrypted_content = encrypt(content=content, key=key, bind_to_system=bind_to_system)

    with open(file, "wb") as f:
        f.write(encrypted_content)

    return encrypted_content


def load(file: str = None, key: str | bytes = None, to_dict: dict = True, bind_to_system: bool = True) -> bytes | dict:
    """
    Load and decrypt content from a file.

    Args:
        file (str): File path to read from.
        key (str | bytes): Optional decryption key.
        to_dict (bool): Whether to decode JSON.
        bind_to_system (bool): If True, bind the key to system-specific information.

    Returns:
        bytes | dict: Decrypted content.
    """
    if file is None:
        file = "./account.key"

    with open(file, "rb") as f:
        content = f.read()

    decrypted_content = decrypt(content, key=key, to_dict=to_dict, bind_to_system=bind_to_system)

    return decrypted_content
