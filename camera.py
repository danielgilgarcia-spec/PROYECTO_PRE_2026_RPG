"""
camera.py  –  Gestión de la cámara / viewport.
"""

from defined import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Camera:
    """Calcula el desplazamiento de la cámara centrada en el jugador."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.view_w = SCREEN_WIDTH  // TILE_SIZE
        self.view_h = SCREEN_HEIGHT // TILE_SIZE

    def update(self, player_x: int, player_y: int, current_map: list):
        """Centra la cámara en el jugador y la limita a los bordes del mapa."""
        map_w = len(current_map[0])
        map_h = len(current_map)

        max_cam_x = max(0, map_w - self.view_w)
        max_cam_y = max(0, map_h - self.view_h)

        target_x = player_x - self.view_w // 2
        target_y = player_y - self.view_h // 2

        self.x = max(0, min(target_x, max_cam_x))
        self.y = max(0, min(target_y, max_cam_y))

    def visible_range(self, current_map: list) -> tuple:
        """Devuelve (start_x, end_x, start_y, end_y) de tiles visibles."""
        start_y = self.y
        end_y   = min(self.y + self.view_h, len(current_map))
        start_x = self.x
        end_x   = min(self.x + self.view_w, len(current_map[0]))
        return start_x, end_x, start_y, end_y
