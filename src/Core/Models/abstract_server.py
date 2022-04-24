from abc import ABC, abstractmethod
from typing import Any, Iterable, List


class AbstractServer(ABC):

    @abstractmethod
    def start_server(self):
        """
        Method for starting connection to environment hook
        """
        pass

    @abstractmethod
    def close_server(self):
        """
        Method for closing connection to environment hook
        """
        pass

    @abstractmethod
    def send_payload(self, payload: Iterable, sending_mask: str):
        """
        Method for sending the payload to environment hub
        """
        pass
    
    @abstractmethod
    def receive_payload(self, receiving_mask) -> List[Any]:
        """
        Method for receiving the payload from environment hook
        """
        pass