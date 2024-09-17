import os
import json
import struct
import socket
import threading

from dotenv import load_dotenv

from main import setup

from src.common.utilities.logger import Logger

from src.common.constants.constants import HEADER_LENGTH, SERVER_TYPES


load_dotenv()

HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("SERVER_PORT"))


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = 0
        self.clients = {}

    def add_client(self, id, connection):
        self.clients[id] = {
            "connection": connection,
            "username": "",
            "received_messages": [],
            "sent_messages": [],
        }

        self.send(connection, {"type": "assign_id", "id": id})
        self.id += 1

        thread = threading.Thread(target=self.handle_client, args=(id,))
        thread.start()

    def get_receiver_id(self, id):
        for client_id in self.clients:
            if client_id != id:
                return client_id

        return -1

    def handle_client_data(self, id, data):
        match data["type"]:
            case "login":
                self.handle_client_login(id, data["username"])
            case "message":
                self.handle_client_message(id, data["message"])

    def handle_client_login(self, id, username):
        self.clients[id]["username"] = username

    def handle_client_message(self, id, message):
        receiver_id = self.get_receiver_id(id)

        if receiver_id == -1:
            Logger.warn("Server: Second user has not joined the server yet")
            return

        self.clients[id]
        self.clients[receiver_id]["messages"].append(message)

    def handle_client(self, id):
        connection = self.clients[id]["connection"]

        while True:
            data = self.receive(connection)

            if not data:
                break

            data = json.loads(data.decode("utf-8"))

            if not self.check_data_format(data):
                return

            self.handle_client_data(id, data)
            Logger.info(f"Server: Received data from client: {data}")

        connection.close()
        Logger.info("Server: Closed client connection.")

    def check_data_format(self, data):
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

    def receive(self, connection):
        raw_length = self.receive_all(connection, HEADER_LENGTH)

        if not raw_length:
            return None

        length = struct.unpack(">I", raw_length)[0]

        return self.receive_all(connection, length)

    def receive_all(self, connection, length):
        data = b""

        while len(data) < length:
            packet = connection.recv(length - len(data))

            if not packet:
                return None

            data += packet

        return data

    def send(self, connection, data):
        message = json.dumps(data).encode("utf-8")
        message = struct.pack(">I", len(message)) + message

        connection.sendall(message)

    def start(self):
        Logger.info(f"Server: Listening for connections on {HOST}:{PORT}")
        self.socket.bind((HOST, PORT))
        self.socket.listen()

        try:
            while True:
                connection, address = self.socket.accept()

                if self.id == 2:
                    Logger.error("Server: Only a maximum of two clients can be connected")
                    pass
                    # continue

                self.add_client(self.id, connection)
                Logger.info(f"Server: Client connection from {address}")

        finally:
            self.socket.close()
            Logger.info("Server: Socket closed.")


if __name__ == "__main__":
    setup()

    Server().start()
