import pygame
import random
import math
from pygame import mixer


# Initialise pygame 
pygame.init()

# Create screen of size width by height
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load("background.png")

# Background Music
mixer.music.load("arcade_music_loop.wav")
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Speed of player and enemy
speedX = 3

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


# Player
playerImg = pygame.image.load('space_invaders.png')
playerX = width
playerY = height-(1.5*64)
playerX_change = 0
# Displays the player at specified playerX and playerY
# x++ = move right
# x-- = move left
# y-- = move up 
# y++ = move down 
# Top left of screen is (0,0)
# Bottom right of screen is (width, height)
def player(x,y):
    screen.blit(playerImg,(x,y))


# Bullet
# "ready" You can't see the bullet on the screen
# "fire" The bullet is moving 
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = -15
bullet_state = "ready"

# Displays the enemy at specified X and Y coordinate
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
# COME BACK
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0,width-64))
    enemyY.append(random.randint(0, height/4))
    enemyX_change.append(speedX)
    enemyY_change.append(40)

# Displays the enemy at specified X and Y coordinate
def enemy(x,y,enemy_num):
    screen.blit(enemyImg[enemy_num],(x,y))

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

    clock.tick(60)

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
        # Key strokes to control player movement 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -speedX
            if event.key == pygame.K_RIGHT:
                playerX_change = speedX
            if event.key == pygame.K_SPACE and bullet_state =="ready":
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
        # Unpress Key
        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            playerX_change = 0
        
    # Update playerX position
    playerX += playerX_change

    # Player wall collision
    if playerX < 0:
        playerX = 0
    elif playerX >= (width-64):
        playerX = (width-64) 

    # Itterate through all enemies
    for i in range(num_of_enemies):

        # Game Over 
        if enemyY[i] > 470:
            for j in range(num_of_enemies):
                enemyY[j] = height*2
            game_over_text()
            break 

        # enemyX[i] movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = speedX
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= (width-64):
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -speedX

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,width-64)
            enemyY[i] = random.randint(0, height/4)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    # Display player and score
    player(playerX, playerY)
    show_score(textX,textY)

    # Update display
    pygame.display.update()



 
