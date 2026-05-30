import pygame
from random import *

pygame.init()

ANCHO, ALTO = 500, 500
COLOR_FONDO = (64, 201, 144)
BLACK = (0,0,0)
WHITE = (255,255,255)
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
    
    def is_collide(self, x, y):
        # devuelve True o False en caso de colision con el rectangulo
        return self.rect.collidepoint(x, y) 

class Picture(Area):
    def __init__(self, img_file, x, y, ancho, alto):
        super().__init__(x, y, ancho, alto)
        self.image = pygame.image.load(img_file)

    def draw(self, dist_x=10, dist_y=10):
        self.fill()
        screen.blit(self.image, (self.rect.x + dist_x, self.rect.y + dist_y))

player = Picture('platform.png', 200, 300, 50, 50)
ball = Picture('ball.png', 200, 200, 50, 50)
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

move_right = True
finish = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_a:
                move_right = False
        
        if move_right == True:
        player.rect.x += 3
        if move_right == False:
        player.rect.x -= 3

    # Validar si el juego ha finalizado
    if not finish:
        screen.fill(COLOR_FONDO)
        player.draw()
        ball.draw()
        for enemy in monsters:
            enemy.draw()

    if move_right == True:
        player.rect.x += 3
    if move_right == False:
        player.rect.x -= 3



    pygame.display.update()
    reloj.tick(FPS)

pygame.quit()
