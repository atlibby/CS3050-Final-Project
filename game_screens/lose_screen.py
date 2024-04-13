import arcade
# from player_select_screen import PlayerSelect
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

class LoseScreen(arcade.View):
  def __init__(self):
    super().__init__()
    self.width = SCREEN_WIDTH
    self.height = SCREEN_HEIGHT
  
  def on_show(self):
    arcade.set_background_color(arcade.color.RED)
    
  def on_draw(self):
    arcade.start_render()

    text_width = len("LOSER you guessed wrong... sorry") * 24 
    text_x = (SCREEN_WIDTH-text_width)/2
    text_y = SCREEN_HEIGHT/2
    arcade.draw_text("LOSER you guessed wrong... sorry", text_x, text_y, arcade.color.BLACK, 30)
      
  