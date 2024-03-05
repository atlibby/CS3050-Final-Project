"""
Player class for the game
Initializing a Player object in main will mean providing information
on the player's color, name, initial position, and player status (whether
the player is a user or an NPC, which will determine whether said player is
controlled by keyboard/mouse events or by RNG)

The mark_sheet method will probably need to be dependent on a Clue Sheet class,
which I can create, and it would appear as a popup window that a player/NPC can interact
with

Conversely, we may not need a Clue Sheet class altogether and just have one generate
in main for each player, but personally I think it would be easier to have the Player
class interact with a Clue Sheet class similarly to how the Player class will interact
with the Card class, since NPC behavior will be much simpler to integrate this way
"""

import arcade
import random as r
from Card import *
from room import Room


class Player:
    def __init__(self, x, y, radius, color, border_width, num_segments, player_name, player_status):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.border_width = border_width
        self.num_segments = num_segments
        self.shape = arcade.draw_circle_filled(x, y, radius, color, num_segments)
        self.player_name = player_name
        self.player_status = player_status

    # getters
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

    def get_player_name(self):
        return self.player_name

    def get_player_status(self):
        return self.player_status

    # setters
    def set_x(self, x_pos):
        self.x = x_pos

    def set_y(self, y_pos):
        self.y = y_pos

    def set_color(self, player_color):
        self.color = player_color

    def set_player_name(self, player_name):
        self.player_name = player_name

    def set_player_status(self, player_status):
        self.player_status = player_status

    # class functions
    def roll_die(self):
        roll = r.randrange(1, 6)
        return roll

    def teleport(self, accused, room_coords):
        accused.move(room_coords)

    def make_accusation(self, accused_name, accused_room, accused_weapon, accuser):
        print(accuser + " thinks it was " + accused_name + " in the " + accused_room + " with the " + accused_weapon)


    def mark_sheet(self):
        pass

    def reveal_card(self):
        pass
