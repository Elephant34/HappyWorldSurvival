'''
Extracts the save data and stores all the world varables
'''
import json
import pathlib
from datetime import datetime

from arcade import Sprite


class World:
    '''
    Stores all the world varables and methods
    '''

    def __init__(self):
        '''
        Gets the save data or makes a new save
        '''

        if not pathlib.Path("static/worldSave.json").exists():
            self.new_world()
        else:
            self.decode_save()

    def new_world(self):
        '''
        Creates and saves a new world file
        '''

        with open(pathlib.Path("static/settings.json"), "r") as settings:
            self.version = json.load(settings)["version"]

        self.tilemap = self.create_tilemap()
        self.players = {}
        self.mobs = {}

        self.save()

    def decode_save(self):
        '''
        Decodes the world file to get the data
        '''

        with open(pathlib.Path("static/worldSave.json"), "r") as save:
            self.raw_data = json.load(save)

            self.version = self.raw_data["version"]
            self.last_save = self.raw_data["last_save"]
            self.tilemap = self.raw_data["tilemap"]
            self.players = self.raw_data["players"]
            self.mobs = self.raw_data["mobs"]

            self.save()

    def create_tilemap(self):
        '''
        Loads a new tilemap
        For now always loads the same thing
        '''

        tilemap = [
            [1 for i in range(15)] for i in range(10)
        ]

        return tilemap

    def save(self):
        '''
        Saves the current game state
        '''

        self.raw_data = {
            "version": self.version,
            "last_save": str(datetime.now()),
            "tilemap": self.tilemap,
            "players": self.players,
            "mobs": self.mobs
        }

        with open(pathlib.Path("static/worldSave.json"), "w") as save:
            json.dump(self.raw_data, save, indent=4)

    def load_tilemap(self, sprite_list):
        '''
        Loads all the tilemap sprites to the list
        '''

        # This is incase I change how tilemaps load
        if self.version == "dev":
            for row_index, row in enumerate(self.tilemap):
                for column_index, column in enumerate(row):
                    if column == 1:
                        img = "static/world/tiles/grass.png"
                    sprite = Sprite(
                            img,
                            center_x=32+(64 * (column_index)),
                            center_y=32+(64 * (row_index))
                            )
                    sprite_list.append(sprite)

    def update_data(self, changed):
        '''
        Updates the world data based off server input
        '''
