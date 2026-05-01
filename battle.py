"""
battle.py  –  Lógica de combate por turnos.

Valores de retorno de handle_input:
    "continue"   – la batalla sigue
    "win"        – jugador ganó (solo se devuelve tras el periodo de espera)
    "exploring"  – volver al mapa (derrota o huida)
"""

import random
import pygame


class BattleSystem:

    def __init__(self):
        self.choice  = 0
        self.message = ""
        self._wait   = 0
        self._pending_result = None  # resultado que se enviará tras la espera

    # ------------------------------------------------------------------
    def start(self, enemy, difficulty: dict):
        """Inicia una batalla. Aplica el multiplicador sobre los stats base
        guardados en el enemigo, nunca acumulativamente."""
        mult = difficulty["enemy_mult"]

        # Guardar stats base la primera vez para no multiplicar varias veces
        if not hasattr(enemy, "_base_max_hp"):
            enemy._base_max_hp = enemy.max_hp
            enemy._base_attack = enemy.attack

        enemy.max_hp = int(enemy._base_max_hp * mult)
        enemy.hp     = enemy.max_hp
        enemy.attack = int(enemy._base_attack * mult)

        self.choice          = 0
        self.message         = f"¡{enemy.name} aparece!"
        self._wait           = 0
        self._pending_result = None   # <-- reseteo crítico

    # ------------------------------------------------------------------
    def handle_input(self, keys, player, enemy) -> str:
        # Si estamos en periodo de espera, contar frames y luego devolver resultado
        if self._pending_result is not None:
            if self._wait > 0:
                self._wait -= 1
                return "continue"
            result = self._pending_result
            self._pending_result = None
            return result

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
    def _resolve_attack(self, player, enemy) -> str:
        damage   = random.randint(max(1, player.attack - 3), player.attack + 5)
        enemy.hp = max(0, enemy.hp - damage)          # nunca negativo
        self.message = f"¡Atacaste por {damage} de daño!"

        if enemy.hp <= 0:
            player.exp  += enemy.exp_reward
            self.message = f"¡Derrotaste a {enemy.name}! +{enemy.exp_reward} EXP"
            self._check_levelup(player)
            self._pending_result = "win"
            self._wait           = 120   # ~2 seg a 60fps
            return "continue"

        # Contraataque
        enemy_dmg  = random.randint(max(1, enemy.attack - 2), enemy.attack + 3)
        player.hp  = max(0, player.hp - enemy_dmg)   # nunca negativo
        self.message += f" | {enemy.name} te atacó por {enemy_dmg}!"

        if player.hp <= 0:
            self.message = "¡Has sido derrotado! Volviendo al inicio..."
            player.hp    = player.max_hp
            player.x     = 5
            player.y     = 5
            self._pending_result = "exploring"
            self._wait           = 120
            return "continue"

        return "continue"

    def _resolve_flee(self) -> str:
        self.message         = "¡Escapaste con éxito!"
        self._pending_result = "exploring"
        self._wait           = 60
        return "continue"

    @staticmethod
    def _check_levelup(player):
        while player.exp >= player.level * 100:
            player.level  += 1
            player.max_hp += 20
            player.hp      = player.max_hp
            player.attack += 3