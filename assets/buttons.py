'''
Conatins the buttons used in game
'''
import arcade


class MenuButton(arcade.gui.TextButton):
    '''
    Button for the main menu
    '''

    def __init__(self, game, y, text, function):
        '''
        Loads the button
        '''

        super().__init__(
            game.get_size()[0] / 2,
            y,
            300,
            75,
            text=text,
            theme=game.menu_theme
        )

        self.function = function

    def on_press(self):
        '''
        Button is pressed
        '''
        self.pressed = True

    def on_release(self):
        '''
        Button is released
        '''
        if self.pressed:
            self.function()
            self.pressed = False
