import base64
import gzip
import json
import os
from typing import Any

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from . import bfile, bfunc
from .btype import XPath

FLAG = 'bcrypto---'


def encrypt(data: bytes, password: str) -> bytes:
    compressData = gzip.compress(data)
    if len(compressData) < len(data):
        data = compressData
    assert len(data) < 200 * 1024, '内容太大无法加密'
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = _getEncryptKey(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    result = salt + iv + encrypted_message
    result = bfunc.obfuscate(result)
    return result


def encryptText(data: str, password: str) -> str:
    content = encrypt(data.encode(), password)
    return FLAG + base64.b64encode(content).decode('utf-8')


def encryptJson(data: dict[str, Any], password: str) -> str:
    content = bfunc.jsonDumpsMini(data)
    return encryptText(content, password)


async def encryptFile(file: XPath, password: str) -> None:
    data = await bfile.readBytes(file)
    data = FLAG.encode() + encrypt(data, password)
    await bfile.writeBytes(file, data)


def decrypt(data: bytes, password: str) -> bytes:
    data = bfunc.deobfuscate(data)
    salt = data[:16]
    iv = data[16:32]
    data = data[32:]
    key = _getEncryptKey(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    result = unpadder.update(decrypted_message) + unpadder.finalize()
    try:
        result = gzip.decompress(result)
    except:
        pass
    return result


def decryptText(data: str, password: str) -> str:
    data = data.strip().replace('\n', ' ').split(' ')[::-1][0]
    if data.startswith(FLAG):
        data = data[len(FLAG):]
    content = decrypt(base64.b64decode(data), password)
    return content.decode()


def decryptJson(data: str, password: str) -> dict[str, Any]:
    content = decryptText(data, password)
    return json.loads(content)


async def decryptFile(file: XPath, password: str) -> None:
    data = await bfile.readBytes(file)
    flag = FLAG.encode()
    if data.startswith(flag):
        data = data[len(flag):]
    data = decrypt(data, password)
    await bfile.writeBytes(file, data)


# ------------------------------------------------------------------------------------


def _getEncryptKey(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())
