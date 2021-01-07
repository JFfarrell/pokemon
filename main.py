import pygame
import time
import random
import math
from pygame import mixer

# initialise pygame
pygame.init()
pygame.mixer.init()

# create the screen
screen = pygame.display.set_mode((832, 688))

# background
background = pygame.image.load('ground.png')

# background sound
mixer.music.load("Battle!.mp3")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Zubats")
icon = pygame.image.load("zubaticon.png")
pygame.display.set_icon(icon)

# dialogue box
dialogue = pygame.image.load("dialogue.png")
dialogueX = 7
dialogueY = 7

# player
playerImg = pygame.image.load("pikachu.png")
playerX = 370
playerY = 620
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("zubat.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(65)
    enemyX_change.append(0.75)
    enemyY_change.append(40)


# bullet
bulletImg = pygame.image.load("lightning.png")
bulletX = 0
bulletY = 630
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("Pokemon.ttf", 28)
textX = 10
textY = 10

rate = 0.5

gameOver = pygame.font.Font("Pokemon.ttf", 15)

pikachu = mixer.Sound("Pikachu.wav")
pikachu.play()

# time
current_time = pygame.time.get_ticks()
exit_time = current_time + 5000
clock = pygame.time.Clock()


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (0, 0, 0))
    screen.blit(dialogue, (x-6, y-6))
    screen.blit(score, (x+20, y+15))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def collide(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over():
    fainted = gameOver.render("Pikachu fainted.", True, (0, 0, 0))
    whited = gameOver.render("Ash whited out...", True, (0, 0, 0))
    screen.blit(dialogue, (440, 600))
    screen.blit(fainted, (465, 620))
    mixer.music.stop()


# game loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check if right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    thunder = mixer.Sound("ThunderShock1.wav")
                    thunder.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 10:
        playerX = 10
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        # enemyX_change[i] = rate
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 9:
            enemyX_change[i] = rate
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1 * rate
            enemyY[i] += enemyY_change[i]

        # collision
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            faintZu = mixer.Sound("faintZu.wav")
            faintZu.play()
            bulletY = 630
            bullet_state = "ready"
            score_value += 1
            rate += 0.1
            enemyX[i] = random.randint(10, 735)
            enemyY[i] = 65

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= -20:
        bulletY = 630
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
