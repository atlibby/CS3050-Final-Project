import arcade
import random
from room import Room


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
        self.background = arcade.load_texture("clue_board2.jpg")

    # Draw screen
    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # self.clear()


#simulates a roll of the dice using Clue die faces
def dice_roll():
    roll_options = ['c', 2, 3, 4, 5, 6]
    return random.choice(roll_options)

#returns a list of the classic rooms from Clue
def generate_rooms():
    #Hall, Lounge, Dining Room, Kitchen, Ballroom, Conservatory, Billiard Room, Library, and Study
    hall = Room("hall", "", [1, 1])
    lounge = Room("lounge", "conservatory", [1, 1])
    dining_room = Room("dining_room", "", [1, 1])
    kitchen = Room("kitchen", "study", [1, 1])
    ballroom = Room("ballroom", "", [1, 1])
    conservatory = Room("conservatory", "lounge", [1, 1])
    billiard_room = Room("billiard_room", "", [1, 1])
    library = Room("library", "", [1, 1])
    study = Room("study", "kitchen", [1, 1])
    return [hall, lounge, dining_room, kitchen, ballroom, conservatory, billiard_room, library, study]


def main():
    screen = clueGame()
    screen.setup()
    arcade.run()


if __name__ == "__main__":
    print(dice_roll())
    rooms = generate_rooms()
    main()