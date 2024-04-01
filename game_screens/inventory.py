import arcade
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

CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 10

all_card_names = ['Miss Scarlett', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Professor Plum', 'Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge', 'Hall', 'Study', 'Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']

# show the inventory of the player
class InventoryMenu(arcade.View):
    def __init__(self, game_view, hand):
        super().__init__()
        self.game_view = game_view
        self.hand = hand
        
            
        # create a sprite list to hold your sprite objects
        self.card_sprite_list = arcade.SpriteList()
        
        num_columns = 8  # number of columns in the grid
        for i, item in enumerate(hand):
            column = i % num_columns
            row = i // num_columns

            x = column * (CARD_WIDTH + CARD_MARGIN) + (CARD_WIDTH / 2 + CARD_MARGIN)
            y = row * (CARD_HEIGHT + CARD_MARGIN) + (CARD_HEIGHT / 2 + CARD_MARGIN)
            card_sprite = arcade.SpriteSolidColor(CARD_WIDTH, CARD_HEIGHT, arcade.color.FLORAL_WHITE)
            card_sprite.center_x = x
            card_sprite.center_y = y
            
            self.card_sprite_list.append(card_sprite)
        
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Inventory", SCREEN_WIDTH/2, SCREEN_HEIGHT-30, arcade.color.WHITE, 24)
        self.card_sprite_list.draw()
        
    def on_key_press(self, key, modifiers):
         self.window.show_view(self.game_view)
