import arcade
import random

# Open the window. Set the window title and dimensions (width and height)
arcade.open_window(500, 500, "Rolling Die")
arcade.set_background_color(arcade.color.COOL_BLACK)
# Start the render process. This must be done before any drawing commands.
arcade.start_render()

''' functionality '''


# generate points function
def generatePoints(die_value):
    # Set of points ( this will be the die values ), which will be manipulated in a larger function
    point_list = ()  # x1 & y1 - x6 & y6
    if die_value == 1:
        point_list = ((250, 250),  # x1 & y1
                      (250, 250),  # x2 & y2
                      (250, 250),  # x3 & y3
                      (250, 250),  # x4 & y4
                      (250, 250),  # x5 & y5
                      (250, 250))  # x6 & y6
    elif die_value == 2:
        point_list = ((210, 210),  # x1 & y1
                      (210, 210),  # x2 & y2
                      (210, 210),  # x3 & y3
                      (210, 210),  # x4 & y4
                      (210, 210),  # x5 & y5
                      (290, 290))  # x6 & y6
    elif die_value == 3:
        point_list = ((210, 210),  # x1 & y1
                      (210, 210),  # x2 & y2
                      (210, 210),  # x3 & y3
                      (210, 210),  # x4 & y4
                      (290, 290),  # x5 & y5
                      (250, 250))  # x6 & y6
    elif die_value == 4:
        point_list = ((210, 210),  # x1 & y1
                      (290, 290),  # x2 & y2
                      (290, 210),  # x3 & y3
                      (210, 290),  # x4 & y4
                      (210, 210),  # x5 & y5
                      (210, 210))  # x6 & y6
    elif die_value == 5:
        point_list = ((210, 210),  # x1 & y1
                      (290, 290),  # x2 & y2
                      (290, 210),  # x3 & y3
                      (210, 290),  # x4 & y4
                      (250, 250),  # x5 & y5
                      (250, 250))  # x6 & y6
    elif die_value == 6:
        point_list = ((210, 210),  # x1 & y1
                      (290, 290),  # x2 & y2
                      (290, 210),  # x3 & y3
                      (210, 290),  # x4 & y4
                      (210, 250),  # x5 & y5
                      (290, 250))  # x6 & y6
    text = "You rolled a " + str(die_value) + "!"
    arcade.draw_text(text, 162, 100, arcade.color.WHITE, 20)
    return point_list


# function for drawing die points
def drawDiePoints(point_list):
    for point in point_list:
        arcade.draw_circle_filled(point[0], point[1], 10, arcade.color.WHITE)


def rollDie():
    # arcade.draw_text("Press the spacebar to roll the die!", 105, 100, arcade.color.WHITE, 15)
    # Drawing in die rectangle
    arcade.draw_rectangle_filled(250, 250, 150, 150, arcade.color.BLUSH)
    drawDiePoints(generatePoints(random.randint(1, 6)))


rollDie()
# Finish the render.
# Nothing will be drawn without this.
# Must happen after all draw commands
arcade.finish_render()
# Keep the window up until someone closes it.
arcade.run()

