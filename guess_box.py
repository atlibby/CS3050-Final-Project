import arcade

class Guess:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.clicked = False

    def draw(self):
        if self.clicked:
            arcade.draw_rectangle_filled(self.x, self.y-8, self.width, self.height, arcade.color.GREEN)
        else:
            arcade.draw_rectangle_filled(self.x, self.y-8, self.width, self.height, arcade.color.BLACK)
        if not self.guess:
            arcade.draw_text(self.text, self.x - 125, self.y, arcade.color.BLACK, 9, width=180,
                             align="left", anchor_x="left", anchor_y="top")

    def check_click(self, x, y):
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y + 8 < self.y + self.height / 2:
            self.clicked = not self.clicked