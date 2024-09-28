from datetime import datetime

import unqlite

from src.common.utilities.utility import Utility
from src.common.utilities.security import Security

from src.common.constants.constants import COLLECTIONS, PATHS


class Database:
    __DATABASE_FILE = Utility.get_path(PATHS["database"], ["chat.db"])

    def __init__(self):
        self.database = unqlite.UnQLite(self.__DATABASE_FILE)
        self.output_collection("users")
        self.initialise()
        self.output_collection("users")

    def initialise(self):
        self.clear_all_collections()
        self.database.collection("users").create()

    def create_user(self, username, password):
        timestamp = datetime.now().isoformat()

        self.database.collection("users").store(
            {
                "username": username,
                "password": password,
                "online": True,
                "created_at": timestamp,
            }
        )

        self.output_collection("users")

    def create_message(self): ...

    def get_username(self, username):
        return self.database.collection("users").filter(lambda user: user["username"] == username)

    def get_username_and_password(self, username, password):
        return self.database.collection("users").filter(
            lambda user: user["username"] == username and Security.check_password(password, user["password"])
        )

    def output_collection(self, collection_name):
        print(self.database.collection(collection_name).all())

    def clear_all_collections(self):
        for collection in COLLECTIONS:
            self.database.collection(collection).drop()
