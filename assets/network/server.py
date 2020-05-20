'''
The game server- this is started when a new game is loaded
'''
import json
import socket
import threading
import pathlib


class ConnectedGame(threading.Thread):
    '''
    A thread created for every connected client
    '''

    def __init__(self, conn, addr):
        '''
        Sets the thread
        '''

        self.conn = conn
        self.addr = addr

        threading.Thread.__init__(self)
        self.start()

    def run(self):
        '''
        The main recieve loop for all clients
        '''

        while True:
            msg = self.recieve_data()

            if msg:
                self.send_data(msg)

    def recieve_data(self):
        '''
        Recieves a message from the client
        '''

        full_msg = ""

        header = self.conn.recv(8).decode("utf-8")
        if header:
            full_msg = self.conn.recv(int(header)).decode("utf-8")

        return full_msg

    def send_data(self, data):
        '''
        sends a message to the client
        '''

        send_data = str(data)
        send_data = format(len(send_data), "08d") + send_data
        self.conn.sendall(send_data.encode("utf-8"))


HOST = socket.gethostbyname(socket.gethostname())
try:
    with open(pathlib.Path("static/settings.json"), "r") as settings:
        PORT = json.load(settings)["game_port"]
except FileNotFoundError:
    PORT = 8700


def run_server():
    '''
    Runs the server on the local machine
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()

            header = conn.recv(8).decode("utf-8")
            full_msg = conn.recv(int(header)).decode("utf-8")

            send_data = str(full_msg)
            send_data = format(len(send_data), "08d") + send_data
            conn.sendall(send_data.encode("utf-8"))

            # ConnectedGame(conn, addr)


if __name__ == "__main__":
    '''
    For testing the server
    This is never run otherwise
    '''

    run_server()
