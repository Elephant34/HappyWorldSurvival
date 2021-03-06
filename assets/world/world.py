'''
Connects to the server and loads the local game world
'''
import json
import logging
import pathlib
import random
import socket
import threading

import arcade

from assets.enitites.player import Player


class World(threading.Thread):
    '''
    Talks to the server and stores all local data
    '''

    def __init__(self, host, origin):
        '''
        Loads the thread
        '''

        logging.info("World thread loading")

        self.host = host
        self.origin = origin

        with pathlib.Path("static/settings.json").open() as settings:
            self.port = json.load(settings)["game_port"]

        self.world_data = {}

        self.loaded = False
        self.connected = False

        self.player = None
        self.enities_loaded = False

        super().__init__()
        self.start()

    def run(self):
        '''
        Connects to the server
        '''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            self.conn.connect((self.host, self.port))

            self.connected = True

            logging.info("Connected to server")

            # Gets the first load of data, sets tilemap and loads varables
            changed_data = json.loads(
                    self.recieve_data().replace("'", "\"")
                )

            for key in changed_data.keys():
                self.world_data[key] = changed_data[key]
            self.update_varables()
            self.load_world()
            self.load_player()
            self.load_enities()

            logging.info("Loaded world")

            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player,
                self.collision_list
            )
            self.loaded = True

            while self.connected:
                try:
                    got_data = self.recieve_data().replace("'", "\"")
                    changed_data = json.loads(
                        got_data
                    )

                    self.update_varables()
                except json.decoder.JSONDecodeError:
                    pass

    def send_changed(self, to_server):
        '''
        Sends the changed world state to the server
        '''

        to_server = str(to_server)
        data = (format(len(to_server), "08d") + to_server).encode("utf-8")

        self.conn.sendall(data)

    def recieve_data(self):
        '''
        Recieves the changed world from the server
        '''
        header = self.conn.recv(8).decode("utf-8")
        raw_data = self.conn.recv(int(header)).decode("utf-8")

        return raw_data

    def send_player_update(self):
        '''
        Sends updated players data to the server
        '''

        send_data = {"players": self.players}
        self.send_changed(str(send_data))

    def update_varables(self):
        '''
        Updates all self varables to be usful for the game
        '''

        self.version = self.world_data["version"]
        self.last_save = self.world_data["last_save"]
        self.tilemap = self.world_data["tilemap"]
        self.players = self.world_data["players"]
        self.mobs = self.world_data["mobs"]

        with pathlib.Path("static/settings.json").open() as settings:
            save_path = json.load(settings)["save_path"]

        with pathlib.Path(save_path).open("w") as save:
            json.dump(self.world_data, save, indent=4)

    def load_world(self):
        '''
        Loads all the tiles to varables
        '''

        self.tilemap_list = arcade.SpriteList(
            use_spatial_hash=True,
            is_static=True
        )
        self.collision_list = arcade.SpriteList(
            use_spatial_hash=True,
            is_static=True
        )

        # Adds backwards compatabilitiy
        if self.version == "dev":
            for row_index, row in enumerate(self.tilemap):
                for column_index, column in enumerate(row):
                    if column == 1:
                        img = pathlib.Path("static/world/tiles/grass.png")

                    # Adds the tile
                    tile = arcade.Sprite(
                            img,
                            center_x=32+(64 * (column_index)),
                            center_y=32+(64 * (row_index))
                            )
                    self.tilemap_list.append(tile)

    def load_player(self):
        '''
        Loads the user controled player
        '''

        local_settings_path = pathlib.Path("static/localSettings.json")

        if not local_settings_path.exists():
            with local_settings_path.open("w") as ls:
                ls.write('{"server": {}}')

        with local_settings_path.open() as ls:
            local_data = json.load(ls)
            try:
                connected_id = local_data["server"][str(self.host)]
            except KeyError:
                connected_id = None

        # If the player already exists on server
        if connected_id:
            self.player_data = self.players[connected_id]
        else:
            while True:
                connected_id = str(random.randint(0, 10000))
                try:
                    self.players[connected_id]
                except KeyError:
                    break

            local_data["server"][str(self.host)] = connected_id
            with local_settings_path.open("w") as ls:
                json.dump(local_data, ls)

            self.player_data = {
                "pos": [300, 300],
                "connected": "False"
            }

            self.players[connected_id] = self.player_data

        self.connected_id = connected_id

        self.player = Player(self.player_data)

        self.players[self.connected_id]["connected"] = "True"
        self.send_player_update()

    def load_enities(self):
        '''
        Loads the NPC's and other players
        '''
        self.moving_sprite_list = arcade.SpriteList()

        # Loads the active players
        image_selection = pathlib.Path(
            "static/enities/players/"
        ).glob("*.png")
        for player in self.players.keys():
            if player != self.connected_id:
                if self.players[player]["connected"].lower() == "true":
                    image = random.choice(list(image_selection))
                    sprite = arcade.Sprite(
                        image,
                        0.5,
                        center_x=self.players[player]["pos"][0],
                        center_y=self.players[player]["pos"][1]
                    )
                    self.moving_sprite_list.append(sprite)

    def update_enities(self):
        '''
        Ensures that any changes are applied to te game window
        '''
        # Loads the active players
        image_selection = pathlib.Path(
            "static/enities/players/"
        ).glob("*.png")
        for player in self.players.keys():
            if player != self.connected_id:
                if self.players[player]["connected"].lower() == "true":
                    image = random.choice(list(image_selection))
                    sprite = arcade.Sprite(
                        image,
                        0.5,
                        center_x=self.players[player]["pos"][0],
                        center_y=self.players[player]["pos"][1]
                    )
                    self.moving_sprite_list.append(sprite)

        self.enities_loaded = True

    def on_update(self, dt):
        '''
        Updates the player and if origin also the server
        '''
        if not self.loaded:
            return

        if self.origin:
            self.origin.on_update(dt)

        self.collisions = self.physics_engine.update()

        if self.enities_loaded:
            self.update_enities()

        if self.player:
            self.player_data["pos"] = list(self.player.position)
            self.send_player_update()

    def on_draw(self):
        '''
        Draws all the tiles and other sprites
        '''
        if not self.loaded:
            return

        self.tilemap_list.draw()
        self.moving_sprite_list.draw()
        self.player.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        if key in self.player.keys["up"]:
            self.player.change_y += self.player.speed
        elif key in self.player.keys["down"]:
            self.player.change_y += -self.player.speed
        elif key in self.player.keys["left"]:
            self.player.change_x += -self.player.speed
        elif key in self.player.keys["right"]:
            self.player.change_x += self.player.speed

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """

        if key in self.player.keys["up"]:
            self.player.change_y += -self.player.speed
        elif key in self.player.keys["down"]:
            self.player.change_y += self.player.speed
        elif key in self.player.keys["left"]:
            self.player.change_x += self.player.speed
        elif key in self.player.keys["right"]:
            self.player.change_x += -self.player.speed

    def shutdown(self):
        '''
        Closes the connection to the server
        '''

        self.players[self.connected_id]["connected"] = "False"
        self.send_player_update()
        self.connected = False

        if self.origin:
            self.send_changed("SHUTDOWN")
        else:
            self.send_changed("EXIT")
