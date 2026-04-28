import pygame

from maps import game_map_1, game_map_2, game_map_3

class Player:
    def __init__(self, name="Zoro", max_hp=100, attack=15):
        self.x = 5
        self.y = 5
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.level = 1
        self.exp = 0

        # Cargar imagen PNG con transparencia
        self.imagen = pygame.image.load("assets/big_enemies/zoro.png").convert_alpha()
        # Opcional: redimensionar si es muy grande
        self.imagen = pygame.transform.scale(self.imagen, (32, 32))
        
    def move(self, dx, dy, game_map_1):
        new_x = self.x + dx
        new_y = self.y + dy

        # Verificar límites y colisiones en mapa 1
        if 0 <= new_x < len(game_map_1[0]) and 0 <= new_y < len(game_map_1):
            if game_map_1[new_y][new_x] != 1 and game_map_1[new_y][new_x] != 2:  # 1 es árbol y 2 es agua -> obstáculo
                self.x = new_x
                self.y = new_y
                return True
        return False
    
    def move(self, dx, dy, game_map_2):
        new_x = self.x + dx
        new_y = self.y + dy

        # Verificar límites y colisiones en mapa 2
        if 0 <= new_x < len(game_map_2[0]) and 0 <= new_y < len(game_map_2):
            if game_map_2[new_y][new_x] != 1 and game_map_2[new_y][new_x] != 2:  # 1 es árbol y 2 es agua -> obstáculo
                self.x = new_x
                self.y = new_y
                return True
        return False
       
    def move(self, dx, dy, game_map_3):
        new_x = self.x + dx
        new_y = self.y + dy

        # Verificar límites y colisiones en mapa 3
        if 0 <= new_x < len(game_map_3[0]) and 0 <= new_y < len(game_map_3):
            if game_map_3[new_y][new_x] != 1 and game_map_3[new_y][new_x] != 2:  # 1 es árbol y 2 es agua -> obstáculo
                self.x = new_x
                self.y = new_y
                return True
        return False

    def heal(self):
        self.hp = self.max_hp