import arcade
import os

# Set how many rows and columns we will have
ROW_COUNT = 15
COLUMN_COUNT = 15

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Clue"


class clueGame(arcade.Window):
    def __init__(self, width, height, title):
        # Call parent class and set up game window
        super().__init__(width, height, title)

        self.grid = []
        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)  # Append a cell


        arcade.set_background_color(arcade.color.AMAZON)
        self.background = None

        # Create a spritelist for batch drawing all the grid sprites
        self.grid_sprite_list = arcade.SpriteList()

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
        # file_path = os.path.dirname(os.path.abspath(__file__))
        # os.chdir(file_path)
    def resync_grid_with_sprites(self):
        """
        Update the color of all the sprites to match
        the color/stats in the grid.

        We look at the values in each cell.
        If the cell contains 0 we assign a white color.
        If the cell contains 1 we assign a green color.
        """
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # We need to convert our two dimensional grid to our
                # one-dimensional sprite list. For example a 10x10 grid might have
                # row 2, column 8 mapped to location 28. (Zero-basing throws things
                # off, but you get the idea.)
                # ALTERNATIVELY you could set self.grid_sprite_list[pos].texture
                # to different textures to change the image instead of the color.
                pos = row * COLUMN_COUNT + column
                if self.grid[row][column] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                else:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN

    # Restart game
    def setup(self):
        self.background = arcade.load_texture("clue_board2.jpg")

    # Draw screen
    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw all the sprites
        self.grid_sprite_list.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Convert the clicked mouse position into grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return

        # Flip the location between 1 and 0.
        if self.grid[row][column] == 0:
            self.grid[row][column] = 1
        else:
            self.grid[row][column] = 0

        # Update the sprite colors to match the new grid
        self.resync_grid_with_sprites()


def main():
    screen = clueGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    #screen.setup()
    arcade.run()


if __name__ == "__main__":
    main()