import arcade
from room_dimensions import *

# Constants
SIDEBAR_WIDTH = 200

MIN_X_LIST = [STUDY_MIN_X, HALL_MIN_X, LOUNGE_MIN_X, LIBRARY_MIN_X, BILLIARD_ROOM_MIN_X,
              CONSERVATORY_MIN_X, BALLROOM_MIN_X, KITCHEN_MIN_X, DINING_ROOM_MIN_X, GUESSING_ROOM_MIN_X]
MAX_X_LIST = [STUDY_MAX_X, HALL_MAX_X, LOUNGE_MAX_X, LIBRARY_MAX_X, BILLIARD_ROOM_MAX_X,
              CONSERVATORY_MAX_X, BALLROOM_MAX_X, KITCHEN_MAX_X, DINING_ROOM_MAX_X, GUESSING_ROOM_MAX_X]
MIN_Y_LIST = [STUDY_MIN_Y, HALL_MIN_Y, LOUNGE_MIN_Y, LIBRARY_MIN_Y, BILLIARD_ROOM_MIN_Y,
              CONSERVATORY_MIN_Y, BALLROOM_MIN_Y, KITCHEN_MIN_Y, DINING_ROOM_MIN_Y, GUESSING_ROOM_MIN_Y]
MAX_Y_LIST = [STUDY_MAX_Y, HALL_MAX_Y, LOUNGE_MAX_Y, LIBRARY_MAX_Y, BILLIARD_ROOM_MAX_Y,
              CONSERVATORY_MAX_Y, BALLROOM_MAX_Y, KITCHEN_MAX_Y, DINING_ROOM_MAX_Y, GUESSING_ROOM_MAX_Y]



class Button:
    def __init__(self, x, y, width, height, card, guess, guess_box):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.card = card
        self.clicked = False
        self.guess = guess
        self.guess_box = guess_box

    def draw(self):
        room_names = ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Conservatory',
                      'Ballroom', 'Kitchen', 'Dining Room', 'Guessing Room']
        if self.clicked:
            if not self.guess:
                arcade.draw_rectangle_filled(self.x, self.y-8, self.width, self.height, arcade.color.GREEN)
            elif self.guess and self.guess_box.guess_clicked:
                arcade.draw_rectangle_filled(self.x, self.y-8, self.width, self.height, arcade.color.GREEN)
                self.card.selected = True
            else:
                self.clicked = not self.clicked
        else:
            for x in range(0, len(MIN_Y_LIST)):
                if not self.guess:
                    arcade.draw_rectangle_filled(self.x, self.y-8, self.width, self.height, arcade.color.BLACK)
                    self.card.selected = False
                elif self.guess_box.guess_clicked:
                    arcade.draw_rectangle_filled(self.x, self.y-8, self.width, self.height, arcade.color.BLACK)
                    self.card.selected = False

        if not self.guess:
            arcade.draw_text(self.card.name, self.x - 125, self.y, arcade.color.BLACK, 9, width=180,
                             align="left", anchor_x="left", anchor_y="top")

    def check_click(self, x, y):
        if(not self.guess):
            if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y + 8 < self.y + self.height / 2:
                self.clicked = not self.clicked
        elif(self.guess_box.guess_clicked):
            if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y + 8 < self.y + self.height / 2:
                self.clicked = not self.clicked
