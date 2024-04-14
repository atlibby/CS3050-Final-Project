import random
from random import randint

import arcade.gui
from die_arcade import DIE_X, DIE_Y, Die
from checkboxes import Button
import time
from typing import List
from player import *
from room_dimensions import room_list, door_dict
import room_dimensions
from guess_box import Guess, GUESS_BOX_X, GUESS_BOX_Y
from game_screens.inventory import InventoryMenu
from game_screens.npc_show_card import CardViewNPC
from game_screens.player_show_card import CardShowViewPlayer, PlayerWatchExchange
from game_screens.win_screen import WinScreen
from game_screens.lose_screen import LoseScreen
from game_screens.instructions import Instructions


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
    def __init__(self, width, height, player_selected):
        super().__init__()
        # super().__init__(width, height, title)
        self.width = width
        self.height = height

        self.character_cards = ['Miss Scarlett', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock',
                           'Professor Plum']
        self.room_cards = ['Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge',
                      'Hall', 'Study']
        self.weapon_cards = ['Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']

        self.door_list = []
        for room in door_dict:
            for door in door_dict.get(room):
                self.door_list.append(door)

        self.deck = Deck.initialize_cards()
        Deck.shuffle_deck(self.deck)
        # We can quickly build a grid with python list comprehension
        self.grid = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

        # Set the window's background color
        self.background_color = arcade.color.BLACK

        # Create a dictionary to store room locations
        self.rooms = {
            'study': room_dimensions.study,
            'hall': room_dimensions.hall,
            'lounge': room_dimensions.lounge,
            'library': room_dimensions.library,
            'billiard_room': room_dimensions.billiard_room,
            'conservatory': room_dimensions.conservatory,
            'ballroom': room_dimensions.ballroom,
            'kitchen': room_dimensions.kitchen,
            'dining-room': room_dimensions.dining_room,
            'guessing_room': room_dimensions.guessing_room
        }

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

        for player in self.players:
            print(player)
        # self.user will be the player object using the index of player_selected,
        # then from a list of players not the user, will iterate thru them
        self.user = self.players[player_selected]

        # creating a copy of self.players, which I will pop self.user and then
        # that will be the ai players
        self.ai_players = arcade.SpriteList()

        for i in range(0, len(self.players)):
            if self.players[i] != self.user:
                self.ai_players.append(self.players[i])

        # split up the cards, player select screen
        # self.current_player = 0 #this will be a function that calls player select view or gets information fed into it by player-select
        # Make a deck

        self.hands = Player.divide_cards(self.deck)
        self.case_file = self.hands[-1]

        self.old_coords = []

        # all the hands for all the players are innitialized
        for i, player in enumerate(self.players):
            player.set_player_hand(self.hands[i])
        self.player_hand = self.user.get_player_hand()
        for npc in self.ai_players:
            npc_hand = npc.get_player_hand()
            for card in npc_hand:
                npc.set_player_seen_cards(card.name)
                if card.cardType == "room":
                    npc.no_go_rooms.append(card.name)

            random_room_index = random.randint(0, len(self.door_list) - 1)
            npc.target_coords = self.door_list[random_room_index]

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

        self.valid_move = True

        self.idle = 90

        # steven - changing self.move_limit from 6 to 0, so that player cannot move until this value is updated from
        # rollDie()
        self.move_limit = 0

        self.left_pressed = False

        self.right_pressed = False

        self.up_pressed = False

        self.down_pressed = False

        self.key_presses = []

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
        self.last_clicked = [[], [], []]

        ''' 
        variables for turns

        '''
        # self.whos_turn: overhead manager type variable which keeps track of who's turn it is. This will be used
        # later on to determine what gets drawn, who can move, and who's icon is shown. Will hold the first player
        # object in self.players for now, could become a dictionary if it works better later.
        self.whos_turn = self.user

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

        self.user_guessed = False

        self.ai_guessed = False

        self.player_in_room = False

        # Resyncing
        self.resync_grid_with_sprites()

    def test_player_accusation(self, player_card, weapon_card, room_card):
        card_seen = False
        npc_cards = []
        npc_with_card = ''
        for npc in self.ai_players:
            npc_hand = npc.get_player_hand()
            # check for suspect card
            for npc_card in npc_hand:
                if npc_card.name in [player_card, weapon_card, room_card]:
                    npc_cards.append(npc_card)
                    npc_with_card = npc.name
                    card_seen = True
            # if a card is found, break out of the loop
            if card_seen:
                break
        # show the card if found
        if card_seen:
            random_index = randint(0, len(npc_cards) - 1)
            npc_card_view = CardViewNPC(self, npc_with_card, npc_cards[random_index])
            self.window.show_view(npc_card_view)

    def test_non_player_accusation(self, player_card, weapon_card, room_card):
        turn_order = []
        npc_guess = [player_card, weapon_card, room_card]
        npc_accusing = self.whos_turn  # self.players[3]
        npc_accusing_index = self.players.index(npc_accusing)

        # creating a queue of players to show their cards in turn
        # the player making a guess is not in this list
        for i in range(npc_accusing_index + 1, len(self.players)):
            turn_order.append(self.players[i])

        if npc_accusing_index != 0:
            for i in range(0, npc_accusing_index):
                turn_order.append(self.players[i])
        # now we want to iterate through each character in the list, and compare the cards in their hand with what's in the accusation hand
        # this is going to check all the cards that match in one players hand, once a player has a card that matches it looks for no other players but finishes looking through their hand
        seen_cards = []
        match_found = False
        player_with_matched_card = None
        done_searching = 0
        while match_found == False and done_searching == 0:
            for player in turn_order:
                player_hand = player.get_player_hand()
                for card in player_hand:
                    if card.name in [player_card, weapon_card, room_card]:
                        seen_cards.append(card)
                        match_found = True
                        player_with_matched_card = player
                        break
                if match_found:
                    break  # break out of the outer loop
            done_searching = 1
        # at this point we have the player with the card, and the card(s) they have that match
        if match_found == False:
            print("no matches were found")
        else:
            if player_with_matched_card == self.user:
                # this is where we will show the player npc view
                print(f"you have the card: {seen_cards[0].name}")
                card_show_view_player = CardShowViewPlayer(self, npc_accusing, seen_cards, npc_guess)
                self.window.show_view(card_show_view_player)
            else:
                # now we have the player_with_matched card show one card to the npc
                print(f"{player_with_matched_card.name} has {seen_cards[0].name}")
                npc_exchange_view = PlayerWatchExchange(self, npc_accusing, player_with_matched_card, seen_cards[0], npc_guess)
                self.window.show_view(npc_exchange_view)

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
            win = WinScreen()
            self.window.show_view(win)

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
            if button.guess:
                if button.clicked:
                    if self.last_clicked[0] and button == self.last_clicked[0][len(self.last_clicked[0]) - 1]:
                        button.draw(True)
                    elif self.last_clicked[1] and button == self.last_clicked[1][len(self.last_clicked[1]) - 1]:
                        button.draw(True)
                    elif self.last_clicked[2] and button == self.last_clicked[2][len(self.last_clicked[2]) - 1]:
                        button.draw(True)
                    else:
                        button.draw(False)
                else:
                    button.draw(True)
            else:
                button.draw(True)

        self.guess_box.draw()

        ''' Turn Based Drawings '''
        # first, an indication of who's turn it is at the top of the sidebar
        arcade.draw_text(str(self.whos_turn.name) + "'s turn!", (self.width - SIDEBAR_WIDTH) + 110, 755,
                         color=arcade.color.BLACK, font_size=10)
        arcade.draw_text("Press G for Instructions", DIE_X - 150, DIE_Y - 100, arcade.color.BLACK, 15)
        # for when it's the user's turn
        if self.whos_turn == self.user:  # it's the user player's turn
            if not self.has_die_rolled:
                # indicate the user to roll the die
                arcade.draw_text("Roll The Die!", DIE_X - 37, DIE_Y - 50, arcade.color.BLACK, 10)
            else:
                # now after the die has been rolled, it will display the value
                text = f"You rolled a {self.die.die_value}!"
                arcade.draw_text(text, DIE_X - 45, DIE_Y - 50, arcade.color.BLACK, 10)
                self.check_player_in_room()

                if self.player_in_room and (not self.user_guessed) and self.has_player_moved:
                    arcade.draw_text("Check the boxes, then click ENTER", DIE_X - 115, DIE_Y + 50, arcade.color.BLACK, 10)

                # if the player has already done all their moves, but hasn't submitted their turn
                elif not self.player_in_room and self.has_player_moved:
                    # indicate the user to press enter to switch turns
                    arcade.draw_text("ENTER to Continue!", DIE_X - 65, DIE_Y + 50, arcade.color.BLACK, 10)
        else:
            if self.has_die_rolled:
                # now after the die has been rolled, it will display the value
                text = f"{self.whos_turn.name} rolled a {self.die.die_value}!"
                arcade.draw_text(text, DIE_X - 50, DIE_Y - 50, arcade.color.BLACK, 10)

                if self.player_in_room and not self.ai_guessed and not self.has_player_moved:
                    # indicate the user to press A to show cards
                    arcade.draw_text("A to Show Cards!", DIE_X - 75, DIE_Y + 50, arcade.color.BLACK, 10)
                # if the player has already done all their moves, but hasn't submitted their turn
                if self.has_player_moved:
                    # indicate the user to press enter to switch turns
                    arcade.draw_text("ENTER to Continue!", DIE_X - 65, DIE_Y + 50, arcade.color.BLACK, 10)

    # Redraw sprite when sprite moves
    def on_update(self, delta_time):
        # run
        self.check_guess_for_win()
        self.run()

    # Allow player movement with arrow keys
    # time delay to allow for sprite to move
    # one grid square at a time per key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.L:
             lose = LoseScreen()
             self.window.show_view(lose)
        if key == arcade.key.G:
            instructions = Instructions(self, self.width, self.height)
            self.window.show_view(instructions)
        if not self.player_in_room:
            self.old_coords = [self.whos_turn.center_y, self.whos_turn.center_x]
        print(self.old_coords)

        # if its the player's turn and the player can't move (so theyve made their moves) and they're in a room and
        # they haven't guessed, then they can guess

        if self.whos_turn != self.user:
            if not self.can_player_move and not self.ai_guessed:
                if key == arcade.key.A:
                    player_card = None
                    room_card = None
                    weapon_card = None
                    player_seen_cards = self.whos_turn.get_player_seen_cards()
                    save_list = []
                    for card in self.weapon_cards:
                        if card in player_seen_cards:
                            save_list.append(card)
                            self.weapon_cards.remove(card)
                    random_index = random.randint(0, len(self.weapon_cards) - 1)
                    weapon_card = self.weapon_cards[random_index].lower()
                    for card in self.character_cards:
                        if card in player_seen_cards:
                            save_list.append(card)
                            self.character_cards.remove(card)
                    random_index = random.randint(0, len(self.character_cards) - 1)
                    player_card = self.character_cards[random_index].lower()
                    for card in self.room_cards:
                        if card in player_seen_cards:
                            save_list.append(card)
                            self.room_cards.remove(card)
                    random_index = random.randint(0, len(self.character_cards) - 1)
                    room_card = self.room_cards[random_index].lower()
                    for card in save_list:
                        if card.cardType == 'weapon':
                            self.weapon_cards.append(card)
                        elif card.cardType == 'room':
                            self.room_cards.append(card)
                        else:
                            self.character_cards.append(card)
                    self.test_non_player_accusation(player_card, room_card, weapon_card)
                    self.ai_guessed = True

        if key == arcade.key.I:
            inv = InventoryMenu(self, self.player_hand)
            self.window.show_view(inv)

        user_coords = [self.user.center_y // (WIDTH + MARGIN), self.user.center_x // (HEIGHT + MARGIN)]
        if self.whos_turn == self.user:
            if self.can_player_move:
                if key == arcade.key.UP:
                    self.up_pressed = True
                    self.key_presses.append(1)
                elif key == arcade.key.DOWN:
                    self.down_pressed = True
                    self.key_presses.append(2)
                elif key == arcade.key.LEFT:
                    self.left_pressed = True
                    self.key_presses.append(3)
                elif key == arcade.key.RIGHT:
                    self.right_pressed = True
                    self.key_presses.append(4)
                # if the user hits a room wall, that movement won't count as a move
                for room in room_list:
                    if self.right_pressed and [user_coords[0], user_coords[1] + 1] in room:
                        self.valid_move = False
                    if self.left_pressed and [user_coords[0], user_coords[1] - 1] in room:
                        self.valid_move = False
                    if self.up_pressed and [user_coords[0] + 1, user_coords[1]] in room:
                        self.valid_move = False
                    if self.down_pressed and [user_coords[0] - 1, user_coords[1]] in room:
                        self.valid_move = False

                # if the user tries to go back a grid square, they won't be able to
                # won't count as a move
                if len(self.key_presses) >= 2:
                    if self.up_pressed and self.key_presses[-2] == 2:
                        self.valid_move = False
                        self.key_presses.remove(self.key_presses[-1])
                    if self.down_pressed and self.key_presses[-2] == 1:
                        self.valid_move = False
                        self.key_presses.remove(self.key_presses[-1])
                    if self.left_pressed and self.key_presses[-2] == 4:
                        self.valid_move = False
                        self.key_presses.remove(self.key_presses[-1])
                    if self.right_pressed and self.key_presses[-2] == 3:
                        self.valid_move = False
                        self.key_presses.remove(self.key_presses[-1])

                if (self.valid_move):
                    self.update_player_movement()
                    self.press += 1
                self.valid_move = True

        # in the case the turn is over, either ai or player, and its time to switch turns
        if self.has_player_moved:
            # if its either the user's turn and they're not in the room anymore, or its the ai's turn and
            # it doesn't matter if they're in the room or not
            if (self.whos_turn == self.user and not self.player_in_room) or self.whos_turn != self.user:
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

        # in the case that it's the user's turn and they went into the room, but haven't guessed yet.
        if self.whos_turn == self.user and self.has_player_moved and self.player_in_room and not self.user_guessed:
            if key == arcade.key.ENTER:
                if self.guess_box.guess_clicked:
                    accusation = []
                    for button in self.sidebar_buttons:
                        if button.guess:
                            if button.card.selected:
                                accusation.append(button.card.name)
                    self.test_player_accusation(accusation[0], accusation[1], accusation[2])

                    # if (self.guess_box.guess_clicked):
                    self.user.center_y = self.old_coords[0]
                    self.user.center_x = self.old_coords[1]
                    self.player_in_room = False
                self.update_player_movement()
                self.user_guessed = True


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
        self.whos_turn.change_x = 0
        self.whos_turn.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.whos_turn.change_y = PLAYER_MOVEMENT
            time.sleep(0.1)
        elif self.down_pressed and not self.up_pressed:
            self.whos_turn.change_y = -PLAYER_MOVEMENT
            time.sleep(0.1)
        if self.left_pressed and not self.right_pressed:
            self.whos_turn.change_x = -PLAYER_MOVEMENT
            time.sleep(0.1)
        elif self.right_pressed and not self.left_pressed:
            self.whos_turn.change_x = PLAYER_MOVEMENT
            time.sleep(0.1)

        self.whos_turn.update()

        if self.press >= self.move_limit:
            self.whos_turn.change_y = 0
            self.whos_turn.change_x = 0
            self.press = 0
            self.key_presses.clear()

        self.guess_box.update_user_position(self.user.center_x, self.user.center_y)


    def check_player_in_room(self):
        current_player_coords = [self.whos_turn.center_y // (WIDTH + MARGIN),
                                 self.whos_turn.center_x // (HEIGHT + MARGIN)]
        for room in room_list:
            if current_player_coords in room:
                self.player_in_room = True
                break
            else:
                self.player_in_room = False

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

        if self.whos_turn == self.user:  # it's the user player's turn
            """ 
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
            """
            # once the die has been rolled, the limit for the amount of moves will be set to
            # the die value
            if self.has_die_rolled:
                if not self.move_limit_set:  # prevents move_limit from being reset each update of run
                    self.move_limit = self.die.die_value
                    self.move_limit_set = True

                if self.move_limit >= 1:
                    self.can_player_move = True
                    user_coords = [self.user.center_y // (WIDTH + MARGIN), self.user.center_x // (HEIGHT + MARGIN)]
                    in_door_list = False
                    door = -1
                    for x in range(0, len(self.door_list)):
                        if self.door_list[x] == user_coords:
                            in_door_list = True
                            door = x
                    if in_door_list:
                        self.has_player_moved = True
                        teleport_list = [[12, 3], [11, 11], [11, 11], [11, 11], [11, 20], [6, 20], [6, 20],
                                         [8, 3], [8, 3], [5, 2], [5, 2], [3, 11], [3, 11], [3, 11], [3, 11],
                                         [2, 3], [2, 21], [7, 11], [7, 11], [7, 11]]
                        # add offset for each character
                        self.press = self.move_limit
                        self.user.center_x = teleport_list[door][1] * (WIDTH + MARGIN)
                        self.user.center_y = teleport_list[door][0] * (WIDTH + HEIGHT)
                        self.player_in_room = True

                        # add offset for each character
                        self.press = self.move_limit

                    if self.press >= self.move_limit:
                        self.can_player_move = False

                        # before making has_player_moved true to end turn, handle in-room scenario

                        '''
                        Handling room logic. Either inside user turn, or in a different area
                        if player in room, then they MUST guess
                            After they guess, pass the card values to player_accusation() as params
                            Then, change turns
                        '''
                        # self.check_player_in_room()

                        # if self.player_in_room:
                        if self.player_in_room and self.has_player_moved:
                            if self.user_guessed:
                                self.move_limit = 0
                                self.valid_move = True
                                self.press = 0
                                self.user_guessed = False
                                self.player_in_room = False
                        else:
                            self.has_player_moved = True
                            self.move_limit = 0
                            self.valid_move = True
                            self.press = 0

                        '''else:
                            self.has_player_moved = True
                            self.move_limit = 0
                            self.valid_move = True
                            self.press = 0'''


        # otherwise it's the ai's turn, so the list of ai players will be iterated through
        # to handle their turns
        else:
            for i in range(0, len(self.ai_players)):
                # first will be second player, then third, etc
                if self.whos_turn == self.ai_players[i]:
                    ai_coords = [self.ai_players[i].center_y // (WIDTH + MARGIN),
                                 self.ai_players[i].center_x // (HEIGHT + MARGIN)]
                    # die will be rolled for them and the value they get will be shown
                    if not self.has_die_rolled:
                        self.die.roll_die()
                        self.has_die_rolled = True
                        self.move_limit = self.die.die_value
                        self.move_limit_set = True
                        # npc movement
                        last_move = -1
                        while self.move_limit > 0:
                            ai_coords = [self.ai_players[i].center_y // (WIDTH + MARGIN),
                                         self.ai_players[i].center_x // (HEIGHT + MARGIN)]
                            self.ai_players[i].priority.clear()
                            # for each move, we prioritize a list of directions based on NPC position
                            if ai_coords[1] < self.whos_turn.get_target_coords()[1]:
                                self.whos_turn.priority.append(1)
                                if ai_coords[0] < self.whos_turn.get_target_coords()[0]:
                                    self.whos_turn.priority.append(3)
                                    self.whos_turn.priority.append(4)
                                else:
                                    self.whos_turn.priority.append(4)
                                    self.whos_turn.priority.append(3)
                                self.whos_turn.priority.append(2)
                            elif ai_coords[1] > self.whos_turn.get_target_coords()[1]:
                                self.whos_turn.priority.append(2)
                                if ai_coords[0] < self.whos_turn.get_target_coords()[0]:
                                    self.whos_turn.priority.append(3)
                                    self.whos_turn.priority.append(4)
                                else:
                                    self.whos_turn.priority.append(4)
                                    self.whos_turn.priority.append(3)
                                self.whos_turn.priority.append(1)
                            elif ai_coords[1] == self.whos_turn.get_target_coords()[1]:
                                if ai_coords[0] < self.whos_turn.get_target_coords()[0]:
                                    self.whos_turn.priority.append(3)
                                    self.whos_turn.priority.append(4)
                                else:
                                    self.whos_turn.priority.append(4)
                                    self.whos_turn.priority.append(3)
                                self.whos_turn.priority.append(2)
                                self.whos_turn.priority.append(1)
                            in_door_list = False
                            # if the npc is not in a door or room, we update their last location
                            if not self.player_in_room and ai_coords not in self.door_list:
                                self.old_coords = [self.whos_turn.center_y, self.whos_turn.center_x]
                            # if they are in a door, we teleport them inside the room
                            for x in range(0, len(self.door_list)):
                                if self.door_list[x] == ai_coords:
                                    in_door_list = True
                                    door = x
                            if in_door_list:
                                teleport_list = [[12, 3], [11, 11], [11, 11], [11, 11], [11, 20], [6, 20], [6, 20],
                                                 [8, 3], [8, 3], [5, 2], [5, 2], [3, 11], [3, 11], [3, 11], [3, 11],
                                                 [2, 3], [2, 21], [7, 11], [7, 11], [7, 11]]
                                #TODO: add offset for each character
                                self.press = self.move_limit
                                self.whos_turn.center_x = teleport_list[door][1] * (WIDTH + MARGIN)
                                self.whos_turn.center_y = teleport_list[door][0] * (WIDTH + HEIGHT)
                                self.player_in_room = True
                                break
                            # bad moves are ones that are invalid (walking into a wall)
                            bad_move_list = [False, False, False, False]
                            # here we loop through the directions by priority, and try to find a good move
                            for direction in self.whos_turn.priority:
                                if direction == 1 and last_move != 2 and not bad_move_list[0]:
                                    if ai_coords[1] != 23:
                                        for room in room_list:
                                            if [ai_coords[0], ai_coords[1] + 1] in room:
                                                self.valid_move = False
                                        if self.valid_move:
                                            self.ai_players[i].change_x = PLAYER_MOVEMENT
                                            self.ai_players[i].change_y = 0
                                            self.ai_players[i].update()
                                            self.move_limit -= 1
                                            last_move = 1
                                            count = 0
                                            break
                                        bad_move_list[0] = True
                                if direction == 3 and last_move != 4 and not bad_move_list[2]:
                                    if ai_coords[0] != 23:
                                        for room in room_list:
                                            if [ai_coords[0] + 1, ai_coords[1]] in room:
                                                self.valid_move = False
                                        if self.valid_move:
                                            self.ai_players[i].change_y = PLAYER_MOVEMENT
                                            self.ai_players[i].change_x = 0
                                            self.move_limit -= 1
                                            self.ai_players[i].update()
                                            last_move = 3
                                            count = 0
                                            break
                                        bad_move_list[2] = True
                                if direction == 2 and last_move != 1 and not bad_move_list[1]:
                                    if ai_coords[1] != 0:
                                        for room in room_list:
                                            if [ai_coords[0], ai_coords[1] - 1] in room:
                                                self.valid_move = False
                                        if self.valid_move:
                                            self.ai_players[i].change_x = -PLAYER_MOVEMENT
                                            self.ai_players[i].change_y = 0
                                            self.move_limit -= 1
                                            self.ai_players[i].update()
                                            last_move = 2
                                            count = 0
                                            break
                                        bad_move_list[1] = True
                                if direction == 4 and last_move != 3 and not bad_move_list[3]:
                                    if ai_coords[0] != 0:
                                        for room in room_list:
                                            if [ai_coords[0] - 1, ai_coords[1]] in room:
                                                self.valid_move = False
                                        if self.valid_move:
                                            self.ai_players[i].change_y = -PLAYER_MOVEMENT
                                            self.ai_players[i].change_x = 0
                                            self.move_limit -= 1
                                            self.ai_players[i].update()
                                            last_move = 4
                                            count = 0
                                            break
                                        bad_move_list[3] = True
                                self.valid_move = True

                        self.can_player_move = False
                    self.check_player_in_room()
                    # if the AI is in a room, we reset their target coordinates and teleport them
                    # out of the room once they have guessed
                    if self.player_in_room:
                        if self.ai_guessed:
                            if len(self.whos_turn.player_seen_cards) > 14:
                                self.whos_turn.target_coords = [15, 11]
                            else:
                                random_room_index = random.randint(0, len(self.door_list) - 1)
                                self.whos_turn.target_coords = self.door_list[random_room_index]
                            self.has_player_moved = True
                            self.move_limit = 0
                            self.valid_move = True
                            self.ai_guessed = False
                            self.ai_players[i].center_y = self.old_coords[0]
                            self.ai_players[i].center_x = self.old_coords[1]
                            self.update_player_movement()
                    else:
                        self.has_player_moved = True
                        self.move_limit = 0
                        self.valid_move = True

                        # self.has_player_moved = True

                    # logic for npc player making an accusation

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
        """
        # Flip the location between 1 and 0.
        if self.grid[row][column] == 0:
            self.grid[row][column] = 1
        else:
            self.grid[row][column] = 0
        """
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
            if button.guess:
                if button.card.cardType == 'weapon' and button not in self.last_clicked[0]:
                    self.last_clicked[0].append(button)
                if button.card.cardType == 'room' and button not in self.last_clicked[1]:
                    self.last_clicked[1].append(button)
                if button.card.cardType == 'character' and button not in self.last_clicked[2]:
                    self.last_clicked[2].append(button)
            if not button.clicked and button in self.last_clicked[0]:
                self.last_clicked[0].remove(button)
            elif not button.clicked and button in self.last_clicked[1]:
                self.last_clicked[1].remove(button)
            elif not button.clicked and button in self.last_clicked[2]:
                self.last_clicked[2].remove(button)

        # check for guess | make sure player is in room for this to be possible
        self.guess_box.check_click(x, y)
