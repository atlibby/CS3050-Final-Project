import arcade.gui
from die_arcade import DIE_X, DIE_Y
import time
from typing import List
from player import *
import room_dimensions

# Set how many rows and columns we will have
ROW_COUNT = 24
COLUMN_COUNT = 34

TIME = 0.5

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell and offset for screen edges
MARGIN = 2

# Screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Clue"

# Width of Sidebar
SIDEBAR_WIDTH = 320

# Sprite settings
PLAYER_MOVEMENT = 32
SPRITE_SCALING = 0.06


class ClueGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        # UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout(DIE_X, DIE_Y)
        # Create the buttons
        roll_button = arcade.gui.UIFlatButton(DIE_X, DIE_Y, text="Roll Die", width=200)
        self.v_box.add(roll_button.with_space_around(bottom=20))
        # Click event handler
        roll_button.on_click = self.on_click_roll
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=self.v_box
            )
        )

        # We can quickly build a grid with python list comprehension
        self.grid = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

        # Set the window's background color
        self.background_color = arcade.color.BLACK

        # Create a dictionary to store room locations
        self.rooms = {'study': room_dimensions.study, 'hall': room_dimensions.hall, 'lounge': room_dimensions.lounge,
                      'library': room_dimensions.library, 'billiard_room': room_dimensions.billiard_room,
                      'conservatory': room_dimensions.conservatory, 'ballroom': room_dimensions.ballroom,
                      'kitchen': room_dimensions.kitchen, 'dining-room': room_dimensions.dining_room,
                      'guessing_room': room_dimensions.guessing_room}

        # Player Info
        self.player_names = ["Scarlet", "Plum", "Peacock", "Mustard", "Green", "White"]

        self.player_xs = [753, 17, 17, 497, 753, 561]

        self.player_ys = [241, 625, 209, 753, 561, 17]

        self.player_npcs = []

        self.players = []

        # Sprite Info
        self.grid_sprite_list = arcade.SpriteList()

        self.player_list = arcade.SpriteList()

        self.ms_scarlet = Player("images/Red-Circle-Transparent.png", 0.06)

        self.ms_scarlet.center_x = self.player_xs[0]

        self.ms_scarlet.center_y = self.player_ys[0]

        self.player_list.append(self.ms_scarlet)

        self.prof_plum = Player("images//Purple_Circle.png", 0.065)

        self.prof_plum.center_x = self.player_xs[1]

        self.prof_plum.center_y = self.player_ys[1]

        self.player_list.append(self.prof_plum)

        self.mrs_peacock = Player("images/Pan_Blue_Circle.png", 0.045)

        self.mrs_peacock.center_x = self.player_xs[2]

        self.mrs_peacock.center_y = self.player_ys[2]

        self.player_list.append(self.mrs_peacock)

        self.col_mustard = Player("images/Yellow_Circle.png", 0.065)

        self.col_mustard.center_x = self.player_xs[3]

        self.col_mustard.center_y = self.player_ys[3]

        self.player_list.append(self.col_mustard)

        self.mayor_green = Player("images/—Pngtree—circle clipart green circle_5553152.png", 0.028)

        self.mayor_green.center_x = self.player_xs[4]

        self.mayor_green.center_y = self.player_ys[4]

        self.player_list.append(self.mayor_green)

        self.chef_white = Player("images/open-circle-ring-transparent-png-png-see-through-background.png", 0.027)

        self.chef_white.center_x = self.player_xs[5]

        self.chef_white.center_y = self.player_ys[5]

        self.player_list.append(self.chef_white)

        self.turn = True

        self.moves = 0

        self.press = 0

        self.idle = 50

        self.limit = 7

        self.left_pressed = False

        self.right_pressed = False

        self.up_pressed = False

        self.down_pressed = False

        self.current_player = 1

        for player in self.player_list:
            self.players.append(player)
        print(len(self.players))

        for player in self.players:
            self.player_npcs.append(player)
        self.player_npcs.remove(self.player_npcs[0])
        print(len(self.player_npcs))

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.FLORAL_WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

        # Room generation
        self.room_sprite_list = arcade.SpriteList()
        self.roomList = self.generate_rooms()

        for self.room in self.roomList:
            self.room_sprite_list.append(self.room)

        # Resyncing
        self.resync_grid_with_sprites()

    # Method for reloading sprites after I/O or other changes
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

    # Method for creating and returning a list of the classic rooms from Clue
    def generate_rooms(self):
        # Hall, Lounge, Dining Room, Kitchen, Ballroom, Conservatory, Billiard Room, Library, and Study
        hall = Room("hall", "", [[19, 8], [16, 11], [16, 12]], "images/hall.jpeg", .99)
        lounge = Room("lounge", "conservatory", [[17, 17]], "images/lounge.jpeg", 1)
        clue_room = Room("clue_room", "", [], "images/clue-room.jpeg", 1)
        dining_room = Room("dining_room", "", [[11, 15], [15, 17]], "images/dining-room.png", .399)
        kitchen = Room("kitchen", "study", [[6, 19]], "images/kitchen.jpeg", 1)
        ballroom = Room("ballroom", "", [[4, 7], [4, 16]], "images/ballroom.png", .4)
        conservatory = Room("conservatory", "lounge", [[4, 6]], "images/conservatory.jpeg", 1)
        billiard_room = Room("billiard_room", "", [[8, 6], [12, 1]], "images/billiard.jpeg", 1)
        library = Room("library", "", [[12, 3], [15, 7]], "images/library.png", .4)
        study = Room("study", "kitchen", [[19, 6]], "images/study.jpeg", 1)
        
        return [hall, lounge, study, clue_room, dining_room, billiard_room, kitchen, conservatory, ballroom, library]

    # Dice Roll event caller
    def on_click_roll(self, event):
        print("Roll:", event)

    # Method  that randomly selects three cards for the case file
    def get_case_file(self, deck):
        one_of_each_list = ["character", "room", "weapon"]
        case_file = []
        for card in deck:
            if (card.cardType in one_of_each_list):
                case_file.append(card)
                one_of_each_list.remove(card.cardType)
                deck.remove(card)
        return case_file

    # Method for drawing sidebar
    def draw_sidebar(self):
        arcade.draw_rectangle_filled(
            self.width - SIDEBAR_WIDTH / 2,
            self.height / 2,
            SIDEBAR_WIDTH,
            self.height,
            arcade.color.LIGHT_BROWN
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
        # rollDie()

    def on_draw(self):

        # Clear pixels
        self.clear()

        arcade.start_render()

        # Draw grid sprites
        self.grid_sprite_list.draw()
        self.room_sprite_list.draw()

        # Draw players & sidebar
        self.player_list.draw()
        self.draw_sidebar()

        # render button
        self.manager.draw()

    # Redraw sprite when sprite moves
    def on_update(self, delta_time):
        self.players[0].update()
        self.run()

    # Allow player movement with arrow keys
    # time delay to allow for sprite to move
    # one grid square at a time per key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.players[0].change_y = PLAYER_MOVEMENT
            time.sleep(0.1)
        elif key == arcade.key.DOWN:
            self.players[0].change_y = -PLAYER_MOVEMENT
            time.sleep(0.1)
        elif key == arcade.key.LEFT:
            self.players[0].change_x = -PLAYER_MOVEMENT
            time.sleep(0.1)
        elif key == arcade.key.RIGHT:
            self.players[0].change_x = PLAYER_MOVEMENT
            time.sleep(0.1)
        self.press += 1
        # limit the number of times a player moves to the dice number rolled
        if self.press >= self.limit:
            self.players[0].change_y = 0
            self.players[0].change_x = 0

    # Keyboard listener
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.players[0].change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT or self.press == self.moves:
            self.players[0].change_x = 0

    def update_player_movement(self):
        self.players[0].change_x = 0
        self.players[0].change_y = 0

    # TODO: Make npcs wait until after user has moved before they start moving
    # TODO: Make npcs move one grid block at a time instead of multiple at a time
    # TODO: Prevent diagonal movement from npcs
    def run(self):
        rand = random.randrange(0, 4)
        if self.current_player == 1:
            # self.current_player += 1
            pass
        for count, npc in enumerate(self.player_npcs):
            if self.current_player == 1 + count:
                self.moves += 1
                i = 0
                if self.moves >= self.idle:
                    for i in range(self.limit):
                        if rand == 0:
                            time.sleep(0.1)
                            npc.change_x = PLAYER_MOVEMENT
                            rand = random.randrange(0, 4)
                        elif rand == 1:
                            time.sleep(0.1)
                            npc.change_y = PLAYER_MOVEMENT
                            rand = random.randrange(0, 4)
                        elif rand == 2:
                            time.sleep(0.1)
                            npc.change_x = -PLAYER_MOVEMENT
                            rand = random.randrange(0, 4)
                        elif rand == 3:
                            time.sleep(0.1)
                            npc.change_y = -PLAYER_MOVEMENT
                            rand = random.randrange(0, 4)
                        print(i)
                        npc.update()
                    if i >= self.limit:
                        npc.change_x = 0
                        npc.change_y = 0
                    self.current_player += 1
                    self.moves = 0
        if self.current_player > len(self.player_npcs):
            self.current_player = 1

    # Mouse listener
    def on_mouse_press(self, x, y, button, modifiers):
        # Convert the clicked mouse position into grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return

        # 915 - 925,  718 - 728 -16y

        # Flip the location between 1 and 0.
        if self.grid[row][column] == 0:
            self.grid[row][column] = 1
        else:
            self.grid[row][column] = 0

        # Update the sprite colors to match the new grid
        self.resync_grid_with_sprites()


def main():
    ClueGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    deck = Deck.initialize_cards()
    arcade.run()

#kvdf
if __name__ == "__main__":
    main()