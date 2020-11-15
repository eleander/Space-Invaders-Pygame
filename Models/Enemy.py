import pygame
class Enemy(object):
    def __init__(self, x, y, x_change, y_change):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def draw(self, enemy_img, screen):
        screen.blit(enemy_img, (self.x, self.y))
