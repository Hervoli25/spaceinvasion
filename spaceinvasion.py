import pygame
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load assets
background = pygame.image.load("background.jpg")
mixer.music.load('punch.mp3')
mixer.music.play(-1)
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invasion")

player_img = pygame.image.load("Rocket.png")
player_width = 64
player_height = 64
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_x_change = 0

enemy_img = pygame.image.load("enemy.png")
enemy_width = 64
enemy_height = 64

bullet_img = pygame.image.load("bullet.png")
bullet_width = 32
bullet_height = 32
bullet_x = 0
bullet_y = player_y
bullet_y_change = -4
bullet_visible = False

font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
text_x = 10
text_y = 10

# Level attributes
levels = [
    {'number_of_enemies': 100, 'enemy_speed': 0.4, 'enemy_y_change': 40},
    {'number_of_enemies': 150, 'enemy_speed': 0.6, 'enemy_y_change': 50},
    {'number_of_enemies': 200, 'enemy_speed': 0.8, 'enemy_y_change': 60},
]
current_level = 0

# Enemy attributes
def create_enemies(level):
    enemies = []
    for _ in range(levels[level]['number_of_enemies']):
        enemies.append({
            'img': enemy_img,
            'x': random.randint(0, SCREEN_WIDTH - enemy_width),
            'y': random.randint(50, 200),
            'x_change': levels[level]['enemy_speed'],
            'y_change': levels[level]['enemy_y_change']
        })
    return enemies

enemies = create_enemies(current_level)

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(enemy):
    screen.blit(enemy['img'], (enemy['x'], enemy['y']))

def shoot_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    return distance < 27

def show_game_over():
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (200, 250))
    pygame.display.update()
    pygame.time.delay(2000)

def show_level_up():
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render("LEVEL UP!", True, (255, 255, 255))
    screen.blit(text, (200, 250))
    pygame.display.update()
    pygame.time.delay(2000)

# Game loop
is_running = True
while is_running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            elif event.key == pygame.K_RIGHT:
                player_x_change = 1
            elif event.key == pygame.K_SPACE and not bullet_visible:
                bullet_sound = mixer.Sound('shot.mp3')
                bullet_sound.play()
                bullet_x = player_x
                shoot_bullet(bullet_x, bullet_y)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_x_change = 0

    player_x += player_x_change
    player_x = max(0, min(player_x, SCREEN_WIDTH - player_width))

    for enemy in enemies:
        if enemy['y'] > player_y:
            for e in enemies:
                e['y'] = 1000
            show_game_over()
            is_running = False
            break

        enemy['x'] += enemy['x_change']
        if enemy['x'] <= 0:
            enemy['x_change'] = abs(enemy['x_change'])
            enemy['y'] += enemy['y_change']
        elif enemy['x'] >= SCREEN_WIDTH - enemy_width:
            enemy['x_change'] = -abs(enemy['x_change'])
            enemy['y'] += enemy['y_change']

        if is_collision(enemy['x'], enemy['y'], bullet_x, bullet_y):
            collision_sound = mixer.Sound('punch.mp3')
            collision_sound.play()
            bullet_y = player_y
            bullet_visible = False
            score += 1
            enemy['x'] = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy['y'] = random.randint(50, 200)

        draw_enemy(enemy)

    if bullet_visible:
        shoot_bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_visible = False

    draw_player(player_x, player_y)
    show_score(text_x, text_y)

    # Check if level is completed
    if score >= sum(level['number_of_enemies'] for level in levels[:current_level + 1]):
        if current_level < len(levels) - 1:
            current_level += 1
            show_level_up()
            enemies = create_enemies(current_level)
        else:
            show_game_over()
            is_running = False

    pygame.display.update()

pygame.quit()
quit()
