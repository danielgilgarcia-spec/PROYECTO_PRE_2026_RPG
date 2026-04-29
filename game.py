"""
game.py  –  Clase principal Game.

Orquesta los módulos: Renderer, BattleSystem, Camera, AssetLoader.
"""

import random
import pygame
import sys

from defined import TILE_SIZE, INTRO, EXPLORING, BATTLE, EXIT
from maps import game_map_1, game_map_2, game_map_3
from Player import Player
from randomEnemies1 import RandomEnemy1
from randomEnemies2 import RandomEnemy2
from randomEnemies3 import RandomEnemy3
from Enemy_final_1 import Enemy
from Enemy_final_2 import Enemy
from Enemy_final_3 import Enemy
from menu import add_player_record
from asset_loader import AssetLoader
from camera import Camera
from renderer import Renderer
from battle import BattleSystem


class Game:
    def __init__(self, screen: pygame.Surface, player_name: str = "Héroe", difficulty: dict = None):
        self.screen      = screen
        self.clock       = pygame.time.Clock()
        self.player_name = player_name
        self.difficulty  = difficulty or {
            "name": "Normal", "enemy_mult": 1.0,
            "player_hp": 100, "player_atk": 10, "encounter_rate": 0.15
        }

        # Estado
        self.state        = INTRO
        self.intro_screen = 0
        self.intro_timer  = 0
        self.message      = f"¡Bienvenido, {self.player_name}! Usa las flechas para moverte."

        # Mapa activo
        self.current_map = game_map_1

        # Fuentes
        self.font     = pygame.font.Font(None, 24)
        self.font_big = pygame.font.Font(None, 36)

        # Jugador
        self.player         = Player()
        self.player.max_hp  = self.difficulty["player_hp"]
        self.player.hp      = self.player.max_hp
        self.player.attack  = self.difficulty["player_atk"]

        # Enemigo (se renueva en cada encuentro)
                # Nivel 1 -> Nivel 2
        if self.current_map is game_map_1:
            self.enemy = RandomEnemy1(self.player.level)

        # Nivel 2 -> Nivel 3
        elif self.current_map is game_map_2:
            self.enemy = RandomEnemy2(self.player.level)

        # Final del juego
        else:
            self.enemy = RandomEnemy3(self.player.level)
        

        # Módulos
        self.assets   = AssetLoader(TILE_SIZE)
        self.camera   = Camera()
        self.renderer = Renderer(screen, self.assets, self.font, self.font_big)
        self.battle   = BattleSystem()

        # variables para control de diálogos y malos finales de nivel

        self.dialog_timer = 0
        self.pending_boss = False


    # ------------------------------------------------------------------
    # Loop principal
    # ------------------------------------------------------------------
    def run(self):
        running       = True
        space_pressed = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.get_pressed() if False else pygame.key.get_pressed()

            if self.state == INTRO:
                self._update_intro(keys, space_pressed)
                space_pressed = not keys[pygame.K_SPACE]  # reset cuando se suelta

            elif self.state == EXPLORING:
                self._update_exploring(keys)

            elif self.state == BATTLE:
                result = self.battle.handle_input(keys, self.player, self.enemy)
                self.message = self.battle.message
                if result == "exploring":
                    self.state = EXPLORING
                self.renderer.draw_battle(self.player, self.enemy, self.message, self.battle.choice)

            elif self.state == EXIT:
                add_player_record(self.player_name, self.player.level, self.difficulty["name"])
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    # Updates por estado
    # ------------------------------------------------------------------
    def _update_intro(self, keys, space_pressed: bool):
        self.intro_timer += 1

        if keys[pygame.K_SPACE] and not space_pressed:
            self.intro_screen += 1
            self.intro_timer   = 0
            pygame.time.wait(200)

        finished = self.renderer.draw_intro(self.intro_screen, self.intro_timer)
        if finished:
            self.state = EXPLORING

    def _update_exploring(self, keys):
        moved = False

        if keys[pygame.K_UP]:
            moved = self.player.move(0, -1, self.current_map); pygame.time.wait(150)
        elif keys[pygame.K_DOWN]:
            moved = self.player.move(0,  1, self.current_map); pygame.time.wait(150)
        elif keys[pygame.K_LEFT]:
            moved = self.player.move(-1, 0, self.current_map); pygame.time.wait(150)
        elif keys[pygame.K_RIGHT]:
            moved = self.player.move( 1, 0, self.current_map); pygame.time.wait(150)

        if moved:
            self._check_random_encounter()

        # Curación en casa
        if self.current_map[self.player.y][self.player.x] == 4 and keys[pygame.K_SPACE]:
            self.player.heal()
            self.message = "¡Te curaste en la casa! HP restaurado."
            pygame.time.wait(1000)

        # Cambio de nivel / salida
        if self.current_map[self.player.y][self.player.x] == 5:
            self._handle_exit()

        # Si hay malo final pendiente, mostrar diálogo y luego batalla
        if self.pending_boss:
            tiempo_actual = pygame.time.get_ticks()

            if tiempo_actual - self.dialog_timer > 2000:
                self.enemy = Enemy(self.player.level)  # boss final
                self.battle.start(self.enemy, self.difficulty)
                self.message = f"¡{self.enemy.name} aparece!"
                self.state = BATTLE
                self.pending_boss = False


        self.renderer.draw_exploring(
            self.player, self.player_name, self.difficulty,
            self.current_map, self.camera, self.message
        )

    def _check_random_encounter(self):
        if self.current_map[self.player.y][self.player.x] == 0:
            if random.random() < self.difficulty["encounter_rate"]:
                        # Nivel 1 -> Nivel 2
                if self.current_map is game_map_1:
                    self.enemy = RandomEnemy1(self.player.level)

                         # Nivel 2 -> Nivel 3
                elif self.current_map is game_map_2:
                    self.enemy = RandomEnemy2(self.player.level)

                        # Final del juego
                else:
                    self.enemy = RandomEnemy3(self.player.level)

                self.battle.start(self.enemy, self.difficulty)
                self.message = self.battle.message
                self.state   = BATTLE

    def _handle_exit(self):
        # Nivel 1 -> Nivel 2
        if self.current_map is game_map_1:
            self.current_map = game_map_2
            self.player.x = 5
            self.player.y = 5
            self.message = "¡Has llegado a una nueva isla..."
            self.dialog_timer = pygame.time.get_ticks()
            self.pending_boss = True
            pygame.time.wait(500)

        # Nivel 2 -> Nivel 3
        elif self.current_map is game_map_2:
            self.current_map = game_map_3
            self.player.x = 5
            self.player.y = 5
            self.message = "Una presencia poderosa te espera..."
            self.dialog_timer = pygame.time.get_ticks()
            self.pending_boss = True
            pygame.time.wait(500)

        # Final del juego
        else:
            self.message = "¡Nivel completado!"
            pygame.time.wait(800)
            self.state = EXIT

