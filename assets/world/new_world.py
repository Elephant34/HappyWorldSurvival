'''
Creats a new world and saves it to file
'''
import json
import pathlib
from datetime import datetime


def get_version():
    '''
    Gets the current game version from settings
    '''
    with pathlib.Path("static/settings.json").open() as settings:
        return json.load(settings)["version"]


def generate_tilemap():
    '''
    Creates a new randly generated tilemap
    Work in progress
    '''

    return [[1 for i in range(15)] for i in range(10)]


def generate_mobs():
    '''
    Populates a small area of the world with mobs
    Work in progress
    '''

    return {}


def create_world(save_file):
    '''
    Creates and saves a new world file
    '''

    data = {
        "version": get_version(),
        "last_save": str(datetime.now()),
        "tilemap": generate_tilemap(),
        "players": {},  # No players have connected yet
        "mobs": generate_mobs()
    }

    with pathlib.Path(save_file).open("w") as save:
        json.dump(data, save, indent=4)
