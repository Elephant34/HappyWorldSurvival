'''
Conatins the buttons used in game
'''
import arcade


class MenuButton(arcade.gui.TextButton):
    '''
    Button for the main menu
    '''

    def __init__(self, game_size, y, text, function, theme=None):
        '''
        Loads the button
        '''

        super().__init__(
            game_size[0] / 2,
            y,
            250,
            75,
            text=text,
            theme=theme
        )

        self.function = function

        self.locked = False

    def on_press(self):
        '''
        Button is pressed
        '''
        if not self.locked:
            self.pressed = True

    def on_release(self):
        '''
        Button is released
        '''
        if self.pressed:
            self.function()
            self.pressed = False

    def draw_texture_theme(self):
        if self.locked:
            arcade.draw_texture_rectangle(self.center_x, self.center_y,
                                          self.width, self.height,
                                          self.locked_texture
                                          )
        elif self.pressed:
            arcade.draw_texture_rectangle(self.center_x, self.center_y,
                                          self.width, self.height,
                                          self.clicked_texture
                                          )
        else:
            arcade.draw_texture_rectangle(self.center_x, self.center_y,
                                          self.width, self.height,
                                          self.normal_texture
                                          )
