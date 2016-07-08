from .. import Player
import socket
import pickle

BYTES_LENGTH = 4096
DEFAULT_HOST = '127.0.0.1'
DEFAULT_CONNECT = 'localhost'
DEFAULT_PORT = 5007
DEFAULT_TIMEOUT = 1


class RemotePlayer(Player):
    def __init__(self, opponentName='Remote player',
                 host=DEFAULT_CONNECT, port=DEFAULT_PORT):
        super(RemotePlayer, self).__init__(None)
        self.host = host
        self.port = port
        self.opponentName = opponentName

    def choose_move(self, macroboard):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(DEFAULT_TIMEOUT)
            s.connect((self.host, self.port))
            s.sendall(self.get_data(macroboard))
            data = s.recv(BYTES_LENGTH)
            print('Received', repr(data), ' Size:', len(data))
            self.name, move = pickle.loads(data)
        return move

    def get_data(self, macroboard):
        byte_array = pickle.dumps((self.opponentName, macroboard))
        print('size', len(byte_array))
        return byte_array

    def set_target(self, host, port=DEFAULT_PORT):
        self.host = host
        self.port = port


class ServerPlayer(Player):
    def __init__(self, name='Server player'):
        super(ServerPlayer, self).__init__(name)
        self.opponent = None
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT

    def listen(self, on_move_request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.settimeout(DEFAULT_TIMEOUT)
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
                connection.sendall(pickle.dumps((self.name, move)))

    def reset(self):
        self.opponent = None

    def set_host(self, host):
        self.host = host

    def set_port(self, port):
        self.port = port
