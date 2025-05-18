import pygame
import sys
import os
import math
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()
laser_sound = pygame.mixer.Sound("sounds/laser.wav")

# Window setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Blasters")

# Colors
BLUE = (0, 0, 255)

# Image folder
image_folder = "images"

# Load player
player_img = pygame.transform.scale(
    pygame.image.load(os.path.join(image_folder, "player.png")),
    (64, 64)
)
player_x = screen_width // 2 - player_img.get_width() // 2
player_y = screen_height - 80
player_speed = 5

# Load enemy
enemy_img = pygame.transform.scale(
    pygame.image.load(os.path.join(image_folder, "enemy.png")),
    (84, 84)
)
num_of_enemies = 5
enemy_x = []
enemy_y = []
enemy_speed = []
enemy_direction = []
print("Enemy image width:", enemy_img.get_width())

for _ in range(num_of_enemies):
    enemy_x.append(random.randint(0, screen_width - enemy_img.get_width()))
    enemy_y.append(random.randint(50, 150))
    enemy_speed.append(2)
    enemy_direction.append(1)

# Load bullet
bullet_img = pygame.transform.scale(
    pygame.image.load(os.path.join(image_folder, "bullet.png")),
    (64, 64)
)
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font(None, 36)

def show_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + player_img.get_width()//2 - bullet_img.get_width()//2, y))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    return distance < 27

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(x, y, index):
    screen.blit(enemy_img, (x, y))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
                laser_sound.play()

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Player bounds
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_img.get_width():
        player_x = screen_width - player_img.get_width()

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_y = player_y
            bullet_state = "ready"

    # Enemy movement and collision
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_speed[i] * enemy_direction[i]

        if enemy_x[i] <= 0 or enemy_x[i] >= screen_width - enemy_img.get_width():
            enemy_direction[i] *= -1
            enemy_y[i] += 40

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, screen_width - enemy_img.get_width())
            enemy_y[i] = random.randint(50, 150)

        draw_enemy(enemy_x[i], enemy_y[i], i)

    # Draw everything
    draw_player(player_x, player_y)
    show_score()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
