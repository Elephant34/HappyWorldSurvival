'''
Starts the game opening to the main menu
'''
import pathlib

import arcade

from assets.buttons import MenuButton


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

        self.on_menu = True

    def main_menu(self):
        '''
        loads the main menu GUI
        '''

        self.menu_theme = arcade.gui.Theme()

        normal = pathlib.Path("static/buttons/Normal.png")
        hover = pathlib.Path("static/buttons/Hover.png")
        clicked = pathlib.Path("static/buttons/Clicked.png")
        locked = pathlib.Path("static/buttons/Locked.png")

        self.menu_theme.add_button_textures(normal, hover, clicked, locked)

        self.button_list.append(
            MenuButton(self, 350, "Load Game", self.load_game)
        )
        self.button_list.append(
            MenuButton(self, 250, "Connect to Game", self.connect_server)
        )
        self.button_list.append(
            MenuButton(self, 150, "Quit", self.quit_game)
        )

    def on_draw(self):
        '''
        Draws the game to the screen
        '''
        arcade.start_render()

        if self.on_menu:
            for button in self.button_list:
                if button.active:
                    button.draw()
            arcade.draw_text(
                "Happy World Survival",
                self.get_size()[0] / 2,
                500,
                arcade.color.WHITE,
                60,
                anchor_x="center",
                anchor_y="center"
            )

    def load_game(self):
        '''
        Loads the game by starting a server and then connecting
        '''
        print("Load Game")

    def connect_server(self):
        '''
        Gets an ip from user and attempts to connect
        '''
        print("Connect Server")

    def quit_game(self):
        '''
        Exits the game
        '''
        self.close()


if __name__ == "__main__":

    game = GameWindow()
    game.set_caption("Happy World Survival")
    game.set_size(800, 600)

    game.main_menu()

    arcade.run()
