import random
import arcade

"""
Card Class for all card objects in the game.

Will need:
- Character card
- Room card
- Weapon card
- Clue card

The way I envision implementing it, the cards will be instantiated with existing information and intent,
so it's not like the cards will be created randomly. They have discrete values, so they have to be called with
discrete values.

Member variables:
@:param cardType - string (one word, will be lower-cased so case-insensitive) which describes the card type.
Can be either Character, Room, Weapon, Clue.
@:param name - string (can be multiple words, will be case-insensitive, maybe space-insensitive) describing the name
of the card. If character, name of char. If room, name of room. If weapon, name of weapon. If clue: different case,
must refer back to clue cards.
@:param owner - string, or player object, which will describe who owns this card. Will be initialized to none, such
that it can be initialized later perhaps in the game class when the cards are dealt.

Functions:
- to string for printing


Class Deck which is just a collection of cards
"""


class Card:
    def __init__(self, cardType, name):
        if cardType.lower() in ['character', 'room', 'weapon', 'clue']:
            self.cardType = cardType.lower()
        else:
            raise ValueError("Invalid card type. Must be 'character', 'room', 'weapon', or 'clue'.")
        self.name = name.lower()
        self.owner = None
        self.selected = False

    def __str__(self):
        return f"{self.cardType.capitalize()}: {self.name.capitalize()}, Owner: {self.owner}"


class Deck:
    @staticmethod
    def initialize_cards():
        character_cards = ['Miss Scarlett', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock',
                           'Professor Plum']
        room_cards = ['Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge',
                      'Hall', 'Study']
        weapon_cards = ['Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']

        cards = []
        # Initialize character cards
        for character in character_cards:
            cards.append(Card('character', character))
        # Initialize room cards
        for room in room_cards:
            cards.append(Card('room', room))
        # Initialize weapon cards
        for weapon in weapon_cards:
            cards.append(Card('weapon', weapon))

        # shuffling cards
        return cards
    
    def shuffle_deck(cards):
        random.shuffle(cards)

    def shuffle_deck(cards):
        random.shuffle(cards)

class ClueCard(arcade.Sprite):
    def __init__(self, name, description, task):
        self.name = name
        self.description = description
        self.task = task

    @staticmethod
    def initialize_cards(f_name):
        self_clue_cards = []
        with open(f_name, 'r') as file:
            for i, line in enumerate(file):
                if i == 0:
                    continue  # Skip the first line
                data = line.strip().split(',')
                if len(data) == 3:
                    name = data[0]
                    description = data[1]
                    task = data[2]
                    clue_card = ClueCard(name, description, task)
                    self_clue_cards.append(clue_card)
        return self_clue_cards


# Test the Card class
if __name__ == "__main__":
    # Test initializing cards, and creating our own decks to select from deck where owner is our names
    stevens_deck = []
    reubens_deck = []
    andrews_deck = []
    nats_deck = []

    deck = Deck.initialize_cards()
    players = ['steven', 'reuben', 'nat', 'andrew']
    idx = 0
    print("----------------------------------\nPlayer, Location, and Weapon cards"
          "\n----------------------------------\n")
    for card in deck:
        card.owner = players[idx]
        print(card)
        # go to beginning of player list again, simulating loop
        if idx == len(players) - 1:
            idx = 0
        else:
            idx += 1

    for card in deck:
        if card.owner == 'steven':
            stevens_deck.append(card)
        elif card.owner == 'reuben':
            reubens_deck.append(card)
        elif card.owner == 'andrew':
            andrews_deck.append(card)
        elif card.owner == 'nat':
            nats_deck.append(card)

    print("\n-------------------\n\tClue Cards:\n-------------------\n")
    # testing initializing clue cards
    clue_cards = ClueCard.initialize_cards("clue_cards.txt")
    for card in clue_cards:
        print(card.name + "\n" + card.description, card.task + "\n")