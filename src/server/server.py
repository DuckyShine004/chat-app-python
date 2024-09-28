import os
import ssl
import json
import struct
import socket
import threading

from dotenv import load_dotenv

from main import setup

from src.server.database.database import Database

from src.common.utilities.logger import Logger
from src.common.utilities.utility import Utility
from src.common.utilities.security import Security

from src.common.constants.constants import CIPHER, HEADER_LENGTH, PATHS, SERVER_TYPES


load_dotenv()

HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("SERVER_PORT"))


# Suppose we are retrieving using a key store like Amazon KMS
class Server:
    __CERTIFICATE = Utility.get_path(PATHS["certificates"], ["server.crt"])
    __KEY = Utility.get_path(PATHS["keys"], ["server.key"])

    def __init__(self):
        self.socket = self.get_socket()
        self.id = 0
        self.clients = [None, None]
        self.database = Database()

    def get_socket(self):
        unsecure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=self.__CERTIFICATE, keyfile=self.__KEY)
        context.set_ciphers(CIPHER)

        return context.wrap_socket(unsecure_socket)

    def add_client(self, id, connection):
        self.clients[id] = {
            "connection": connection,
            "username": None,
        }

        if id == 0:
            self.clients[id]["messages"] = []

        self.send(connection, {"type": "assign_id", "id": id})
        self.id += 1

        thread = threading.Thread(target=self.handle_client, args=(id,))
        thread.start()

    def handle_client_data(self, id, data):
        match data["type"]:
            case "login":
                self.handle_client_login(id, data["username"], data["password"])
            case "client_signup":
                self.handle_client_signup(id, data["username"], data["password"])
            case "message":
                self.handle_client_message(id, data["message"])
            case "receive_messages":
                self.handle_receive_messages()

    def handle_client_login(self, id, username, password):
        if not (username and password):
            self.send_server_login_error(id, "Username and password are required")
            return

        users = self.database.get_username_and_password(username, password)
        print("users:", users)

        if not users:
            self.send_server_login_error(id, "Incorrect username or password")
            return

        if users[0]["online"]:
            self.send_server_login_error(id, "User is already online")
            return

        self.send_server_login_error(id, "")

        self.clients[id]["username"] = username
        self.send_server_message_to_clients(f"{username} joined the chat")

    def handle_client_signup(self, id, username, password):
        if not (username and password):
            self.send_server_signup_error(id, "Username and password are required")
            return

        if len(self.database.get_username(username)) == 1:
            self.send_server_signup_error(id, "Username must be unique")
            return

        password = Security.get_hashed_password(password)

        self.database.create_user(username, password)
        self.send_server_signup_error(id, "")

        self.clients[id]["username"] = username
        self.send_server_message_to_clients(f"{username} joined the chat")

    def handle_client_message(self, id, message):
        serialised_message = {
            "username": self.clients[id]["username"],
            "message": message,
        }

        if self.clients[1] is None:
            self.clients[0]["messages"].append(serialised_message)
            Logger.warn("Server: Second user has not joined the server yet")
            return

        self.send_message_to_client(id, message)

    def handle_receive_messages(self):
        self.send(
            self.clients[1]["connection"],
            {"type": "send_messages", "messages": self.clients[0]["messages"]},
        )

    def handle_client(self, id):
        connection = self.clients[id]["connection"]

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

    def send_server_login_error(self, id, error):
        data = {"type": "server_login_error", "error": error}
        self.send(self.clients[id]["connection"], data)

    def send_server_signup_error(self, id, error):
        data = {"type": "server_signup_error", "error": error}
        self.send(self.clients[id]["connection"], data)

    def send_message_to_client(self, id, message):
        receiver_id = id ^ 1
        serialised_message = {
            "username": self.clients[id]["username"],
            "message": message,
        }

        data = {"type": "receive_message", "message": serialised_message}
        self.send(self.clients[receiver_id]["connection"], data)

    def send_server_message_to_clients(self, message):
        for client in self.clients:
            if client is not None:
                data = {"type": "server_message", "message": message}
                self.send(client["connection"], data)

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
        data = bytearray()

        while len(data) < length:
            packet = connection.recv(length - len(data))

            if not packet:
                return None

            data.extend(packet)

        return data

    def send(self, connection, data):
        message = json.dumps(data).encode("utf-8")
        message = struct.pack(">I", len(message)) + message

        connection.sendall(message)

    def start(self):
        Logger.info(f"Server: Listening for connections on {HOST}:{PORT}")
        self.socket.bind((HOST, PORT))
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

    def disconnect_all_connections(self):
        for id, client in enumerate(self.clients):
            if client is not None:
                client["connection"].close()
                Logger.info(f"Server: Client {id} disconnected")

        self.socket.close()
        Logger.info("Server: Server disconnected")


if __name__ == "__main__":
    setup()

    Server().start()
