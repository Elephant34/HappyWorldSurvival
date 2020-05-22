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

    def __init__(self, server, conn, addr):
        '''
        Starts the thread
        '''

        self.server = server
        self.conn = conn
        self.addr = addr

        super().__init__()
        self.start()

    def run(self):
        '''
        Runs the main clinet loop
        '''

        self.send_data(self.server.raw_save)

        while True:
            data = self.recieve_data()
            print(data)

    def recieve_data(self):
        '''
        Recieves a data from the client
        '''

        header = self.conn.recv(8).decode("utf-8")
        changed_data = self.conn.recv(int(header)).decode("utf-8")

        return changed_data

    def send_data(self, changed_data):
        '''
        sends a data to the client
        '''

        changed_data = str(changed_data)

        send_data = format(len(changed_data), "08d") + changed_data
        self.conn.sendall(send_data.encode("utf-8"))


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
            self.save_path = json_data["save_path"]

        try:
            with pathlib.Path(self.save_path).open() as save:
                self.raw_save = json.load(save)
        except FileNotFoundError:
            create_world(self.save_path)
            with pathlib.Path(self.save_path).open() as save:
                self.raw_save = json.load(save)

        super().__init__()
        self.start()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(5)

            while True:
                conn, addr = s.accept()

                # Creates a new client
                ConnectedGame(self, conn, addr)

    def on_update(self, dt):
        '''
        Updates the mobs and anything not player controled
        '''
