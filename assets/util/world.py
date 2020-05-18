'''
Extracts the save data and stores all the world varables
'''
import pathlib


class World:
    '''
    Stores all the world varables and methods
    '''

    def __init__(self):
        '''
        Gets the save data or makes a new save
        '''

        open(pathlib.Path("static/jeff.json"))
