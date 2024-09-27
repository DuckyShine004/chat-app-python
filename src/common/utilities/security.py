import os

from Crypto.Cipher import PKCS1_OAEP

from Crypto.PublicKey import RSA

from src.common.utilities.logger import Logger
from src.common.utilities.utility import Utility

from src.common.constants.constants import KEY_LENGTH, PATHS


class Security:
    @staticmethod
    def generate_rsa_keys(is_server, key_length=KEY_LENGTH):
        key = RSA.generate(key_length)

        private_key = key.export_key()
        public_key = key.publickey().export_key()

        Security.save_keys(private_key, public_key, is_server)

    @staticmethod
    def get_key_path(is_private, is_server):
        prefix = "server_" if is_server else "client_"
        filename = prefix + ("private" if is_private else "public") + ".pem"

        return Utility.get_path(PATHS["keys"], [filename])

    @staticmethod
    def save_key(key, path):
        if os.path.isfile(path):
            Logger.info(f"Server: RSA key is already generated and is stored in {path}")
            return

        with open(path, "wb") as file:
            file.write(key)

    @staticmethod
    def save_keys(private_key, public_key, is_server):
        private_key_path = Security.get_key_path(True, is_server)
        public_key_path = Security.get_key_path(False, is_server)

        Security.save_key(private_key, private_key_path)
        Security.save_key(public_key, public_key_path)

    @staticmethod
    def get_key(is_private, is_server):
        path = Security.get_key_path(is_private, is_server)

        with open(path, "rb") as file:
            return RSA.import_key(file.read())

    @staticmethod
    def encrypt(public_pki, message):
        public_key = RSA.import_key(public_pki)
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message.encode("utf-8"))

        return encrypted_message.hex()

    @staticmethod
    def decrypt(private_pki, message):
        encrypted_message = bytes.fromhex(message)
        private_key = RSA.import_key(private_pki)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(encrypted_message)

        return decrypted_message.decode("utf-8")
