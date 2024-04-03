import arcade
import random
from arcade.gui import UIInteractiveWidget, UIMousePressEvent

''' functionality '''

# SIDEBAR CONSTANTS
SCREEN_WIDTH = 1090
SCREEN_HEIGHT = 770
SIDEBAR_WIDTH = 320

SIDEBAR_X = SCREEN_WIDTH - SIDEBAR_WIDTH / 2
SIDEBAR_Y = SCREEN_HEIGHT / 2

DIE_X = SIDEBAR_X + 50
DIE_Y = SIDEBAR_Y - 250
DIE_OFFSET = 15


# generate points function
def generate_points(die_value):
    point_list = ()
    if die_value == 1:
        point_list = ((DIE_X, DIE_Y),) * 6
    elif die_value == 2:
        point_list = ((DIE_X - DIE_OFFSET, DIE_Y - DIE_OFFSET),) * 2 + ((DIE_X + DIE_OFFSET, DIE_Y + DIE_OFFSET),) * 4
    elif die_value == 3:
        point_list = ((DIE_X - DIE_OFFSET, DIE_Y - DIE_OFFSET),) * 2 + (
        (DIE_X + DIE_OFFSET, DIE_Y + DIE_OFFSET),) * 2 + ((DIE_X, DIE_Y),) * 2
    elif die_value == 4:
        point_list = ((DIE_X - DIE_OFFSET, DIE_Y - DIE_OFFSET), (DIE_X + DIE_OFFSET, DIE_Y + DIE_OFFSET),
                      (DIE_X + DIE_OFFSET, DIE_Y - DIE_OFFSET), (DIE_X - DIE_OFFSET, DIE_Y + DIE_OFFSET),
                      (DIE_X - DIE_OFFSET, DIE_Y - DIE_OFFSET),) * 2
    elif die_value == 5:
        point_list = ((DIE_X - DIE_OFFSET, DIE_Y - DIE_OFFSET), (DIE_X + DIE_OFFSET, DIE_Y + DIE_OFFSET),
                      (DIE_X + DIE_OFFSET, DIE_Y - DIE_OFFSET), (DIE_X - DIE_OFFSET, DIE_Y + DIE_OFFSET),
                      (DIE_X, DIE_Y),) * 2
    elif die_value == 6:
        point_list = ((DIE_X - DIE_OFFSET, DIE_Y - DIE_OFFSET), (DIE_X + DIE_OFFSET, DIE_Y + DIE_OFFSET),
                      (DIE_X + DIE_OFFSET, DIE_Y - DIE_OFFSET), (DIE_X - DIE_OFFSET, DIE_Y + DIE_OFFSET),
                      (DIE_X - DIE_OFFSET, DIE_Y), (DIE_X + DIE_OFFSET, DIE_Y),)

    for point in point_list:
        arcade.draw_circle_filled(point[0], point[1], 5, arcade.color.WHITE)


class Die:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.die_value = 1

    def roll_die(self):
        self.die_value = random.randint(1, 6)
        generate_points(self.die_value)

        return self.die_value


    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.BLUSH)
        generate_points(self.die_value)


class MyWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.Die = Die(DIE_X, DIE_Y, 100, 100)

    def on_draw(self):
        arcade.start_render()
        self.Die.draw()

    # Creating function to check the mouse clicks
    def on_mouse_press(self, x, y, button, modifiers):
        if (self.Die.x - self.Die.width / 2 < x < self.Die.x + self.Die.width / 2
                and self.Die.y - self.Die.height / 2 < y < self.Die.y + self.Die.height / 2):
            self.Die.roll_die()
            print("Mouse button is pressed")


def main():
    MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Interactive Die Example")
    arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
    arcade.run()


if __name__ == "__main__":
    main()
