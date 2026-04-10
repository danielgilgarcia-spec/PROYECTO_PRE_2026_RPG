"""
battle.py  –  Lógica de combate por turnos.
"""

import random
import pygame

from randomEnemies1 import RandomEnemy


class BattleSystem:
    """Gestiona toda la lógica de un combate por turnos."""

    def __init__(self):
        self.choice = 0   # 0 = Atacar, 1 = Huir
        self.message = ""

    # ------------------------------------------------------------------
    # Inicio de batalla
    # ------------------------------------------------------------------
    def start(self, enemy: RandomEnemy, difficulty: dict):
        mult = difficulty["enemy_mult"]
        enemy.max_hp = int(enemy.max_hp * mult)
        enemy.hp     = enemy.max_hp
        enemy.attack = int(enemy.attack * mult)
        self.choice  = 0
        self.message = f"¡Un {enemy.name} salvaje apareció!"

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_input(self, keys, player, enemy) -> str:
        """
        Procesa input del jugador.

        Devuelve:
            "continue"   – la batalla sigue
            "exploring"  – volver al mapa (victoria, derrota o huida)
        """
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
        damage = random.randint(player.attack - 3, player.attack + 5)
        enemy.hp -= damage
        self.message = f"¡Atacaste por {damage} de daño!"
        pygame.time.wait(800)

        if enemy.hp <= 0:
            player.exp += enemy.exp_reward
            self.message = f"¡Derrotaste a {enemy.name}! +{enemy.exp_reward} EXP"
            self._check_levelup(player)
            pygame.time.wait(2000)
            return "exploring"

        # Contraataque del enemigo
        pygame.time.wait(200)
        enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
        player.hp -= enemy_damage
        self.message += f" | {enemy.name} te atacó por {enemy_damage}!"

        if player.hp <= 0:
            self.message = "¡Has sido derrotado! Volviendo al inicio..."
            pygame.time.wait(2000)
            player.hp = player.max_hp
            player.x  = 5
            player.y  = 5
            return "exploring"

        pygame.time.wait(500)
        return "continue"

    def _resolve_flee(self) -> str:
        self.message = "¡Escapaste con éxito!"
        pygame.time.wait(1000)
        return "exploring"

    @staticmethod
    def _check_levelup(player):
        if player.exp >= player.level * 100:
            player.level   += 1
            player.max_hp  += 20
            player.hp       = player.max_hp
            player.attack  += 3
