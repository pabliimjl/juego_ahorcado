import pygame
from pantalla_inicio import PantallaInicio

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Ahorcado")

PantallaInicio(window=window,running=True)