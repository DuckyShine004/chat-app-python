"""This module contains the code for creating a database, and provides APIs for
the server to query and fetch data."""

from datetime import datetime, timezone

from typing import Any, Optional

import unqlite

from src.common.utilities.utility import Utility
from src.common.utilities.security import Security

from src.common.constants.constants import COLLECTIONS, PATHS


class Database:
    """The Database class provides APIs for querying and fetching data.

    Attributes:
        __DATABASE_FILE: the path to the database file on the disk
        database: the database instance using unqlite
    """

    __DATABASE_FILE = Utility.get_path(PATHS["database"], ["chat.db"])

    def __init__(self) -> None:
        """Initialises the Database instance."""

        self.database = unqlite.UnQLite(self.__DATABASE_FILE)

        # self.clear_collections()
        self.create_collections()

    def create_collections(self) -> None:
        """Creates all of the necessary collections."""

        for collection in COLLECTIONS:
            self.database.collection(collection).create()

    def create_user(self, username: str, password: str) -> None:
        """Creates and stores the user in the database given their username and
        password.

        Args:
            username: the username
            password: the password
        """

        timestamp = datetime.now(timezone.utc).isoformat()

        user = {
            "username": username,
            "password": password,
            "online": True,
            "created_at": timestamp,
        }

        self.database.collection("users").store(user)

    def create_message(self, role: str, content: str, username: Optional[str] = "") -> None:
        """Creates a message to be stored in the database.

        Args:
            role: the role, can be client or server, ideally should be using enums
            content: the content to be stored
            username: the username
        """

        timestamp = datetime.now(timezone.utc).isoformat()

        message = {
            "role": role,
            "username": username,
            "content": content,
            "timestamp": timestamp,
        }

        self.database.collection("messages").store(message)

    def get_username(self, username: str) -> Any:
        """Retrieves the user for the queried username.

        Args:
            username: the queried username

        Returns: the user with the matching username
        """

        return self.database.collection("users").filter(lambda user: user["username"] == username)

    def get_username_and_password(self, username: str, password: str) -> Any:
        """Retrieves the user with the matching username and password.

        Args:
            username: the queried username
            password: the queried password

        Returns: the user with the matching username and password
        """

        return self.database.collection("users").filter(
            lambda user: user["username"] == username and Security.check_password(password, user["password"])
        )

    def get_messages(self) -> Any:
        """Retrieves all messages sent.

        Returns: all messages stored in the messages collection
        """

        return self.database.collection("messages").all()

    def get_last_message(self) -> Any:
        """Retrieves the last message sent by any client.

        Returns: the last message sent
        """

        collection = self.database.collection("messages")

        return collection.fetch(collection.last_record_id())

    def update_user_online_status(self, username: str, status: bool) -> None:
        """Sets a user's online status to the actual status. For example, if a
        user disconnects, then their status should be set to False.

        Args:
            username: the user's username
            status: the status to be set
        """

        user = self.get_username(username)[0]
        user["online"] = status

        self.database.collection("users").update(user["__id"], user)

    def output_collection(self, collection_name: str) -> None:
        """Displays all records in all collections. This should only be used
        for debugging purposes.

        Args:
            collection_name: the name of the collections
        """

        print(self.database.collection(collection_name).all())

    def clear_collections(self) -> None:
        """Clears all collections."""

        for collection in COLLECTIONS:
            self.database.collection(collection).drop()
