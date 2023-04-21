import socket
import json
import sys

import func_timeout
from Utilities import Singleton as S
from Utilities.Vector import Vector


@S.singleton
class SocketTCP:
    def __init__(self, host, port):
        self.address = (host, int(port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_address = None
        self.conn = None

    def connect(self):
        """
        Tries to connect socket to address and return a (bool, string)
        according to the result
        :return: (Bool, String)
        """
        try:
            self.socket.bind(self.address)
            self.socket.listen()
            return True, "READY"
        except socket.error as e:
            return False, "ERROR"

    def wait_client(self, client_id, waiting_time=10):
        """
        Block the execution waiting a message from socket with string client_id,
        if maximum waiting time is consumed, return False. If client connects
        successfully, return True
        :param client_id: String
        :param waiting_time: Int
        :return: Bool
        """

        client_ready = False
        while not client_ready:
            try:
                # Wait client connection with waiting_time budged
                self.conn, self.remote_address = func_timeout.func_timeout(waiting_time, self.socket.accept)

                # Wait client id message
                data = self.receive_message()

                if data is None:
                    client_ready = False
                else:
                    client_ready = data.decode() == client_id

            except func_timeout.FunctionTimedOut:
                return False
        return True

    def receive_message(self, waiting_time=1):
        """
        Wait message for waiting_time, if received return it, return None otherwise
        """
        try:
            # Wait client message
            data = func_timeout.func_timeout(waiting_time, self.conn.recv, args=[1024])
        except func_timeout.FunctionTimedOut:
            data = None
        return data

    def send_game_state(self, gs):
        """Try send serialized game state,
        return True if no error ocurred, return False otherwise"""
        json_string = json.dumps(gs.serialize(), indent=4)
        try:
            self.conn.sendall(json_string.encode())
            result = True
        except:
            result = False
        return result

    def send_message(self, message):
        """Try send message, return True if no error ocurred,
        return False otherwise"""
        try:
            self.conn.sendall(message.encode())
            return True
        except:
            return False

    def change_information(self, gamestate):
        """Send game state and wait for message,
        if message is json manage it, return data received decoded otherwise."""
        self.send_game_state(gamestate)
        data = self.receive_message()
        if not data: return None
        if self.is_json(data):
            return self.manage_json(data)
        return data.decode()

    def manage_json(self, data):
        """Receive encoded json string, return parsed to Vector if is input,
        return None otherwise"""
        dic = json.loads(data.decode())
        if self.is_input(data):
            # Return Vector with coords
            return Vector([dic["x"], dic["y"]])
        else:
            return None

    def is_json(self, data):
        """Receive encoded data and check if
        it format is compatible with json"""
        try:
            json.loads(data.decode())
            return True
        except:
            return False

    def is_input(self, data):
        """Receive encoded data and check if
        it format is compatible with input"""
        data = data.decode()
        try:
            data = json.loads(data)
        except:
            return False

        if "x" in data and "y" in data:
            return True
        return False

    def close(self):
        self.socket.close()


