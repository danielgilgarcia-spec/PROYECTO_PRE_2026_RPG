"""
RPG - EN BUSCA DE LA TRIPULACIÓN PERDIDA
Controles: Flechas para moverse, ESPACIO para interactuar/atacar
"""

import pygame
import sys

from defined import SCREEN_WIDTH, SCREEN_HEIGHT
from menu import show_main_menu
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EN BUSCA DE LA TRIPULACIÓN PERDIDA")

    running = True

    while running:
        # ── MENÚ ───────────────────────────────
        result = show_main_menu(screen)

        if result is None:
            break  # salir del juego completamente

        # ── INICIAR JUEGO ──────────────────────
        game = Game(
            screen,
            player_name=result["name"],
            difficulty=result["difficulty"]
        )

        game_result = game.run()

        # ── SALIDA DESDE EL JUEGO ──────────────
        if game_result is None:
            running = False  # cerrar todo

        # Si quieres usar resultados:
        # else:
        #     print("Nivel alcanzado:", game_result["level"])

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
