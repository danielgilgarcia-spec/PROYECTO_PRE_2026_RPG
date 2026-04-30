import pygame


class Player:
    def __init__(self, name="Zoro", max_hp=100, attack=15):
        self.x      = 5
        self.y      = 5
        self.name   = name
        self.max_hp = max_hp
        self.hp     = max_hp
        self.attack = attack
        self.level  = 1
        self.exp    = 0

        try:
            self.imagen = pygame.image.load("assets/big_enemies/zoro.png").convert_alpha()
            self.imagen = pygame.transform.scale(self.imagen, (32, 32))
        except Exception as e:
            print(f"Error cargando sprite de Zoro: {e}")
            # Fallback: cuadrado verde
            self.imagen = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.imagen.fill((34, 139, 34))

    def move(self, dx: int, dy: int, game_map: list) -> bool:
        """Mueve al jugador si la celda destino es transitable."""
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
            tile = game_map[new_y][new_x]
            if tile != 1 and tile != 2:   # 1=árbol, 2=agua → obstáculo
                self.x = new_x
                self.y = new_y
                return True
        return False

    def heal(self):
        self.hp = self.max_hp