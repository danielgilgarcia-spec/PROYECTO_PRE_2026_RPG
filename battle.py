"""
battle.py  –  Combate por turnos estricto.

Flujo de un turno completo:
    PLAYER_CHOICE  → jugador elige ATACAR o HUIR con flechas + ESPACIO
    PLAYER_ATTACK  → se muestra el daño del jugador, esperar ESPACIO o timer
    ENEMY_ATTACK   → se muestra el daño del enemigo, esperar ESPACIO o timer
    (vuelta a PLAYER_CHOICE si ninguno ha muerto)

Valores de retorno de update():
    "continue"   – la batalla sigue
    "win"        – jugador ganó
    "exploring"  – volver al mapa (derrota o huida)
"""

import random
import pygame

# ── Estados internos del turno ───────────────────────────────────────────────
_CHOICE      = "choice"       # jugador elige qué hacer
_PLAYER_ATK  = "player_atk"  # mostrando daño del jugador
_ENEMY_ATK   = "enemy_atk"   # mostrando daño del enemigo
_RESULT_WAIT = "result_wait"  # victoria/derrota confirmando salida
_FLEE        = "flee"         # huida exitosa

# Frames mínimos que dura cada mensaje de ataque antes de aceptar input (~1.5s)
_PHASE_FRAMES = 90


class BattleSystem:

    def __init__(self):
        self.choice          = 0     # 0 = ATACAR, 1 = HUIR
        self.message         = ""
        self._phase          = _CHOICE
        self._phase_timer    = 0
        self._input_cooldown = 0
        self._pending_result = None

    # ── Inicio ───────────────────────────────────────────────────────────────
    def start(self, enemy, difficulty: dict):
        mult = difficulty["enemy_mult"]
        if not hasattr(enemy, "_base_max_hp"):
            enemy._base_max_hp = enemy.max_hp
            enemy._base_attack = enemy.attack
        enemy.max_hp = int(enemy._base_max_hp * mult)
        enemy.hp     = enemy.max_hp
        enemy.attack = int(enemy._base_attack * mult)

        self.choice          = 0
        self.message         = f"!{enemy.name} aparece!  -  Que haras?"
        self._phase          = _CHOICE
        self._phase_timer    = 0
        self._pending_result = None
        self._input_cooldown = 20   # frames de gracia para teclas arrastradas

    # ── Update principal (llamar cada frame) ─────────────────────────────────
    def update(self, keys, space_just_pressed, player, enemy) -> str:
        if self._input_cooldown > 0:
            self._input_cooldown -= 1
            return "continue"

        self._phase_timer += 1

        if self._phase == _CHOICE:
            return self._handle_choice(keys, space_just_pressed, player, enemy)

        if self._phase == _PLAYER_ATK:
            if self._phase_timer >= _PHASE_FRAMES or space_just_pressed:
                if self._pending_result == "win":
                    self._phase = _RESULT_WAIT
                    self._phase_timer = 0
                else:
                    self._enemy_attack(player, enemy)
            return "continue"

        if self._phase == _ENEMY_ATK:
            if self._phase_timer >= _PHASE_FRAMES or space_just_pressed:
                if self._pending_result == "exploring":
                    self._phase = _RESULT_WAIT
                    self._phase_timer = 0
                else:
                    self._phase = _CHOICE
                    self._phase_timer = 0
                    self.message = "Que haras?"
            return "continue"

        if self._phase == _FLEE:
            if self._phase_timer >= _PHASE_FRAMES or space_just_pressed:
                return "exploring"
            return "continue"

        if self._phase == _RESULT_WAIT:
            if self._phase_timer >= _PHASE_FRAMES or space_just_pressed:
                result = self._pending_result
                self._pending_result = None
                return result
            return "continue"

        return "continue"

    # ── Elección del jugador ─────────────────────────────────────────────────
    def _handle_choice(self, keys, space_just_pressed, player, enemy) -> str:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.choice = 1 - self.choice
            pygame.time.wait(150)
        if space_just_pressed:
            if self.choice == 1:
                self._phase       = _FLEE
                self._phase_timer = 0
                self.message      = "¡Escapaste con éxito!"
                self._pending_result = "exploring"
            else:
                self._player_attack(player, enemy)
        return "continue"

    # ── Ataque del jugador ───────────────────────────────────────────────────
    def _player_attack(self, player, enemy):
        damage   = random.randint(max(1, player.attack - 3), player.attack + 5)
        enemy.hp = max(0, enemy.hp - damage)
        if enemy.hp <= 0:
            player.exp += enemy.exp_reward
            self._check_levelup(player)
            self.message = (
                f"¡Atacaste por {damage}!  |  "
                f"¡{enemy.name} fue derrotado!  +{enemy.exp_reward} EXP"
            )
            self._pending_result = "win"
        else:
            self.message = (
                f"¡Atacaste a {enemy.name} por {damage} de daño!  |  "
                f"HP enemigo: {enemy.hp}/{enemy.max_hp}  —  Pulsa ESPACIO"
            )
        self._phase       = _PLAYER_ATK
        self._phase_timer = 0

    # ── Ataque del enemigo ───────────────────────────────────────────────────
    def _enemy_attack(self, player, enemy):
        damage    = random.randint(max(1, enemy.attack - 2), enemy.attack + 3)
        player.hp = max(0, player.hp - damage)
        if player.hp <= 0:
            self.message = (
                f"¡{enemy.name} te golpeó por {damage}!  |  "
                f"¡Has sido derrotado!"
            )
            player.hp = player.max_hp
            player.x  = 5
            player.y  = 5
            self._pending_result = "exploring"
        else:
            self.message = (
                f"¡{enemy.name} te atacó por {damage} de daño!  |  "
                f"Tu HP: {player.hp}/{player.max_hp}  —  Pulsa ESPACIO"
            )
        self._phase       = _ENEMY_ATK
        self._phase_timer = 0

    # ── Level up ─────────────────────────────────────────────────────────────
    @staticmethod
    def _check_levelup(player):
        while player.exp >= player.level * 100:
            player.level  += 1
            player.max_hp += 20
            player.hp      = player.max_hp
            player.attack += 3

    # ── Helper para el renderer ──────────────────────────────────────────────
    @property
    def in_choice_phase(self) -> bool:
        return self._phase == _CHOICE and self._input_cooldown == 0