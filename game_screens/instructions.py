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
    "At the beginning of the players turn, they must roll the die. Use the arrow keys to move that number of times. \n"
    "The object of the player is to enter a room so that they can make a guess. Each guess will be comprised of a character, a room, and a weapon. \n"
    "Guesses can only be made while a player is in a room. Pressing enter will submit a guess. \n"
    "If another player has one of the cards you guessed, they will show it to you in turn. \n"
    "At the end of each players turn the user will hit enter to contiue gameplay. \n"
    "NPC characters will make guesses as well. In this case, you will be prompted to show them a card if you have one of the cards they guessed in your hand.\n"
    "To win, a player must make an accusation in the guessing room at the center of the board and correctly identify all three aspects of the murder. If the player gets one of the aspects wrong, they lose!\n\n"
    
    "Controls:\n"
    "Use arrow keys to move around the board.\n"
    "Click on the die to roll it.\n"
    "Press 'I' to access your inventory.\n"
    "Press 'A' to show your cards when prompted.\n"
    "Use the checkbox on the right hand side of the screen to keep track of what you have seen.\n"
    "Enter guesses in the rightmost checkbox column, press enter to submit a guess.\n\n"
    
    "Good luck!"
)


class Instructions(arcade.View):
  def __init__(self, game_view, width, height):
    super().__init__()
    self.manager = UIManager()
    self.manager.enable()
    self.game_view = game_view
    self.width = width
    self.height = height
    self.background_img = arcade.load_texture("images/clue_image.jpeg")
    # arcade.set_background_color(arcade.color.BLACK)

    # Load background texture
    bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
    
    # Create text area with instructions
    text_area = UITextArea(x=100,
                            y=200,
                            width=800,
                            height=500,
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
    arcade.draw_texture_rectangle(
        self.width // 2,
        self.height // 2,
        self.width,
        self.height,
        self.background_img
    )
    # Draw UI elements
    self.manager.draw()
  
  def on_key_press(self, symbol: int, modifiers: int):
    self.window.show_view(self.game_view)
    self.manager.remove_all_ui()
