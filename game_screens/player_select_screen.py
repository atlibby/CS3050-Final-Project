import arcade
from clue_game import ClueGameView

# show the inventory of the player
player_names = ["Scarlet", "Plum", "Peacock", "Mustard", "Green", "White"]

class PlayerSelect(arcade.View):
  def __init__(self, width, height):
    super().__init__()
    # a UIManager to handle the UI.
    self.manager = arcade.gui.UIManager()
    self.manager.enable()
    
    self.width = width
    self.height = height
    self.player_selected = None
    self.player_buttons = arcade.SpriteList()
    self.background_img = arcade.load_texture("images/clue_image.jpeg")

    # arcade.set_background_color(arcade.color.RASPBERRY)
    self.v_box = arcade.gui.UIBoxLayout()
    
    i = 0
    self.player_buttons = []
    for name in player_names:
      self.player_button = arcade.gui.UIFlatButton(text=name, width=200)
      self.player_buttons.append(self.player_button)
      self.v_box.add(self.player_button.with_space_around(bottom=20))
      
    self.player_buttons[0].on_click = self.on_click_player_0
    self.player_buttons[1].on_click = self.on_click_player_1
    self.player_buttons[2].on_click = self.on_click_player_2
    self.player_buttons[3].on_click = self.on_click_player_3
    self.player_buttons[4].on_click = self.on_click_player_4
    self.player_buttons[5].on_click = self.on_click_player_5
    
    # Create a widget to hold the v_box widget, that will center the buttons
    self.manager.add(
        arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.v_box)
    )
    
  def on_click_player_0(self, event):
    self.player_selected = 0
    clue_game_view = ClueGameView(self.width, self.height, self.player_selected)
    self.manager.disable()
    self.window.show_view(clue_game_view)
    
    
  def on_click_player_1(self, event):
    self.player_selected = 1
    clue_game_view = ClueGameView(self.width, self.height, self.player_selected)
    self.manager.disable()
    self.window.show_view(clue_game_view)
    
  def on_click_player_2(self, event):
    self.player_selected = 2
    clue_game_view = ClueGameView(self.width, self.height, self.player_selected)
    self.manager.disable()
    self.window.show_view(clue_game_view)
  
    
  def on_click_player_3(self, event):
    self.player_selected = 3
    clue_game_view = ClueGameView(self.width, self.height, self.player_selected)
    self.manager.disable()
    self.window.show_view(clue_game_view)
    
    
  def on_click_player_4(self, event):
    self.player_selected = 4
    clue_game_view = ClueGameView(self.width, self.height, self.player_selected)
    self.manager.disable()
    self.window.show_view(clue_game_view)
    
    
  def on_click_player_5(self, event):
    self.player_selected = 5
    clue_game_view = ClueGameView(self.width, self.height, self.player_selected)
    self.manager.disable()
    self.window.show_view(clue_game_view)
    
    
  def on_draw(self):
    self.clear()
    arcade.draw_texture_rectangle(
        self.width // 2,
        self.height // 2,
        self.width,
        self.height,
        self.background_img
    )

    self.manager.draw()