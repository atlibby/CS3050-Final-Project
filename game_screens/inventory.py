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

CARD_WIDTH = 150
CARD_HEIGHT = 225
CARD_MARGIN = 15


all_card_names = ['Miss Scarlett', 'Colonel Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Professor Plum', 'Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge', 'Hall', 'Study', 'Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']


# show the inventory of the player
class InventoryMenu(arcade.View):
    def __init__(self, game_view, hand):
        super().__init__()
        self.game_view = game_view
        self.hand = hand

        # create a sprite list to hold your sprite objects
        self.card_sprite_list = arcade.SpriteList()

        num_columns = len(self.hand)  # Set the number of columns based on the number of cards in the hand
        print(num_columns)
        for i, card in enumerate(self.hand):
            # Calculate the x position to center the cards horizontally

            x = (SCREEN_WIDTH - (CARD_WIDTH * num_columns) - (CARD_MARGIN * (num_columns - 1))) / 2 + (CARD_WIDTH + CARD_MARGIN) * i
            
            # Center the cards vertically
            y = SCREEN_HEIGHT / 2

            
            #card_sprite = arcade.Sprite(filename="card_images/"+card+".jpeg",image_width=CARD_WIDTH, image_height=CARD_HEIGHT)
            card_sprite = arcade.Sprite(filename="card_images/revolver.png",image_width=CARD_WIDTH, image_height=CARD_HEIGHT)
            card_sprite.scale = 1

            card_sprite.center_x = x
            card_sprite.center_y = y
            self.card_sprite_list.append(card_sprite)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        text_width = len("Inventory") * 24 
        text_x = (SCREEN_WIDTH - text_width)/2
        text_y = SCREEN_HEIGHT - 60  # 30 pixels from the top
        arcade.draw_text("Inventory", text_x, text_y, arcade.color.WHITE, 30)

        self.card_sprite_list.draw()
        
    def on_key_press(self, key, modifiers):
         self.window.show_view(self.game_view)
