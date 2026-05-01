"""
renderer.py   Todas las funciones de dibujo del juego.
"""

import random
import pygame

from defined import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from text import INTRO_SCREENS


# Paleta visual por nivel para la pantalla de batalla
_NIVEL_STYLE = {
    1: {
        "accent":       (74,  159, 255),   # azul mar
        "name_color":   (160, 220, 255),   # celeste para nombres
        "menu_bg":      (5,   15,  35),    # negro azulado
        "hp_bar":       (30,  120, 220),   # barra HP en azul
    },
    2: {
        "accent":       (232, 160,  32),   # naranja desierto
        "name_color":   (255, 210, 120),   # amarillo arena
        "menu_bg":      (30,  15,   5),    # negro anaranjado
        "hp_bar":       (200, 120,  20),   # barra HP en naranja
    },
    3: {
        "accent":       (192,  96, 248),   # púrpura fortaleza
        "name_color":   (220, 160, 255),   # lavanda
        "menu_bg":      (10,   5,  20),    # negro púrpura
        "hp_bar":       (150,  50, 220),   # barra HP en púrpura
    },
}


class Renderer:
    def __init__(self, screen: pygame.Surface, assets, font: pygame.font.Font, font_big: pygame.font.Font):
        self.screen    = screen
        self.assets    = assets
        self.font      = font
        self.font_big  = font_big
        self.nivel_actual = 1

        self._loaded_intro_images:  dict = {}
        self._loaded_dialog_images: dict = {}
        self._zoro_img = None   # None = no intentado, False = fallido

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
                self.screen.blit(label, label.get_rect(
                    center=(screen_x + TILE_SIZE // 2, screen_y + TILE_SIZE // 2)))

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
    # Batalla — tres estilos visuales según nivel
    # ------------------------------------------------------------------
    def draw_battle(self, player, enemy, message: str, battle_choice: int,
                    show_menu: bool = True):
        nivel  = self.nivel_actual
        style  = _NIVEL_STYLE.get(nivel, _NIVEL_STYLE[1])
        accent = style["accent"]

        self.screen.fill(style["menu_bg"])

        battle_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, 200)

        bg = self.assets.battle_bg.get(nivel)
        if bg:
            self.screen.blit(bg, (50, 50))
        else:
            self._draw_battle_bg_fallback(nivel, battle_rect)

        pygame.draw.rect(self.screen, accent, battle_rect, 3)

        # --- Enemigo (derecha) ---
        enemy_x, enemy_y = SCREEN_WIDTH - 160, 148
        if hasattr(enemy, "imagen") and enemy.imagen is not None:
            img = enemy.imagen
            if enemy.name == "Mihawk":
                img = pygame.transform.scale(enemy.imagen, (120, 120))
            self.screen.blit(img, img.get_rect(center=(enemy_x, enemy_y)))
        else:
            pygame.draw.circle(self.screen, accent,          (enemy_x, enemy_y), 42)
            pygame.draw.circle(self.screen, style["menu_bg"], (enemy_x, enemy_y), 38)
            pygame.draw.circle(self.screen, COLORS["RED"],   (enemy_x - 10, enemy_y - 10), 7)
            pygame.draw.circle(self.screen, COLORS["RED"],   (enemy_x + 10, enemy_y - 10), 7)

        name_e = self.font.render(enemy.name, True, style["name_color"])
        self.screen.blit(name_e, (enemy_x - name_e.get_width() // 2, 58))
        self._draw_hp_bar(enemy_x - 75, enemy_y + 58, enemy.hp, enemy.max_hp, accent)
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
            self.screen.blit(self._zoro_img,
                             self._zoro_img.get_rect(center=(player_x, player_y)))
        else:
            pygame.draw.circle(self.screen, COLORS["RED"], (player_x, player_y), 30)

        name_p = self.font.render(player.name, True, (160, 210, 255))
        self.screen.blit(name_p, (player_x - name_p.get_width() // 2, player_y + 58))
        self._draw_hp_bar(player_x - 55, player_y + 75, player.hp, player.max_hp, (80, 200, 120))
        self.screen.blit(
            self.font.render(f"{player.hp}/{player.max_hp}", True, COLORS["WHITE"]),
            (player_x - 20, player_y + 77)
        )

        # --- Panel de mensaje / menú ---
        menu_rect = pygame.Rect(50, 295, SCREEN_WIDTH - 100, 145)
        pygame.draw.rect(self.screen, style["menu_bg"], menu_rect)
        pygame.draw.rect(self.screen, accent, menu_rect, 3)

        # Mensaje partido en hasta 2 líneas por el separador " | "
        lines = message.split("  |  ", 1)
        for li, line in enumerate(lines):
            msg_surf = self.font.render(line, True, COLORS["WHITE"])
            self.screen.blit(msg_surf, (70, 310 + li * 24))

        if show_menu:
            # Botones ATACAR / HUIR
            for i, label in enumerate(["ATACAR", "HUIR"]):
                ox = 70 if i == 0 else 300
                if battle_choice == i:
                    btn_rect = pygame.Rect(ox - 8, 358, 120, 36)
                    btn_surf = pygame.Surface((btn_rect.width, btn_rect.height), pygame.SRCALPHA)
                    btn_surf.fill((*accent, 60))
                    self.screen.blit(btn_surf, btn_rect.topleft)
                    pygame.draw.rect(self.screen, accent, btn_rect, 2, border_radius=6)
                    color = COLORS["WHITE"]
                else:
                    color = COLORS["GRAY"]
                self.screen.blit(self.font_big.render(label, True, color), (ox, 365))

            self.screen.blit(
                self.font.render("Flechas: Seleccionar  |  ESPACIO: Confirmar",
                                 True, COLORS["GRAY"]),
                (70, 408)
            )
        else:
            # Fuera de la fase de elección: indicar que ESPACIO avanza
            hint = self.font.render("Pulsa ESPACIO para continuar...", True, COLORS["GRAY"])
            self.screen.blit(hint, (70, 390))

    def _draw_battle_bg_fallback(self, nivel: int, battle_rect: pygame.Rect):
        """Fondo de batalla con primitivas cuando no hay imagen."""
        if nivel == 1:   # Mar nocturno
            pygame.draw.rect(self.screen, (8, 18, 42), battle_rect)
            # Estrellas
            for _ in range(25):
                sx = random.randint(50, SCREEN_WIDTH - 50)
                sy = random.randint(50, 160)
                pygame.draw.circle(self.screen, (200, 220, 255),
                                   (sx, sy), random.choice([1, 1, 2]))
            # Olas
            for i in range(5):
                wy    = 175 + i * 13
                color = (18, 55, 110) if i % 2 == 0 else (12, 40, 85)
                pygame.draw.ellipse(self.screen, color,
                                    (50, wy, SCREEN_WIDTH - 100, 18))

        elif nivel == 2:  # Desierto al atardecer
            pygame.draw.rect(self.screen, (28, 10, 2), battle_rect)
            # Cielo degradado manual
            for i in range(80):
                r = min(255, 28 + i * 2)
                g = min(255, 10 + i)
                pygame.draw.line(self.screen, (r, g, 2),
                                 (50, 50 + i), (SCREEN_WIDTH - 50, 50 + i))
            # Arena
            pygame.draw.rect(self.screen, (140, 80, 20),
                             pygame.Rect(50, 180, SCREEN_WIDTH - 100, 70))
            # Dunas
            for d in range(3):
                pygame.draw.ellipse(self.screen, (160, 100, 30),
                                    (50 + d * 150, 170, 200, 30))
            # Sol
            pygame.draw.circle(self.screen, (255, 200, 60),
                               (SCREEN_WIDTH - 100, 80), 26)
            pygame.draw.circle(self.screen, (255, 230, 120),
                               (SCREEN_WIDTH - 100, 80), 18)

        else:             # Fortaleza nocturna
            pygame.draw.rect(self.screen, (8, 2, 16), battle_rect)
            # Estrellas
            for _ in range(30):
                sx = random.randint(50, SCREEN_WIDTH - 50)
                sy = random.randint(50, 170)
                pygame.draw.circle(self.screen, (180, 140, 255),
                                   (sx, sy), random.choice([1, 1, 1, 2]))
            # Muralla
            pygame.draw.rect(self.screen, (18, 8, 32),
                             pygame.Rect(50, 178, SCREEN_WIDTH - 100, 72))
            # Almenas
            for b in range(10):
                bx = 55 + b * ((SCREEN_WIDTH - 110) // 10)
                pygame.draw.rect(self.screen, (25, 12, 44),
                                 pygame.Rect(bx, 162, (SCREEN_WIDTH - 110) // 10 - 4, 18))
            # Líneas de sillares
            for row in range(3):
                pygame.draw.line(self.screen, (30, 15, 50),
                                 (50, 190 + row * 20),
                                 (SCREEN_WIDTH - 50, 190 + row * 20), 1)
            # Resplandor púrpura central
            glow_surf = pygame.Surface((200, 80), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (140, 60, 220, 40), glow_surf.get_rect())
            self.screen.blit(glow_surf, (SCREEN_WIDTH // 2 - 100, 100))

    # ------------------------------------------------------------------
    # Diálogo con imágenes
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

        # ── Bocadillo de diálogo ──────────────────────────────────────────
        text_lines  = screen_data.get("text", "").split("\n")
        line_height = 38
        has_bg      = bool(screen_data.get("image_background"))
        offset_x    = -100 if has_bg else 0

        # Calcular ancho/alto del bocadillo según el texto
        text_surfs = [self.font_big.render(l, True, COLORS["WHITE"]) for l in text_lines]
        max_width  = max((ts.get_width() for ts in text_surfs), default=100)

        # Clampear para que nunca sobresalga de la pantalla
        BOX_MAX_W = SCREEN_WIDTH - 80   # margen de 40px a cada lado
        box_w = min(max_width + 60, BOX_MAX_W)
        box_h = len(text_surfs) * line_height + 30
        box_x = max(20, (SCREEN_WIDTH - box_w) // 2 + offset_x)
        # Asegurarse de que el borde derecho no salga de pantalla
        box_x = min(box_x, SCREEN_WIDTH - box_w - 20)
        box_y = SCREEN_HEIGHT - box_h - 55   # 55px sobre el pie de instrucción

        # Nombre del hablante encima del bocadillo
        speaker = screen_data.get("speaker", "")
        if speaker:
            speaker_font = pygame.font.Font(None, 26)
            spk_surf = speaker_font.render(f"  {speaker}  ", True, COLORS["BLACK"])
            spk_bg   = pygame.Rect(box_x + 12, box_y - 22,
                                   spk_surf.get_width() + 4, spk_surf.get_height() + 2)
            pygame.draw.rect(self.screen, screen_data.get("color", COLORS["WHITE"]), spk_bg, border_radius=4)
            spk_surf.set_alpha(alpha)
            self.screen.blit(spk_surf, (spk_bg.x + 2, spk_bg.y + 1))

        bocadillo = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(self.screen, COLORS["D_GREEN"],    bocadillo, border_radius=6)
        pygame.draw.rect(self.screen, COLORS["DARK_GREEN"], bocadillo, 3, border_radius=6)

        center_x = box_x + box_w // 2
        for i, ts in enumerate(text_surfs):
            ts.set_alpha(alpha)
            rect = ts.get_rect(center=(center_x, box_y + 18 + i * line_height))
            self.screen.blit(ts, rect)

        instr = pygame.font.Font(None, 24).render(
            "Pulsa ESPACIO para continuar", True, COLORS["GRAY"])
        self.screen.blit(instr, instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)))

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
        title_surface.set_alpha(alpha)
        self.screen.blit(title_surface,
                         title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120)))

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

        instr = pygame.font.Font(None, 24).render(
            "Pulsa ESPACIO para continuar", True, COLORS["GRAY"])
        self.screen.blit(instr, instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)))

        progress   = (intro_screen + 1) / len(INTRO_SCREENS)
        bar_width  = SCREEN_WIDTH - 100
        bar_height = 10
        pygame.draw.rect(self.screen, COLORS["WHITE"],
                         pygame.Rect(50, SCREEN_HEIGHT - 50, bar_width, bar_height), 2)
        pygame.draw.rect(self.screen, (100, 200, 100),
                         pygame.Rect(50, SCREEN_HEIGHT - 50,
                                     int(bar_width * progress), bar_height))
        return False

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------
    def _draw_hp_bar(self, x: int, y: int, hp: int, max_hp: int,
                     bar_color: tuple = None):
        bar_w = 150
        pct   = max(0, hp) / max(1, max_hp)
        bg    = pygame.Rect(x, y, bar_w, 15)
        fill  = pygame.Rect(x, y, int(bar_w * pct), 15)
        pygame.draw.rect(self.screen, COLORS["DARK_GRAY"], bg)
        if bar_color:
            color = bar_color
        else:
            color = COLORS["GREEN"] if pct > 0.3 else COLORS["RED"]
        pygame.draw.rect(self.screen, color, fill)
        pygame.draw.rect(self.screen, COLORS["WHITE"], bg, 1)

    def _draw_dialog_images(self, screen_data: dict, alpha: int):
        bkg_path = screen_data.get("image_background", "")
        img_path = screen_data.get("image", "")

        if bkg_path and bkg_path not in self._loaded_dialog_images:
            try:
                img_bkg = pygame.image.load(bkg_path).convert_alpha()
                w, h = img_bkg.get_size()
                if w > SCREEN_WIDTH:
                    scale   = SCREEN_WIDTH / w
                    img_bkg = pygame.transform.scale(img_bkg,
                                                     (int(w * scale), int(h * scale)))
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
            self.screen.blit(surf, surf.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
        if img:
            surf = img.copy()
            surf.set_alpha(alpha)
            self.screen.blit(surf, surf.get_rect(
                center=(SCREEN_WIDTH // 2 + 152, SCREEN_HEIGHT // 2 + 33)))

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
                    img_bkg = pygame.transform.scale(img_bkg,
                                                     (int(w * scale), int(h * scale)))
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
            self.screen.blit(img_bkg, img_bkg.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
        if img:
            img = pygame.transform.scale(img, (int(1024 / 4), int(1536 / 4)))
            img.set_alpha(alpha)
            self.screen.blit(img, img.get_rect(
                center=(SCREEN_WIDTH // 2 + 152, SCREEN_HEIGHT // 2 + 33)))