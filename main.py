import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Clue"


class clueGame(arcade.Window):
    def __init__(self):
        # Call parent class and set up game window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = None
        # file_path = os.path.dirname(os.path.abspath(__file__))
        # os.chdir(file_path)

    # Restart game
    def setup(self):
        self.background = arcade.load_texture("/Users/andrewlibby/PycharmProjects/CS3050-Final-Project/clue_board2.jpg")

    # Draw screen
    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # self.clear()


def main():
    screen = clueGame()
    screen.setup()
    arcade.run()


if __name__ == "__main__":
    main()