import os
import ssl
import time
import json
import socket
import struct
import threading

from dotenv import load_dotenv

from src.common.utilities.logger import Logger
from src.common.utilities.utility import Utility

from src.common.constants.constants import CLIENT_TYPES, HEADER_LENGTH, PATHS

load_dotenv()

HOST = os.getenv("CLIENT_HOST")
PORT = int(os.getenv("CLIENT_PORT"))


class Client:
    __CERTIFICATE = Utility.get_path(PATHS["certificates"], ["server.crt"])

    def __init__(self):
        self.socket = self.get_socket()
        self.id = -1
        self.ui = None

    def get_socket(self):
        unsecure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(self.__CERTIFICATE)

        return context.wrap_socket(unsecure_socket, server_hostname=HOST)

    @Utility.timed_event()
    def connect(self):
        self.socket.connect((HOST, PORT))

        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

        while self.id == -1:
            time.sleep(0.1)

    def check_data_format(self, data):
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

    def handle_server_data(self, data):
        match data["type"]:
            case "assign_id":
                self.set_id(data["id"])
            case "message":
                self.handle_sending_message(data["message"])
            case "receive_message":
                self.handle_receiving_message(data["message"])
            case "server_message":
                self.handle_server_message(data["message"])
            case "send_messages":
                self.handle_sent_messages(data["messages"])
            case "server_login_error":
                self.handle_server_login_error(data["error"])
            case "server_signup_error":
                self.handle_server_signup_error(data["error"])

    def set_id(self, id):
        self.id = id

    def handle_sending_message(self, message):
        self.send({"type": "message", "message": message})

    def handle_receiving_message(self, message):
        self.update_chat(message)

    def handle_server_message(self, message):
        self.ui.new_server_message.emit(message)

    def handle_server_login_error(self, error):
        self.ui.login_error.emit(error)

    def handle_server_signup_error(self, error):
        self.ui.signup_error.emit(error)

    def handle_sent_messages(self, messages):
        for message in messages:
            self.update_chat(message)

    def update_chat(self, message):
        username = message["username"]
        content = message["message"]

        self.ui.new_message.emit(username, content)

    def receive(self):
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

    def receive_all(self, length):
        data = bytearray()

        while len(data) < length:
            packet = self.socket.recv(length - len(data))

            if not packet:
                return None

            data.extend(packet)

        return data

    def send(self, data):
        message = json.dumps(data).encode("utf-8")
        message = struct.pack(">I", len(message)) + message

        self.socket.sendall(message)
