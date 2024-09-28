from datetime import datetime

import unqlite

from src.common.utilities.utility import Utility
from src.common.utilities.security import Security

from src.common.constants.constants import COLLECTIONS, PATHS


class Database:
    __DATABASE_FILE = Utility.get_path(PATHS["database"], ["chat.db"])

    def __init__(self):
        self.database = unqlite.UnQLite(self.__DATABASE_FILE)

        self.initialise()

    def initialise(self):
        self.clear_collections()
        self.create_collections()

    def create_collections(self):
        for collection in COLLECTIONS:
            self.database.collection(collection).create()

    def create_user(self, username, password):
        timestamp = datetime.now().isoformat()

        user = {
            "username": username,
            "password": password,
            "online": True,
            "created_at": timestamp,
        }

        self.database.collection("users").store(user)

    def create_message(self, role, username, content):
        timestamp = datetime.now().isoformat()

        message = {
            "role": role,
            "username": username,
            "content": content,
            "timestamp": timestamp,
        }

        self.database.collection("messages").store(message)

    def get_username(self, username):
        return self.database.collection("users").filter(lambda user: user["username"] == username)

    def get_username_and_password(self, username, password):
        return self.database.collection("users").filter(
            lambda user: user["username"] == username and Security.check_password(password, user["password"])
        )

    def get_messages(self):
        messages = self.database.collection("messages").all()

        return sorted(messages, key=lambda message: message["timestamp"])

    def output_collection(self, collection_name):
        print(self.database.collection(collection_name).all())

    def clear_collections(self):
        for collection in COLLECTIONS:
            self.database.collection(collection).drop()
