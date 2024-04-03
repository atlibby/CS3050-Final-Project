import arcade.gui
from die_arcade import DIE_X, DIE_Y, Die
from checkboxes import Button
import time
from typing import List
from player import *
import room_dimensions
from start_screen import StartView
from guess_box import Guess
import card
# from game_screens.inventory import InventoryMenu
import clue_game

# Screen dimensions
SCREEN_WIDTH = (clue_game.WIDTH + clue_game.MARGIN) * clue_game.COLUMN_COUNT + clue_game.MARGIN
SCREEN_HEIGHT = (clue_game.HEIGHT + clue_game.MARGIN) * clue_game.ROW_COUNT + clue_game.MARGIN
SCREEN_TITLE = "Clue"



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    startView = StartView(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.show_view(startView)
    arcade.run()
    
if __name__ == "__main__":
    main()