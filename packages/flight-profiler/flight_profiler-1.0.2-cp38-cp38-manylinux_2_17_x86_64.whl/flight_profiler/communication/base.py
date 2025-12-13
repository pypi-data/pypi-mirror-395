from abc import ABC, abstractmethod


class TargetProcessExitError(Exception):
    pass

class ServerProtocol(ABC):

    @abstractmethod
    async def start_server(self, address: str, port: int) -> None:
        pass

    @abstractmethod
    async def accept_connections(self) -> None:
        pass


class ClientProtocol(ABC):

    @abstractmethod
    def connect(self, address: str, port: int) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
