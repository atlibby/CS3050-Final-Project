import arcade

# Constants
GUESS_BOX_X = 840
GUESS_BOX_Y = 130


class Guess:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.guess_clicked = False
        self.text = text

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.ASH_GREY)
        arcade.draw_text(self.text, self.x - 43, self.y + 10, arcade.color.BLACK, 12, width=180,
                             align="left", anchor_x="left", anchor_y="top")

    def check_click(self, x, y):
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
            self.guess_clicked = not self.guess_clicked

guessing_box = Guess(GUESS_BOX_X, GUESS_BOX_Y, 110, 30, "Make Guess")
