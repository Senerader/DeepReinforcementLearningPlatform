import unittest
import socket

class TestUdpServer(unittest.TestCase):
    def setUp(self):
        self.hook_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hook_test.bind(("localhost", 65555))
