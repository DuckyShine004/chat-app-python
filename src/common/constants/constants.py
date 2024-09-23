# General Constants
PATHS = {
    "logs": [".cache", "logs"],
    "resources": ["src", "common", "resources"],
    "database": ["src", "server", "database"],
}

CLIENT_TYPES = {
    "assign_id",
    "message",
    "receive_message",
    "send_messages",
    "server_message",
    "server_login_error",
}

SERVER_TYPES = {
    "login",
    "message",
    "receive_messages",
}

COLLECTIONS = ["users"]

WINDOW_TITLE = "Shiny Duck"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# COLOURS
RED = (255, 0, 0)

# Client-server Constants
HEADER_LENGTH = 1 << 2
