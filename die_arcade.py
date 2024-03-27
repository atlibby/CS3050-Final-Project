import arcade
import arcade.gui
import random

''' functionality '''

# Side bar width is 320, therefore:
# 250 / 500 === 160 / 320


# SIDEBAR CONSTANTS
SCREEN_WIDTH = 1090
SCREEN_HEIGHT = 770
SIDEBAR_WIDTH = 320

SIDEBAR_X = SCREEN_WIDTH - SIDEBAR_WIDTH / 2
SIDEBAR_Y = SCREEN_HEIGHT / 2

DIE_X = SIDEBAR_X
DIE_Y = SIDEBAR_Y - 200
DIE_OFFSET = 25


#arcade.draw_rectangle_filled(self.width - SIDEBAR_WIDTH / 2, self.height / 2, SIDEBAR_WIDTH, self.height, arcade.color.LIGHT_YELLOW)
# generate points function
def generatePoints(die_value):
    # Set of points ( this will be the die values ), which will be manipulated in a larger function
    point_list = ()  # x1 & y1 - x6 & y6
    if die_value == 1:
        point_list = ((DIE_X, DIE_Y),  # x1 & y1
                      (DIE_X, DIE_Y),  # x2 & y2
                      (DIE_X, DIE_Y),  # x3 & y3
                      (DIE_X, DIE_Y),  # x4 & y4
                      (DIE_X, DIE_Y),  # x5 & y5
                      (DIE_X, DIE_Y))  # x6 & y6
    elif die_value == 2:
        point_list = ((DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x1 & y1
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x2 & y2
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x3 & y3
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x4 & y4
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x5 & y5
                      (DIE_X+DIE_OFFSET, DIE_Y+DIE_OFFSET))  # x6 & y6
    elif die_value == 3:
        point_list = ((DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x1 & y1
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x2 & y2
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x3 & y3
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x4 & y4
                      (DIE_X+DIE_OFFSET, DIE_Y+DIE_OFFSET),  # x5 & y5
                      (DIE_X, DIE_Y))  # x6 & y6
    elif die_value == 4:
        point_list = ((DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x1 & y1
                      (DIE_X+DIE_OFFSET, DIE_Y+DIE_OFFSET),  # x2 & y2
                      (DIE_X+DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x3 & y3
                      (DIE_X-DIE_OFFSET, DIE_Y+DIE_OFFSET),  # x4 & y4
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x5 & y5
                      (DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET))  # x6 & y6
    elif die_value == 5:
        point_list = ((DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x1 & y1
                      (DIE_X+DIE_OFFSET, DIE_Y+DIE_OFFSET),  # x2 & y2
                      (DIE_X+DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x3 & y3
                      (DIE_X-DIE_OFFSET, DIE_Y+DIE_OFFSET),  # x4 & y4
                      (DIE_X, DIE_Y),  # x5 & y5
                      (DIE_X, DIE_Y))  # x6 & y6
    elif die_value == 6:
        point_list = ((DIE_X-DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x1 & y1
                      (DIE_X+DIE_OFFSET, DIE_Y+DIE_OFFSET),  # x2 & y2
                      (DIE_X+DIE_OFFSET, DIE_Y-DIE_OFFSET),  # x3 & y3
                      (DIE_X-DIE_OFFSET, DIE_Y+DIE_OFFSET),  # x4 & y4
                      (DIE_X-DIE_OFFSET, DIE_Y),  # x5 & y5
                      (DIE_X+DIE_OFFSET, DIE_Y))  # x6 & y6
    text = "You rolled a " + str(die_value) + "!"
    arcade.draw_text(text, DIE_X-40, DIE_Y - 100, arcade.color.BLUSH, 10)
    return point_list


# function for drawing die points
def drawDiePoints(point_list):
    for point in point_list:
        arcade.draw_circle_filled(point[0], point[1], 10, arcade.color.WHITE)


def rollDie():
    # arcade.draw_text("Press the spacebar to roll the die!", 105, 100, arcade.color.WHITE, 15)
    # Drawing in die rectangle
    arcade.draw_rectangle_filled(SIDEBAR_X, (SIDEBAR_Y - 200), 100, 100, arcade.color.BLUSH)
    drawDiePoints(generatePoints(random.randint(1, 6)))
    

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

DIE_X = SIDEBAR_X
DIE_Y = SIDEBAR_Y - 200
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

    text = f"You rolled a {die_value}!"
    arcade.draw_text(text, DIE_X - 45, DIE_Y - 50, arcade.color.BLUSH, 10)
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
