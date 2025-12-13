import json
import socket
import struct
from collections.abc import Iterator
from typing import Any

from flight_profiler.communication.base import ClientProtocol, TargetProcessExitError


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        data = sock.recv(1, socket.MSG_PEEK)  # Try to peek 1 byte without removing it
        if not data:  # If no data is available, the peer has likely closed
            return True
        return False
    except BlockingIOError:
        # Socket is open and would block if we tried to read
        return False
    except ConnectionResetError:
        # Connection was reset by the peer
        return True
    except Exception as e:
        # Handle other potential socket errors
        return True

class FlightClient(ClientProtocol):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.running = True
        self.sock = None
        self.connect(self.host, self.port)

    def connect(self, address: str, port: int) -> None:
        for res in socket.getaddrinfo(
            address, port, socket.AF_INET, socket.SOCK_STREAM
        ):
            af, socktype, proto, canonname, sa = res
            self.sock = socket.socket(af, socktype, proto)
            error_code = self.sock.connect_ex(sa)
            if error_code == 0:
                return
            else:
                self.sock.close()
        raise TargetProcessExitError

    def request(self, data: Any) -> bytes:
        if type(data) is bytes:
            self.send(data)
        else:
            self.send(json.dumps(data).encode("utf-8"))
        return self.recv()

    def request_stream(self, data: Any) -> Iterator:
        if type(data) is bytes:
            self.send(data)
        else:
            self.send(json.dumps(data).encode("utf-8"))
        while not is_socket_closed(self.sock):
            data = self.recv()
            if data:
                yield data
            else:
                break

    def send(self, data: bytes):
        header = struct.pack("<L", len(data))
        try:
            self.sock.sendall(header + data)
        except OSError as e:
            if e.errno == 9:  # Bad file descriptor
                raise TargetProcessExitError
            else:
                raise e

    def recv(self) -> bytes:
        header_data = self._recv_bytes(4)
        if len(header_data) == 4:
            msg_len = struct.unpack("<L", header_data)[0]
            data = self._recv_bytes(msg_len)
            if len(data) == msg_len:
                return data
        return b""

    def _recv_bytes(self, n) -> bytes:
        data = "".encode("utf-8")
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                break
            data += chunk
        return data

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        except:
            pass
