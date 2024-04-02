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


class StartView(arcade.View):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.background_img = arcade.load_texture("images/clue_image.jpeg")
        arcade.load_font("bulletin-gothic/BulletinGothic.otf")
        self.text_effect = 0
        self.min_font_size_reached = True
        self.max_font_size_reached = False

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        clueGameView = ClueGameView(self.width, self.height)
        self.window.show_view(clueGameView)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # example text
        text = "Click"
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.background_img)
        # sets text size to initial small size, and adds text_effect at each iteration, which increases and decreases,
        # pulsating.
        text_size = 25 + self.text_effect

        arcade.draw_text(text, self.window.width / 2, self.window.height / 2 - 150,
                         arcade.color.FLORAL_WHITE, font_name="Bulletin Gothic", font_size=text_size, anchor_x="center")

        # flags min and max font size reached, tells font when to steadily decrease or increase until other flag is set
        # this keeps font size within an interval, 25 & 100 (text size + text_effect which grows to 75).
        # time sleep to slow pulsating
        if self.text_effect <= 75 and self.min_font_size_reached:
            self.text_effect += 1
            time.sleep(0.03)
            if self.text_effect == 75:
                self.max_font_size_reached = True
                self.min_font_size_reached = False
        elif self.text_effect >= 25 and self.max_font_size_reached:
            self.text_effect -= 1
            time.sleep(0.05)
            if self.text_effect == 25:
                self.max_font_size_reached = False
                self.min_font_size_reached = True
        print(self.text_effect)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)