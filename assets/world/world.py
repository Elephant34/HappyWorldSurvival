'''
Connects to the server and loads the local game world
'''
import socket
import threading
import json
import pathlib

import arcade


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

        self.world_data = {}

        self.loaded = False

        super().__init__()
        self.start()

    def run(self):
        '''
        Connects to the server
        '''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            self.conn.connect((self.host, self.port))

            # Gets the first load of data, sets tilemap and loads varables
            changed_data = json.loads(
                    self.recieve_data().replace("'", "\"")
                )
            self.update_varables(changed_data)
            self.load_tilemap()
            self.load_self_player()
            self.loaded = True

            while True:
                changed_data = json.loads(
                    self.recieve_data().replace("'", "\"")
                )

                self.update_varables(changed_data)

    def send_changed(self, to_server):
        '''
        Sends the changed world state to the server
        '''

        data = (format(len(to_server), "08d") + to_server).encode("utf-8")

        self.conn.sendall(data)

    def recieve_data(self):
        '''
        Recieves the changed world from the server
        '''
        header = self.conn.recv(8).decode("utf-8")
        raw_data = self.conn.recv(int(header)).decode("utf-8")

        return raw_data

    def update_varables(self, data):
        '''
        Updates all self varables to be usful for the game
        '''

        for key in data.keys():
            self.world_data[key] = data[key]

        self.version = self.world_data["version"]
        self.last_save = self.world_data["last_save"]
        self.tilemap = self.world_data["tilemap"]
        self.players = self.world_data["players"]
        self.mobs = self.world_data["mobs"]

    def load_tilemap(self):
        '''
        Loads all the tiles to varables
        '''

        self.tilemap_list = arcade.SpriteList(
            use_spatial_hash=True,
            is_static=True
        )

        # Adds backwards compatabilitiy
        if self.version == "dev":
            for row_index, row in enumerate(self.tilemap):
                for column_index, column in enumerate(row):
                    if column == 1:
                        img = "static/world/tiles/grass.png"

                    # Adds the tile
                    tile = arcade.Sprite(
                            img,
                            center_x=32+(64 * (column_index)),
                            center_y=32+(64 * (row_index))
                            )
                    self.tilemap_list.append(tile)

    def load_self_player(self):
        '''
        Loads the user controled player
        '''

    def on_update(self, dt):
        '''
        Updates the player and if origin also the server
        '''
        if not self.loaded:
            return

        if self.origin:
            self.origin.on_update(dt)

    def on_draw(self):
        '''
        Draws all the tiles and other sprites
        '''
        if not self.loaded:
            return

        self.tilemap_list.draw()
