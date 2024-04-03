import arcade.gui
from die_arcade import DIE_X, DIE_Y, Die
from checkboxes import Button
import time
from typing import List
from player import *
import room_dimensions
from guess_box import Guess
import card
from game_screens import InventoryMenu

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

        self.player_images = ["images/Red-Circle-Transparent.png", "images//Purple_Circle.png",
                              "images/Pan_Blue_Circle.png",
                              "images/Yellow_Circle.png", "images/—Pngtree—circle clipart green circle_5553152.png",
                              "images/open-circle-ring-transparent-png-png-see-through-background.png"]

        self.players = arcade.SpriteList()

        for x in range(0, len(self.player_names)):
            self.players.append(
                Player(self.player_names[x], self.player_xs[x], self.player_ys[x], self.player_images[x],
                       self.player_scales[x]))

        # split up the cards, player select screen
        self.current_player = 0  # this will be a function that calls player select view or gets information fed into it by player-select

        self.hands = Player.divide_cards()
        print(self.hands)
        self.player_cards = []
        for i, hand in enumerate(self.hands):
            if i == self.current_player:
                for card in hand:
                    self.player_cards.append(card)
        print(len(self.player_cards))
        print(self.player_cards)
        self.player_npcs = []

        # Sprite Info
        self.grid_sprite_list = arcade.SpriteList()

        self.turn = True

        self.moves = 0

        self.press = 0

        self.idle = 50

        # steven - changing self.move_limit from 6 to 0, so that player cannot move until this value is updated from
        # rollDie()
        self.move_limit = 0

        self.left_pressed = False

        self.right_pressed = False

        self.up_pressed = False

        self.down_pressed = False

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

        ''' 
        variables for turns
        - self.whos_turn: overhead manager type variable which keeps track of who's turn it is. This will be used
        later on to determine what gets drawn, who can move, and who's icon is shown. Will hold the first player object
        in self.players for now, could become a dictionary if it works better later.
        
        - self.has_die_rolled: overhead manager type variable which keeps track of whether the player has rolled the die
        or not, which enforces the die to be rolled only once per turn. Example use: If player has rolled die,
        then self.has_die_rolled will be true, and in on_mouse_click(), the code that allows the player to click the 
        die will be false.
        '''
        self.whos_turn = self.players[0]
        self.has_die_rolled = False
        # setting can_player_move to false so that player cannot move until die has been rolled
        # this will be reflected in on_key_press, where all key presses will be unavailable if
        # can_player_move is false
        self.can_player_move = False

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

        ''' Turn Based Drawings '''

        # first, an indication of who's turn it is at the top of the sidebar
        arcade.draw_text(str(self.whos_turn.name) + "'s turn!", (self.width - SIDEBAR_WIDTH) + 110, 755,
                         color=arcade.color.BLACK, font_size=10)

        # for when it's the user's turn
        if self.whos_turn == self.players[0]:  # it's the user player's turn
            if not self.has_die_rolled:
                # indicate for user to roll the die
                arcade.draw_text("Roll The Die!", DIE_X - 37, DIE_Y - 50, arcade.color.BLACK, 10)
            else:
                # now after the die has been rolled, it will display the value
                text = f"You rolled a {self.die.die_value}!"
                arcade.draw_text(text, DIE_X - 45, DIE_Y - 50, arcade.color.BLACK, 10)
        else:
            if self.has_die_rolled:
                # now after the die has been rolled, it will display the value
                text = f"{self.whos_turn.name} rolled a {self.die.die_value}!"
                arcade.draw_text(text, DIE_X - 50, DIE_Y - 50, arcade.color.BLACK, 10)


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
        if self.whos_turn == self.players[0]:
            if self.can_player_move:
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
        if self.press >= self.move_limit:
            self.players[0].change_y = 0
            self.players[0].change_x = 0
            self.press = 0
        # for i in range(self.moves_list):
        #     if self.players[0].center == self.moves_list[i-1]:

    # turn function
    def run(self):
        """
        pseudocode / design:

        first, it'll be the player's turn.
        What should happen in the player's turn?

        Player's turn:

            1. An indication that it is their turn.
            2. Roll the die
            3. From the value of the die, move that many spaces.
            4. Either they enter a room, or it's the next player's turn
                For when player enters a room:

                1. The accuse function will then become available, and will be indicated that it is available
                2. The player would then check the boxes for what they want to accuse (this will have to be validated)
                and will submit the accusation.
                3. If any AI player has any of the cards, then the card to be shown would be randomly chosen and added
                to the inventory of the player.
                4. Turn Ends.

                For when player is already in a room when their turn starts, the can roll the die or just accuse.

        It's the next player's turn. (AI)

            1. The indication for whose turn it is will change from the player to the AI
            2. The die will be rolled for them, so rollDie() will be called from here, then
            the AI will move that many spaces to a certain room entrance, as Reuben was saying.
            3. Either they enter a room, or it's the next player's turn
                For when AI player enters a room:

                1. They will automatically accuse based on what they know (which could just be an array of the cards
                they don't have, randomly chosen)
                2. If the player has any of the cards, then they have to go into inventory and click on the card they
                want to show, to the inventory of the AI.
                3. Turn Ends.

                For when AI is already in a room when their turn starts...

        """
        if self.whos_turn == self.players[0]:  # it's the user player's turn
            ''' 
            Following code present in on_draw, based on some variables such as whos_turn and has_die_rolled:
            
            Under "Turn Based Drawings"
            
            - an indication of who's turn it is at the top of the sidebar
            

            - for when it's the user's turn and the die has not been rolled,
            text will be drawn that says "Roll The Die!"
            - otherwise if the die has been rolled, then the value will be shown in text.
            - the validation of whether the die has been rolled is present in on_mouse_click(),
            where the bool will be true once the area of the die is clicked. Which can only happen
            during the user's turn.
            - these drawings will go away once its not the players turn anymore
            '''
            # once the die has been rolled, the limit for the amount of moves will be set to
            # the die value
            if self.has_die_rolled:
                self.move_limit = self.die.die_value        # player movement has to be tuned to this
                if self.move_limit > 1:
                    self.can_player_move = True
                    if self.right_pressed or self.left_pressed or self.up_pressed or self.down_pressed:
                        self.press += 1
                        if self.press >= self.move_limit:
                            self.can_player_move = False        # this still has issues, player still moves if key held
                            self.whos_turn = self.players[1]
                            self.has_die_rolled = False     # reinitializing die roll so that AI can roll once

        # now handling AI turns
        # first will be second player, then third, etc
        if self.whos_turn == self.players[1]:
            # die will be rolled for them and the value they get will be shown
            if not self.has_die_rolled:
                self.die.roll_die()
                self.has_die_rolled = True
                self.move_limit = self.die.die_value
                # npc movement

                """
                # after npc movement, turn shifts to next person and has die rolled is reinitialized to false,
                # but has to be in a way that everything is frozen except for current player
                self.whos_turn = self.players[2]
                self.has_die_rolled = False  # reinitializing die roll so that AI can roll once
                """

    '''
        if self.whos_turn == self.players[2]:
            # die will be rolled for them and the value they get will be shown
            if not self.has_die_rolled:
                self.die.roll_die()
                self.has_die_rolled = True
                self.move_limit = self.die.die_value
                # npc movement

                self.whos_turn = self.players[3]
                self.has_die_rolled = False  # reinitializing die roll so that AI can roll once

        if self.whos_turn == self.players[3]:
            # die will be rolled for them and the value they get will be shown
            if not self.has_die_rolled:
                self.die.roll_die()
                self.has_die_rolled = True
                self.move_limit = self.die.die_value
                # npc movement

                self.whos_turn = self.players[4]
                self.has_die_rolled = False  # reinitializing die roll so that AI can roll once

        if self.whos_turn == self.players[4]:
            # die will be rolled for them and the value they get will be shown
            if not self.has_die_rolled:
                self.die.roll_die()
                self.has_die_rolled = True
                self.move_limit = self.die.die_value
                # npc movement

                self.whos_turn = self.players[5]
                self.has_die_rolled = False  # reinitializing die roll so that AI can roll once

        if self.whos_turn == self.players[5]:
            # die will be rolled for them and the value they get will be shown
            if not self.has_die_rolled:
                self.die.roll_die()
                self.has_die_rolled = True
                self.move_limit = self.die.die_value
                # npc movement

                # this was the last player's turn, so it goes back to player 1
                self.whos_turn = self.players[0]
                self.has_die_rolled = False  # reinitializing die roll so that AI can roll once

        # still need a game ending event
    '''
    '''
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
    '''

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

        # if it's the player's turn and the die hasn't been rolled, then the user can roll the die
        # once. In another section of the code, has_die_rolled will be reinitialized to false once the
        # turn has ended
        if self.whos_turn == self.players[0]:
            if not self.has_die_rolled:
                # clicking within area of die to roll it, if die is visible
                # if self.die_visible:
                if (self.die.x - self.die.width / 2 < x < self.die.x + self.die.width / 2
                        and self.die.y - self.die.height / 2 < y < self.die.y + self.die.height / 2):
                    self.die.roll_die()
                    self.has_die_rolled = True

        # making boxes clickable
        for button in self.sidebar_buttons:
            button.check_click(x, y)
