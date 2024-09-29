"""This module contains the code for providing the server client contexts."""

from ssl import SSLSocket


class Context:
    """The Context class is a used by the server to store necessary data for a
    user's session.

    Attributes:
        connection: the client connection
        username: the username
    """

    def __init__(self, connection: SSLSocket) -> None:
        """Intialises the Context instance.

        Args:
            connection: the client connection
        """

        self.connection: SSLSocket = connection
        self.username: str = None
