import os
import json
import struct
import socket
import threading

from dotenv import load_dotenv

from main import setup

from src.common.utilities.logger import Logger

from src.common.constants.constants import HEADER_LENGTH


load_dotenv()

HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("SERVER_PORT"))


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self, connection):
        while True:
            data = self.receive(connection)

            if not data:
                break

            data = json.loads(data.decode("utf-8"))

            Logger.info(f"Server: Received data from client: {data}")
            # connection.sendall(data)

        connection.close()
        Logger.info("Server: Closed client connection.")

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

    def start(self):
        Logger.info(f"Server: Listening for connections on {HOST}:{PORT}")
        self.socket.bind((HOST, PORT))
        self.socket.listen()

        try:
            while True:
                connection, address = self.socket.accept()
                Logger.info(f"Server: Client connection from {address}")

                thread = threading.Thread(target=self.handle_client, args=(connection,))
                thread.start()
        finally:
            self.socket.close()
            Logger.info("Server: Socket closed.")


if __name__ == "__main__":
    setup()

    Server().start()
