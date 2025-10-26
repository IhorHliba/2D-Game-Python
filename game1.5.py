import os
import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE

pygame.init()

# --- Basic constants ---
WIDTH, HEIGHT = 1200, 800
COLOR_WHITE   = (255, 255, 255)
COLOR_BLACK   = (0, 0, 0)
COLOR_RED     = (255, 0, 0)
COLOR_YELLOW  = (255, 255, 0)

# --- Display setup ---
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python 2D Arcade: Laser Edition")

# --- Fonts and clock ---
FONT = pygame.font.SysFont('Verdana', 50)
SMALL_FONT = pygame.font.SysFont('Verdana', 35)
clock = pygame.time.Clock()
FPS_DELAY = 90

# --- Background setup (scrolling background) ---
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

# --- Player setup ---
IMAGE_PATH = "Goose"                     # Folder with animation frames
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect(center=(WIDTH // 5, HEIGHT // 2))

# Movement vectors
player_move_down  = [0, 4]
player_move_up    = [0, -4]
player_move_right = [4, 0]
player_move_left  = [-4, 0]

# --- Game events ---
CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_ENEMY, 2500)
pygame.time.set_timer(CREATE_BONUS, 2500)
pygame.time.set_timer(CHANGE_IMAGE, 250)

# --- Object lists ---
enemies = []
bonuses = []
bullets = []

# ---------- Utility functions ----------

def create_enemy():
    """Create a new enemy at a random vertical position moving left."""
    enemy_img = pygame.image.load('enemy.png').convert_alpha()
    ew, eh = enemy_img.get_size()
    enemy_rect = pygame.Rect(WIDTH, random.randrange(0, HEIGHT - eh), ew, eh)
    enemy_move = [random.randint(-8, -4), random.randint(-3, 3)]
    return [enemy_img, enemy_rect, enemy_move]

def create_bonus():
    """Create a bonus object that falls from the top."""
    bonus_img = pygame.image.load('bonus.png').convert_alpha()
    bw, bh = bonus_img.get_size()
    bonus_rect = pygame.Rect(random.randrange(0, WIDTH - bw), 0, bw, bh)
    bonus_move = [random.randint(-3, 3), random.randint(2, 6)]
    return [bonus_img, bonus_rect, bonus_move]

def spawn_laser(center_pos):
    """Create a red laser beam with light glow."""
    bullet_length = 30
    bullet_height = 4
    surf = pygame.Surface((bullet_length, bullet_height), pygame.SRCALPHA)
    # main beam
    pygame.draw.rect(surf, (255, 0, 0), (0, 1, bullet_length, 2))
    # subtle glow lines
    pygame.draw.rect(surf, (255, 180, 180, 120), (0, 0, bullet_length, 1))
    pygame.draw.rect(surf, (255, 180, 180, 120), (0, 3, bullet_length, 1))
    rect = surf.get_rect(center=center_pos)
    speed = [18, 0]
    return [surf, rect, speed]

def show_text_centered(text, font, color, y_offset=0):
    """Draw centered text at a vertical offset."""
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    main_display.blit(surf, rect)

def start_screen():
    """Display start screen until SPACE is pressed."""
    waiting = True
    while waiting:
        main_display.blit(bg, (0, 0))
        show_text_centered("Python 2D Arcade", FONT, COLOR_YELLOW, -50)
        show_text_centered("Press SPACE to start", SMALL_FONT, COLOR_WHITE, 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                waiting = False

def game_over_screen(final_score):
    """Display game-over screen with restart/exit options."""
    waiting = True
    while waiting:
        main_display.blit(bg, (0, 0))
        show_text_centered("Game Over", FONT, COLOR_RED, -70)
        show_text_centered(f"Your score: {final_score}", SMALL_FONT, COLOR_YELLOW, 20)
        show_text_centered("Press R to restart or ESC to quit", SMALL_FONT, COLOR_WHITE, 90)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# ---------- Main game loop ----------

def run_game():
    """Core gameplay loop: handles updates, collisions, and drawing."""
    global bg_X1, bg_X2, player
    enemies.clear()
    bonuses.clear()
    bullets.clear()

    score = 0
    lives = 3
    image_index = 0
    playing = True

    while playing:
        clock.tick(FPS_DELAY)

        # --- Handle events ---
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            elif event.type == CREATE_ENEMY:
                enemies.append(create_enemy())

            elif event.type == CREATE_BONUS:
                bonuses.append(create_bonus())

            elif event.type == CHANGE_IMAGE:
                if PLAYER_IMAGES:
                    try:
                        player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])).convert_alpha()
                    except:
                        pass
                    image_index = (image_index + 1) % len(PLAYER_IMAGES)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(spawn_laser(player_rect.center))

        # --- Background scrolling ---
        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))
        bg_X1 -= bg_move
        bg_X2 -= bg_move
        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        # --- Player movement ---
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] and player_rect.bottom < HEIGHT: player_rect.move_ip(0, 4)
        if keys[K_UP] and player_rect.top > 0:          player_rect.move_ip(0, -4)
        if keys[K_RIGHT] and player_rect.right < WIDTH: player_rect.move_ip(4, 0)
        if keys[K_LEFT] and player_rect.left > 0:       player_rect.move_ip(-4, 0)

        # --- Draw player ---
        main_display.blit(player, player_rect)

        # --- Enemies ---
        for enemy in enemies[:]:
            enemy[1].move_ip(enemy[2])
            main_display.blit(enemy[0], enemy[1])
            if player_rect.colliderect(enemy[1]):
                enemies.remove(enemy)
                lives -= 1
            elif enemy[1].right < 0:
                enemies.remove(enemy)
        if lives <= 0:
            playing = False
            break

        # --- Bonuses ---
        for bonus in bonuses[:]:
            bonus[1].move_ip(bonus[2])
            main_display.blit(bonus[0], bonus[1])
            if player_rect.colliderect(bonus[1]):
                bonuses.remove(bonus)
                score += 1
            elif bonus[1].top > HEIGHT:
                bonuses.remove(bonus)

        # --- Bullets (lasers) ---
        for bullet in bullets[:]:
            bullet[1].move_ip(bullet[2])
            main_display.blit(bullet[0], bullet[1])

            # remove bullet if out of bounds
            if bullet[1].left > WIDTH:
                bullets.remove(bullet)
                continue

            # collision: bullet ↔ enemy
            for enemy in enemies[:]:
                if bullet[1].colliderect(enemy[1]):
                    enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 1
                    break

        # --- HUD (Score & Lives) ---
        score_surface = FONT.render(f"score: {score}", True, COLOR_YELLOW)
        main_display.blit(score_surface, (WIDTH - 250, 20))
        lives_surface = FONT.render(f"lives: {lives}", True, COLOR_RED)
        main_display.blit(lives_surface, (WIDTH - 250, 80))

        # --- Flip the display ---
        pygame.display.flip()

    # --- Game over screen after losing ---
    game_over_screen(score)

# ---------- Main loop ----------
while True:
    start_screen()
    run_game()