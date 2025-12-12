# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import socket
import struct


def unlink(file: str) -> None:
    try:
        os.unlink(file)
    except OSError:
        pass


def get_from_socket(sock: socket.socket) -> bytes:
    MSGLEN = struct.unpack(">L", sock.recv(4))[0]
    return sock.recv(MSGLEN)


def send_through_socket(sock: socket.socket, data: bytes) -> None:
    sock.send(struct.pack(">L", len(data)))
    sock.send(data)
