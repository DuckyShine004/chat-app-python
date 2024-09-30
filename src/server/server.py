"""This module contains the code for defining a server interface."""

import os
import json
import struct
import socket
import threading

from ssl import SSLContext, SSLSocket, PROTOCOL_TLS_SERVER

from typing import Any, List, Union

from dotenv import load_dotenv

from main import setup

from src.server.database.database import Database

from src.server.context.context import Context

from src.common.utilities.logger import Logger
from src.common.utilities.utility import Utility
from src.common.utilities.security import Security

from src.common.constants.constants import CIPHER, HEADER_LENGTH, MAX_CLIENTS, PATHS, SERVER_TYPES

load_dotenv()


class Server:
    """The Server class containing server-side APIs. The private key and
    certificate is generated using openSSL, however, in practice, we should use
    a trusted key-store and certificate-store like Amazon KMS.

    Attributes:
        __KEY: the server private key
        __HOST: the server host
        __PORT: the server port
        __CERTIFICATE: the digital certificate
        socket: the server socket secured under TLS
        id: the auto-incrementing client id
        clients: a list containing client resources
        database: the database
    """

    __KEY = Utility.get_path(PATHS["keys"], ["server.key"])
    __HOST: str = os.getenv("SERVER_HOST")
    __PORT: int = int(os.getenv("SERVER_PORT"))
    __CERTIFICATE: str = Utility.get_path(PATHS["certificates"], ["server.crt"])

    def __init__(self) -> None:
        """Initialises the server class fields."""

        self.socket: SSLSocket = self.get_secure_socket()
        self.id: int = 0
        self.clients: List[Context] = [None, None]
        self.database: Database = Database()

    def get_secure_socket(self) -> SSLSocket:
        """Returns a secure socket wrapped with a TLS protection layer.

        Returns: a secure socket wrapped with a protection layer; TLS
        """

        unsecure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = SSLContext(PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=self.__CERTIFICATE, keyfile=self.__KEY)
        context.set_ciphers(CIPHER)

        return context.wrap_socket(unsecure_socket)

    def add_client(self, id: int, connection: SSLSocket) -> None:
        """Handles adding a new client connection. It sends the id assigned to
        the client connection to the client.

        Args:
            id: the client id
            connection: the client connection
        """

        self.clients[id] = Context(connection)

        self.send(connection, {"type": "server_assign_id", "id": id})
        self.id += 1

        thread = threading.Thread(target=self.handle_client, args=(id,))
        thread.start()

    def handle_client_data(self, id: int, data: Any) -> None:
        """Handles the data sent by the client with the corresponding id. It
        executes the corresponding RPC.

        Args:
            id: the client id
            data: the data sent by the client
        """

        if data["type"] == "client_login":
            self.handle_client_login(id, data["username"], data["password"])
        if data["type"] == "client_signup":
            self.handle_client_signup(id, data["username"], data["password"])
        if data["type"] == "client_message":
            self.handle_client_message(id, data["message"])

    def handle_client_login(self, id: int, username: str, password: str) -> None:
        """Handles the client login request.

        Args:
            id: the client id
            username: the user's username
            password: the user's password
        """

        if not self.check_login_details(id, username, password):
            return

        self.send_server_login_error(id, "")
        self.clients[id].username = username

        if self.clients[1] is not None:
            self.send_messages_to_second_client()
            self.exchange_usernames()

        self.send_server_message_to_clients(f"{username} joined the chat")

    def handle_client_signup(self, id: int, username: str, password: str) -> None:
        """Handles the client signup request.

        Args:
            id: the client id
            username: the user's username
            password: the user's password
        """

        if not self.check_signup_details(id, username, password):
            return

        password = Security.get_hashed_password(password)

        self.database.create_user(username, password)
        self.send_server_signup_error(id, "")
        self.clients[id].username = username

        if self.clients[1] is not None:
            self.send_messages_to_second_client()
            self.exchange_usernames()

        self.send_server_message_to_clients(f"{username} joined the chat")

    def handle_client_message(self, id: int, message: str) -> None:
        """Handles the client request when a message is sent.

        Args:
            id: the client id
            message: the message to be sent to the receiver
        """

        if self.clients[1] is None:
            self.database.create_message("client", message, self.clients[id].username)
            Logger.warn("Server: Second user has not joined the server yet")
            return

        self.send_message_to_client(id, message)

    def send_messages_to_second_client(self) -> None:
        """Sends stored messages to the second client."""

        data = {"type": "server_messages", "messages": self.database.get_messages()}
        self.send(self.clients[1].connection, data)

    def handle_client(self, id: int) -> None:
        """Handles the client connections. It handles any data sent from the
        client.

        Args:
            id: the client connection id
        """

        connection = self.clients[id].connection

        while True:
            data = self.receive(connection)

            if not data:
                break

            data = json.loads(data.decode("utf-8"))

            if not self.check_data_format(data):
                break

            self.handle_client_data(id, data)
            Logger.info(f"Server: Received data from client: {data}")

        connection.close()
        Logger.info(f"Server: Closed client {id} connection.")

    def send_server_login_error(self, id: int, error: str) -> None:
        """Sends a login error message to the client with the corresponding id.

        Args:
            id: the client id
            error: the error message
        """

        data = {"type": "server_login_error", "error": error}
        self.send(self.clients[id].connection, data)

    def exchange_usernames(self) -> None:
        """Exchange usernames between the first client and the second
        client."""

        for id in range(MAX_CLIENTS):
            data = {"type": "server_exchange_usernames", "username": self.clients[id ^ 1].username}
            self.send(self.clients[id].connection, data)

    def send_server_signup_error(self, id: int, error: str) -> None:
        """Sends a signup error message to the client with the corresponding
        id.

        Args:
            id: the client id
            error: the error message
        """

        data = {"type": "server_signup_error", "error": error}
        self.send(self.clients[id].connection, data)

    def send_message_to_client(self, id: int, message: str) -> None:
        """Sends a message to the receiver.

        Args:
            id: the sender
            message: the message to be sent to the receiver
        """

        receiver_id = id ^ 1

        serialised_message = {
            "role": "client",
            "username": self.clients[id].username,
            "content": message,
        }

        data = {"type": "server_message", "message": serialised_message}
        self.send(self.clients[receiver_id].connection, data)

    def send_server_message_to_clients(self, message: str) -> None:
        """Sends a server message to all clients.

        Args:
            message: the message to be sent to all clients
        """

        role = "server"

        serialised_message = {
            "role": role,
            "content": message,
        }

        for client in self.clients:
            if client is not None:
                data = {"type": "server_message", "message": serialised_message}
                self.send(client.connection, data)

        self.database.create_message(role, message)

    def check_data_format(self, data: Any) -> bool:
        """Check if the data sent from the client is valid or not. It should
        include a 'type', so that the corresponding RPC can be executed.

        Args:
            data: the data sent from the client

        Returns: the validity of the data
        """

        if not isinstance(data, dict):
            Logger.error("Server: data is not in the correct format")
            return False

        if "type" not in data:
            Logger.error("Server: 'type' is not present in data")
            return False

        if data["type"] not in SERVER_TYPES:
            Logger.error(f"Server: 'type': {data['type']} is not a valid type")
            return False

        return True

    def check_login_details(self, id: int, username: str, password: str) -> bool:
        """Validates the user's login details.

        Args:
            id: the client id
            username: the user's username
            password: the user's password

        Returns: the validity of their login details
        """

        if not (username and password):
            self.send_server_login_error(id, "Username and password are required")
            return False

        users = self.database.get_username_and_password(username, password)

        if not users:
            self.send_server_login_error(id, "Incorrect username or password")
            return False

        if users[0]["online"]:
            self.send_server_login_error(id, "User is already online")
            return False

        return True

    def check_signup_details(self, id: int, username: str, password: str) -> bool:
        """Validates the user's signup details.

        Args:
            id: the client id
            username: the user's username
            password: the user's password

        Returns: the validity of their signup details
        """

        if not (username and password):
            self.send_server_signup_error(id, "Username and password are required")
            return False

        if self.database.get_username(username):
            self.send_server_signup_error(id, "Username must be unique")
            return False

        return True

    def receive(self, connection: SSLSocket) -> Union[bytearray, None]:
        """Receive data based on the length of the incoming data. Returns a
        50-byte payload. Either all or no data is returned.

        Args:
            connection: the client connection

        Returns: data in the form of a bytearray or nothing
        """

        raw_length = self.receive_all(connection, HEADER_LENGTH)

        if not raw_length:
            return None

        length = struct.unpack(">I", raw_length)[0]

        return self.receive_all(connection, length)

    def receive_all(self, connection: SSLSocket, length: int) -> Union[bytearray, None]:
        """Receive all data sent from a client. If the client connection is
        closed then nothing will be returned.

        Args:
            connection: the client connection
            length: the size of the data to be retrieved

        Returns: data in the form of a bytearray or nothing
        """

        data = bytearray()

        while len(data) < length:
            packet = connection.recv(length - len(data))

            if not packet:
                return None

            data.extend(packet)

        return data

    def send(self, connection: SSLSocket, data: Any) -> None:
        """Sends data to the client. The payload contains the header along with
        the data.

        Args:
            connection: the client connection
            data: the data to be sent to the client
        """

        message = json.dumps(data).encode("utf-8")
        message = struct.pack(">I", len(message)) + message

        connection.sendall(message)

    def start(self) -> None:
        """Starts the server and listens for client connections.

        If the server connection closes, then client client connections
        will also be closed.
        """

        Logger.info(f"Server: Listening for connections on {self.__HOST}:{self.__PORT}")
        self.socket.bind((self.__HOST, self.__PORT))
        self.socket.listen(2)

        try:
            while True:
                connection, address = self.socket.accept()

                if self.id == 2:
                    Logger.error("Server: Only a maximum of two clients can be connected")
                    continue

                self.add_client(self.id, connection)
                Logger.info(f"Server: Client connection from {address}")
        finally:
            self.disconnect_all_connections()

    def disconnect_all_connections(self) -> None:
        """Disconnects all client connections."""

        for id, client in enumerate(self.clients):
            if client is not None:
                client.connection.close()
                Logger.info(f"Server: Client {id} disconnected")

        self.socket.close()
        Logger.info("Server: Server disconnected")


if __name__ == "__main__":
    setup()

    Server().start()
