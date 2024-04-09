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

player_names = ["Scarlet", "Plum", "Peacock", "Mustard", "Green", "White"]

class CardViewNPC(arcade.View):
  def __init__(self, game_view, player, npc_hands):
    super().__init__()
    self.game_view = game_view
    self.player = player_names[player]
    self.npc_hand = npc_hands

  def on_show(self):
    arcade.set_background_color(arcade.color.BLACK)

  def on_draw(self):
    arcade.start_render()

    text_width = len(self.player + " shows you") * 24 
    text_x = (SCREEN_WIDTH - text_width)/2
    text_y = SCREEN_HEIGHT - 60 
    arcade.draw_text(self.player + " shows you", text_x, text_y, arcade.color.WHITE, 30)

    self.card_sprite_list.draw()
      
  def on_key_press(self, key, modifiers):
    self.window.show_view(self.game_view)
