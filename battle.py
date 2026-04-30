"""
battle.py  –  Lógica de combate por turnos.

Valores de retorno de handle_input:
    "continue"   – la batalla sigue
    "win"        – jugador ganó (para detectar jefes y lanzar diálogo post)
    "exploring"  – volver al mapa (derrota o huida)
"""

import random
import pygame


class BattleSystem:
    """Gestiona toda la lógica de un combate por turnos."""

    def __init__(self):
        self.choice  = 0      # 0 = Atacar, 1 = Huir
        self.message = ""
        self._wait   = 0      # frames de espera no bloqueante
        self._state  = "input"  # "input" | "waiting_win" | "waiting_flee" | "waiting_death"

    # ------------------------------------------------------------------
    # Inicio de batalla
    # ------------------------------------------------------------------
    def start(self, enemy, difficulty: dict):
        mult         = difficulty["enemy_mult"]
        enemy.max_hp = int(enemy.max_hp * mult)
        enemy.hp     = enemy.max_hp
        enemy.attack = int(enemy.attack * mult)
        self.choice  = 0
        self.message = f"¡Un {enemy.name} salvaje apareció!"
        self._state  = "input"
        self._wait   = 0

    # ------------------------------------------------------------------
    # Input — no bloqueante, usa frames en lugar de pygame.time.wait
    # ------------------------------------------------------------------
    def handle_input(self, keys, player, enemy) -> str:
        """
        Procesa input del jugador cada frame.

        Devuelve:
            "continue"   – la batalla sigue
            "win"        – jugador venció al enemigo
            "exploring"  – volver al mapa (derrota o huida)
        """
        # Estados de espera no bloqueantes
        if self._state == "waiting_win":
            self._wait -= 1
            if self._wait <= 0:
                self._state = "input"
                return "win"
            return "continue"

        if self._state == "waiting_flee":
            self._wait -= 1
            if self._wait <= 0:
                self._state = "input"
                return "exploring"
            return "continue"

        if self._state == "waiting_death":
            self._wait -= 1
            if self._wait <= 0:
                self._state = "input"
                return "exploring"
            return "continue"

        # Input normal
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.choice = 1 - self.choice
            pygame.time.wait(150)
            return "continue"

        if keys[pygame.K_SPACE]:
            if self.choice == 0:
                return self._resolve_attack(player, enemy)
            else:
                return self._resolve_flee()

        return "continue"

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------
    def _resolve_attack(self, player, enemy) -> str:
        damage   = random.randint(max(1, player.attack - 3), player.attack + 5)
        enemy.hp -= damage
        self.message = f"¡Atacaste por {damage} de daño!"

        if enemy.hp <= 0:
            player.exp  += enemy.exp_reward
            self.message = f"¡Derrotaste a {enemy.name}! +{enemy.exp_reward} EXP"
            self._check_levelup(player)
            # Espera ~120 frames (2 seg a 60fps) sin bloquear
            self._state = "waiting_win"
            self._wait  = 120
            return "continue"

        # Contraataque
        enemy_damage  = random.randint(max(1, enemy.attack - 2), enemy.attack + 3)
        player.hp    -= enemy_damage
        self.message += f" | {enemy.name} te atacó por {enemy_damage}!"

        if player.hp <= 0:
            self.message = "¡Has sido derrotado! Volviendo al inicio..."
            player.hp    = player.max_hp
            player.x     = 5
            player.y     = 5
            self._state  = "waiting_death"
            self._wait   = 120
            return "continue"

        return "continue"

    def _resolve_flee(self) -> str:
        self.message = "¡Escapaste con éxito!"
        self._state  = "waiting_flee"
        self._wait   = 60
        return "continue"

    @staticmethod
    def _check_levelup(player):
        if player.exp >= player.level * 100:
            player.level  += 1
            player.max_hp += 20
            player.hp      = player.max_hp
            player.attack += 3