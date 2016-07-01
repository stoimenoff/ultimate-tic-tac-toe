from .. import Player
import socket
import pickle

BYTES_LENGTH = 4096


class RemotePlayer(Player):
    def __init__(self, host='localhost', port=5007, name='Remote player'):
        super(RemotePlayer, self).__init__(name)
        self.host = host
        self.port = port

    def choose_move(self, macroboard):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(self.get_data(macroboard))
            data = s.recv(BYTES_LENGTH)
            print('Received', repr(data), ' Size:', len(data))
        return pickle.loads(data)

    def get_data(self, macroboard):
        byte_array = pickle.dumps((self.name, macroboard))
        print('size', len(byte_array))
        return byte_array

    def set_target(self, host, port):
        self.host = host
        self.port = port


class ServerPlayer(Player):
    def __init__(self, name='Remote player'):
        super(ServerPlayer, self).__init__(name)
        self.opponent = None

    def listen(self, on_move_request, host='localhost', port=5007):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            connection, address = s.accept()
            if self.opponent is not None and self.opponent != address[0]:
                return
            self.opponent = address[0]
            print('Connected by', address)
            with connection:
                data = connection.recv(BYTES_LENGTH)
                name, macroboard = pickle.loads(data)
                move = on_move_request(name, macroboard)
                connection.sendall(pickle.dumps(move))

    def reset(self):
        self.opponent = None
