import unqlite

from src.common.utilities.utility import Utility

from src.common.constants.constants import COLLECTIONS, PATHS


class Database:
    __DATABASE_FILE = Utility.get_path(PATHS["database"], ["chat.db"])

    def __init__(self):
        self.database = unqlite.UnQLite(self.__DATABASE_FILE)

        self.initialise()

    def initialise(self):
        self.database.collection("users").create()

    def create_user(self, username, password):
        hashed_password = password

        self.database.collection("users").store(
            {
                "username": username,
                "password": hashed_password,
            }
        )

    def get_username(self, username):
        return self.database.collection("users").filter(lambda user: user["username"])

    def get_username_and_password(self, username, password):
        return self.database.collection("users").filter(
            lambda user: user["username"] == username and user["password"] == password
        )

    def output_collection(self, collection_name):
        print(self.database.collection(collection_name).all())

    def clear_all_collections(self):
        for collection in COLLECTIONS:
            self.database.collection(collection).drop()


if __name__ == "__main__":
    database = Database()
