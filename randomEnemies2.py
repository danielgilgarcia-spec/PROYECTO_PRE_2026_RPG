import pygame
import random


class RandomEnemy:
    def __init__(self, level):
        enemy_types = [
            {"name": "Golem_1", "hp": 30, "atk": 8, "exp": 20},
            {"name": "Golem_2", "hp": 50, "atk": 12, "exp": 35}
        ]
        enemy = random.choice(enemy_types)
        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        # Cargar imagen PNG según el tipo de enemigo
        imagenes = {
            "Golem_1": "assets/enemies/Golem_1.png",
            "Golem_2": "assets/enemies/Golem_2.png"
        }
        img_file1 = imagenes.get(self.name, "assets/enemies/Golem_1.png")
        img_file2 = imagenes.get(self.name, "assets/enemies/Golem_2.png")
        try:
            self.imagen1 = pygame.image.load(img_file1).convert_alpha()
            self.imagen2 = pygame.image.load(img_file2).convert_alpha()
        except Exception:
            self.imagen1 = None
            self.imagen2 = None