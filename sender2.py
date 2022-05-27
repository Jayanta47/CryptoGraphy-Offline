from cgitb import text
import socket
import json
from random import randint
from time import time, sleep
from typing import Dict, Any
from BitVector import *


from encrypt import encrypt

IP = "127.0.0.1"
PORT = 5000


def generate_json_message():
    """Generate random json packet with hashed data bits"""
    return {
        "id": randint(1, 100),
        "timestamp": time(),
        "data": "hello"*4096
    }


def send_json_message(
    sock: socket.socket,
    json_message: Dict[str, Any],
):
    """Send json packet to server"""
    message = (json.dumps(json_message) + '\n').encode()
    sock.sendall(message)
    print(f'{len(message)} bytes sent')


def main():
    with socket.socket() as sock:
        sock.connect((IP, PORT))
        while True:
            json_message = generate_json_message()
            send_json_message(sock, json_message)
            sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


