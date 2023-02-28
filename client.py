import socket


class Sender:
    def __init__(self):
        ip = "192.168.43.105"
        port = 9999
        print("Connecting to server...")
        self._sock = socket.socket()
        self._sock.connect((ip, port))
        print("Connected")

    def send(self, filename):
        print("Sending file")
        self._sock.send((bytes(filename, encoding='UTF-8')))

        f = open("motions/" + filename, "rb")
        line = f.read(1024)
        while line:
            self._sock.send(line)
            line = f.read(1024)
        print("File Sended")
        f.close()
