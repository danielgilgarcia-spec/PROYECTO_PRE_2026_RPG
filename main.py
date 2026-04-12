"""
RPG - EN BUSCA DE LA TRIPULACIÓN PERDIDA - Un juego de rol de aventura y exploración
Controles: Flechas para moverse, ESPACIO para interactuar/atacar
"""

import pygame
import sys

from defined import SCREEN_WIDTH, SCREEN_HEIGHT
from menu import show_main_menu
from game import Game

# Inicialización
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("EN BUSCA DE LA TRIPULACIÓN PERDIDA")

if __name__ == "__main__":
    result = show_main_menu(screen)
    game = Game(screen, player_name=result["name"], difficulty=result["difficulty"])
    game.run()
