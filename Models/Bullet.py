import pygame
class Bullet(object):
    # "ready" You can't see the bullet on the screen
    # "fire" The bullet is moving 
    def __init__(self, x, y, x_change):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = -15
        self.state = "ready"

    def fire(self, bullet_img, screen):
        self.state = "fire"
        screen.blit(bullet_img, (self.x + 16, self.y + 10))
