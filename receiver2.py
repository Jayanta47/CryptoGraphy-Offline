import random
import string
from socketserver import StreamRequestHandler, TCPServer


def save_json(data: bytes):
    """Saves json packets to file and name it with id"""
    filename = ''.join(
        random.choice(string.digits)
        for _ in range(3)
    ) + '.json'
    with open(filename, 'wb') as f:
        f.write(data)
    print('saved to', filename)


class DumpHandler(StreamRequestHandler):
    def handle(self):
        """receive json packets from client"""
        print('connection from {}:{}'.format(*self.client_address))
        try:
            while True:
                data = self.rfile.readline()
                if not data:
                    break
                print('received', data.decode().rstrip())
                save_json(data)
        finally:
            print('disconnected from {}:{}'.format(*self.client_address))


def main():
    server_address = ('localhost', 5000)
    print('starting up on {}:{}'.format(*server_address))
    with TCPServer(server_address, DumpHandler) as server:
        print('waiting for a connection')
        server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass