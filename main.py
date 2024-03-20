import arcade
import random
from room import Room
from Card import Deck
import Card
import time
from Player import *

# Set how many rows and columns we will have
ROW_COUNT = 24
COLUMN_COUNT = 34

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 2

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Array Backed Grid Example"

PLAYER_MOVEMENT = 32

SIDEBAR_WIDTH = 320

SPRITE_SCALING = 0.06

study = [(23, 0),(22, 0),(21, 0),(20, 0),(20, 1),(20, 2),(20, 3),(20, 4),(20, 5),(20, 6), (22, 6),(21, 6),(23, 5),(23, 4),(23, 3),(23, 2),(23, 1),(22, 1),(22, 2),(22, 3),(22, 4),(22, 5),(21, 5),(21, 4),(21, 3),(21, 2),(21, 1)]
hall = [
    (22, 9), (23, 9), (21, 9), (20, 9), (19, 9), (18, 9), (17, 9), (17, 10), (17, 11), (17, 12), 
    (17, 13), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14), (23, 14), (23, 13), 
    (23, 12), (23, 11), (23, 10), (22, 10), (22, 11), (22, 12), (22, 13), (21, 13), (21, 12), 
    (21, 11), (21, 10), (20, 10), (20, 11), (20, 12), (20, 13), (19, 13), (18, 13), (19, 12), 
    (18, 12), (18, 11), (19, 11), (19, 10), (18, 10)
]
lounge = [
    (18, 17), (18, 18), (18, 19), (18, 20), (18, 21), (18, 22), (18, 23),
    (19, 23), (20, 23), (21, 23), (22, 23), (23, 23), (23, 18), (23, 19),
    (23, 20), (23, 21), (23, 22), (21, 17), (21, 17), (21, 17), (20, 17),
    (19, 17), (19, 18), (19, 19), (19, 20), (19, 21), (19, 22), (20, 22),
    (20, 21), (20, 20), (20, 19), (20, 18), (21, 18), (21, 19), (21, 20),
    (21, 21), (21, 22), (22, 22), (22, 21), (22, 20), (22, 19), (22, 18),
    (22, 17)
]
library = [
    (17, 1), (17, 2), (17, 3), (17, 4), (17, 5),
    (16, 6), (15, 6), (14, 6),
    (13, 5), (13, 4), (13, 3), (13, 2), (13, 1),
    (14, 0), (15, 0), (16, 0),
    (16, 1), (16, 2), (16, 3), (16, 4), (16, 5),
    (15, 5), (14, 5), (14, 4), (15, 4), (15, 3),
    (14, 3), (14, 2), (15, 2), (15, 1), (14, 1)
]
billiard_room = [
    (11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5),
    (10, 5), (9, 5), (8, 5), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1), (7, 0),
    (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (9, 4), (9, 3), (9, 2), (9, 1), (9, 0),
    (10, 0), (10, 1), (10, 2), (10, 3), (10, 4)
]
conservatory = [
    (4, 5), (3, 5), (2, 5), (1, 5), (0, 5),
    (4, 4), (4, 3), (4, 2), (4, 1), (4, 0),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
    (2, 4), (1, 4), (0, 4),
    (2, 3), (1, 3), (0, 3),
    (2, 2), (1, 2), (0, 2),
    (2, 1), (1, 1), (0, 1),
    (2, 0), (1, 0), (0, 0)
]
ballroom = [
    (6, 8), (5, 8), (4, 8), (3, 8), (2, 8),
    (2, 9),
    (1, 10), (1, 11), (1, 12), (1, 13),
    (2, 14), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15),
    (6, 14), (6, 13), (6, 12), (6, 11), (6, 10), (6, 9),
    (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14),
    (4, 14), (3, 14), (4, 13), (3, 13), (2, 13), (2, 12),
    (3, 12), (4, 12), (4, 11), (3, 11), (2, 11), (2, 10),
    (3, 10), (3, 9), (4, 9), (4, 10)
]
kitchen = [
    (0, 18), (1, 18), (2, 18), (3, 18), (4, 18), (5, 18),
    (5, 19), (5, 20), (5, 21),
    (4, 22), (4, 23), (3, 23), (2, 23), (1, 23), (0, 23),
    (0, 22), (0, 21), (0, 20), (0, 19),
    (1, 19), (1, 20), (1, 21), (1, 22),
    (2, 22), (2, 21), (2, 20), (2, 19),
    (3, 19), (3, 20), (3, 21), (3, 22),
    (4, 21), (4, 20), (4, 19)
]
dining_room = [
    (9, 18), (9, 17), (9, 16), (8, 19), (8, 20), (8, 21), (8, 22), (8, 23),
    (10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23),
    (13, 23), (12, 23), (11, 23), (10, 23), (9, 23), (9, 22), (10, 22), (11, 22), (12, 22), (13, 22), (13, 21), (12, 21),
    (11, 21), (10, 21), (9, 21), (9, 20), (10, 20), (11, 20), (12, 20), (13, 20), (13, 19), (12, 19), (11, 19), (10, 19),
    (9, 19), (10, 18), (11, 18), (12, 18), (13, 18), (13, 17), (12, 17), (11, 17), (10, 17)
]
guessing_room = [
    (15, 9), (15, 10), (15, 11), (15, 12), (15, 13), 
    (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), 
    (9, 12), (9, 11), (9, 10), 
    (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), 
    (14, 10), (14, 11), (14, 12), 
    (13, 12), (13, 11), (13, 10), (12, 10), (12, 11), (12, 12), 
    (11, 12), (11, 11), (11, 10), 
    (10, 10), (10, 11), (10, 12)
]


# def spawn_player(x, y, width, height, color):
#     shape_list = arcade.ShapeElementList()
#     shape = arcade.create_ellipse_filled(x, y, width, height, color)
#     shape_list.append(shape)
#     return shape_list


class ClueGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        # We can quickly build a grid with python list comprehension
        self.grid = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

        # Set the window's background color
        self.background_color = arcade.color.BLACK

        # Create a dictionary to store room locations
        self.rooms = {'study': study, 'hall': hall, 'lounge': lounge, 'library': library, 'billiard_room': billiard_room, 'conservatory': conservatory, 'ballroom': ballroom, 'kitchen': kitchen, 'dining-room': dining_room, 'guessing_room': guessing_room}

        player_names = ["Ms. Scarlet", "Professor Plum", "Mrs. Peacock", "Colonel Mustard", "Mayor Green", "Chef White"]

        player_xs = [753, 17, 17, 497, 753, 561]

        player_ys = [241, 625, 209, 753, 561, 17]

        # Create a spritelist for batch drawing all the grid sprites
        self.grid_sprite_list = arcade.SpriteList()

        self.player_list = arcade.SpriteList()

        self.ms_scarlet = Player("../CS3050-Final-Project/Red-Circle-Transparent.png", 0.06)

        self.ms_scarlet.center_x = player_xs[0]

        self.ms_scarlet.center_y = player_ys[0]

        self.player_list.append(self.ms_scarlet)

        self.prof_plum = Player("../CS3050-Final-Project/Purple_Circle.png", 0.065)

        self.prof_plum.center_x = player_xs[1]

        self.prof_plum.center_y = player_ys[1]

        self.player_list.append(self.prof_plum)

        self.mrs_peacock = Player("../CS3050-Final-Project/Pan_Blue_Circle.png", 0.045)

        self.mrs_peacock.center_x = player_xs[2]

        self.mrs_peacock.center_y = player_ys[2]

        self.player_list.append(self.mrs_peacock)

        self.col_mustard = Player("../CS3050-Final-Project/Yellow_Circle.png", 0.065)

        self.col_mustard.center_x = player_xs[3]

        self.col_mustard.center_y = player_ys[3]

        self.player_list.append(self.col_mustard)

        self.mayor_green = Player("../CS3050-Final-Project/—Pngtree—circle clipart green circle_5553152.png", 0.028)

        self.mayor_green.center_x = player_xs[4]

        self.mayor_green.center_y = player_ys[4]

        self.player_list.append(self.mayor_green)

        self.chef_white = Player("../CS3050-Final-Project/open-circle-ring-transparent-png-png-see-through-background.png", 0.027)

        self.chef_white.center_x = player_xs[5]

        self.chef_white.center_y = player_ys[5]

        self.player_list.append(self.chef_white)

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.FLORAL_WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

        #FOR ROOM SPRITES
        # draw all the initial colors
        self.resync_grid_with_sprites()

    def resync_grid_with_sprites(self):
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                pos = row * COLUMN_COUNT + column
                for room, locations in self.rooms.items():
                    if (row, column) in locations:
                        self.grid_sprite_list[pos].color = self.get_color_for_room(room)
                        break
                else:
                    if self.grid[row][column] == 0:
                        self.grid_sprite_list[pos].color = arcade.color.GRAY
                    else:
                        self.grid_sprite_list[pos].color = arcade.color.GREEN
                    
    def get_color_for_room(self, room):
        room_colors = {
        'lounge': arcade.color.JET,
        'library': arcade.color.ANTIQUE_BRASS,
        'hall': arcade.color.APRICOT,
        'study': arcade.color.CORDOVAN,
        'billiard_room': arcade.color.BITTERSWEET_SHIMMER,
        'conservatory': arcade.color.BRIGHT_UBE,
        'ballroom': arcade.color.DARK_LIVER,
        'kitchen': arcade.color.KHAKI,
        'dining-room': arcade.color.FIELD_DRAB,
        'guessing_room': arcade.color.BLACK
        
    }
        return room_colors.get(room, arcade.color.BURNT_ORANGE)

    # returns a list of the classic rooms from Clue
    def generate_rooms(self):
        # Hall, Lounge, Dining Room, Kitchen, Ballroom, Conservatory, Billiard Room, Library, and Study
        hall = Room("hall", "", [[19, 8], [16, 11], [16, 12]])
        lounge = Room("lounge", "conservatory", [[17, 17]])
        dining_room = Room("dining_room", "", [[11, 15], [15, 17]])
        kitchen = Room("kitchen", "study", [[6, 19]])
        ballroom = Room("ballroom", "", [[4, 7], [4, 16]])
        conservatory = Room("conservatory", "lounge", [[4, 6]])
        billiard_room = Room("billiard_room", "", [[8, 6], [12, 1]])
        library = Room("library", "", [[12, 3], [15, 7]])
        study = Room("study", "kitchen", [[19, 6]])
        return [hall, lounge, dining_room, kitchen, ballroom, conservatory, billiard_room, library, study]

    # def generate_characters(self):
    #     self.players = []
    #     i = 0
    #     player_names = ["Ms. Scarlet", "Professor Plum", "Mrs. Peacock", "Colonel Mustard", "Mayor Green", "Chef White"]
    #     player_x = [23, 18, 6, 0, 0, 16]
    #     player_y = [16, 0, 0, 9, 14, 23]
    #     player_radius = [1, 1, 1, 1, 1, 1]
    #     player_color = [arcade.color.RED, arcade.color.PURPLE, arcade.color.BLUE, arcade.color.YELLOW, arcade.color.GREEN, arcade.color.WHITE]
    #     player_status = [0, 0, 0, 0, 0, 0]
    #
    #     for i in range(6):
    #         x = player_x[i]
    #         y = player_y[i]
    #         color = player_color[i]
    #         radius = player_radius[i]
    #         # status = player_status[i]
    #         player = Player(x, y, color, radius)
    #         self.players.append(player)
    #         # i += 1
    #     return self.players



    def get_case_file(self, deck):
        one_of_each_list = ["character", "room", "weapon"]
        case_file = []
        for card in deck:
            if (card.cardType in one_of_each_list):
                case_file.append(card)
                one_of_each_list.remove(card.cardType)
                deck.remove(card)
        return case_file
    
    def draw_sidebar(self):
        arcade.draw_rectangle_filled(
            self.width - SIDEBAR_WIDTH / 2,
            self.height / 2,
            SIDEBAR_WIDTH,
            self.height,
            arcade.color.LIGHT_YELLOW
        )
        deck = Deck.initialize_cards()
        characters = ['Miss Scarlett', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock',
                            'Professor Plum']
        rooms = ['Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge',
                        'Hall', 'Study']
        weapons = ['Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']
        self.checkbox_states = {item: False for item in weapons + rooms + characters}
        y_value = 780
        for card_type, items in [("Weapons", weapons), ("Rooms", rooms), ("Players", characters)]:
            y_value -= 30
            arcade.draw_text(card_type, self.width - SIDEBAR_WIDTH + 10, y_value,
                            arcade.color.BLACK, 12, width=180, align="left", anchor_x="left", anchor_y="top")
            y_value -= 12
            for item in items:
                y_value -= 16
                arcade.draw_rectangle_filled(self.width - SIDEBAR_WIDTH + 150, y_value, 10, 10, arcade.color.BLACK)
                arcade.draw_text(item, self.width - SIDEBAR_WIDTH + 10, y_value + 8,
                            arcade.color.BLACK, 9, width=180, align="left", anchor_x="left", anchor_y="top")
            

    

    def on_draw(self):
        """
        Render the screen.
        """
        # # We should always start by clearing the window pixels
        self.clear()

        arcade.start_render()

        # Draw grid sprites
        self.grid_sprite_list.draw()

        # Draw players
        self.player_list.draw()

        self.draw_sidebar()

    # Redraw sprite when sprite moves
    def on_update(self, delta_time):
        self.player_list.update()

    # Allow player movement with arrow keys
    # time delay to allow for sprite to move
    # one grid square at a time per key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.ms_scarlet.change_y = PLAYER_MOVEMENT
            time.sleep(0.1)
        elif key == arcade.key.DOWN:
            self.ms_scarlet.change_y = -PLAYER_MOVEMENT
            time.sleep(0.1)
        elif key == arcade.key.LEFT:
            self.ms_scarlet.change_x = -PLAYER_MOVEMENT
            time.sleep(0.1)
        elif key == arcade.key.RIGHT:
            self.ms_scarlet.change_x = PLAYER_MOVEMENT
            time.sleep(0.1)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.ms_scarlet.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ms_scarlet.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return
        

        # Flip the location between 1 and 0.
        if self.grid[row][column] == 0:
            self.grid[row][column] = 1
        else:
            self.grid[row][column] = 0

        # Update the sprite colors to match the new grid
        self.resync_grid_with_sprites()


# #simulates a roll of the dice using Clue die faces
# def dice_roll():
#     roll_options = ['c', 2, 3, 4, 5, 6]
#     return random.choice(roll_options)


def main():
    ClueGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    deck = Deck.initialize_cards()
    # case_file = get_case_file(deck)
    print(deck)
    arcade.run()


if __name__ == "__main__":
    main()
