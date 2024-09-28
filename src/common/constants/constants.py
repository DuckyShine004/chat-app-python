# General Constants
PATHS = {
    "logs": [".cache", "logs"],
    "resources": ["src", "common", "resources"],
    "database": ["src", "server", "database"],
    "keys": [".cache", "keys"],
    "certificates": [".cache", "certificates"],
}

CLIENT_TYPES = {
    "assign_id",
    "message",
    "receive_message",
    "send_messages",
    "server_message",
    "server_login_error",
    "server_signup_error",
}

SERVER_TYPES = {
    "login",
    "client_signup",
    "message",
    "receive_messages",
}

COLLECTIONS = ["users"]

WINDOW_TITLE = "Shiny Duck"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

KEY_LENGTH = 1 << 11
CIPHER = "AES128-SHA"

# COLOURS
RED = (255, 0, 0)

# Client-server Constants
HEADER_LENGTH = 1 << 2
