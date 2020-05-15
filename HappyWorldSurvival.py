'''
Starts the game opening to the main menu
'''
import arcade


class GameWindow(arcade.Window):
    '''
    The main game window
    Will handel user inputs and all sprites
    '''

    def __init__(self):
        '''
        Sets up needed varables
        '''
        super().__init__()

    def setup(self):
        '''
        Starts the game going
        '''


if __name__ == "__main__":

    game = GameWindow()
    game.set_caption("Happy World Survival")
    game.set_size(800, 600)

    game.setup()

    arcade.run()
