import arcade

# Constants
SIDEBAR_WIDTH = 200


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.clicked = False

    def draw(self):
        if self.clicked:
            arcade.draw_rectangle_filled(self.x, self.y-5, self.width, self.height, arcade.color.GRAY)
        else:
            arcade.draw_rectangle_filled(self.x, self.y-5, self.width, self.height, arcade.color.BLACK)
        arcade.draw_text(self.text, self.x - 125, self.y,
                         arcade.color.BLACK, 9, width=180, align="left", anchor_x="left", anchor_y="top")

    def check_click(self, x, y):
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
            self.clicked = not self.clicked


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.buttons = []

    def setup(self):
        characters = ['Miss Scarlett', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock',
                      'Professor Plum']
        rooms = ['Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge',
                 'Hall', 'Study']
        weapons = ['Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']
        y_value = 780
        for card_type, items in [("Weapons", weapons), ("Rooms", rooms), ("Players", characters)]:
            y_value -= 30
            self.buttons.append(Button(self.width - SIDEBAR_WIDTH + 150, y_value, 10, 10, card_type))
            y_value -= 12
            for item in items:
                y_value -= 16
                self.buttons.append(Button(self.width - SIDEBAR_WIDTH + 150, y_value, 10, 10, item))

    def on_draw(self):
        arcade.start_render()
        for button in self.buttons:
            button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for button in self.buttons:
            button.check_click(x, y)


def main():
    window = MyGame(800, 600, "Clue Game")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
