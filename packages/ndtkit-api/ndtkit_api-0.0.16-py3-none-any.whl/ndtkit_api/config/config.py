import configparser
from pathlib import Path

config = configparser.ConfigParser()

config.read(Path(__file__).parent / 'config.ini')

SERVER_HOST = config.get('Parameters', 'SERVER_HOST', fallback="127.0.0.1")
SERVER_PORT = config.getint('Parameters', 'SERVER_PORT', fallback=32146)
MESSAGE_TYPE = config.getint('Parameters', 'MESSAGE_TYPE', fallback=10)

# Command to launch NDTkit's socket server.
NDTKIT_FILEPATH = config.get('Parameters', 'NDTKIT_FILEPATH', fallback="C:/Program Files/NDTkit/modules/serverMode/serverMode.vbs")
SERVER_CONNECTION_TIMEOUT = config.getint('Parameters', 'SERVER_CONNECTION_TIMEOUT', fallback=120)
