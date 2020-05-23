'''
Creates a player class
'''
import pathlib
import random

import arcade


class Player(arcade.Sprite):
    '''
    Creates a player on the game
    '''

    def __init__(self, data, user_controled: bool = False):
        '''
        Sets up the player varables
        '''

        self.user_controled = user_controled
        self.data = data

        image_selection = pathlib.Path("static/enities/players/").glob("*.png")
        image = random.choice(list(image_selection))

        super().__init__(
            image,
            0.5,
            center_x=self.data["pos"][0],
            center_y=self.data["pos"][1]
        )

        self.keys = {
            "up": [
                arcade.key.W,
                arcade.key.UP
            ],
            "down": [
                arcade.key.S,
                arcade.key.DOWN
            ],
            "left": [
                arcade.key.A,
                arcade.key.LEFT
            ],
            "right": [
                arcade.key.D,
                arcade.key.RIGHT
            ]
        }
        self.speed = 5
