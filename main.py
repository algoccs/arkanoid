import pygame
from random import *

pygame.init()
pygame.font.init()

ANCHO, ALTO = 500, 500
COLOR_FONDO = (64, 201, 144)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (163, 26, 26)
FPS = 40
# CONFIGURACION DE LA PANTALLA
screen = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# CLASES 
class Area():
    def __init__(self, x, y, ancho, alto, color=COLOR_FONDO):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
    
    def fill(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def change_color(self, new_color):
        self.color = new_color

    def set_border(self, border_color, border_size):
        pygame.draw.rect(screen, border_color, self.rect, border_size)
    
    def rebote(self, rect):
        # devuelve True o False en caso de colision con el rectangulo
        return self.rect.colliderect(rect) 

class Picture(Area):
    def __init__(self, img_file, x, y, ancho, alto):
        super().__init__(x, y, ancho, alto)
        self.image = pygame.image.load(img_file)

    def draw(self, dist_x=10, dist_y=10):
        self.fill()
        screen.blit(self.image, (self.rect.x + dist_x, self.rect.y + dist_y))

class Label(Area):
    def set_text(self, text, size, text_color=BLACK):
        self.image = pygame.font.SysFont("Arial", size).render(text, 1, text_color)

    def draw(self, dist_x=10, dist_y=10):
        self.fill()
        screen.blit(self.image, (self.rect.x + dist_x, self.rect.y + dist_y))

player = Picture('platform.png', 200, 300, 100, 50)
ball = Picture('ball.png', 300, 200, 50, 50)
monsters = [] # LISTA PARA ALMACENAR LOS ENEMIGOS
enemigos_por_fila = [9, 8, 7] 

for fila in range(3):
    columnas = enemigos_por_fila[fila]
    margen = 5 + ((9 - columnas) * 30)
    for col in range(columnas):
        x = margen + (col * 55)
        y = 5 + (fila * 60)
        enemy = Picture('enemy.png', x, y, 50, 50)
        monsters.append(enemy)

finish = False
move_right = False
move_left = False
speed_x, speed_y = 1, 1
quedan_mostruos = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                move_right = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False

    if move_right and player.rect.x <=  ANCHO -100:
        player.rect.x += 3
    if move_left and player.rect.x >= 0:
        player.rect.x -= 3
        
    ball.rect.x += speed_x
    ball.rect.y += speed_y

    if ball.rect.x >= ANCHO -50:
        speed_x *= -1
    if ball.rect.x <= 0:
        speed_x *= -1
    if ball.rect.y <= 0:
        speed_y *= -1
    # COMO HACER QUE REBOTE CON LA PLATAFORMA???
    if player.rebote(ball.rect):
        speed_y *= -1

    # Validar si el juego ha finalizado
    if not finish:
        screen.fill(COLOR_FONDO)
        player.draw()
        ball.draw()
        for enemy in monsters:
            enemy.draw()
        
        # CONDICION DE DERROTA
        if ball.rect.y > player.rect.y + 10:
            finish = True
            screen.fill(RED)
            text_derrota = Label(50, 200, 300, 100, RED)
            text_derrota.set_text('PERDISTE', 80, WHITE)
            text_derrota.draw()

        # CONDICION DE VICTORIA
        if len(monsters) == 0:
            quedan_mostruos = False
            # mostrar pantalla de victoria!

    pygame.display.update()
    reloj.tick(FPS)

pygame.quit()
