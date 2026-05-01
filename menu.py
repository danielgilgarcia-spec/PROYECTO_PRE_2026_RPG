"""
Menú inicial del RPG
Incluye: selección de dificultad, nombre de usuario y historial de jugadores
"""

import pygame
import os
import sys
from player_history import PLAYER_HISTORY
from defined import COLORS, DIFFICULTIES, SCREEN_WIDTH, SCREEN_HEIGHT

MAX_NAME_LEN = 12




# ── Persistencia ────────────────────────────────────────────────────────────

def load_history():
    history = []
    if not os.path.exists("player_history.txt"):
        return history
    with open("player_history.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, level, difficulty = line.split(",")
            history.append({"name": name, "max_level": int(level), "difficulty": difficulty})
    return history  


def save_history(history):
    with open("player_history.txt", "w", encoding="utf-8") as f:  # "w" no "a"
        for entry in history:
            f.write(f"{entry['name']},{entry['max_level']},{entry['difficulty']}\n")


def add_player_record(name, level, difficulty):
    history = load_history()
    for entry in history:
        if entry['name'].lower() == name.lower():
            if level > entry["max_level"]:
                entry["max_level"] = level
                entry["difficulty"] = difficulty
                save_history(history)  # ← guardar si se actualiza
            return
    history.append({"name": name, "max_level": level, "difficulty": difficulty})
    save_history(history)


# ── Helpers de dibujo ────────────────────────────────────────────────────────

def draw_gradient_bg(surface):
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        r = int(10 + 20 * t)
        g = int(10 + 10 * t)
        b = int(40 + 40 * (1 - t))
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def draw_panel(surface, rect, border_color=COLORS["WHITE"], alpha=200):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, alpha))
    surface.blit(panel, rect.topleft)
    pygame.draw.rect(surface, border_color, rect, 2)


def render_text_centered(surface, text, font, color, cy):
    surf = font.render(text, True, color)
    x = (SCREEN_WIDTH - surf.get_width()) // 2
    surface.blit(surf, (x, cy))
    return surf.get_height()


