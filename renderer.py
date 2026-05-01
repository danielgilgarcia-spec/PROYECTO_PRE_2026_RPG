"""
renderer.py   Todas las funciones de dibujo del juego.
"""

import random
import pygame

from defined import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from text import INTRO_SCREENS


# Colores de acento por nivel para la pantalla de batalla
_NIVEL_ACCENT = {
    1: (74,  159, 255),   # azul mar
    2: (232, 160,  32),   # naranja desierto
    3: (192,  96, 248),   # púrpura fortaleza
}


class Renderer:
    def __init__(self, screen: pygame.Surface, assets, font: pygame.font.Font, font_big: pygame.font.Font):
        self.screen    = screen
        self.assets    = assets
        self.font      = font
        self.font_big  = font_big
        self.nivel_actual = 1

        self._loaded_intro_images: dict  = {}
        self._loaded_dialog_images: dict = {}  # caché para imágenes de diálogo
        self._zoro_img = None   # None=no intentado, False=fallido

    # ------------------------------------------------------------------
    # Tiles
    # ------------------------------------------------------------------
    def draw_tile(self, tile_type: int, x: int, y: int, camera_x: int, camera_y: int,
                  mini_imgs: dict = None, nivel: int = 1):
        screen_x = (x - camera_x) * TILE_SIZE
        screen_y = (y - camera_y) * TILE_SIZE
        rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
        a = self.assets

        if tile_type == 0:
            if a.tile_grass:
                self.screen.blit(a.tile_grass, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["GREEN"], rect)
                for _ in range(3):
                    px = screen_x + random.randint(5, 25)
                    py = screen_y + random.randint(5, 25)
                    pygame.draw.circle(self.screen, COLORS["DARK_GREEN"], (px, py), 2)

        elif tile_type == 1:
            if a.tile_grass:
                self.screen.blit(a.tile_grass, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["GREEN"], rect)
            if a.tree_image:
                tree_img = pygame.transform.scale(a.tree_image, (TILE_SIZE, TILE_SIZE))
                self.screen.blit(tree_img, (screen_x, screen_y))

        elif tile_type == 2:
            if a.tile_water:
                self.screen.blit(a.tile_water, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["BLUE"], rect)

        elif tile_type == 3:
            if a.tile_path:
                self.screen.blit(a.tile_path, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["LIGHT_GRAY"], rect)

        elif tile_type == 4:
            if a.tile_grass:
                self.screen.blit(a.tile_grass, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["GREEN"], rect)
            if a.tile_house:
                self.screen.blit(a.tile_house, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["BROWN"], rect)
                roof = [
                    (screen_x,      screen_y + 10),
                    (screen_x + 16, screen_y),
                    (screen_x + 32, screen_y + 10),
                ]
                pygame.draw.polygon(self.screen, COLORS["RED"], roof)

        elif tile_type == 5:
            if a.tile_grass:
                self.screen.blit(a.tile_grass, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["GREEN"], rect)
            if mini_imgs and mini_imgs.get(nivel):
                self.screen.blit(mini_imgs[nivel], (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["GOLD"], rect, 3)
                label = self.font_big.render("!", True, COLORS["GOLD"])
                self.screen.blit(label, label.get_rect(center=(screen_x + TILE_SIZE // 2,
                                                                screen_y + TILE_SIZE // 2)))

        elif tile_type == 6:
            if a.tile_arena:
                self.screen.blit(a.tile_arena, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, COLORS["DARK_BLUE"], rect)

    # ------------------------------------------------------------------
    # Exploración
    # ------------------------------------------------------------------
    def draw_exploring(self, player, player_name: str, difficulty: dict,
                       current_map: list, camera, message: str,
                       mini_imgs: dict = None, nivel: int = 1):
        self.screen.fill(COLORS["BLACK"])
        camera.update(player.x, player.y, current_map)

        start_x, end_x, start_y, end_y = camera.visible_range(current_map)
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.draw_tile(current_map[y][x], x, y, camera.x, camera.y,
                               mini_imgs=mini_imgs, nivel=nivel)

        px = (player.x - camera.x) * TILE_SIZE
        py = (player.y - camera.y) * TILE_SIZE
        self.screen.blit(player.imagen, (px, py))

        hud_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, COLORS["BLACK"], hud_rect)
        pygame.draw.rect(self.screen, COLORS["WHITE"], hud_rect, 2)

        stats_text = (
            f"{player_name}  |  HP: {player.hp}/{player.max_hp}"
            f"  |  Nv: {player.level}  |  EXP: {player.exp}"
            f"  [{difficulty['name']}]"
        )
        self.screen.blit(self.font.render(stats_text, True, COLORS["WHITE"]), (10, SCREEN_HEIGHT - 70))
        self.screen.blit(self.font.render(message,    True, COLORS["WHITE"]), (10, SCREEN_HEIGHT - 40))

    # ------------------------------------------------------------------
    # Batalla
    # ------------------------------------------------------------------
    def draw_battle(self, player, enemy, message: str, battle_choice: int):
        self.screen.fill(COLORS["BLACK"])

        nivel  = self.nivel_actual
        accent = _NIVEL_ACCENT.get(nivel, COLORS["WHITE"])

        # --- Fondo de batalla ---
        battle_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, 200)
        bg = self.assets.battle_bg.get(nivel)
        if bg:
            self.screen.blit(bg, (50, 50))
        else:
            if nivel == 1:
                pygame.draw.rect(self.screen, (10, 25, 55), battle_rect)
                for i in range(6):
                    wy    = 170 + i * 14
                    color = (20, 60, 120) if i % 2 == 0 else (15, 45, 95)
                    pygame.draw.ellipse(self.screen, color, (50, wy, SCREEN_WIDTH - 100, 20))
            elif nivel == 2:
                pygame.draw.rect(self.screen, (30, 12, 2), battle_rect)
                pygame.draw.rect(self.screen, (100, 50, 10),
                                 pygame.Rect(50, 165, SCREEN_WIDTH - 100, 85))
                pygame.draw.circle(self.screen, (255, 185, 60), (SCREEN_WIDTH - 110, 95), 28)
            else:
                pygame.draw.rect(self.screen, (10, 0, 18), battle_rect)
                pygame.draw.rect(self.screen, (22, 12, 40),
                                 pygame.Rect(50, 185, SCREEN_WIDTH - 100, 65))
                for b in range(8):
                    bx = 50 + b * ((SCREEN_WIDTH - 100) // 8)
                    pygame.draw.rect(self.screen, (26, 12, 42),
                                     pygame.Rect(bx + 2, 169, (SCREEN_WIDTH - 100) // 8 - 4, 16))

        # Borde con color de acento del nivel
        pygame.draw.rect(self.screen, accent, battle_rect, 3)

        # --- Enemigo (derecha) ---
        enemy_x, enemy_y = SCREEN_WIDTH - 160, 148

        if hasattr(enemy, "imagen") and enemy.imagen is not None:
            img = enemy.imagen
            if enemy.name == "Mihawk":
                img = pygame.transform.scale(enemy.imagen, (120, 120))
            self.screen.blit(img, img.get_rect(center=(enemy_x, enemy_y)))
        else:
            pygame.draw.circle(self.screen, (100, 0, 100), (enemy_x, enemy_y), 40)
            pygame.draw.circle(self.screen, COLORS["RED"], (enemy_x - 10, enemy_y - 10), 8)
            pygame.draw.circle(self.screen, COLORS["RED"], (enemy_x + 10, enemy_y - 10), 8)

        # Nombre enemigo — mismo estilo que el héroe (font pequeña, color acento)
        name_e = self.font.render(enemy.name, True, accent)
        self.screen.blit(name_e, (enemy_x - name_e.get_width() // 2, 58))

        # HP enemigo
        self._draw_hp_bar(enemy_x - 75, enemy_y + 58, enemy.hp, enemy.max_hp)
        self.screen.blit(
            self.font.render(f"{enemy.hp}/{enemy.max_hp}", True, COLORS["WHITE"]),
            (enemy_x - 25, enemy_y + 60)
        )

        # --- Jugador (izquierda) ---
        player_x, player_y = 140, 140

        if self._zoro_img is None:
            try:
                img = pygame.image.load("assets/big_enemies/zoro_lucha.png").convert_alpha()
                self._zoro_img = pygame.transform.scale(img, (110, 110))
            except Exception as e:
                print(f"Error cargando zoro_lucha: {e}")
                self._zoro_img = False

        if self._zoro_img:
            self.screen.blit(self._zoro_img, self._zoro_img.get_rect(center=(player_x, player_y)))
        else:
            pygame.draw.circle(self.screen, COLORS["RED"], (player_x, player_y), 30)

        # Nombre héroe
        name_p = self.font.render(player.name, True, (160, 210, 255))
        self.screen.blit(name_p, (player_x - name_p.get_width() // 2, player_y + 58))

        # HP héroe
        self._draw_hp_bar(player_x - 55, player_y + 75, player.hp, player.max_hp)
        self.screen.blit(
            self.font.render(f"{player.hp}/{player.max_hp}", True, COLORS["WHITE"]),
            (player_x - 20, player_y + 77)
        )

        # --- Menú de combate con borde de acento ---
        menu_rect = pygame.Rect(50, 300, SCREEN_WIDTH - 100, 130)
        pygame.draw.rect(self.screen, COLORS["BLACK"], menu_rect)
        pygame.draw.rect(self.screen, accent, menu_rect, 3)

        self.screen.blit(self.font.render(message, True, COLORS["WHITE"]), (70, 320))

        attack_color = COLORS["WHITE"] if battle_choice == 0 else COLORS["GRAY"]
        flee_color   = COLORS["WHITE"] if battle_choice == 1 else COLORS["GRAY"]
        self.screen.blit(self.font_big.render("ATACAR", True, attack_color), (70,  360))
        self.screen.blit(self.font_big.render("HUIR",   True, flee_color),   (300, 360))
        self.screen.blit(
            self.font.render("Flechas: Seleccionar  |  ESPACIO: Confirmar", True, COLORS["GRAY"]),
            (70, 400)
        )

    # ------------------------------------------------------------------
    # Diálogo (pre-jefe, post-jefe, final) con caché de imágenes
    # ------------------------------------------------------------------
    def draw_dialog(self, screen_data: dict, timer: int):
        self.screen.fill(COLORS["BLACK"])

        for y in range(SCREEN_HEIGHT):
            f = y / SCREEN_HEIGHT
            r = int(20 * (1 - f)); g = int(20 * (1 - f)); b = int(40 * (1 - f))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        alpha = int(255 * min(1, timer / 20))

        if screen_data.get("image_background"):
            self._draw_dialog_images(screen_data, alpha)

        title = screen_data.get("title", "")
        if title:
            title_font = pygame.font.Font(None, 44)
            title_surf = title_font.render(title, True, screen_data.get("color", COLORS["WHITE"]))
            title_surf.set_alpha(alpha)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 110)))

        text_lines    = screen_data.get("text", "").split("\n")
        line_height   = 46
        has_bg        = bool(screen_data.get("image_background"))
        offset_x      = -100 if has_bg else 0

        text_surfaces = [self.font_big.render(l, True, COLORS["WHITE"]) for l in text_lines]
        max_width     = max((ts.get_width() for ts in text_surfaces), default=100)
        box_w = max_width + 80
        box_h = len(text_surfaces) * line_height + 20
        box_x = (SCREEN_WIDTH - box_w) // 2 + offset_x
        box_y = 390

        bocadillo = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(self.screen, COLORS["D_GREEN"],    bocadillo)
        pygame.draw.rect(self.screen, COLORS["DARK_GREEN"], bocadillo, 4)

        for i, ts in enumerate(text_surfaces):
            ts.set_alpha(alpha)
            rect = ts.get_rect(center=(SCREEN_WIDTH // 2 + offset_x,
                                       box_y + 20 + i * line_height))
            self.screen.blit(ts, rect)

        instr = pygame.font.Font(None, 24).render("Pulsa ESPACIO para continuar", True, COLORS["GRAY"])
        self.screen.blit(instr, instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))

    # ------------------------------------------------------------------
    # Intro
    # ------------------------------------------------------------------
    def draw_intro(self, intro_screen: int, intro_timer: int) -> bool:
        if intro_screen >= len(INTRO_SCREENS):
            return True

        self.screen.fill(COLORS["BLACK"])
        current_screen = INTRO_SCREENS[intro_screen]

        for y in range(SCREEN_HEIGHT):
            f = y / SCREEN_HEIGHT
            r = int(20 * (1 - f)); g = int(20 * (1 - f)); b = int(40 * (1 - f))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        alpha = int(255 * min(1, intro_timer / 30))

        if current_screen.get("image_background"):
            self._draw_intro_images(intro_screen, current_screen, alpha)

        title_font    = pygame.font.Font(None, 50)
        title_surface = title_font.render(current_screen["title"], True, current_screen["color"])
        title_rect    = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        title_surface.set_alpha(alpha)
        self.screen.blit(title_surface, title_rect)

        text_lines  = current_screen["text"].split("\n")
        line_height = 50
        offset_x    = 0

        if current_screen.get("image_background"):
            offset_x      = -100
            text_surfaces = [self.font_big.render(l, True, COLORS["WHITE"]) for l in text_lines]
            max_width     = max(ts.get_width() for ts in text_surfaces)
            box_w  = max_width + 80
            box_h  = len(text_surfaces) * line_height + 3
            box_x  = (SCREEN_WIDTH - box_w) // 2 + offset_x
            box_y  = 398
            bocadillo = pygame.Rect(box_x, box_y, box_w, box_h)
            pygame.draw.rect(self.screen, COLORS["D_GREEN"],    bocadillo)
            pygame.draw.rect(self.screen, COLORS["DARK_GREEN"], bocadillo, 4)
            start_y = box_y + 20
        else:
            start_y = SCREEN_HEIGHT // 2 - (len(text_lines) * line_height) // 2

        for i, line in enumerate(text_lines):
            ts = self.font_big.render(line, True, COLORS["WHITE"])
            ts.set_alpha(alpha)
            rect = ts.get_rect(center=(SCREEN_WIDTH // 2 + offset_x, start_y + i * line_height))
            self.screen.blit(ts, rect)

        instr = pygame.font.Font(None, 24).render("Pulsa ESPACIO para continuar", True, COLORS["GRAY"])
        self.screen.blit(instr, instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))

        progress   = (intro_screen + 1) / len(INTRO_SCREENS)
        bar_width  = SCREEN_WIDTH - 100
        bar_height = 10
        pygame.draw.rect(self.screen, COLORS["WHITE"],
                         pygame.Rect(50, SCREEN_HEIGHT - 50, bar_width, bar_height), 2)
        pygame.draw.rect(self.screen, (100, 200, 100),
                         pygame.Rect(50, SCREEN_HEIGHT - 50, int(bar_width * progress), bar_height))

        return False

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------
    def _draw_hp_bar(self, x: int, y: int, hp: int, max_hp: int):
        bar_w = 150
        pct   = max(0, hp) / max(1, max_hp)
        bg    = pygame.Rect(x, y, bar_w, 15)
        fill  = pygame.Rect(x, y, int(bar_w * pct), 15)
        pygame.draw.rect(self.screen, COLORS["LIGHT_GRAY"], bg)
        pygame.draw.rect(self.screen, COLORS["GREEN"] if pct > 0.3 else COLORS["RED"], fill)
        pygame.draw.rect(self.screen, COLORS["WHITE"], bg, 2)

    def _draw_dialog_images(self, screen_data: dict, alpha: int):
        """Dibuja imágenes de un diálogo con caché para no recargar cada frame."""
        bkg_path = screen_data.get("image_background", "")
        img_path = screen_data.get("image", "")

        # Caché por ruta
        if bkg_path and bkg_path not in self._loaded_dialog_images:
            try:
                img_bkg = pygame.image.load(bkg_path).convert_alpha()
                w, h = img_bkg.get_size()
                if w > SCREEN_WIDTH:
                    scale   = SCREEN_WIDTH / w
                    img_bkg = pygame.transform.scale(img_bkg, (int(w * scale), int(h * scale)))
                self._loaded_dialog_images[bkg_path] = img_bkg
            except Exception as e:
                print(f"[dialog bkg] {e}")
                self._loaded_dialog_images[bkg_path] = None

        if img_path and img_path not in self._loaded_dialog_images:
            try:
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (int(1024 / 4), int(1536 / 4)))
                self._loaded_dialog_images[img_path] = img
            except Exception as e:
                print(f"[dialog img] {e}")
                self._loaded_dialog_images[img_path] = None

        img_bkg = self._loaded_dialog_images.get(bkg_path)
        img     = self._loaded_dialog_images.get(img_path)

        if img_bkg:
            surf = img_bkg.copy()
            surf.set_alpha(alpha)
            self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
        if img:
            surf = img.copy()
            surf.set_alpha(alpha)
            self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2 + 152, SCREEN_HEIGHT // 2 + 33)))

    def _draw_intro_images(self, intro_screen: int, current_screen: dict, alpha: int):
        img_bkg_path = current_screen.get("image_background")
        img_path     = current_screen.get("image")
        img_bkg = self._loaded_intro_images.get(f"{intro_screen}_bkg")
        img     = self._loaded_intro_images.get(f"{intro_screen}_fg")

        if img_bkg is None and img_bkg_path:
            try:
                img_bkg = pygame.image.load(img_bkg_path).convert_alpha()
                w, h = img_bkg.get_size()
                if w > SCREEN_WIDTH:
                    scale   = SCREEN_WIDTH / w
                    img_bkg = pygame.transform.scale(img_bkg, (int(w * scale), int(h * scale)))
                self._loaded_intro_images[f"{intro_screen}_bkg"] = img_bkg
            except Exception:
                img_bkg = None

        if img is None and img_path:
            try:
                img = pygame.image.load(img_path).convert_alpha()
                self._loaded_intro_images[f"{intro_screen}_fg"] = img
            except Exception:
                img = None

        if img_bkg:
            img_bkg.set_alpha(alpha)
            self.screen.blit(img_bkg, img_bkg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
        if img:
            img = pygame.transform.scale(img, (int(1024 / 4), int(1536 / 4)))
            img.set_alpha(alpha)
            self.screen.blit(img, img.get_rect(center=(SCREEN_WIDTH // 2 + 152, SCREEN_HEIGHT // 2 + 33)))