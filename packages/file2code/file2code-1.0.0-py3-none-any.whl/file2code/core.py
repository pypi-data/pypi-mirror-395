import os
import base64
import secrets
from pathlib import Path
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

backend = default_backend()

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=400000,
        backend=backend,
    )
    return kdf.derive(password.encode())

def encrypt_file(input_path: str | Path, password: str | None = None) -> str:
    input_path = Path(input_path)
    if not input_path.is_file():
        raise FileNotFoundError(f"File not found: {input_path}")

    data = input_path.read_bytes()
    filename = input_path.name

    # Header: filename length (2 bytes) + filename
    filename_bytes = filename.encode("utf-8")
    header = len(filename_bytes).to_bytes(2, "big") + filename_bytes

    payload = header + data

    if password:
        salt = secrets.token_bytes(16)
        iv = secrets.token_bytes(16)
        key = _derive_key(password, salt)

        padder = padding.PKCS7(128).padder()
        padded = padder.update(payload) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded) + encryptor.finalize()

        final_data = salt + iv + encrypted
        prefix = "ENC1:"
    else:
        final_data = payload
        prefix = "RAW1:"

    return prefix + base64.b85encode(final_data).decode()

def decrypt_code(code: str, password: str | None = None, output_path: str | Path | None = None) -> Path:
    if code.startswith("ENC1:"):
        is_encrypted = True
        data = base64.b85decode(code[5:])
    elif code.startswith("RAW1:"):
        is_encrypted = False
        data = base64.b85decode(code[5:])
    else:
        raise ValueError("Invalid code – must start with ENC1: or RAW1:")

    if is_encrypted:
        if not password:
            raise ValueError("Password required for encrypted code")
        salt, iv, encrypted = data[:16], data[16:32], data[32:]
        key = _derive_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padded = decryptor.update(encrypted) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        payload = unpadder.update(padded) + unpadder.finalize()
    else:
        payload = data

    filename_len = int.from_bytes(payload[:2], "big")
    filename = payload[2:2+filename_len].decode("utf-8")
    file_data = payload[2+filename_len:]

    output_path = Path(output_path) if output_path else Path(filename)
    output_path.write_bytes(file_data)
    return output_path.resolve()