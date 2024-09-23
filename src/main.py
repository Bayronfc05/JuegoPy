import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Battle")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

player_size = 50
player_pos = [375, 500]
player_speed = 10

enemy_size = 50
enemy_list = []
enemy_speed = 10

powerful_enemy_size = 75
powerful_enemy_pos = None
powerful_enemy_life = 3
powerful_enemy_present = False

bullet_size = [5, 20]
bullet_list = []

score = 0
font = pygame.font.SysFont("monospace", 35)

game_state = "MENU"

def crear_enemigos(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, 750)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def crear_enemigo_poderoso():
    global powerful_enemy_pos, powerful_enemy_present, powerful_enemy_life
    if not powerful_enemy_present and score > 0 and score % 15 == 0:
        x_pos = random.randint(0, 725)
        y_pos = 0
        powerful_enemy_pos = [x_pos, y_pos]
        powerful_enemy_life = 3
        powerful_enemy_present = True

def mover_enemigos(enemy_list):
    for enemy_pos in enemy_list:
        if enemy_pos[1] >= 0 and enemy_pos[1] < 600:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.remove(enemy_pos)

def mover_enemigo_poderoso():
    global powerful_enemy_pos, powerful_enemy_present
    if powerful_enemy_present and powerful_enemy_pos and powerful_enemy_pos[1] >= 0 and powerful_enemy_pos[1] < 600:
        powerful_enemy_pos[1] += 7
    elif powerful_enemy_present:
        resetear_enemigo_poderoso()

def colision(player_pos, enemy_pos, enemy_size):
    if enemy_pos is None:
        return False
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos[:2]
    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def disparar(bullet_list, player_pos):
    bullet_list.append([player_pos[0] + player_size // 2, player_pos[1]])

def mover_balas(bullet_list):
    for bullet in bullet_list[:]:
        bullet[1] -= 15
        if bullet[1] < 0:
            bullet_list.remove(bullet)

def detectar_colisiones_balas(bullet_list, enemy_list):
    global score
    for bullet in bullet_list[:]:
        for enemy_pos in enemy_list[:]:
            if colision(bullet, enemy_pos, enemy_size):
                if bullet in bullet_list:
                    bullet_list.remove(bullet)
                if enemy_pos in enemy_list:
                    enemy_list.remove(enemy_pos)
                score += 1

def detectar_colisiones_balas_poderoso(bullet_list):
    global score, powerful_enemy_life, powerful_enemy_present, powerful_enemy_pos
    if not powerful_enemy_present or powerful_enemy_pos is None:
        return
    for bullet in bullet_list[:]:
        if colision(bullet, powerful_enemy_pos, powerful_enemy_size):
            bullet_list.remove(bullet)
            powerful_enemy_life -= 1
            if powerful_enemy_life <= 0:
                powerful_enemy_present = False
                powerful_enemy_pos = None
                score += 5

def resetear_enemigo_poderoso():
    global powerful_enemy_pos, powerful_enemy_present
    powerful_enemy_pos = None
    powerful_enemy_present = False

def dibujar_texto(texto, font, color, superficie, x, y):
    textobj = font.render(texto, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    superficie.blit(textobj, textrect)

def mostrar_menu():
    screen.fill(BLACK)
    dibujar_texto('Space Battle', font, WHITE, screen, 400, 250)
    dibujar_texto('Presiona Enter para jugar', font, WHITE, screen, 400, 350)
    pygame.display.update()

def mostrar_game_over():
    screen.fill(BLACK)
    dibujar_texto('Game Over', font, WHITE, screen, 400, 250)
    dibujar_texto(f'Puntuación: {score}', font, WHITE, screen, 400, 350)
    dibujar_texto('Presiona Enter para reiniciar', font, WHITE, screen, 400, 450)
    pygame.display.update()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "MENU":
        mostrar_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_state = "PLAYING"
            score = 0
            player_pos = [375, 500]
            enemy_list = []
            bullet_list = []
            resetear_enemigo_poderoso()

    elif game_state == "PLAYING":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < 750:
            player_pos[0] += player_speed
        if keys[pygame.K_SPACE]:
            disparar(bullet_list, player_pos)

        screen.fill(BLACK)

        crear_enemigos(enemy_list)
        crear_enemigo_poderoso()
        mover_enemigos(enemy_list)
        mover_enemigo_poderoso()
        mover_balas(bullet_list)

        detectar_colisiones_balas(bullet_list, enemy_list)
        detectar_colisiones_balas_poderoso(bullet_list)

        for enemy_pos in enemy_list:
            pygame.draw.rect(screen, WHITE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

        if powerful_enemy_present and powerful_enemy_pos is not None:
            pygame.draw.rect(screen, RED, (powerful_enemy_pos[0], powerful_enemy_pos[1], powerful_enemy_size, powerful_enemy_size))

        pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))

        for bullet in bullet_list:
            pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_size[0], bullet_size[1]))

        for enemy_pos in enemy_list:
            if colision(player_pos, enemy_pos, enemy_size):
                game_state = "GAME_OVER"

        if powerful_enemy_pos is not None and colision(player_pos, powerful_enemy_pos, powerful_enemy_size):
            game_state = "GAME_OVER"

        dibujar_texto(f'Puntuación: {score}', font, WHITE, screen, 400, 30)

        pygame.display.update()
        clock.tick(30)

    elif game_state == "GAME_OVER":
        mostrar_game_over()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_state = "MENU"
