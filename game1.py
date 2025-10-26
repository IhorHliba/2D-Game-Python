import random
import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE
pygame.init()

HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
FPS = pygame.time.Clock ()
FONT = pygame.font.SysFont('Verdana', 50)

fps_clock = pygame.time.Clock ()
FONT = pygame.font.SysFont ('Verdana', 50)
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.transform.scale (pygame.image.load ('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load ('player.png').convert_alpha()        #pygame.Surface(player_size)
#player.fill((COLOR_BLACK))
player_rect = player.get_rect()
player_rect = player.get_rect(center=(WIDTH/5, HEIGHT/2))
# player_speed = [1, 1]
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

def create_enemy ():
    enemy_size = (30, 30)
    enemy = pygame.Surface (enemy_size)
    # enemy.fill(COLOR_RED)
    enemy = pygame.image.load ('enemy.png').convert_alpha()
    # enemy_size = enemy.get_size ()
    # enemy_rect = pygame.Rect (WIDTH, random.randint (0, HEIGHT - enemy.get_height()), *enemy_size)    # те що було на уроці
    # enemy_move = [random.randint (-8, -4), 0]   # те що було на уроці
    enemy_rect = pygame.Rect(WIDTH, random.randrange(0, HEIGHT - enemy.get_height()), *enemy_size) #код для рандомного польоту ракети
    enemy_move = [random.randint(-8, -4), random.randint(-3, 3)]  #код для рандомного польоту ракети
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1 
pygame.time.set_timer(CREATE_ENEMY, 2500)
enemies = []

def create_bonus ():
    bonus_size = (20, 20)
    bonus = pygame.Surface (bonus_size)
    #bonus.fill(COLOR_GREEN)
    bonus = pygame.image.load ('bonus.png').convert_alpha()
    #bonus_rect = pygame.Rect (random.randint (0, WIDTH - bonus.get_width()), 0, *bonus_size)   #те що було на уроці
    #bonus_move = [0, random.randint (3,7)]    #те що було на уроці
    bonus_rect = pygame.Rect(random.randrange(0, WIDTH - bonus.get_width()), 0, *bonus_size)
    bonus_move = [random.randint(-3, 3), random.randint(2, 6)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer (CREATE_BONUS, 2500)
bonuses = []
score = 0
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 250)
image_index = 0

def show_lose_message():
    message = FONT.render("Oh no! Boom! You lose", True, COLOR_RED)
    message_rect = message.get_rect(center=(WIDTH/2, HEIGHT/2))
    main_display.blit(message, message_rect)
    pygame.display.update()


lives = 3  # кількість життів гравця
LIFE_COLOR = (255, 0, 0)  # колір тексту для відображення життів гравця
life_font = pygame.font.SysFont('Verdana', 50)  # створення об'єкту Font для відображення життів гравця

FPS_DELAY = 120 # змінна, яка зберігає кількість кадрів на секунду
FPS = pygame.time.Clock()  # для зміни кадрів


#def create_bullet ():
#    bullet_size = (20, 20)
#    bullet = pygame.Surface(bullet_size, pygame.SRCALPHA)
#    pygame.draw.circle(bullet, COLOR_GREEN, (10, 10), 10)
#    bullet_rect = bullet.get_rect(center=player_rect.center)
#    bullet_speed = [10, 0]
#    bullets.append([bullet, bullet_rect, bullet_speed])

bullets = []

pygame.time.delay(100)
playing = True
while playing: 
    # FPS.tick (120)  # те що було на уроці
    FPS.tick(FPS_DELAY) # затримка між кадрами
    for event in pygame.event.get ():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append (create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append (create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])) 
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        if event.type == pygame.USEREVENT + 4:  # обробник події для зменшення кількості життів
            lives -= 1  # зменшуємо кількість життів
            if lives == 0:   #для відображення життя
                playing = False  # якщо житті закінчилися, гра закінчується
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_size = (20, 20)
                bullet = pygame.Surface(bullet_size)
                bullet.fill (COLOR_GREEN)
                bullet_rect = bullet.get_rect(center=player_rect.center)
                bullet_speed = [5, 0]
                #bullet_speed = pygame.math.Vector2 (10, 0).rotate(-player_rect.angle)
                bullets.append([bullet, bullet_rect, bullet_speed])             
    
    #main_display.fill (COLOR_BLACK)
    main_display.blit (bg, (bg_X1, 0))
    main_display.blit (bg, (bg_X2, 0))
    bg_X1 -= bg_move
    bg_X2 -= bg_move
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
    main_display.blit (player, player_rect)
    #main_display.blit (FONT.render(str(score), True, COLOR_YELLOW), (WIDTH-70, 20)) --- те що було на уроці
    #main_display.blit (FONT.render('score:', True, COLOR_BLACK) (680, 19))
    #main_display.blit (FONT.render (f"score: {score}", True, COLOR_YELLOW) (680, 19))
    score_surface = FONT.render(f"score: {score}", True, COLOR_YELLOW)
    main_display.blit(score_surface, (WIDTH-250, 20))

    keys = pygame.key.get_pressed()
    if keys [K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
        #player_rect = player_rect.rotate(-player_rect.angle)
    if keys [K_UP] and player_rect.top > 0:
        player_rect = player_rect.move (player_move_up)
        #player_rect = player_rect.rotate(-player_rect.angle)
    if keys [K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move (player_move_right)
        #player_rect = player_rect.rotate(-player_rect.angle)
    if keys [K_LEFT] and player_rect.left >0:
        player_rect = player_rect.move (player_move_left)
        #player_rect = player_rect.rotate(-player_rect.angle)

    for enemy in enemies:
        enemy[1] = enemy[1].move (enemy[2]) 
        main_display.blit (enemy[0], enemy [1])
        if player_rect.colliderect (enemy[1]):
            #playing = False
            lives -= 1
            enemies.remove(enemy)
            # pygame.time.set_timer(pygame.USEREVENT+4, 1000)          # запускаємо таймер для зменшення життів гравця через 1 секунду
        if lives == 0:           #для відображення життя
            playing = False         #для відображення життя
            # print("Oh no! Boom!")
            show_lose_message()
            pygame.time.delay(2000)  # затримка перед виходом з гри
            pygame.time.set_timer(pygame.USEREVENT+4, 0)      # зупиняємо таймер, якщо гра закінчилась
    
    lives_surface = life_font.render(f"lives: {lives}", True, LIFE_COLOR)     # для відображення життя
    main_display.blit (lives_surface, (WIDTH -250, 80))     #для відображення життя

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit (bonus[0], bonus [1])   
        if player_rect.colliderect (bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1
            #print("YEAH! Great job!")   
    pygame.display.flip()

    for enemy in enemies:
        if enemy [1].left < 0:
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus [1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
    
    for bullet in bullets:
        bullet[1] = bullet[1].move (bullet[2])
        main_display.blit (bullet[0], bullet[1])
    
    for bullet in bullets:
        if bullet[1].right > WIDTH:
            bullets.remove(bullet)

    for bullet in bullets:
        for enemy in enemies:
            if bullet[1].colliderect(enemy[1]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
   

    #print(len(enemies))
    #enemy_rect = enemy_rect.move (enemy_move)
    #main_display.blit (enemy, enemy_rect)
#    if player_rect.bottom >= HEIGHT:
#        player_speed = random.choice(([1, -1], [-1, -1])) 
#    if player_rect.top <= 0:
#        player_speed = random.choice(([-1, 1], [1, 1])) 
#    if player_rect.right >= WIDTH:
#        player_speed = random.choice(([-1, -1], [-1, 1]))     
#    if player_rect.left <= 0:
#        player_speed = random.choice(([1, 1], [1, -1]))
#    player_rect = player_rect.move(player_speed)
    
    
