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

class CardShowViewPlayer(arcade.View):
  def __init__(self, game_view, guessing_player, cards, npc_guess):
    super().__init__()
    self.game_view = game_view
    self.guessing_player = guessing_player
    self.cards = cards
    self.npc_guess_cards = npc_guess
    
    self.card_sprite_list = arcade.SpriteList()

    num_columns = len(self.cards)  # set the number of columns based on the number of cards in the hand
    for i, card in enumerate(self.cards):
        # calculate the x position to center the cards horizontally

        x = (SCREEN_WIDTH - (CARD_WIDTH * num_columns) - (CARD_MARGIN * (num_columns - 1))) / 2 + (CARD_WIDTH + CARD_MARGIN) * i
        
        # center the cards vertically
        y = SCREEN_HEIGHT / 2
        card_sprite = arcade.Sprite(filename="card_images/" + card.name + ".png",image_width=CARD_WIDTH, image_height=CARD_HEIGHT)
        card_sprite.scale = 1
        card_sprite.name = card.name
        
        card_sprite.center_x = x
        card_sprite.center_y = y
        self.card_sprite_list.append(card_sprite)
  
  def on_show(self):
    arcade.set_background_color(arcade.color.BLACK)

  def on_draw(self):
    arcade.start_render()
    
    text_width = len("Pick a card you want to show: " + self.guessing_player.name) * 24 
    text_x = (SCREEN_WIDTH - text_width)/2
    text_y = SCREEN_HEIGHT - 60 
    arcade.draw_text("Pick a card you want to show: " + self.guessing_player.name, text_x+25, text_y, arcade.color.WHITE, 30)

    text_width_two = len(self.guessing_player.name + " guesses " + self.npc_guess_cards[0] + ", " + self.npc_guess_cards[1] + ", " + self.npc_guess_cards[2]) * 20 
    text_x2 = (SCREEN_WIDTH - text_width_two)/2
    text_y2 = SCREEN_HEIGHT - 150 
    arcade.draw_text(self.guessing_player.name + " guesses " + self.npc_guess_cards[0] + ", " + self.npc_guess_cards[1] + ", " + self.npc_guess_cards[2], text_x2+40, text_y2, arcade.color.WHITE, 30)

    #arcade.draw_text("Click HERE to continue", text_x, text_y - 600, arcade.color.WHITE, 30)

    self.card_sprite_list.draw()
    
  def on_mouse_press(self, x, y, button, modifiers):
    for card_sprite in self.card_sprite_list:
        if card_sprite.collides_with_point((x, y)):
          print(f"Clicked on {card_sprite.name}")
          self.guessing_player.set_player_seen_cards(card_sprite.name)
          self.window.show_view(self.game_view)
          
class PlayerWatchExchange(arcade.View):
  def __init__(self, game_view, guessing_player, player_with_card, card, npc_guess):
    super().__init__()
    self.game_view = game_view
    self.guessing_player = guessing_player
    self.player_with_card = player_with_card
    self.card = card
    self.npc_guess_cards = npc_guess

    self.seen = self.guessing_player.get_player_seen_cards()
    for card in self.seen:
      print(f"{self.guessing_player.name} has seen {card}")
    
  def on_show(self):
    arcade.set_background_color(arcade.color.BLACK)
    
  def on_draw(self):
    arcade.start_render()
    y = SCREEN_HEIGHT/2
    
    text_width = len(self.player_with_card.name + " shows " + self.guessing_player.name + " a card") * 24 
    text_x = (SCREEN_WIDTH - text_width * .95)/2
    text_y = SCREEN_HEIGHT - 60 
    arcade.draw_text(self.player_with_card.name + " shows " + self.guessing_player.name + " a card", text_x+35, y, arcade.color.WHITE, 30)
    
    text_width_two = len(self.guessing_player.name + " guesses " + self.npc_guess_cards[0] + ", " + self.npc_guess_cards[1] + ", " + self.npc_guess_cards[2]) * 20
    text_x2 = (SCREEN_WIDTH - text_width_two / 1.05)
    arcade.draw_text(self.guessing_player.name + " guesses " + self.npc_guess_cards[0] + ", " + self.npc_guess_cards[1] + ", " + self.npc_guess_cards[2], text_x2+40, text_y, arcade.color.WHITE, 20)

    arcade.draw_text("Click HERE to continue", text_x+75, text_y - 600, arcade.color.WHITE, 30)

  def on_mouse_press(self, x, y, button, modifiers):
    self.window.show_view(self.game_view)