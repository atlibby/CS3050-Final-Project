import arcade.gui
from die_arcade import DIE_X, DIE_Y, Die
from checkboxes import Button
import time
from typing import List
from player import *
import room_dimensions
from guess_box import Guess
import card
from game_screens.inventory import InventoryMenu

# Width of Sidebar
SIDEBAR_WIDTH = 320

# Sprite settings
PLAYER_MOVEMENT = 32
SPRITE_SCALING = 0.06

# Set how many rows and columns we will have
ROW_COUNT = 24
COLUMN_COUNT = 34

TIME = 0.5

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell and offset for screen edges
MARGIN = 2

class ClueGameView(arcade.View):  # (arcade.Window)
    def __init__(self, width, height):
        super().__init__()
        # super().__init__(width, height, title)
        self.width = width
        self.height = height

        # initializing deck and cards
        self.deck = Deck.initialize_cards()
        self.player_cards = self.deck

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

        self.player_scales = [0.06, 0.065, 0.045, 0.065, 0.028, 0.027]

        self.player_images = ["images/Red-Circle-Transparent.png", "images//Purple_Circle.png", "images/Pan_Blue_Circle.png",
                              "images/Yellow_Circle.png", "images/—Pngtree—circle clipart green circle_5553152.png",
                              "images/open-circle-ring-transparent-png-png-see-through-background.png"]

        self.players = arcade.SpriteList()

        for x in range(0, len(self.player_names)):
            self.players.append(Player(self.player_names[x], self.player_xs[x], self.player_ys[x], self.player_images[x],
                                       self.player_scales[x]))


        self.player_npcs = []

        # Sprite Info
        self.grid_sprite_list = arcade.SpriteList()

        self.turn = True

        self.moves = 0

        self.press = 0

        self.idle = 50

        self.limit = 6

        self.left_pressed = False

        self.right_pressed = False

        self.up_pressed = False

        self.down_pressed = False

        self.current_player = 0

        self.move_list = []


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

        # adding die to sidebar as class object
        self.die = Die(DIE_X, DIE_Y, 50, 50)
        # bool to control whether die appears or not
        self.die_visible = True

        # adding class object, sidebar buttons
        self.sidebar_buttons = []
        self.draw_buttons()

    # Method for reloading sprites after I/O or other changes
    def resync_grid_with_sprites(self):
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                pos = row * COLUMN_COUNT + column
                if self.grid[row][column] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.GRAY

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
        conservatory = Room("conservatory", "lounge", [[4, 6]], "images/conservatory.png", .4)
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
            if card.cardType in one_of_each_list:
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
        y_value = 750
        for card_type in ['Weapons', 'Rooms', 'Players']:
            if card_type == 'Players':
                y_value -= 50
            arcade.draw_text(card_type, self.width - SIDEBAR_WIDTH + 10, y_value,
                             arcade.color.BLACK, 12, width=180, align="left", anchor_x="left", anchor_y="top")
            y_value -= 135

    def draw_buttons(self):
        characters = ['Miss Scarlett', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock',
                      'Professor Plum']
        rooms = ['Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge',
                 'Hall', 'Study']
        weapons = ['Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']
        y_value = 780
        for items in [weapons, rooms, characters]:
            y_value -= 42
            for item in items:
                y_value -= 16
                # adding button objects so that checkboxes can be clickable
                self.sidebar_buttons.append(Button(self.width - SIDEBAR_WIDTH + 150, y_value, 10, 10, item, False))
                self.sidebar_buttons.append(Button(self.width - SIDEBAR_WIDTH + 200, y_value, 10, 10, item, True))

    def draw_guess_box(self):
        text = 'Make Guess'

    def on_draw(self):
        # Clear pixels
        self.clear()

        arcade.start_render()

        # Draw grid sprites
        self.grid_sprite_list.draw()
        self.room_sprite_list.draw()

        # Draw players & sidebar
        self.players.draw()
        self.draw_sidebar()

        # draw clickable die
        if self.die_visible:
            self.die.draw()

        # draw sidebar buttons:
        for button in self.sidebar_buttons:
            button.draw()

    # Redraw sprite when sprite moves
    def on_update(self, delta_time):
        self.players[0].update()
        self.run()

    # Allow player movement with arrow keys
    # time delay to allow for sprite to move
    # one grid square at a time per key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.I:
            inv = InventoryMenu(self, self.player_cards)
            self.window.show_view(inv)
        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_movement()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_movement()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_movement()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_movement()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_movement()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_movement()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_movement()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_movement()

    def update_player_movement(self):
        self.players[0].change_x = 0
        self.players[0].change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.players[0].change_y = PLAYER_MOVEMENT
            time.sleep(0.1)
            self.move_list.append(self.players[0].center_y)
        elif self.down_pressed and not self.up_pressed:
            self.players[0].change_y = -PLAYER_MOVEMENT
            time.sleep(0.1)
            self.move_list.append(self.players[0].center_y)
        if self.left_pressed and not self.right_pressed:
            self.players[0].change_x = -PLAYER_MOVEMENT
            time.sleep(0.1)
            self.move_list.append(self.players[0].center_x)
        elif self.right_pressed and not self.left_pressed:
            self.players[0].change_x = PLAYER_MOVEMENT
            time.sleep(0.1)
            self.move_list.append(self.players[0].center_x)
        if self.press >= self.limit:
            self.players[0].change_y = 0
            self.players[0].change_x = 0
        # for i in range(self.moves_list):
        #     if self.players[0].center == self.moves_list[i-1]:

    # event handler for player turn order and npc movement
    def run(self):
        rand = random.randrange(0, 4)
        if self.current_player == 0:
            if self.right_pressed or self.left_pressed or self.up_pressed or self.down_pressed:
                self.press += 1
                print(self.press)
            if self.press >= self.limit:
                self.current_player += 1
        for count, npc in enumerate(self.player_npcs):
            if self.current_player == 1 + count:
                self.moves += 1
                i = 0
                if self.moves >= self.idle:
                    for j in range(self.limit):
                        if rand == 0:
                            npc.change_x = PLAYER_MOVEMENT
                            # Mustard NPC: Target Destination: [12, 25] Currently [11, 50]
                            # Mustard NPC Preferences: [3, 1, 0, 2]
                            rand = random.randrange(0, 4)
                            # time.sleep(0.25)
                            i += 1
                            npc.update()
                            time.sleep(0.25)
                            # self.step = 0
                        elif rand == 1:
                            npc.change_y = PLAYER_MOVEMENT
                            rand = random.randrange(0, 4)
                            # time.sleep(0.25)
                            i += 1
                            npc.update()
                            time.sleep(0.25)
                            # self.step = 0
                        elif rand == 2:
                            npc.change_x = -PLAYER_MOVEMENT
                            rand = random.randrange(0, 4)
                            print(rand)
                            # time.sleep(0.25)
                            i += 1
                            npc.update()
                            time.sleep(0.25)
                            # self.step = 0
                        elif rand == 3:
                            npc.change_y = -PLAYER_MOVEMENT
                            rand = random.randrange(0, 4)
                            print(rand)
                            i += 1
                            npc.update()
                            time.sleep(0.25)
                            # self.step = 0
                        # npc.update()
                    print('next player')
                    if i >= self.limit:
                        npc.change_x = 0
                        npc.change_y = 0
                    self.current_player += 1
                    self.moves = 0
        if self.current_player > len(self.player_npcs):
            self.press = 0
            self.current_player = 0

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
        """
        # Flip the location between 1 and 0.
        if self.grid[row][column] == 0:
            self.grid[row][column] = 1
        else:
            self.grid[row][column] = 0
        """
        # Update the sprite colors to match the new grid
        self.resync_grid_with_sprites()

        # clicking within area of die to roll it, if die is visible
        if self.die_visible:
            if (self.die.x - self.die.width / 2 < x < self.die.x + self.die.width / 2
                    and self.die.y - self.die.height / 2 < y < self.die.y + self.die.height / 2):
                self.die.roll_die()
                print("Rolled Die")
        # making boxes clickable
        for button in self.sidebar_buttons:
            button.check_click(x, y)

