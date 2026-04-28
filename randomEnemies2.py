import pygame
import random


class RandomEnemy:
    def __init__(self, level):
        enemy_types = [
            {
                "name": "Golem_1",
                "hp": 30,
                "atk": 8,
                "exp": 20,
                "image": "assets/enemies/Golem_1.png"
            },
            {
                "name": "Golem_2",
                "hp": 50,
                "atk": 12,
                "exp": 35,
                "image": "assets/enemies/Golem_2.png"
            }
        ]

        # Selección aleatoria del enemigo
        enemy = random.choice(enemy_types)

        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        try:
            # Cargar únicamente la imagen del enemigo elegido aleatoriamente
            self.image = pygame.image.load(enemy["image"]).convert_alpha()
            print(f"Imagen cargada correctamente: {enemy['image']}")

        except Exception as e:
            print(f"Error cargando imagen: {e}")
            self.image = None
