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

        self.live = True

        super().__init__()
        self.start()

    def run(self):
        '''
        Runs the main clinet loop
        '''

        self.send_data(self.server.raw_save)

        while self.live:
            data = self.recieve_data()

            if data.lower() == "exit":
                self.disconnect()
            elif data.lower() == "shutdown":
                self.disconnect()
                self.server.shutdown()
            else:
                self.server.send_all(data)

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

    def disconnect(self):
        '''
        Disconnect the clients from the server
        '''

        self.live = False
        self.server.remove_player(self)
        self.send_data("KILL")


class RunServer(threading.Thread):
    '''
    Holds the game server
    '''

    def __init__(self, host):
        '''
        starts game server thread
        '''
        self.host = host
        self.live = True

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

        self.client_list = []

        super().__init__()
        self.start()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.bind((self.host, self.port))
            self.s.listen(5)

            while self.live:
                try:
                    conn, addr = self.s.accept()

                    # Creates a new client
                    game = ConnectedGame(self, conn, addr)
                    self.client_list.append(game)
                except OSError:
                    pass

    def send_all(self, data):
        '''
        Sends data to all clients
        '''
        for game in self.client_list:
            game.send_data(data)

    def on_update(self, dt):
        '''
        Updates the mobs and anything not player controled
        '''

    def remove_player(self, game):
        '''
        Removes a game from the connected list
        '''
        self.client_list.remove(game)

    def shutdown(self):
        '''
        Shuts down the server when host closes
        '''

        self.live = False
        self.s.close()
