import arcade.gui
from die_arcade import DIE_X, DIE_Y, Die
from checkboxes import Button
import time
from typing import List
from player import *
import room_dimensions
from guess_box import Guess, GUESS_BOX_X, GUESS_BOX_Y
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

ROOM_BOUNDARIES_X = room_dimensions.ROOM_BOUNDARIES_X
ROOM_BOUNDARIES_Y = room_dimensions.ROOM_BOUNDARIES_Y



class ClueGameView(arcade.View):  # (arcade.Window)
    def __init__(self, width, height, player_selected):
        super().__init__()
        # super().__init__(width, height, title)
        self.width = width
        self.height = height

        self.deck = Deck.initialize_cards()
        Deck.shuffle_deck(self.deck)
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

        # self.user will be the player object using the index of player_selected,
        # then from a list of players not the user, will iterate thru them
        self.user = self.players[player_selected]

        # split up the cards, player select screen
        # self.current_player = 0 #this will be a function that calls player select view or gets information fed into it by player-select
        # Make a deck

        self.hands = Player.divide_cards(self.deck)
        self.player_cards = []
        # creating player hands
        for i, hand in enumerate(self.hands):
            if i == player_selected:
                for card in hand:
                    self.player_cards.append(card)
        self.case_file = self.hands[-1]

        # self.player_npcs = arcade.SpriteList()

        # for player in self.players:
        # self.player_npcs.append(player)

        # self.player_npcs.remove(self.player_npcs[self.current_player])

        for card in self.case_file:
            print(card)
        # test = testNPCShowCard(self.hands, self.player_npcs)

        # Sprite Info
        self.grid_sprite_list = arcade.SpriteList()

        self.turn = True

        self.moves = 0

        self.press = 0

        self.idle = 90

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

        # adding die to sidebar as class object
        self.die = Die(DIE_X, DIE_Y, 50, 50)
        # bool to control whether die appears or not
        self.die_visible = True

        # guess box
        self.guess_box = Guess(GUESS_BOX_X, GUESS_BOX_Y, 110, 30, "Make Guess",
                               [self.user.center_x / WIDTH,
                                self.user.center_y / HEIGHT])

        # adding class object, sidebar buttons
        self.sidebar_buttons = []
        self.draw_buttons()

        ''' 
        variables for turns

        '''
        # self.whos_turn: overhead manager type variable which keeps track of who's turn it is. This will be used
        # later on to determine what gets drawn, who can move, and who's icon is shown. Will hold the first player
        # object in self.players for now, could become a dictionary if it works better later.
        self.whos_turn = self.user

        # creating a copy of self.players, which I will pop self.user and then
        # that will be the ai players
        self.ai_players = arcade.SpriteList()

        for i in range(0, len(self.players)):
            if self.players[i] != self.user:
                self.ai_players.append(self.players[i])

        # self.has_die_rolled: overhead manager type variable which keeps track of whether the player has rolled the die
        # or not, which enforces the die to be rolled only once per turn. Example use: If player has rolled die,
        # then self.has_die_rolled will be true, and in on_mouse_click(), the code that allows the player to click the
        # die will be false.
        self.has_die_rolled = False

        # can_player_move is false so that player cannot move until die has been rolled
        # this will be reflected in on_key_press, where all key presses will be unavailable if
        # can_player_move is false
        self.can_player_move = False

        # has_player_moved is false to prevent the user pressing the enter button from doing anything until
        # the player has finished moving.
        self.has_player_moved = False

        # move_limit_set is set to false, to become true later once the move_limit takes the die_value
        # purpose of this var is to prevent the move_limit from being reinitialized
        self.move_limit_set = False

        # Resyncing
        self.resync_grid_with_sprites()

    # Method for reloading sprites after I/O or other changes
    def resync_grid_with_sprites(self):
        arcade.set_background_color(arcade.color.BLACK)
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                pos = row * COLUMN_COUNT + column
                if self.grid[row][column] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.GRAY

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

    def check_guess_for_win(self):
        guess = []
        for card in self.deck:
            if card.selected:
                guess.append(card)
        if set(guess) == set(self.case_file):
            print("WINNER")

    # Method for drawing sidebar
    def draw_sidebar(self):
        arcade.draw_rectangle_filled(
            self.width - SIDEBAR_WIDTH / 2,
            self.height / 2,
            SIDEBAR_WIDTH,
            self.height,
            arcade.color.LIGHT_BROWN
        )
        y_value = 730
        for card_type in ['Players', 'Rooms', 'Weapons']:
            if card_type == 'Weapons':
                y_value -= 50
            arcade.draw_text(card_type, self.width - SIDEBAR_WIDTH + 10, y_value,
                             arcade.color.BLACK, 12, width=180, align="left", anchor_x="left", anchor_y="top")
            y_value -= 135

    def draw_buttons(self):
        y_value = 720
        player_card_list = []
        room_card_list = []
        weapon_card_list = []
        for card in self.deck:
            if (card.cardType == 'character'):
                player_card_list.append(card)
            elif (card.cardType == 'room'):
                room_card_list.append(card)
            else:
                weapon_card_list.append(card)
        all_card_list = []
        for card in player_card_list:   all_card_list.append(card)
        for card in room_card_list:   all_card_list.append(card)
        for card in weapon_card_list:   all_card_list.append(card)
        last_card_type = all_card_list[0].cardType
        for card in all_card_list:
            if (last_card_type != card.cardType):
                y_value -= 42
            y_value -= 16
            # adding button objects so that checkboxes can be clickable
            self.sidebar_buttons.append(
                Button(self.width - SIDEBAR_WIDTH + 150, y_value, 10, 10, card, False, self.guess_box))
            self.sidebar_buttons.append(
                Button(self.width - SIDEBAR_WIDTH + 200, y_value, 10, 10, card, True, self.guess_box))
            last_card_type = card.cardType

    def on_draw(self):
        # Clear pixels
        self.clear()

        arcade.start_render()

        # Draw grid sprites
        self.grid_sprite_list.draw()
        self.room_sprite_list.draw()

        # Draw players & sidebar
        self.user.draw()
        self.ai_players.draw()
        self.draw_sidebar()

        # draw clickable die
        if self.die_visible:
            self.die.draw()

        # draw sidebar buttons:
        for button in self.sidebar_buttons:
            button.draw()

        self.guess_box.draw()

        ''' Turn Based Drawings '''
        # first, an indication of who's turn it is at the top of the sidebar
        arcade.draw_text(str(self.whos_turn.name) + "'s turn!", (self.width - SIDEBAR_WIDTH) + 110, 755,
                         color=arcade.color.BLACK, font_size=10)

        # for when it's the user's turn
        if self.whos_turn == self.user:  # it's the user player's turn
            if not self.has_die_rolled:
                # indicate the user to roll the die
                arcade.draw_text("Roll The Die!", DIE_X - 37, DIE_Y - 50, arcade.color.BLACK, 10)
            else:
                # now after the die has been rolled, it will display the value
                text = f"You rolled a {self.die.die_value}!"
                arcade.draw_text(text, DIE_X - 45, DIE_Y - 50, arcade.color.BLACK, 10)
                # if the player has already done all their moves, but hasn't submitted their turn
                if self.has_player_moved:
                    # indicate the user to press enter to switch turns
                    arcade.draw_text("ENTER to Continue!", DIE_X - 65, DIE_Y + 50, arcade.color.BLACK, 10)
        else:
            if self.has_die_rolled:
                # now after the die has been rolled, it will display the value
                text = f"{self.whos_turn.name} rolled a {self.die.die_value}!"
                arcade.draw_text(text, DIE_X - 50, DIE_Y - 50, arcade.color.BLACK, 10)
                # if the player has already done all their moves, but hasn't submitted their turn
                if self.has_player_moved:
                    # indicate the user to press enter to switch turns
                    arcade.draw_text("ENTER to Continue!", DIE_X - 65, DIE_Y + 50, arcade.color.BLACK, 10)

    # Redraw sprite when sprite moves
    def on_update(self, delta_time):
        self.check_guess_for_win()
        self.user.update()
        self.run()

    # Allow player movement with arrow keys
    # time delay to allow for sprite to move
    # one grid square at a time per key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.I:
            inv = InventoryMenu(self, self.player_cards)
            self.window.show_view(inv)

        if self.whos_turn == self.user:
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

        # in the case the player (ai or user) has moved but not submitted turn
        if self.has_player_moved:
            if key == arcade.key.ENTER:

                # creating the next player index for ai
                next_player_index = 0
                if self.whos_turn in self.ai_players:
                    current_player_index = self.ai_players.index(self.whos_turn)  # Get index of current player
                    next_player_index = (current_player_index + 1) % len(self.ai_players)  # Calculate the next index

                # covers three cases where its the user, so it moves to the first ai player
                # or its the last ai player, so it goes to the user
                # or its in the middle, so its just the next ai player
                if self.whos_turn == self.user:
                    self.whos_turn = self.ai_players[0]

                elif self.whos_turn == self.ai_players[len(self.ai_players) - 1]:
                    self.whos_turn = self.user

                else:
                    self.whos_turn = self.ai_players[next_player_index]  # Assign based on calculated index

                # reinitializing variables for AI to roll die and move
                self.has_player_moved = False
                self.has_die_rolled = False
                self.move_limit_set = False

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
        self.user.change_x = 0
        self.user.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.user.change_y = PLAYER_MOVEMENT
            time.sleep(0.1)
        elif self.down_pressed and not self.up_pressed:
            self.user.change_y = -PLAYER_MOVEMENT
            time.sleep(0.1)
        if self.left_pressed and not self.right_pressed:
            self.user.change_x = -PLAYER_MOVEMENT
            time.sleep(0.1)
        elif self.right_pressed and not self.left_pressed:
            self.user.change_x = PLAYER_MOVEMENT
            time.sleep(0.1)

        if self.press >= self.move_limit:
            self.user.change_y = 0
            self.user.change_x = 0
            self.press = 0

        # for i in range(self.moves_list):
        #     if self.players[0].center == self.moves_list[i-1]:

    # turn function
    def run(self):

        """
        pseudocode / design:
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

        """
        if self.whos_turn == self.user:  # it's the user player's turn
            # once the die has been rolled, the limit for the amount of moves will be set to
            # the die value
            if self.has_die_rolled:
                if not self.move_limit_set:  # prevents move_limit from being reset each update of run
                    self.move_limit = self.die.die_value
                    self.move_limit_set = True

                if self.move_limit >= 1:
                    self.can_player_move = True

                    if self.right_pressed or self.left_pressed or self.up_pressed or self.down_pressed:
                        self.press += 1

                    if self.press >= self.move_limit:
                        self.can_player_move = False  # this still has issues, player still moves if key held
                        """
                        in on_key_press, a condition exists for when has_player_moved is true,
                        which allows the player to press enter to switch the turn. This allows the
                        sprite to catch up to the player's final move before switching turns,
                        which was previously an issue.
                        boolean that indicates the player has moved, which activates the ability
                        to press ENTER to officially switch the next player
                        """
                        self.has_player_moved = True
                        self.move_limit = 0

        # otherwise it's the ai's turn, so the list of ai players will be iterated through
        # to handle their turns
        else:
            for i in range(0, len(self.ai_players)):
                # first will be second player, then third, etc
                if self.whos_turn == self.ai_players[i]:
                    # die will be rolled for them and the value they get will be shown
                    if not self.has_die_rolled:
                        self.die.roll_die()
                        self.has_die_rolled = True
                        self.move_limit = self.die.die_value
                        self.move_limit_set = True
                        # npc movement
                        for j in range(0, self.move_limit):
                            # for each move, will move a random direction, either up, left, or down
                            rand = random.randrange(0, 4)
                            if rand == 0:
                                self.ai_players[i].change_x = PLAYER_MOVEMENT
                                self.ai_players[i].update()
                                time.sleep(0.25)
                            elif rand == 1:
                                self.ai_players[i].change_y = PLAYER_MOVEMENT
                                self.ai_players[i].update()
                                time.sleep(0.25)
                            elif rand == 2:
                                self.ai_players[i].change_x = -PLAYER_MOVEMENT
                                self.ai_players[i].update()
                                time.sleep(0.25)
                            elif rand == 3:
                                self.ai_players[i].change_y = -PLAYER_MOVEMENT
                                self.ai_players[i].update()
                                time.sleep(0.25)
                        self.has_player_moved = True

    # Mouse listener
    def on_mouse_press(self, x, y, button, modifiers):

        # Convert the clicked mouse position into grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({column}, {row})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        # if row >= ROW_COUNT or column >= COLUMN_COUNT:
        # Simply return from this method since nothing needs updating
        # return

        # 915 - 925,  718 - 728 -16y

        # Update the sprite colors to match the new grid
        # self.resync_grid_with_sprites()

        # if it's the player's turn and the die hasn't been rolled, then the user can roll the die
        # once. In another section of the code, has_die_rolled will be reinitialized to false once the
        # turn has ended
        if self.whos_turn == self.user:
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

        # check for guess | make sure player is in room for this to be possible
        self.guess_box.check_click(x, y)
