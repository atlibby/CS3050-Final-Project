import arcade
# Constants
SIDEBAR_WIDTH = 200

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
