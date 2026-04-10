import pygame
import random
#modificar, crear un archivo por cada enemy y cargar imagenes de cada uno, con un fondo de batalla diferente para cada uno, y una imagen de fondo para la historia, y una imagen para el mapa.

class RandomEnemy:
    def __init__(self, level):
        enemy_types = [
            {"name": "Lobo_1", "hp": 30, "atk": 8, "exp": 20},
            {"name": "Bat_1", "hp": 50, "atk": 12, "exp": 35}
        ]
        enemy = random.choice(enemy_types)
        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        # Cargar imagen PNG según el tipo de enemigo
        imagenes = {
            "Lobo_1": "assets/enemies/Lobo_1.png",
            "Bat_1": "assets/enemies/Bat_1.png"
        }
        img_file1 = imagenes.get(self.name, "assets/enemies/Lobo_1.png")
        img_file2 = imagenes.get(self.name, "assets/enemies/Bat_1.png")
        try:
            self.imagen1 = pygame.image.load(img_file1).convert_alpha()
            self.imagen2 = pygame.image.load(img_file2).convert_alpha()
        except Exception:
            self.imagen1 = None
            self.imagen2 = None