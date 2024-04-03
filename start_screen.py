import arcade
import time
from clue_game import ClueGameView
import arcade.gui
from die_arcade import DIE_X, DIE_Y, Die
from checkboxes import Button
import time
from typing import List
from player import *
import room_dimensions
from guess_box import Guess
import card

from game_screens.inventory import InventoryMenu
from game_screens.player_select_screen import PlayerSelect


class StartView(arcade.View):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.background_img = arcade.load_texture("images/clue_image.jpeg")
        arcade.load_font("bulletin-gothic/BulletinGothic.otf")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        selectScreen = PlayerSelect(self.width, self.height)
        self.window.show_view(selectScreen)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # example text
        text = "Click"
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.background_img)

        text_size = 50


        arcade.draw_text(text, self.window.width / 2, self.window.height / 2 - 150,
                         arcade.color.FLORAL_WHITE, font_name="Bulletin Gothic", font_size=text_size, anchor_x="center")


    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)