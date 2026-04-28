"""
asset_loader.py   Carga y escala todos los assets gráficos del juego.

Uso:
    from asset_loader import AssetLoader
    assets = AssetLoader(TILE_SIZE)
    tile_grass = assets.tile_grass
"""

import pygame
from defined import TILE_SIZE, SCREEN_WIDTH


class AssetLoader:
    """Centraliza la carga de imágenes y assets gráficos."""

    def __init__(self, tile_size: int = TILE_SIZE):
        self.tile_size = tile_size

        # Tiles del overworld
        self.overworld   = None
        self.tile_grass  = None
        self.tile_path   = None
        self.tile_water  = None
        self.tile_house  = None
        self.tile_exit   = None
        self.tile_arena  = None

        # Sprite del árbol
        self.tree_image  = None

        # Fondos de batalla por nivel
        self.battle_bg   = {1: None, 2: None, 3: None}

        self._load_all()

    # ------------------------------------------------------------------
    # Carga principal
    # ------------------------------------------------------------------
    def _load_all(self):
        self._load_tree()
        self._load_overworld_tileset()
        self._load_individual_tiles()
        self._load_battle_backgrounds()

    def _load_tree(self):
        """Carga el sprite del árbol con fallback."""
        for path in ("assets/tiles/arbol.png", "assets/trees/tree_0.png"):
            try:
                self.tree_image = pygame.image.load(path).convert_alpha()
                return
            except Exception:
                pass

    def _load_overworld_tileset(self):
        """Intenta cargar el tileset overworld completo."""
        try:
            self.overworld = pygame.image.load("assets/tiles/overworld.png").convert_alpha()
            self.tile_grass = self._crop_tile(0, 0)
            self.tile_path  = self._crop_tile(1, 0)
            self.tile_water = self._crop_tile(2, 0)
            self.tile_house = self._crop_tile(3, 0)
            self.tile_exit  = self._crop_tile(4, 0)
            self.tile_arena = self._crop_tile(5, 0)
        except Exception:
            self.overworld = None

    def _load_individual_tiles(self):
        """Sobrescribe con texturas individuales si existen."""
        tile_map = {
            "assets/tiles/hierba.png": "tile_grass",
            "assets/tiles/camino.png": "tile_path",
            "assets/tiles/agua.png":   "tile_water",
            "assets/tiles/Casa.png":   "tile_house",
            "assets/tiles/arena.png":  "tile_arena",
        }
        for path, attr in tile_map.items():
            try:
                img = pygame.image.load(path).convert_alpha()
                setattr(self, attr, pygame.transform.scale(img, (self.tile_size, self.tile_size)))
            except Exception:
                pass

    def _load_battle_backgrounds(self):
        """Carga y escala los fondos de batalla para cada nivel con fallback a None."""
        size = (SCREEN_WIDTH - 100, 200)
        files = {
            1: "assets/battle_backgrounds/bg_mar.png",
            2: "assets/battle_backgrounds/bg_desierto.png",
            3: "assets/battle_backgrounds/bg_fortaleza.png",
        }
        for nivel, path in files.items():
            try:
                img = pygame.image.load(path).convert()
                self.battle_bg[nivel] = pygame.transform.scale(img, size)
            except Exception:
                self.battle_bg[nivel] = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _crop_tile(self, col: int, row: int) -> pygame.Surface:
        """Recorta un tile del tileset overworld en (col, row)."""
        ts = self.tile_size
        rect = pygame.Rect(col * ts, row * ts, ts, ts)
        surface = pygame.Surface((ts, ts), pygame.SRCALPHA)
        surface.blit(self.overworld, (0, 0), rect)
        return surface