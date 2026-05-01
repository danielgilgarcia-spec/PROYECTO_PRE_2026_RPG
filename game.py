"""
game.py  –  Clase principal Game.

Música por estado:
    INTRO          → MUSIC_STORY      (narrativa de apertura)
    EXPLORING      → MUSIC_EXPLORE    (exploración del mapa)
    BATTLE         → MUSIC_BATTLE     (combate)
    DIALOG_PRE     → MUSIC_DIALOGUE   (conversación antes del jefe)
    DIALOG_POST    → MUSIC_DIALOGUE   (conversación después del jefe)
    FINAL_DIALOG   → MUSIC_STORY      (cierre narrativo)
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

        self.state        = INTRO
        self.intro_screen = 0
        self.intro_timer  = 0
        self.message      = f"¡Bienvenido, {self.player_name}! Usa las flechas para moverte."
        self.nivel_actual = 1

        self.map_1 = make_map_1()
        self.map_2 = make_map_2()
        self.map_3 = make_map_3()
        self.current_map = self.map_1

        self.font     = pygame.font.Font(None, 24)
        self.font_big = pygame.font.Font(None, 36)

        self.player        = Player()
        self.player.max_hp = self.difficulty["player_hp"]
        self.player.hp     = self.player.max_hp
        self.player.attack = self.difficulty["player_atk"]

        self.enemy = RandomEnemy1(self.player.level)

        self.assets   = AssetLoader(TILE_SIZE)
        self.camera   = Camera()
        self.renderer = Renderer(screen, self.assets, self.font, self.font_big)
        self.renderer.nivel_actual = self.nivel_actual
        self.battle   = BattleSystem()

        self._mini_imgs = self._load_mini_images()

        self.dialog_screens    = []
        self.dialog_index      = 0
        self.dialog_timer      = 0
        self.dialog_next_state = EXPLORING

        pygame.mixer.init()
        music.play(music.MUSIC_STORY)   # intro = narrativa

        self._space_was_pressed = False
        self._exit_triggered    = False

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

    def _start_dialog(self, screens: list, next_state: str):
        self.dialog_screens    = screens
        self.dialog_index      = 0
        self.dialog_timer      = 0
        self.dialog_next_state = next_state
        if next_state == BATTLE:
            self.state = DIALOG_PRE
            music.play(music.MUSIC_DIALOGUE)   # diálogo con el jefe → dialogue
        else:
            self.state = DIALOG_POST
            music.play(music.MUSIC_DIALOGUE)   # diálogo post-jefe → dialogue

    # ------------------------------------------------------------------
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None  # ← IMPORTANTE

            keys               = pygame.key.get_pressed()
            space_pressed      = keys[pygame.K_SPACE]
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
                add_player_record(
                    self.player_name,
                    self.player.level,
                    self.difficulty["name"]
                )
                return {"level": self.player.level}

            pygame.display.flip()
            self.clock.tick(60)

        return None  # ← por seguridad


    # ------------------------------------------------------------------
    def _update_intro(self, keys, space_just_pressed):
        self.intro_timer += 1
        if space_just_pressed:
            self.intro_screen += 1
            self.intro_timer   = 0
        finished = self.renderer.draw_intro(self.intro_screen, self.intro_timer)
        if finished:
            self.state = EXPLORING
            music.play(music.MUSIC_EXPLORE)    # empieza exploración

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
            self._exit_triggered = False   # al moverse, habilitar el tile de salida de nuevo
            self._check_random_encounter()

        tile_actual = self.current_map[self.player.y][self.player.x]

        if tile_actual == 4 and keys[pygame.K_SPACE]:
            self.player.heal()
            self.message = "¡Te curaste en la casa! HP restaurado."
            pygame.time.wait(500)

        if tile_actual == 5:
            if not self._exit_triggered:
                self._exit_triggered = True
                self._handle_exit()

        self.renderer.draw_exploring(
            self.player, self.player_name, self.difficulty,
            self.current_map, self.camera, self.message,
            mini_imgs=self._mini_imgs, nivel=self.nivel_actual
        )

    def _update_battle(self, keys):
        result       = self.battle.handle_input(keys, self.player, self.enemy)
        self.message = self.battle.message

        self.renderer.draw_battle(
            self.player, self.enemy, self.message, self.battle.choice
        )

        if result == "win":
            if isinstance(self.enemy, (Enemy1, Enemy2, Enemy3)):
                post_map = {
                    1: ENEMY1_DIALOG_POST,
                    2: ENEMY2_DIALOG_POST,
                    3: ENEMY3_DIALOG_POST,
                }
                post_screens = post_map.get(self.nivel_actual, [])
                if post_screens:
                    self._start_dialog(post_screens, EXPLORING)
                    self.state = DIALOG_POST
                    # música ya cambiada en _start_dialog → MUSIC_DIALOGUE
                else:
                    self._after_boss_dialog()
            else:
                # Enemigo aleatorio derrotado → exploración
                self.state = EXPLORING
                self._exit_triggered = False
                music.play(music.MUSIC_EXPLORE)

        elif result == "exploring":
            # Huida o derrota → exploración
            # Si era un boss, mover al jugador a posición segura para no
            # volver a pisar el tile 5 y relanzar el diálogo/batalla
            if isinstance(self.enemy, (Enemy1, Enemy2, Enemy3)):
                self.player.x = 5
                self.player.y = 5
            self.state = EXPLORING
            self._exit_triggered = True   # evitar re-trigger inmediato del tile 5
            music.play(music.MUSIC_EXPLORE)

    def _update_dialog(self, keys, space_just_pressed):
        self.dialog_timer += 1

        if space_just_pressed:
            self.dialog_index += 1
            self.dialog_timer  = 0

        if self.dialog_index >= len(self.dialog_screens):
            # Dibujar la última pantalla un frame más antes de transicionar,
            # así el SPACE que agotó el diálogo no se filtra a la batalla.
            if self.dialog_index > len(self.dialog_screens):
                # Segunda vez que llegamos aquí: ahora sí transicionamos
                if self.state == DIALOG_PRE:
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
                # Primera vez: index == len. Dibujar la última pantalla todavía.
                last = self.dialog_screens[self.dialog_index - 1]
                self.renderer.draw_dialog(last, self.dialog_timer)
        else:
            self.renderer.draw_dialog(
                self.dialog_screens[self.dialog_index], self.dialog_timer
            )

    def _after_boss_dialog(self):
        if self.nivel_actual == 1:
            self.nivel_actual          = 2
            self.current_map           = self.map_2
            self.player.x              = 5
            self.player.y              = 5
            self.renderer.nivel_actual = 2
            self.message               = "¡Has llegado a una nueva isla!"
            self.state                 = EXPLORING
            music.play(music.MUSIC_EXPLORE)        # exploración nivel 2

        elif self.nivel_actual == 2:
            self.nivel_actual          = 3
            self.current_map           = self.map_3
            self.player.x              = 5
            self.player.y              = 5
            self.renderer.nivel_actual = 3
            self.message               = "Una presencia poderosa te espera..."
            self.state                 = EXPLORING
            music.play(music.MUSIC_EXPLORE)        # exploración nivel 3

        else:
            # Nivel 3 completado → cierre narrativo
            self._start_dialog(FINAL_SCREENS, EXIT)
            self.state = FINAL_DIALOG
            music.play(music.MUSIC_STORY)          # narrativa final (override del dialogue)

    def _check_random_encounter(self):
        tile = self.current_map[self.player.y][self.player.x]
        if tile == 0 and random.random() < self.difficulty["encounter_rate"]:
            EnemyClass = {1: RandomEnemy1, 2: RandomEnemy2, 3: RandomEnemy3}
            self.enemy = EnemyClass[self.nivel_actual](self.player.level)
            self.battle.start(self.enemy, self.difficulty)
            self.message = self.battle.message
            self.state   = BATTLE
            music.play(music.MUSIC_BATTLE)         # combate aleatorio

    def _handle_exit(self):
        pre_map = {
            1: ENEMY1_DIALOG_PRE,
            2: ENEMY2_DIALOG_PRE,
            3: ENEMY3_DIALOG_PRE,
        }
        screens = pre_map.get(self.nivel_actual, [])
        if screens:
            self._start_dialog(screens, BATTLE)
            # música ya cambiada en _start_dialog → MUSIC_DIALOGUE
        else:
            boss_map   = {1: Enemy1, 2: Enemy2, 3: Enemy3}
            self.enemy = boss_map[self.nivel_actual](self.player.level)
            self.battle.start(self.enemy, self.difficulty)
            self.message = f"¡{self.enemy.name} aparece!"
            self.state   = BATTLE
            music.play(music.MUSIC_BATTLE)