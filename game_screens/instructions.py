import arcade
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UITexturePane

# Instructions for Clue game
CLUE_INSTRUCTIONS = (
    "Welcome to Clue!\n\n"
    "Objective:\n"
    "The objective of the game is to determine the details of the murder mystery: "
    "who committed the murder, in which room, and with which weapon.\n\n"
    
    "Gameplay:\n"
    "Players move around the mansion, making suggestions about the murderer, room, and weapon. "
    "Other players disprove these suggestions using cards in their hands.\n"
    "To win, a player must make an accusation and correctly identify all three aspects of the murder.\n\n"
    
    "Controls:\n"
    "Use arrow keys to move around the mansion.\n"
    "Press 'S' to make a suggestion.\n"
    "Press 'A' to make an accusation.\n\n"
    
    "Good luck!"
)


class Instructions(arcade.View):
  def __init__(self, game_view):
    super().__init__()
    self.manager = UIManager()
    self.manager.enable()
    self.game_view = game_view
    arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    # Load background texture
    bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
    
    # Create text area with instructions
    text_area = UITextArea(x=100,
                            y=200,
                            width=600,
                            height=400,
                            text=CLUE_INSTRUCTIONS,
                            text_color=(0, 0, 0, 255))
      
    # Add text area to the manager
    self.manager.add(
      UITexturePane(
          text_area.with_space_around(right=20),
          tex=bg_tex,
          padding=(10, 10, 10, 10)
      )
  )

  def on_draw(self):
    # Clear the screen
    self.clear()
    # Draw UI elements
    self.manager.draw()
  
  def on_key_press(self, symbol: int, modifiers: int):
    self.window.show_view(self.game_view)
