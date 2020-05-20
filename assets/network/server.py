'''
The game server- this is started when a game is loaded
'''
import json
import pathlib
import socket
import threading

from assets.world.new_world import create_world


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
        print("connection from", self.addr)


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
            json_data = json.load(settings)
            self.port = json_data["game_port"]
            self.save_file = json_data["save_file"]

        try:
            with pathlib.Path(self.save_file).open() as save:
                self.raw_save = json.load(save)
        except FileNotFoundError:
            create_world(self.save_file)

        super().__init__()
        self.start()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(5)

            print("Server started")

            while True:
                conn, addr = s.accept()

                # Creates a new client
                ConnectedGame(conn, addr)
