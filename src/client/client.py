import os
import time
import json
import socket
import struct
import threading

from dotenv import load_dotenv

from src.common.utilities.logger import Logger
from src.common.utilities.utility import Utility

from src.common.constants.constants import CLIENT_TYPES, HEADER_LENGTH

load_dotenv()

HOST = os.getenv("CLIENT_HOST")
PORT = int(os.getenv("CLIENT_PORT"))


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = -1
        self.ui = None

    @Utility.timed_event()
    def connect(self):
        self.socket.connect((HOST, PORT))

        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

        while self.id == -1:
            time.sleep(0.1)

    def check_data_format(self, data):
        if not isinstance(data, dict):
            Logger.error("Client: data is not in the correct format")
            return False

        if "type" not in data:
            Logger.error("Server: 'type' is not present in data")
            return False

        if data["type"] not in CLIENT_TYPES:
            Logger.error(f"Server: 'type': {data['type']} is not a valid type")
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
            case "send_messages":
                self.handle_sent_messages(data["messages"])

    def set_id(self, id):
        self.id = id

    def handle_sending_message(self, message):
        self.send({"type": "message", "message": message})

    def handle_receiving_message(self, message):
        self.update_chat(message)

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
                return

            self.handle_server_data(data)
            Logger.info(f"Client: Received message: {data}")

    def receive_all(self, length):
        data = b""

        while len(data) < length:
            packet = self.socket.recv(length - len(data))

            if not packet:
                return None

            data += packet

        return data

    def send(self, data):
        message = json.dumps(data).encode("utf-8")
        message = struct.pack(">I", len(message)) + message

        self.socket.sendall(message)
