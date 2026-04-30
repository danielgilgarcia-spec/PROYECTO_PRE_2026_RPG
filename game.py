"""
game.py  –  Clase principal Game.

Orquesta los módulos: Renderer, BattleSystem, Camera, AssetLoader, music.
"""

import random
import pygame
import sys

from defined import (
    TILE_SIZE, INTRO, EXPLORING, BATTLE, EXIT,
    DIALOG_PRE, DIALOG_POST, FINAL_DIALOG
)
from maps import make_map_1, make_map_2, make_map_3
from Player import Player
from randomEnemies1 import RandomEnemy1
from randomEnemies2 import RandomEnemy2
from randomEnemies3 import RandomEnemy3
from Enemy_final_1 import Enemy1
from Enemy_final_2 import Enemy2
from Enemy_final_3 import Enemy3
from menu import add_player_record
from asset_loader import AssetLoader
from camera import Camera
from renderer import Renderer
from battle import BattleSystem
from text import (
    INTRO_SCREENS,
    ENEMY1_DIALOG_PRE, ENEMY1_DIALOG_POST,
    ENEMY2_DIALOG_PRE, ENEMY2_DIALOG_POST,
    ENEMY3_DIALOG_PRE, ENEMY3_DIALOG_POST,
    FINAL_SCREENS,
)
import music


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

        # Nivel actual (1, 2 o 3)
        self.nivel_actual = 1

        # Mapas generados con salida aleatoria
        self.map_1 = make_map_1()
        self.map_2 = make_map_2()
        self.map_3 = make_map_3()
        self.current_map = self.map_1

        # Fuentes
        self.font     = pygame.font.Font(None, 24)
        self.font_big = pygame.font.Font(None, 36)

        # Jugador
        self.player        = Player()
        self.player.max_hp = self.difficulty["player_hp"]
        self.player.hp     = self.player.max_hp
        self.player.attack = self.difficulty["player_atk"]

        # Enemigo inicial
        self.enemy = RandomEnemy1(self.player.level)

        # Módulos
        self.assets   = AssetLoader(TILE_SIZE)
        self.camera   = Camera()
        self.renderer = Renderer(screen, self.assets, self.font, self.font_big)
        self.renderer.nivel_actual = self.nivel_actual
        self.battle   = BattleSystem()

        # Mini-imágenes de los jefes para el tile de salida
        self._mini_imgs = self._load_mini_images()

        # Diálogo
        self.dialog_screens    = []
        self.dialog_index      = 0
        self.dialog_timer      = 0
        self.dialog_next_state = EXPLORING

        # Música
        pygame.mixer.init()
        music.play(music.MUSIC_STORY)

        # Control de espacio (evitar repetición)
        self._space_was_pressed = False

    # ------------------------------------------------------------------
    # Carga de mini-imágenes de jefes
    # ------------------------------------------------------------------
    def _load_mini_images(self):
        imgs  = {}
        paths = {
            1: "assets/big_enemies/mihawk.png",
            2: "assets/big_enemies/pica.png",
            3: "assets/big_enemies/king.png",
        }
        for nivel, path in paths.items():
            try:
                img = pygame.image.load(path).convert_alpha()
                imgs[nivel] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except Exception as e:
                print(f"[mini] No se cargó {path}: {e}")
                imgs[nivel] = None
        return imgs

    # ------------------------------------------------------------------
    # Iniciar diálogo genérico
    # ------------------------------------------------------------------
    def _start_dialog(self, screens: list, next_state: str):
        self.dialog_screens    = screens
        self.dialog_index      = 0
        self.dialog_timer      = 0
        self.dialog_next_state = next_state
        if next_state == BATTLE:
            self.state = DIALOG_PRE
        else:
            self.state = DIALOG_POST
        music.play(music.MUSIC_STORY)

    # ------------------------------------------------------------------
    # Loop principal
    # ------------------------------------------------------------------
    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            space_pressed = keys[pygame.K_SPACE]
            space_just_pressed = space_pressed and not self._space_was_pressed
            self._space_was_pressed = space_pressed

            if self.state == INTRO:
                self._update_intro(keys, space_just_pressed)

            elif self.state == EXPLORING:
                self._update_exploring(keys)

            elif self.state == BATTLE:
                self._update_battle(keys)

            elif self.state in (DIALOG_PRE, DIALOG_POST, FINAL_DIALOG):
                self._update_dialog(keys, space_just_pressed)

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
    def _update_intro(self, keys, space_just_pressed: bool):
        self.intro_timer += 1
        if space_just_pressed:
            self.intro_screen += 1
            self.intro_timer   = 0

        finished = self.renderer.draw_intro(self.intro_screen, self.intro_timer)
        if finished:
            self.state = EXPLORING
            music.play(music.MUSIC_EXPLORE)

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
        tile_actual = self.current_map[self.player.y][self.player.x]
        if tile_actual == 4 and keys[pygame.K_SPACE]:
            self.player.heal()
            self.message = "¡Te curaste en la casa! HP restaurado."
            pygame.time.wait(500)

        # Salida al siguiente nivel
        if tile_actual == 5:
            self._handle_exit()

        self.renderer.draw_exploring(
            self.player, self.player_name, self.difficulty,
            self.current_map, self.camera, self.message,
            mini_imgs=self._mini_imgs, nivel=self.nivel_actual
        )

    def _update_battle(self, keys):
        result = self.battle.handle_input(keys, self.player, self.enemy)
        self.message = self.battle.message

        # Dibujar SIEMPRE la pantalla de batalla (incluso durante esperas)
        self.renderer.draw_battle(
            self.player, self.enemy, self.message, self.battle.choice
        )

        if result == "win":
            # Enemigo derrotado → comprobar si es jefe o aleatorio
            post_map = {
                1: ENEMY1_DIALOG_POST,
                2: ENEMY2_DIALOG_POST,
                3: ENEMY3_DIALOG_POST,
            }
            # Solo lanzar diálogo post si el enemigo es un jefe (Enemy1/2/3)
            from Enemy_final_1 import Enemy1
            from Enemy_final_2 import Enemy2
            from Enemy_final_3 import Enemy3
            if isinstance(self.enemy, (Enemy1, Enemy2, Enemy3)):
                post_screens = post_map.get(self.nivel_actual, [])
                if post_screens:
                    self._start_dialog(post_screens, EXPLORING)
                    self.state = DIALOG_POST
                else:
                    self._after_boss_dialog()
            else:
                # Enemigo aleatorio: volver a explorar
                self.state = EXPLORING
                music.play(music.MUSIC_EXPLORE)

        elif result == "exploring":
            self.state = EXPLORING
            music.play(music.MUSIC_EXPLORE)

    def _update_dialog(self, keys, space_just_pressed: bool):
        self.dialog_timer += 1

        if space_just_pressed:
            self.dialog_index += 1
            self.dialog_timer  = 0

        if self.dialog_index >= len(self.dialog_screens):
            if self.state == DIALOG_PRE:
                # Lanzar batalla contra el jefe
                boss_map   = {1: Enemy1, 2: Enemy2, 3: Enemy3}
                BossClass  = boss_map[self.nivel_actual]
                self.enemy = BossClass(self.player.level)
                self.battle.start(self.enemy, self.difficulty)
                self.message = f"¡{self.enemy.name} aparece!"
                self.state   = BATTLE
                music.play(music.MUSIC_BATTLE)

            elif self.state == DIALOG_POST:
                self._after_boss_dialog()

            elif self.state == FINAL_DIALOG:
                self.state = EXIT
        else:
            screen_data = self.dialog_screens[self.dialog_index]
            self.renderer.draw_dialog(screen_data, self.dialog_timer)

    def _after_boss_dialog(self):
        """Lógica tras terminar el diálogo post-jefe."""
        if self.nivel_actual == 1:
            self.nivel_actual          = 2
            self.current_map           = self.map_2
            self.player.x              = 5
            self.player.y              = 5
            self.renderer.nivel_actual = 2
            self.message               = "¡Has llegado a una nueva isla!"
            self.state                 = EXPLORING
            music.play(music.MUSIC_EXPLORE)

        elif self.nivel_actual == 2:
            self.nivel_actual          = 3
            self.current_map           = self.map_3
            self.player.x              = 5
            self.player.y              = 5
            self.renderer.nivel_actual = 3
            self.message               = "Una presencia poderosa te espera..."
            self.state                 = EXPLORING
            music.play(music.MUSIC_EXPLORE)

        else:
            # Nivel 3 completado → diálogo final de cierre
            self._start_dialog(FINAL_SCREENS, EXIT)
            self.state = FINAL_DIALOG

    def _check_random_encounter(self):
        tile = self.current_map[self.player.y][self.player.x]
        if tile == 0:
            if random.random() < self.difficulty["encounter_rate"]:
                EnemyClass = {1: RandomEnemy1, 2: RandomEnemy2, 3: RandomEnemy3}
                self.enemy = EnemyClass[self.nivel_actual](self.player.level)
                self.battle.start(self.enemy, self.difficulty)
                self.message = self.battle.message
                self.state   = BATTLE
                music.play(music.MUSIC_BATTLE)

    def _handle_exit(self):
        """El jugador pisa el tile 5: arranca el diálogo pre-jefe."""
        pre_map = {
            1: ENEMY1_DIALOG_PRE,
            2: ENEMY2_DIALOG_PRE,
            3: ENEMY3_DIALOG_PRE,
        }
        screens = pre_map.get(self.nivel_actual, [])
        if screens:
            self._start_dialog(screens, BATTLE)
        else:
            boss_map   = {1: Enemy1, 2: Enemy2, 3: Enemy3}
            BossClass  = boss_map[self.nivel_actual]
            self.enemy = BossClass(self.player.level)
            self.battle.start(self.enemy, self.difficulty)
            self.message = f"¡{self.enemy.name} aparece!"
            self.state   = BATTLE
            music.play(music.MUSIC_BATTLE)