'''
Extracts the save data and stores all the world varables
'''
from datetime import datetime
import pathlib
import json


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

        self.tilemap = self.load_tilemap()
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

            print(self.raw_data)

    def load_tilemap(self):
        '''
        Loads a new tilemap
        For now always loads the same thing
        '''

        tilemap = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
