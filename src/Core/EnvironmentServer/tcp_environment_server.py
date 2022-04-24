import threading
import socket
import struct
import logging
from socket import socket as Socket
from socket import timeout
from typing import Any, Iterable, List, Optional
from Core.Models.abstract_server import AbstractServer

class EnvironmentServer(AbstractServer):
    """TCP server for receiving the data from digital twins/ sending the data"""
    def __init__(self, 
                 server_host: str, 
                 server_port: int,
                 client_host: str,
                 client_port: int,
                 max_package_size: int = 4096,
                 package_timeout: float = 5.0) -> None:
        """
        :param: server_host:str address to which external environment is going to send the payloads
        :param: server_port:int port to which external environment is going to send the payloads
        :param: client_host:str address on which the Deep Reinforcement Learning platform is supposed to send payloads
        :param: client_port:str port on which the Deep Reinforcement Learning platform is supposed to send payloads
        :param: max_package_size:int size of package which is supposed to be received per single call to external environment
        :param: package_timeout:float timeout before the package is being received from external environment
        """
        self._logger = logging.getLogger(__name__)
        self._server_host = server_host
        self._server_port = server_port
        self._client_host = client_host
        self._client_port = client_port
        self._max_package_size = max_package_size
        self._package_timeout = package_timeout
        self.latest_payload: bytes = b""
        self._latest_payload_flag = threading.Event()
        self._close_server_flag = threading.Event()
        self._server_thread: Optional[threading.Thread] = None

    def start_server(self) -> None:
        """
        Method to start the server.
        """
        def _serve():
            socket_server = Socket(socket.AF_INET, socket.SOCK_STREAM)
            with socket_server as server:
                server.bind((self._server_host, self._server_port))
                server.settimeout(self._package_timeout)
                while not self._close_server_flag.is_set():
                    try:
                        self.latest_payload = server.recv(self._max_package_size)
                        self._latest_payload_flag.set()
                    except timeout:
                        self._logger.error(f"Package was not received in {self._package_timeout}")
                        continue
                self._logger.info("Terminating socket server")

        self._server_thread = threading.Thread(target=_serve, name="TCP DRL server")
        self._server_thread.run()
        self._logger.info("Running TCP environment server on: %s", str(self._server_host+":"+str(self._server_port)))
    
    def close_server(self):
        """
        Method for closing the connection to environment hook
        """
        self._close_server_flag.set()
        if self._server_thread:
            self._logger.warning("Waiting until server is closed")
            self._server_thread.join()
        self._close_server_flag.clear()

    def receive_payload(self, receiving_mask) -> List[Any]:
        """
        Method for receiving the payload from environment hook
        """
        self._latest_payload_flag.wait()
        payload = struct.unpack(receiving_mask, self.latest_payload)
        self._latest_payload_flag.clear()
        return list(payload)

    def send_payload(self, payload: Iterable, sending_mask: str):
        """
        Method for sending the payload to environment hub
        """
        socket_client = Socket(socket.AF_INET, socket.SOCK_STREAM) #type: ignore
        byte_payload_to_send = struct.pack(sending_mask, *payload)
        socket_client.sendto(byte_payload_to_send, (self._client_host, self._client_port))