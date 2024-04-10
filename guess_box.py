import arcade
from room_dimensions import room_list

# Constants
GUESS_BOX_X = 840
GUESS_BOX_Y = 130

WIDTH = 30
HEIGHT = 30

MARGIN = 2

class Guess:
    def __init__(self, x, y, width, height, text, player_coords):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.guess_clicked = False
        self.text = text
        self.player_coords = player_coords

    def draw(self):
        in_room = False
        scaled_coords = []
        scaled_coords.append(self.player_coords[1] // (WIDTH + MARGIN))
        scaled_coords.append(self.player_coords[0] // (HEIGHT + MARGIN))
        for room in room_list:
            if (scaled_coords in room):
                    arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.ASH_GREY)
                    arcade.draw_text(self.text, self.x - 43, self.y + 10, arcade.color.BLACK, 12, width=180,
                                align="left", anchor_x="left", anchor_y="top")
                    in_room = True
        if(not in_room):
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.LIGHT_BROWN)
            self.guess_clicked = False

    def check_click(self, x, y):
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
                self.guess_clicked = not self.guess_clicked

    def update_user_position(self, x_coord, y_coord):
        self.player_coords = [x_coord, y_coord]
