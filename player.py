"""
Player class for the game
Initializing a Player object in main will mean providing information
on the player's color, name, initial position, and player status (whether
the player is a user or an NPC, which will determine whether said player is
controlled by keyboard/mouse events or by RNG)

The mark_sheet method will probably need to be dependent on a Clue Sheet class,
which I can create, and it would appear as a popup window that a player/NPC can interact
with

Conversely, we may not need a Clue Sheet class altogether and just have one generate
in main for each player, but personally I think it would be easier to have the Player
class interact with a Clue Sheet class similarly to how the Player class will interact
with the Card class, since NPC behavior will be much simpler to integrate this way
"""

import arcade
import random as r
from card import *
from room import Room

# test function for dividing cards evenly between six players
# will integrate with get_case_file method in main later
# for now, takes deck of cards from Card class, shuffles them,
# then removes three cards from the deck (one character card,
# one weapon card, one room card), and divides the cards evenly
# depending on how many people are playing
# For testing purposes, doing 6 players (three random cards per player), but later we could maybe add
# an option for an amount of NPCs the user wants to play against from 1-5
# even if the player decides to not play with all 5 other characters,
# the remaining character tokens will remain on the board to be moved into rooms
# if a player accuses them, but they will not do anything on their own and will not
# be granted turns


class Player(arcade.Sprite):

    def __init__(self, name, center_x, center_y, fileName, scale):
        super().__init__(filename = fileName, scale = scale)
        self.name = name
        self.center_x = center_x
        self.center_y = center_y

    # getters
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

    def get_player_name(self):
        return self.player_name

    def get_player_status(self):
        return self.player_status
    
    def get_player_hand(self):
        return self.player_hand
    # setters
    def set_x(self, center_x):
        self.x = center_x

    def set_y(self, center_y):
        self.y = center_y

    def set_color(self, player_color):
        self.color = player_color

    def set_player_name(self, player_name):
        self.player_name = player_name

    def set_player_status(self, player_status):
        self.player_status = player_status
    
    def set_player_hand(self, player_hand):
        self.player_hand = player_hand
        
    # this function returns the hands each player has including the case file
    @staticmethod
    def divide_cards(deck):
        plums_deck = []
        whites_deck = []
        greens_deck = []
        scarlets_deck = []
        peacocks_deck = []
        mustards_deck = []
        card_type = ["character", "room", "weapon"]
        case_file = []
        random.shuffle(deck)
        for card in deck:
            if card.cardType in card_type:
                case_file.append(card)
                card_type.remove(card.cardType)
        random.shuffle(deck)
        deck_size = len(deck)
        players = ["Scarlet", "Plum", "Peacock", "Mustard", "Green", "White"]
        remainder = deck_size % len(players)
        cards_to_deal = deck_size - remainder
        idx = 0
        buffer = 0
        for card in deck:
            if card not in case_file:
                card.owner = players[idx]
                # go to beginning of player list again, simulating loop
                if idx == len(players) - 1:
                    idx = 0
                else:
                    idx += 1

        for card in deck:
            if card.owner == 'Scarlet':
                scarlets_deck.append(card)
                buffer += 1
            elif card.owner == 'Plum':
                plums_deck.append(card)
                buffer += 1
            elif card.owner == 'Peacock':
                peacocks_deck.append(card)
                buffer += 1
            elif card.owner == 'Mustard':
                mustards_deck.append(card)
                buffer += 1
            elif card.owner == 'Green':
                greens_deck.append(card)
                buffer += 1
            elif card.owner == 'White':
                whites_deck.append(card)
                buffer += 1
            if buffer == cards_to_deal:
                break
        return [scarlets_deck, plums_deck, peacocks_deck, mustards_deck, greens_deck, whites_deck, case_file]


    # class functions
    def roll_die(self):
        roll = r.randrange(1, 6)
        return roll

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > 1090 - 321:
            self.right = 1090 - 321

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > 770 - 1:
            self.top = 770 - 1

    # def teleport(self, accused, room_coords):
    #     accused.move(room_coords)

    def make_accusation(self, accused_name, accused_room, accused_weapon, accuser):
        print(accuser + " thinks it was " + accused_name + " in the " + accused_room + " with the " + accused_weapon)


    def mark_sheet(self):
        pass

    def reveal_card(self):
        pass




#divide_cards()

