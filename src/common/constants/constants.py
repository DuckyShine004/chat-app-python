# General Constants
PATHS = {
    "logs": [".cache", "logs"],
    "resources": ["src", "common", "resources"],
    "database": ["src", "server", "database"],
    "keys": [".cache", "keys"],
    "certificates": [".cache", "certificates"],
}

CLIENT_TYPES = {
    "server_assign_id",
    "message",
    "server_message",
    "server_messages",
    "server_login_error",
    "server_signup_error",
}

SERVER_TYPES = {
    "client_login",
    "client_signup",
    "client_message",
}

COLLECTIONS = ["users", "messages"]

WINDOW_TITLE = "Shiny Duck"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# RSA
KEY_LENGTH = 1 << 11
CIPHER = "AES128-SHA"

# COLOURS
RED = (255, 0, 0)

# Client-server Constants
HEADER_LENGTH = 1 << 2
