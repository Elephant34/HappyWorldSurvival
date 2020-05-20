'''
Connects to the server and loads the local game world
'''
import socket
import threading
import json
import pathlib


class World(threading.Thread):
    '''
    Talks to the server and stores all local data
    '''

    def __init__(self, host, origin):
        '''
        Loads the thread
        '''

        self.host = host
        self.origin = origin

        with pathlib.Path("static/settings.json").open() as settings:
            self.port = json.load(settings)["game_port"]

        super().__init__()
        self.start()

    def run(self):
        '''
        Connects to the server
        '''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            self.conn.connect((self.host, self.port))

            print("World connected")

            while True:
                self.world_data = self.recieve_data()

                print(self.world_data)

    def send_changed(self):
        '''
        Sends the changed world state to the server
        '''

        changed_data = "To work out"
        data = format(len(changed_data), "08d").encode("utf-8") + changed_data

        self.conn.sendall(data)

    def recieve_data(self):
        '''
        Recieves the changed world from the server
        '''
        header = self.conn.recv(8).decode("utf-8")
        raw_data = self.conn.recv(int(header)).decode("utf-8")

        return raw_data

    def on_update(self, dt):
        '''
        Updates the player and if origin also the server
        '''

    def on_draw(self):
        '''
        Draws all the tiles and other sprites
        '''
