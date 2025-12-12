"""
Data Layer Encryption Utilities Module

This module contains encryption utility classes used by data layer mappers.
Only includes utilities that are actually used in the data layer.
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.conf import settings


class EncryptDecryptAES256:
    """
    AES256 encryption and decryption utility class.
    Used for encrypting and decrypting sensitive data in the data layer.
    """

    def __init__(self):
        self.cipher_key = bytes.fromhex(settings.AES_256_KEY)
        self.cipher_object = AES.new(self.cipher_key, AES.MODE_ECB)

    def encrypt_data(self, data_value, encrypt=True):
        if not data_value:
            return None

        if encrypt:
            data_bytes = data_value.encode("utf-8")
            encrypted_data = self.cipher_object.encrypt(pad(data_bytes, AES.block_size))
            return encrypted_data.hex()
        else:
            return data_value

    def decrypt_data(self, encrypted_data, decrypt=True):
        if not encrypted_data:
            return None

        if not decrypt:
            return encrypted_data

        try:
            encrypted_bytes = bytes.fromhex(encrypted_data)
            ciphered_data = self.cipher_object.decrypt(encrypted_bytes)
            decrypt_data = unpad(ciphered_data, AES.block_size).decode("utf-8")
            return decrypt_data
        except Exception:
            return encrypted_data

    def update_encoded_value(self, key, user_data, encoded_column_key):
        if key in user_data:
            if encoded_column_key in user_data:
                decrypted_existing_value = self.decrypt_data(
                    user_data[encoded_column_key]
                )
                if decrypted_existing_value != user_data[key]:
                    user_data[encoded_column_key] = self.encrypt_data(user_data[key])
            else:
                user_data[encoded_column_key] = self.encrypt_data(user_data[key])
