'''
The game server- this is started when a game is loaded
'''
import json
import pathlib
import socket
import threading


class ConnectedGame(threading.Thread):
    '''
    An instance of every connected game to send and recieve data
    '''

    def __init__(self, conn, addr):
        '''
        Starts the thread
        '''

        self.conn = conn
        self.addr = addr

        super().__init__()
        self.start()

    def run(self):
        '''
        Runs the main clinet loop
        '''
        print("connected")


class RunServer(threading.Thread):
    '''
    Holds the game server
    '''

    def __init__(self, host):
        '''
        starts game server thread
        '''
        self.host = host
        with pathlib.Path("static/settings.json").open() as settings:
            self.port = json.load(settings)["game_port"]

        super().__init__()
        self.start()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(5)

            while True:
                conn, addr = s.accept()

                print("server listening")

                # Creates a new client
                ConnectedGame(conn, addr)
