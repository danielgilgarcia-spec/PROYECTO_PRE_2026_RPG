import pygame
import random
#modificar, crear un archivo por cada enemy y cargar imagenes de cada uno, con un fondo de batalla diferente para cada uno, y una imagen de fondo para la historia, y una imagen para el mapa.

class Enemy:
    def __init__(self, level):
        enemy_types = [
            {"name": "Mihawk", "hp": 30, "atk": 8, "exp": 20},
            {"name": "Pica", "hp": 50, "atk": 12, "exp": 35},
            {"name": "King", "hp": 60, "atk": 15, "exp": 50}
        ]
        enemy = random.choice(enemy_types)
        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        # Cargar imagen PNG según el tipo de enemigo
        imagenes = {
            "Mihawk": "mihawk_lucha.png",
            "Pica": "pica_lucha.png",
            "King": "king_lucha.png"
        }
        img_file = imagenes.get(self.name, "mihawk_lucha.png")
        try:
            self.imagen = pygame.image.load(img_file).convert_alpha()
            self.imagen = pygame.transform.scale(self.imagen, (100, 100))
        except Exception:
            self.imagen = None