def draw_stars(surface, t):
    """Dibuja estrellas estáticas de fondo (decorativo)."""
    rng_positions = [
        (45, 30), (120, 80), (200, 15), (310, 55), (400, 25),
        (500, 70), (580, 40), (60, 200), (590, 300), (30, 400),
        (560, 450), (280, 130), (450, 180), (150, 350),
    ]
    for px, py in rng_positions:
        brightness = int(180 + 75 * abs((t // 40 + px) % 2 - 1))
        c = (brightness, brightness, brightness)
        pygame.draw.circle(surface, c, (px, py), 1)


# ── Pantallas ────────────────────────────────────────────────────────────────

class MainMenu:
    """
    Estados:
        MAIN     > menú principal (Jugar / Settings / Historial / Salir)

        JUGAR -> NAME     > entrada de nombre
        SETTINGS -> DIFF     > selección de dificultad
        HISTORY  > historial de jugadores
        SALIR     > cierra el juego
    """

    def __init__(self, screen):
        self.screen = screen
        self.state  = "MAIN"
        self.tick   = 0

        # Fuentes
        self.font_title  = pygame.font.Font(None, 40)
        self.font_big    = pygame.font.Font(None, 38)
        self.font_mid    = pygame.font.Font(None, 28)
        self.font_small  = pygame.font.Font(None, 22)

        # Nombre
        self.player_name  = ""
        self.name_active  = True
        self.name_error   = ""

        # Dificultad
        self.diff_index   = 1          # Normal por defecto
        self.diff_cursor_timer = 0

        # Menú principal
        self.main_options = ["Jugar", "Settings", "Historial", "Salir"]
        self.main_cursor    = 0
        self.key_cooldown   = 0

        # Resultado final
        self.result = None             # dict con name, difficulty cuando el jugador confirma

    # ── Loop público ─────────────────────────────────────────────────────────

    def run(self):
        """Bloquea hasta que el jugador inicia la partida o sale."""
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60)
            self.tick += 1
            if self.key_cooldown > 0:
                self.key_cooldown -= dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self._handle_event(event)

            self._draw()
            pygame.display.flip()

            if self.result is not None:
                return self.result          # {"name": ..., "difficulty": {...}}

    # ── Eventos ──────────────────────────────────────────────────────────────

    def _handle_event(self, event):
        if self.state == "MAIN":
            self._event_main(event)
        elif self.state == "NAME":
            self._event_name(event)
        elif self.state == "DIFF":
            self._event_diff(event)
        elif self.state == "SETTINGS":
            self._event_settings(event)
        elif self.state == "HISTORY":
            self._event_history(event)

    def _event_main(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_UP, pygame.K_w):
            self.main_cursor = (self.main_cursor - 1) % len(self.main_options)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.main_cursor = (self.main_cursor + 1) % len(self.main_options)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            choice = self.main_options[self.main_cursor]
            if choice == "Jugar":
                self.state = "NAME"
                self.player_name = ""
                self.name_error  = ""
            elif choice == "Historial":
                self.state = "HISTORY"
            elif choice == "Settings":
                self.state = "SETTINGS"
            elif choice == "Salir":
                pygame.quit()
                sys.exit()

    def _event_name(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.state = "MAIN"
            return
        if event.key == pygame.K_RETURN:
            name = self.player_name.strip()
            if len(name) < 3:
                self.name_error = "El nombre debe tener al menos 3 caracteres."
            else:
                self.name_error = ""
                self.result = {
                    "name": self.player_name.strip(),
                    "difficulty": DIFFICULTIES[self.diff_index],
                }

            return
        if event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
            self.name_error  = ""
            return
        # Solo letras, números y guion bajo
        char = event.unicode
        if char and char.isprintable() and char not in ('/', '\\', '"', "'"):
            if len(self.player_name) < MAX_NAME_LEN:
                self.player_name += char
            else:
                self.name_error = f"Máximo {MAX_NAME_LEN} caracteres."

    def _event_settings(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.state = "MAIN"
            return
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.diff_index = (self.diff_index - 1) % len(DIFFICULTIES)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.diff_index = (self.diff_index + 1) % len(DIFFICULTIES)




    def _event_diff(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.state = "NAME"
            return
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.diff_index = (self.diff_index - 1) % len(DIFFICULTIES)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.diff_index = (self.diff_index + 1) % len(DIFFICULTIES)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.result = {
                "name":       self.player_name.strip(),
                "difficulty": DIFFICULTIES[self.diff_index],
            }

    def _event_history(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN):
                self.state = "MAIN"

    # ── Dibujo ───────────────────────────────────────────────────────────────

    def _draw(self):
        draw_gradient_bg(self.screen)
        draw_stars(self.screen, self.tick)

        if self.state == "MAIN":
            self._draw_main()
        elif self.state == "NAME":
            self._draw_name()
        elif self.state == "DIFF":
            self._draw_diff()
        elif self.state == "SETTINGS":
            self._draw_settings()
        elif self.state == "HISTORY":
            self._draw_history()

    # ── Menú principal ────────────────────────────────────────────────────────

    def _draw_settings(self):
        render_text_centered(self.screen, "SETTINGS", self.font_big, COLORS["GOLD"], 60)
        render_text_centered(self.screen, "Dificultad", self.font_mid, COLORS["WHITE"], 110)

        # Dibujar cartas sin indicador "ARRIBA" ni "Jugador:" (no aplican en Settings)
        self._draw_difficulty_cards(show_player_name=False)

        render_text_centered(self.screen, "IZQ y DER para cambiar  |  ESC para volver", self.font_small, COLORS["GRAY"], SCREEN_HEIGHT - 30)



    def _draw_main(self):
        # Título con efecto pulso
        pulse = int(10 * abs((self.tick % 60) / 30 - 1))
        title_color = (255, 215 + pulse, 0)
        render_text_centered(self.screen, "EN BUSCA DE LA TRIPULACIÓN PERDIDA", self.font_title, title_color, 80)

        subtitle_color = (180, 180, 255)
        render_text_centered(self.screen, "Una aventura épica te espera", self.font_small, subtitle_color, 145)

        # Opciones
        option_y_start = 240
        option_gap     = 60

        for i, opt in enumerate(self.main_options):
            selected = (i == self.main_cursor)
            if selected:
                # Fondo de selección
                bg = pygame.Rect(SCREEN_WIDTH // 2 - 130, option_y_start + i * option_gap - 8, 260, 44)
                draw_panel(self.screen, bg, COLORS["GOLD"], 160)
                color = COLORS["GOLD"]
                prefix = ">  "
            else:
                color = COLORS["GRAY"]
                prefix = "   "

            render_text_centered(
                self.screen,
                prefix + opt,
                self.font_big,
                color,
                option_y_start + i * option_gap,
            )

        # Pie
        render_text_centered(self.screen, "ARRIBA y ABBAJO para Mover  |  ENTER para Confirmar", self.font_small, COLORS["GRAY"], SCREEN_HEIGHT - 30)

    # ── Nombre ────────────────────────────────────────────────────────────────

    def _draw_name(self):
        render_text_centered(self.screen, "¿Cómo te llamas, héroe?", self.font_big, COLORS["GOLD"], 100)

        # Caja de texto
        box = pygame.Rect(SCREEN_WIDTH // 2 - 160, 200, 320, 50)
        draw_panel(self.screen, box, COLORS["NAVY"], 220)

        # Cursor parpadeante
        cursor = "|" if (self.tick // 30) % 2 == 0 else ""
        display_text = self.player_name + cursor
        name_surf = self.font_big.render(display_text, True, COLORS["WHITE"])
        self.screen.blit(name_surf, (box.x + 12, box.y + 10))

        # Contador de caracteres
        counter_text = f"{len(self.player_name)}/{MAX_NAME_LEN}"
        counter_surf = self.font_small.render(counter_text, True, COLORS["GRAY"])
        self.screen.blit(counter_surf, (box.right - counter_surf.get_width() - 8, box.bottom + 6))

        # Error
        if self.name_error:
            render_text_centered(self.screen, self.name_error, self.font_small, COLORS["RED"], 270)

        # Instrucciones
        render_text_centered(self.screen, "ENTER > Continuar  |  ESC > Volver", self.font_small, COLORS["GRAY"], SCREEN_HEIGHT - 30)
        render_text_centered(self.screen, f"Máximo {MAX_NAME_LEN} caracteres, mínimo 3", self.font_small, COLORS["LIGHT_GRAY"], 300)

    # ── Dificultad ────────────────────────────────────────────────────────────

    def _draw_diff(self):
        self._draw_difficulty_cards(show_player_name=True)

    def _draw_difficulty_cards(self, show_player_name: bool = True):
        card_w  = 160
        card_h  = 220
        gap     = 20
        total_w = 3 * card_w + 2 * gap
        start_x = (SCREEN_WIDTH - total_w) // 2

        for i, diff in enumerate(DIFFICULTIES):
            x = start_x + i * (card_w + gap)
            y = 130
            selected = (i == self.diff_index)

            border_color = diff["color"] if selected else COLORS["GRAY"]
            rect = pygame.Rect(x, y, card_w, card_h)
            draw_panel(self.screen, rect, border_color, 210 if selected else 140)

            # Nombre
            name_surf = self.font_mid.render(diff["name"], True, diff["color"])
            self.screen.blit(name_surf, (x + (card_w - name_surf.get_width()) // 2, y + 15))

            # Ícono de dificultad (estrellas)
            icon = "★" * (i + 1)
            icon_surf = self.font_mid.render(icon, True, diff["color"])
            self.screen.blit(icon_surf, (x + (card_w - icon_surf.get_width()) // 2, y + 50))

            # Descripción (wrap manual)
            words = diff["desc"].split()
            lines, line = [], ""
            for w in words:
                test = (line + " " + w).strip()
                if self.font_small.size(test)[0] < card_w - 16:
                    line = test
                else:
                    if line:
                        lines.append(line)
                    line = w
            if line:
                lines.append(line)

            for li, ln in enumerate(lines):
                ls = self.font_small.render(ln, True, COLORS["LIGHT_GRAY"])
                self.screen.blit(ls, (x + (card_w - ls.get_width()) // 2, y + 90 + li * 22))

            # Stats breves
            stats = [
                f"HP: {diff['player_hp']}",
                f"ATK: {diff['player_atk']}",
            ]
            for si, st in enumerate(stats):
                ss = self.font_small.render(st, True, COLORS["WHITE"])
                self.screen.blit(ss, (x + (card_w - ss.get_width()) // 2, y + 155 + si * 22))

        # Nombre del jugador solo cuando corresponde (pantalla de selección durante el juego)
        if show_player_name:
            render_text_centered(
                self.screen,
                f"Jugador: {self.player_name}",
                self.font_mid,
                COLORS["CYAN"],
                390,
            )
            render_text_centered(self.screen, "IZQ y DER para Cambiar  |  ENTER para elegir  |  ESC para Volver", self.font_small, COLORS["GRAY"], SCREEN_HEIGHT - 30)

    # ── Historial ─────────────────────────────────────────────────────────────

    def _draw_history(self):
        render_text_centered(self.screen, "Historial de Héroes", self.font_big, COLORS["GOLD"], 50)

        history = load_history()

        panel = pygame.Rect(60, 100, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 170)
        draw_panel(self.screen, panel, COLORS["GOLD"], 200)

        if not history:
            render_text_centered(self.screen, "Aún no hay héroes registrados.", self.font_mid, COLORS["GRAY"], 260)
        else:
            # Cabecera
            headers = [("Nombre", 80), ("Nivel máx.", 280), ("Dificultad", 420)]
            for label, hx in headers:
                hs = self.font_small.render(label, True, COLORS["GOLD"])
                self.screen.blit(hs, (hx, 112))

            pygame.draw.line(self.screen, COLORS["GOLD"], (70, 132), (SCREEN_WIDTH - 70, 132), 1)

            # Ordenar por nivel descendente
            sorted_history = sorted(history, key=lambda e: e["max_level"], reverse=True)

            row_h = 32
            max_rows = (panel.height - 50) // row_h

            for ri, entry in enumerate(sorted_history[:max_rows]):
                row_y = 140 + ri * row_h
                # Fila alternada
                if ri % 2 == 0:
                    row_bg = pygame.Rect(70, row_y - 4, SCREEN_WIDTH - 140, row_h - 2)
                    pygame.draw.rect(self.screen, (30, 30, 60), row_bg)

                # Posición
                pos_text = f"#{ri+1}"
                pos_color = COLORS["GOLD"] if ri == 0 else (192, 192, 192) if ri == 1 else (205, 127, 50) if ri == 2 else COLORS["WHITE"]
                self.screen.blit(self.font_small.render(pos_text, True, pos_color), (70, row_y))

                # Nombre
                name_s = self.font_mid.render(entry["name"], True, COLORS["WHITE"])
                self.screen.blit(name_s, (100, row_y - 2))

                # Nivel
                level_s = self.font_mid.render(str(entry["max_level"]), True, COLORS["CYAN"])
                self.screen.blit(level_s, (290, row_y - 2))

                # Dificultad
                diff_name = entry.get("difficulty", "Normal")
                diff_color = COLORS["GREEN"] if diff_name == "Fácil" else COLORS["GOLD"] if diff_name == "Normal" else COLORS["RED"]
                diff_s = self.font_small.render(diff_name, True, diff_color)
                self.screen.blit(diff_s, (420, row_y))

        render_text_centered(self.screen, "ESC / ENTER → Volver al menú", self.font_small, COLORS["GRAY"], SCREEN_HEIGHT - 30)


# ── Función de entrada pública ────────────────────────────────────────────────

def show_main_menu(screen):
    """
    Muestra el menú inicial y devuelve un dict con:
        {
            "name":       str,
            "difficulty": dict (con keys: name, enemy_mult, player_hp, player_atk, encounter_rate)
        }
    """
    menu = MainMenu(screen)
    return menu.run()