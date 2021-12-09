import pathlib
import unittest
import sys
from socket import socket, AF_INET, SOCK_STREAM
from unittest.mock import Mock

sys.path.insert(1, str(pathlib.Path(__file__).parent))
from lesson_3 import Client


class ClientTests(unittest.TestCase):

    def setUp(self):
        self.server_addr = 'localhost'
        self.server_port = 7777
        self.socket = socket(AF_INET, SOCK_STREAM)

    def test_presence_mock(self):
        mock_socket = Mock(return_value='')
        mock_send = Mock()
        mock_recv = Mock(return_value={'response': '200', 'time': 1612953360})
        Client.socket.recv = mock_socket
        Client.send_message = mock_send
        Client.get_data_from_message = mock_recv
        self.assertEqual(Client.presence(self.socket), {'response': '200', 'time': 1612953360})

    def tearDown(self):
        self.socket.close()


if __name__ == '__main__':
    unittest.main()
