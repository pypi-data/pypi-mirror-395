import socket
import struct  # Required to pack numbers into bytes
import json   # Required to work with JSON data
from .config import config
from py4j.java_gateway import JavaGateway
import time
import subprocess
import os

gateway = JavaGateway()


def check_server() -> socket.socket | None:
    """
    Creates a socket and tries to connect to the server.
    Returns the connected socket object on success, or None on failure.
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # Set a connection timeout of 2 seconds
        # 2. Attempt to connect
        s.connect((config.SERVER_HOST, config.SERVER_PORT))
        # 3. Return the valid, open socket
        return s
    except (ConnectionRefusedError, socket.timeout):
        # The connection failed, close the created socket and return None
        if s:
            s.close()
        return None


def launch_ndtkit() -> socket.socket | None:
    """
    Launches NDTkit if it's not already running.
    Returns the connected socket object on success, or None on failure.
    """
    start_time = time.time()
    # Loop until the timeout is reached
    is_ndtkit_launch_command_sent = False
    is_wait_message_displayed = False
    client_socket = None
    while time.time() - start_time < config.SERVER_CONNECTION_TIMEOUT:
        client_socket = check_server()
        if client_socket:
            break  # Exit the loop since the server was found
        else:
            if not is_ndtkit_launch_command_sent:
                print(f"NDTkit socket server not detected, command launch: {config.NDTKIT_FILEPATH}")
                is_ndtkit_launch_command_sent = True
                if config.NDTKIT_FILEPATH.lower().endswith(".vbs"):
                    script_directory = os.path.dirname(config.NDTKIT_FILEPATH)
                    script_name = os.path.basename(config.NDTKIT_FILEPATH)
                    subprocess.Popen(['wscript.exe', script_name], cwd=script_directory)
                else:
                    subprocess.Popen(config.NDTKIT_FILEPATH)
            elif not is_wait_message_displayed:
                print("Attempting to connect to socket server...", end="")
                is_wait_message_displayed = True
            else:
                print(".", end="")
            time.sleep(1)

    if not client_socket:
        raise ConnectionError("Impossible to reach the socket server")

    if is_ndtkit_launch_command_sent:
        print("\nNDTkit socket server detected")
    client_socket.settimeout(None)  # Remove the timeout
    return client_socket


def send_custom_protocol_message(json_data):
    """
    Builds and sends a message according to the custom Netty protocol.
    Format: [4-byte length][1-byte type][json payload]
    """
    client_socket = None
    try:
        # 1. Convert the Python dictionary to a JSON string, then encode it into bytes.
        #    Using ensure_ascii=False is good practice for non-latin characters.
        json_payload_bytes = json.dumps(json_data, ensure_ascii=False).encode('utf-8')

        # 2. Calculate the "messageLength" for the header.
        #    This is the length of the type (1 byte) + the length of the JSON payload.
        header_length = 1 + len(json_payload_bytes)

        # 3. Pack the header fields into bytes.
        #    '>' = Big-Endian (Network Byte Order, standard for Java)
        #    'I' = Unsigned Integer (4 bytes)
        #    'B' = Unsigned Char (1 byte)
        length_prefix = struct.pack('>I', header_length)
        type_prefix = struct.pack('>B', config.MESSAGE_TYPE)

        # 4. Assemble the final message by concatenating all parts in the correct order.
        payload_to_send = length_prefix + type_prefix + json_payload_bytes

        # 5. Connect and send the message.
        client_socket = launch_ndtkit()
        client_socket.sendall(payload_to_send)

        # --- Receive the response ---

        # 1. Read the 4-byte total length prefix
        response_len_bytes = client_socket.recv(4)
        if not response_len_bytes:
            print("<-- Server closed connection without response.")
            return None

        total_len = struct.unpack('>I', response_len_bytes)[0]

        # 2. Read the 1-byte message type
        response_type_byte = client_socket.recv(1)
        if not response_type_byte:
            raise ConnectionError("Connection broken after reading length.")

        # 3. Calculate the length of the JSON payload
        json_len = total_len - 1

        # 4. Read the JSON payload
        response_payload = b''
        if json_len > 0:
            while len(response_payload) < json_len:
                chunk = client_socket.recv(json_len - len(response_payload))
                if not chunk:
                    raise ConnectionError("Socket connection broken before full response was received.")
                response_payload += chunk

        # 5. Decode and parse the JSON
        return json.loads(response_payload.decode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client_socket:
            client_socket.close()


def call_api_method(package_name, class_name, method_name, parameters):
    """
    Calls a method in the NDTKit API via the custom socket protocol.
    """
    json_command = {
        "packageName": package_name,
        "className": class_name,
        "methodName": method_name,
        "parameters": parameters
    }
    return send_custom_protocol_message(json_command)
