import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Clue"


class clueGame(arcade.Window):
    def __init__(self):
        # Call parent class and set up game window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BLACK)

    # Restart game
    def setup(self):
        pass

    # Draw screen
    def on_draw(self):
        self.clear()


def main():
    screen = clueGame()
    screen.setup()
    arcade.run()


if __name__ == "__main__":
    main()