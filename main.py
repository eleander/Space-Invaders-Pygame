import pygame
import random
import math
from pygame import mixer
from Models.Player import Player
from Models.Enemy import Enemy
from Models.Bullet import Bullet


# Initialise pygame 
pygame.init()

# Create screen of size width by height
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load("Images/background.png")

# Background Music
mixer.music.load("Sound/arcade_music_loop.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Images/Space Invaders")
icon = pygame.image.load("Images/ufo.png")
pygame.display.set_icon(icon)

# Speed of player and enemy
speedX = 1.5

# Score
score_value = 0
font = pygame.font.Font("font.ttf", 32)
game_over_font = pygame.font.Font("font.ttf", 64)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

# Game Over
def game_over_text():
    game_over = game_over_font.render("game over", True, (255,255,255))
    screen.blit(game_over, (width/4, height/4)) 


# # Player
player_img = pygame.image.load("Images/space_invaders.png")
player = Player(width, height-(1.5*64), 0)

# Bullet
bullet_img = pygame.image.load("Images/bullet.png")
bullet = Bullet(0, 480, 0)

# Enemy
enemy_img = pygame.image.load("Images/ufo.png")
enemies = []
num_of_enemies = 10
for i in range(num_of_enemies):
    enemies.append(Enemy(random.randint(0,width-64), random.randint(0,height/4), speedX,40))

# Clock to enable smooth movement
clock = pygame.time.Clock()

# Tests for collision between enemy and bullet
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x,2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # 120 fps
    clock.tick(120)

    # Fill screen with RGB
    # RGB - Red, Green, Blue 
    screen.fill((0,0,0))

    # Background Image
    screen.blit(background, (0,0))

    # Loops through all events in the game
    for event in pygame.event.get():
        # Quit game condition
        if event.type == pygame.QUIT:
            running = False
        # Key strokes to control player movement and firing of the bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -speedX
            if event.key == pygame.K_RIGHT:
                player.x_change = speedX
            if event.key == pygame.K_SPACE and bullet.state =="ready":
                bullet.x = player.x
                bullet.fire(bullet_img, screen)
                bullet_sound = mixer.Sound("Sound/laser.wav")
                bullet_sound.play()
        # Unpress Key
        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            player.x_change = 0
        
    # Update playerX position
    player.x += player.x_change

    # Player wall collision
    if player.x < 0:
        player.x = 0
    elif player.x >= (width-64):
        player.x = (width-64) 

    # Itterate through all enemies
    for i in range(num_of_enemies):

        # Game Over 
        if enemies[i].y > 470:
            for j in range(num_of_enemies):
                enemies[j].y = height*2
            game_over_text()
            break 

        # enemyX[i] movement
        enemies[i].x += enemies[i].x_change
        if enemies[i].x < 0: 
            enemies[i].x_change = speedX
            enemies[i].y += enemies[i].y_change
        elif enemies[i].x >= (width-64):
            enemies[i].y += enemies[i].y_change
            enemies[i].x_change = -speedX

        # Collision detection of enemy and bullet
        collision = is_collision(enemies[i].x, enemies[i].y, bullet.x, bullet.y)
        if collision:
            explosion_sound = mixer.Sound("Sound/explosion.wav")
            explosion_sound.play()
            bullet.y = 500
            bullet.state = "ready"
            score_value += 1
            enemies[i].x = random.randint(0,width-64)
            enemies[i].y = random.randint(0, height/4)

        enemies[i].draw(enemy_img, screen) 

    # Bullet movement
    if bullet.y <= 0:
        bullet.state = "ready"
        bullet.y = 480

    if bullet.state == "fire":
        bullet.fire(bullet_img, screen)
        bullet.y += bullet.y_change


    # Display player and score
    player.draw(player_img, screen)
    show_score(textX,textY)

    # Update display
    pygame.display.update()



 
