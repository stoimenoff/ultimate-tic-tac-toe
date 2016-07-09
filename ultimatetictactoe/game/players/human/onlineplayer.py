import socket
import pickle
from .. import Player
from ...boards import Macroboard

BYTES_LENGTH = 4096
DEFAULT_HOST = '127.0.0.1'
DEFAULT_CONNECT = 'localhost'
DEFAULT_PORT = 5007
DEFAULT_CLIENT_TIMEOUT = 1
DEFAULT_SERVER_TIMEOUT = 10


class BadRequestError(Exception):
    pass


class BadResponseError(Exception):
    pass


class RemotePlayer(Player):
    def __init__(self, opponentName='Remote player',
                 host=DEFAULT_CONNECT, port=DEFAULT_PORT):
        super(RemotePlayer, self).__init__(None)
        self.host = host
        self.port = port
        self.opponentName = opponentName

    def choose_move(self, macroboard):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.__socket.settimeout(DEFAULT_CLIENT_TIMEOUT)
        with self.__socket:
            self.__socket.connect((self.host, self.port))
            self.__socket.sendall(self.__get_data(macroboard))
            data = self.__socket.recv(BYTES_LENGTH)
            print('Received', repr(data), ' Size:', len(data))
            try:
                unpickled_data = pickle.loads(data)
            except (pickle.UnpicklingError, EOFError):
                raise BadResponseError('Response unpickling failed.')
            if self.__is_not_valid(unpickled_data, macroboard):
                raise BadResponseError('Response object is not valid.')
            self.name, move = pickle.loads(data)
        return move

    def __get_data(self, macroboard):
        byte_array = pickle.dumps((self.opponentName, macroboard))
        print('size', len(byte_array))
        return byte_array

    def set_target(self, host, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def __is_not_valid(self, unpickled_data, board):
        if not isinstance(unpickled_data, tuple):
            return True
        if len(unpickled_data) != 2:
            return True
        if not isinstance(unpickled_data[0], str):
            return True
        if not isinstance(unpickled_data[1], tuple):
            return True
        if unpickled_data[1] not in board.available_moves:
            return True
        return False


class ServerPlayer(Player):
    def __init__(self, name='Server player', port=DEFAULT_PORT,
                 host=DEFAULT_HOST):
        super(ServerPlayer, self).__init__(name)
        self.opponent = None
        self.__host = host
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self, on_move_request):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.__socket.settimeout(DEFAULT_SERVER_TIMEOUT)
        with self.__socket:
            self.__socket.bind((self.__host, self.__port))
            self.__socket.listen(1)
            connection, address = self.__socket.accept()
            print('Connected by', address)
            if self.opponent is not None and self.opponent != address[0]:
                raise BadRequestError('Not opponent.')
            with connection:
                data = connection.recv(BYTES_LENGTH)
                try:
                    unpickled_data = pickle.loads(data)
                except (pickle.UnpicklingError, EOFError):
                    raise BadRequestError('Request unpickling failed.')
                if self.__is_not_valid(unpickled_data):
                    raise BadRequestError('Request object is not valid.')
                name, macroboard = unpickled_data
                self.opponent = address[0]
                move = on_move_request(name, macroboard)
                connection.sendall(pickle.dumps((self.name, move)))

    def reset(self):
        self.opponent = None

    def address(self):
        return (self.__host, self.__port)

    def __is_not_valid(self, unpickled_data):
        if not isinstance(unpickled_data, tuple):
            return True
        if len(unpickled_data) != 2:
            return True
        if not isinstance(unpickled_data[0], str):
            return True
        if not isinstance(unpickled_data[1], Macroboard):
            return True
        return False
