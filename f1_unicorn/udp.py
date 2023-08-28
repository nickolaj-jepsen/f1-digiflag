from errno import EINPROGRESS
import socket

import uasyncio


def open_connection():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setblocking(False)
    ss = uasyncio.StreamReader(client)
    try:
        client.bind(("", 20777))
    except OSError as er:
        if er.errno != EINPROGRESS:
            raise er
    return ss
