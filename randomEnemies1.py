import pygame
import random


class RandomEnemy1:

    def __init__(self, level):
        enemy_types = [
            {
                "name": "Gohst_1",
                "hp": 30,
                "atk": 8,
                "exp": 20,
                "image": "assets/enemies/Gohst_1.png"
            },
            {
                "name": "Bat_1",
                "hp": 50,
                "atk": 12,
                "exp": 35,
                "image": "assets/enemies/Bat_1.png"
            }
        ]

        # Elegir enemigo aleatorio
        enemy = random.choice(enemy_types)

        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        try:
            img = pygame.image.load(enemy["image"]).convert_alpha()
            self.imagen = pygame.transform.scale(img, (100, 100))
            print(f"Imagen cargada correctamente: {enemy['image']}")

        except Exception as e:
            print(f"Error cargando imagen {enemy['image']}: {e}")
            self.imagen = None
