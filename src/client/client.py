"""This module contains the code for defining a client interface."""

from __future__ import annotations

import os
import time
import json
import socket
import struct
import threading

from ssl import SSLSocket, SSLContext, PROTOCOL_TLS_CLIENT

from typing import Any, List, Union, TYPE_CHECKING

from dotenv import load_dotenv

from src.common.utilities.logger import Logger
from src.common.utilities.utility import Utility

from src.common.constants.constants import CLIENT_TYPES, HEADER_LENGTH, PATHS

if TYPE_CHECKING:
    from src.client.ui.ui import UI

load_dotenv()


class Client:
    """The Client class containing client-side APIs.

    Attributes:
        __HOST: the client host
        __PORT: the client port
        __CERTIFICATE: the server certificate
        socket: the client socket secured under TLS
        id: the client id
        ui: the client ui
    """

    __HOST: str = os.getenv("CLIENT_HOST")
    __PORT: int = int(os.getenv("CLIENT_PORT"))
    __CERTIFICATE: str = Utility.get_path(PATHS["certificates"], ["server.crt"])

    def __init__(self) -> None:
        """Initialises the Client instance."""

        self.socket: SSLSocket = self.get_secure_socket()
        self.id: int = -1
        self.ui: UI = None

    def get_secure_socket(self) -> SSLSocket:
        """Returns a secure socket wrapped with a TLS protection layer.

        Returns: a secure socket wrapped with a protection layer; TLS
        """

        unsecure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = SSLContext(PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(self.__CERTIFICATE)

        return context.wrap_socket(unsecure_socket, server_hostname=self.__HOST)

    @Utility.timed_event()
    def connect(self):
        """Connects the client to the server.

        This is a blocking call, as the client should retrieve an id
        before proceeding.
        """

        self.socket.connect((self.__HOST, self.__PORT))

        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

        while self.id == -1:
            time.sleep(0.1)

    def check_data_format(self, data: Any) -> bool:
        """Check if the data sent from the server is valid or not. It should
        include a 'type', so that the corresponding RPC can be executed.

        Args:
            data: the data sent from the server

        Returns: the validity of the data
        """

        if not isinstance(data, dict):
            Logger.error("Client: Data is not in the correct format")
            return False

        if "type" not in data:
            Logger.error("Client: 'type' is not present in data")
            return False

        if data["type"] not in CLIENT_TYPES:
            Logger.error(f"Client: 'type': {data['type']} is not a valid type")
            return False

        return True

    def handle_server_data(self, data: Any) -> None:
        """Handles the data sent by the server with the corresponding id. It
        executes the corresponding RPC.

        Args:
            data: the data sent by the server
        """

        if data["type"] == "server_assign_id":
            self.id = data["id"]
        if data["type"] == "server_message":
            self.handle_server_message(data["message"])
        if data["type"] == "server_messages":
            self.handle_server_messages(data["messages"])
        if data["type"] == "server_login_error":
            self.handle_server_login_error(data["error"])
        if data["type"] == "server_signup_error":
            self.handle_server_signup_error(data["error"])
        if data["type"] == "server_exchange_usernames":
            self.handle_second_username(data["username"])

    def handle_second_username(self, second_username: str) -> None:
        """Updates the chat title to who the current user is chatting with.

        Args:
            second_username: the second user's username
        """

        self.ui.chat_label_signal.emit(second_username)

    def handle_server_message(self, message: str) -> None:
        """Handles messages sent by the server by updating the chat
        accordingly. Messages sent by the server could be from other clients as
        well.

        Args:
            message: the message sent by the server
        """

        self.update_chat(message)

    def handle_server_login_error(self, error: str) -> None:
        """Handles the login error sent by the server.

        Args:
            error: the error sent by the server
        """

        self.ui.login_error_signal.emit(error)

    def handle_server_signup_error(self, error: str) -> None:
        """Handles the signup error sent by the server.

        Args:
            error: the error sent by the server
        """

        self.ui.signup_error_signal.emit(error)

    def handle_server_messages(self, messages: List[Any]) -> None:
        """Updates the current client's chat based on messages sent by other
        clients and the messages stored on the server.

        Args:
            messages: the list of messages
        """

        for message in messages:
            self.update_chat(message)

    def update_chat(self, message: Any) -> None:
        """Updates the chat because the UI is running on a separate thread, and
        must therefore be called within the client code.

        Args:
            message: the message to be sent to the chat
        """

        self.ui.new_message_signal.emit(message["role"], message)

    def receive(self) -> Union[bytearray, None]:
        """Receive data based on the length of the incoming data. Returns a
        50-byte payload. Either all or no data is returned.

        Returns: data in the form of a bytearray or nothing
        """

        while True:
            raw_length = self.receive_all(HEADER_LENGTH)

            if not raw_length:
                break

            length = struct.unpack(">I", raw_length)[0]
            message = self.receive_all(length)

            if not message:
                break

            data = json.loads(message.decode("utf-8"))

            if not self.check_data_format(data):
                break

            self.handle_server_data(data)
            Logger.info(f"Client: Received message: {data}")

    def receive_all(self, length: int) -> Union[bytearray, None]:
        """Receive all data sent from the server. If the server connection is
        closed then nothing will be returned.

        Args:
            length: the size of the data to be retrieved

        Returns: data in the form of a bytearray or nothing
        """

        data = bytearray()

        while len(data) < length:
            packet = self.socket.recv(length - len(data))

            if not packet:
                return None

            data.extend(packet)

        return data

    def send(self, data: Any) -> None:
        """Sends data to the server. The payload contains the header along with
        the data.

        Args:
            data: the data to be sent to the server
        """

        message = json.dumps(data).encode("utf-8")
        message = struct.pack(">I", len(message)) + message

        self.socket.sendall(message)
