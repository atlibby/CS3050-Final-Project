#Set up
import pygame
import random
pygame.init()
size = [500, 500]
window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
count = 0
red = pygame.color.Color('#FF0000')
white = pygame.color.Color('#FFFFFF')
black = pygame.color.Color('#000000')
roll = False
x = 250
y = 250
x2 = 250
y2 = 250
x3 = 250
y3 = 250
x4 = 250
y4 = 250
x5 = 250
y5 = 250
x6 = 250
y6 = 250
done = False
#Loop
while not done:
    window.fill(black)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and roll == False:
        roll = True
    elif roll == True and keys[pygame.K_SPACE]:
        roll = False
    if roll == True:
        count += 1
        if count == 15:
            count = 0
            num = random.randrange(1, 7)
            if num == 1:
                x = 250
                y = 250
                x2 = 250
                y2 = 250
                x3 = 250
                y3 = 250
                x4 = 250
                y4 = 250
                x5 = 250
                y5 = 250
                x6 = 250
                y6 = 250
            elif num == 2:
                x = 210
                y = 210
                x2 = 210
                y2 = 210
                x3 = 210
                y3 = 210
                x4 = 210
                y4 = 210
                x5 = 210
                y5 = 210
                x6 = 290
                y6 = 290
            elif num == 3:
                x = 210
                y = 210
                x2 = 210
                y2 = 210
                x3 = 210
                y3 = 210
                x4 = 210
                y4 = 210
                x5 = 290
                y5 = 290
                x6 = 250
                y6 = 250
            elif num == 4:
                x = 210
                y = 210
                x2 = 290
                y2 = 290
                x3 = 290
                y3 = 210
                x4 = 210
                y4 = 290
                x5 = 210
                y5 = 210
                x6 = 210
                y6 = 210
            elif num == 5:
                x = 210
                y = 210
                x2 = 290
                y2 = 290
                x3 = 290
                y3 = 210
                x4 = 210
                y4 = 290
                x5 = 250
                y5 = 250
                x6 = 250
                y6 = 250
            else:
                x = 210
                y = 210
                x2 = 290
                y2 = 290
                x3 = 290
                y3 = 210
                x4 = 210
                y4 = 290
                x5 = 210
                y5 = 250
                x6 = 290
                y6 = 250
    pygame.draw.rect(window, red, (200, 200, 100, 100))
    pygame.draw.circle(window, white, [x, y], 8)
    pygame.draw.circle(window, white, [x2, y2], 8)
    pygame.draw.circle(window, white, [x3, y3], 8)
    pygame.draw.circle(window, white, [x4, y4], 8)
    pygame.draw.circle(window, white, [x5, y5], 8)
    pygame.draw.circle(window, white, [x6, y6], 8)
    pygame.display.flip()
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()