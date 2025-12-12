import socket

class Bencode:
    @staticmethod
    def encode(data):
        if isinstance(data, int):
            return Bencode.encode_int(data)
        elif isinstance(data, str):
            return Bencode.encode_str(data)
        elif isinstance(data, list):
            return Bencode.encode_list(data)
        elif isinstance(data, dict):
            return Bencode.encode_dict(data)
        else:
            raise TypeError(f"Unsupported type: {type(data)}")

    @staticmethod
    def encode_int(data):
        return f"i{data}e".encode('utf-8')

    @staticmethod
    def encode_str(data):
        return f"{len(data.encode('utf-8'))}:{data}".encode('utf-8')

    @staticmethod
    def encode_list(data):
        return b'l' + b''.join(Bencode.encode(item) for item in data) + b'e'

    @staticmethod
    def encode_dict(data):
        encoded_items = []
        for key, value in sorted(data.items()):
            encoded_items.append(Bencode.encode(key))
            encoded_items.append(Bencode.encode(value))
        return b'd' + b''.join(encoded_items) + b'e'


class Decoder:
    def __init__(self, socket):
        self._socket = socket

    def decode(self):
        token = self._socket.recv(1, socket.MSG_WAITALL)
        return self.decode_token(token)

    def decode_token(self, token):
        if token == b'i':
            return self.decode_number()
        elif token == b'l':
            return self.decode_list()
        elif token == b'd':
            return self.decode_map()
        elif token == b'':
            return None
        else:
            return self.decode_string(token)

    def decode_number(self):
        sofar = b''
        while next := self._socket.recv(1, socket.MSG_WAITALL):
            if next == b'e': return int(sofar)
            sofar += next

    def decode_list(self):
        list = []
        while (next := self._socket.recv(1, socket.MSG_WAITALL)) != b"e":
            list.append(self.decode_token(next))
        return list

    def decode_map(self):
        map = {}
        while (next := self._socket.recv(1, socket.MSG_WAITALL)) != b"e":
            key = self.decode_token(next)
            value = self.decode()
            map[key] = value
        return map

    def decode_string(self, str_size):
        while (next := self._socket.recv(1, socket.MSG_WAITALL)) != b":":
            str_size += next

        string = self._socket.recv(int(str_size), socket.MSG_WAITALL)
        return string.decode('utf-8')
