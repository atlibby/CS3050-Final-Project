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
# show the inventory of the player
class InventoryMenu(arcade.View):
    def __init__(self, game_view, hand):
        super().__init__()
        self.game_view = game_view
        self.hand = hand
        
        for item in hand:
            print(item)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Inventory", SCREEN_WIDTH/2, SCREEN_HEIGHT-30, arcade.color.WHITE, 24)

    def on_key_press(self, key, modifiers):
         self.window.show_view(self.game_view)
