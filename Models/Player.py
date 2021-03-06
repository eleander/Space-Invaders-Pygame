import pygame
class Player(object):
    def __init__(self, x, y, x_change):
        self.x = x
        self.y = y
        self.x_change = x_change

    # Displays the player at specified playerX and playerY
    # x++ = move right
    # x-- = move left
    # y-- = move up 
    # y++ = move down 
    # Top left of screen is (0,0)
    def draw(self, player_img, screen):
        screen.blit(player_img, (self.x, self.y))
