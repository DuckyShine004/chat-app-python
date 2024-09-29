"""This module provides useful APIs for security checks."""

import os
import base64
import bcrypt

from Crypto.Cipher import PKCS1_OAEP

from Crypto.PublicKey import RSA

from src.common.utilities.logger import Logger
from src.common.utilities.utility import Utility

from src.common.constants.constants import KEY_LENGTH, PATHS


class Security:
    """The Security class provides global static APIs for security purposes."""

    @staticmethod
    def generate_rsa_keys(is_server: bool, key_length: int = KEY_LENGTH) -> None:
        """Generate a pair of public and private keys using RSA algorithm. The
        default length is 2048 to offer great end-to-end security.

        Args:
            is_server: is it the client or server keys
            key_length: the length of the key
        """

        key = RSA.generate(key_length)

        private_key = key.export_key()
        public_key = key.publickey().export_key()

        Security.save_keys(private_key, public_key, is_server)

    @staticmethod
    def get_key_path(is_private: bool, is_server: bool) -> str:
        """Retrieves the fixed key path based on some conditions.

        Args:
            is_private: is the key public or private
            is_server: is this for the client or the server

        Returns: the path to the key
        """

        prefix = "server_" if is_server else "client_"
        filename = prefix + ("private" if is_private else "public") + ".pem"

        return Utility.get_path(PATHS["keys"], [filename])

    @staticmethod
    def save_key(key: bytes, path: str) -> None:
        """Saves the key (either public or private).

        Args:
            key: the key
            path: the path in which the key will be saved to
        """

        if os.path.isfile(path):
            Logger.info(f"Server: RSA key is already generated and is stored in {path}")
            return

        with open(path, "wb") as file:
            file.write(key)

    @staticmethod
    def save_keys(private_key: bytes, public_key: bytes, is_server: bool) -> None:
        """Saves the public and private key pairs using local storage. In
        practice, we would use a trusted key-store.

        Args:
            private_key: the private key
            public_key: the public key
            is_server: is this for the client or the server
        """

        private_key_path = Security.get_key_path(True, is_server)
        public_key_path = Security.get_key_path(False, is_server)

        Security.save_key(private_key, private_key_path)
        Security.save_key(public_key, public_key_path)

    @staticmethod
    def get_key(is_private: bool, is_server: bool) -> RSA.RsaKey:
        """Retrieves a public or private key for a client or server.

        Args:
            is_private: is it private or public key
            is_server: is it for the client or the server

        Returns: the key for either client or server
        """

        path = Security.get_key_path(is_private, is_server)

        with open(path, "rb") as file:
            return RSA.import_key(file.read())

    @staticmethod
    def encrypt(public_pki: bytes, message: str) -> str:
        """Encrypts the message using the public key.

        Args:
            public_pki: the public key PEM
            message: the message to be encrypted

        Returns: the encrypted message
        """

        public_key = RSA.import_key(public_pki)
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher.encrypt(message.encode("utf-8"))

        return encrypted_message.hex()

    @staticmethod
    def decrypt(private_pki: bytes, message: str) -> str:
        """Decrypts the message using a private key.

        Args:
            private_pki: the private key PEM
            message: the message to be decrypted

        Returns: the decrypted message
        """

        encrypted_message = bytes.fromhex(message)
        private_key = RSA.import_key(private_pki)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(encrypted_message)

        return decrypted_message.decode("utf-8")

    @staticmethod
    def get_hashed_password(password: str) -> str:
        """Retrieve a random salt hash for the plain text password using the
        bcrypt library.

        Args:
            password: the plain text password

        Returns: the hashed password
        """

        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        return base64.b64encode(password).decode("utf-8")

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """Checks if the input password matches the hashed password.

        Args:
            password: the password
            hashed_password: the hashed password

        Returns: the validity of the match
        """

        hashed_password = base64.b64decode(hashed_password.encode("utf-8"))

        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
