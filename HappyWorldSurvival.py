'''
Starts the game opening to the main menu
'''
import pathlib
import socket
import threading
import json

import arcade

from assets.gui.buttons import MenuButton
from assets.gui.text_input import TextInput
from assets.network.server import run_server
from assets.util.world import World


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

    def on_draw(self):
        '''
        Draws the game to the screen
        '''
        arcade.start_render()

        if self.on_menu:
            for button in self.button_list:
                if button.active:
                    button.draw()
            for dialogue in self.dialogue_box_list:
                if dialogue.active:
                    dialogue.on_draw()
                    arcade.draw_text(
                        "Server IP:",
                        self.get_size()[0] / 2 - 30,
                        self.get_size()[1] / 2 + 100,
                        arcade.color.WHITE,
                        20,
                        anchor_x="right",
                        anchor_y="center"
                    )
                    self.text_input.draw()
            arcade.draw_text(
                "Happy World Survival",
                self.get_size()[0] / 2,
                500,
                arcade.color.WHITE,
                60,
                anchor_x="center",
                anchor_y="center"
            )
            return

        self.tile_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        self.text_input.process_mouse_press(x, y, button, modifiers)

    def on_key_press(self, key, modifiers):
        self.text_input.process_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.text_input.process_key_release(key, modifiers)

    def load_main_menu(self):
        '''
        loads the main menu GUI
        '''

        self.menu_theme = arcade.gui.Theme()

        normal = pathlib.Path("static/buttons/Normal.png")
        hover = pathlib.Path("static/buttons/Hover.png")
        clicked = pathlib.Path("static/buttons/Clicked.png")
        locked = pathlib.Path("static/buttons/Locked.png")

        dialogue_box = pathlib.Path("static/dialogue/dialogue_box.png")

        self.menu_theme.add_button_textures(normal, hover, clicked, locked)
        self.menu_theme.add_dialogue_box_texture(dialogue_box)

        self.menu_dialoguebox = arcade.gui.DialogueBox(
            self.get_size()[0] / 2,
            self.get_size()[1] / 2,
            300,
            300,
            color=arcade.color.WHITE,
            theme=self.menu_theme
        )

        self.text_input = TextInput(
            self.get_size()[0] / 2,
            self.get_size()[1] / 2 + 50,
            250,
            50,
            font_size=28
        )

        self.menu_dialoguebox.button_list.append(
            MenuButton(
                self.get_size(),
                self.get_size()[1] / 2 - 100,
                "Close",
                self.hide_menu_dialogue,
                theme=self.menu_theme
            )
        )

        self.menu_dialoguebox.button_list.append(
            MenuButton(
                self.get_size(),
                self.get_size()[1] / 2 - 20,
                "Connect",
                self.try_user_connection,
                theme=self.menu_theme
            )
        )
        self.dialogue_box_list.append(self.menu_dialoguebox)

        self.button_list.append(
            MenuButton(
                self.get_size(),
                350,
                "Load Game",
                self.load_game,
                theme=self.menu_theme
            )
        )

        self.button_list.append(
            MenuButton(
                self.get_size(),
                250,
                "Connect to Game",
                self.show_manu_dialogue,
                theme=self.menu_theme
            )
        )

        self.button_list.append(
            MenuButton(
                self.get_size(),
                150, "Quit",
                self.quit_game,
                theme=self.menu_theme
            )
        )

    def show_manu_dialogue(self):
        '''
        Shows the dialogue box
        '''

        for button in self.button_list:
            button.locked = True

        self.menu_dialoguebox.active = True

    def hide_menu_dialogue(self):
        '''
        Hides the menu dialogue
        '''

        for button in self.button_list:
            button.locked = False

        self.menu_dialoguebox.active = False

    def load_game(self):
        '''
        Loads the game by starting a server and then connecting
        '''

        self.on_menu = False

        self.game_world = World()

        threading.Thread(target=run_server).start()

        self.tile_list = arcade.SpriteList(
            is_static=True,
            use_spatial_hash=True
        )
        self.game_world.load_tilemap(self.tile_list)

        threading.Thread(
            target=self.connect_server,
            args=(socket.gethostbyname(socket.gethostname()), )
        ).start()

    def try_user_connection(self):
        '''
        Gets the ip out of the input then attampts connection
        '''
        threading.Thread(
            target=self.connect_server,
            args=(self.text_input.text, )
        ).start()

    def connect_server(self, ip):
        '''
        Attempts to connect to server
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.connect((ip, PORT))

            self.send_data(s, self.game_world.raw_data)

            while True:
                self.server_data = self.recieve_data(s)
                self.game_world.update_data(self.server_data)

    def send_data(self, conn, data):
        '''
        Sends the message to the server
        '''

        send_data = str(data).encode("utf-8")
        send_data = format(len(send_data), "08d").encode("utf-8") + send_data

        conn.sendall(send_data)

    def recieve_data(self, s):
        '''
        Recieves a message from the server
        '''
        header = s.recv(8).decode("utf-8")
        game_data = s.recv(int(header)).decode("utf-8")

        json_acceptable_string = game_data.replace("'", "\"")
        game_data = json.loads(json_acceptable_string)

        return game_data

    def quit_game(self):
        '''
        Exits the game
        '''
        self.close()


with open(pathlib.Path("static/settings.json"), "r") as settings:
    PORT = json.load(settings)["game_port"]


if __name__ == "__main__":

    game = GameWindow()
    game.set_caption("Happy World Survival")
    game.set_size(800, 600)

    game.load_main_menu()

    arcade.run()
