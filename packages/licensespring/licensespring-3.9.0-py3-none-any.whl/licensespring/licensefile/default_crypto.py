from __future__ import annotations

import base64
import binascii

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding


class DefaultCryptoProvider:
    """Handling encryption and decryption of strings (JSON)/licensefile"""

    def __init__(self, key=None, iv=None):
        self._key = key
        self._iv = iv

    @property
    def key(self):
        return self._key

    @property
    def iv(self):
        return self._iv

    def derive_key(self, password: str, salt: str, iterations=10000, dklen=32):
        """
        Derive a cryptographic key from a password and salt using PBKDF2 with HMAC-SHA256.
        """
        self._key = binascii.hexlify(
            PBKDF2(
                password, salt, dkLen=dklen, count=iterations, hmac_hash_module=SHA256
            )
        ).decode()

        return self._key

    def generate_random_iv(self, block_size=16):
        """
        Generate a cryptographic IV
        """
        self._iv = binascii.hexlify(get_random_bytes(block_size)).decode()
        return self._iv

    def encrypt(self, input_string: str):
        """
        Encrypt a string
        """
        cipher = AES.new(
            binascii.unhexlify(self._key), AES.MODE_CBC, binascii.unhexlify(self._iv)
        )
        padded_data = Padding.pad(input_string.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded_data)

        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, input_data: str):
        """
        Decrypt a string
        """
        encrypted_data = base64.b64decode(input_data)
        cipher = AES.new(
            binascii.unhexlify(self._key), AES.MODE_CBC, binascii.unhexlify(self._iv)
        )
        decrypted_padded = cipher.decrypt(encrypted_data)
        decrypted = Padding.unpad(decrypted_padded, AES.block_size)
        return decrypted.decode()
