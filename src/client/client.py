import os
import json
import socket
import struct
import threading

from dotenv import load_dotenv

from src.common.utilities.logger import Logger

from src.common.constants.constants import HEADER_LENGTH

load_dotenv()

HOST = os.getenv("CLIENT_HOST")
PORT = int(os.getenv("CLIENT_PORT"))


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((HOST, PORT))

        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

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
