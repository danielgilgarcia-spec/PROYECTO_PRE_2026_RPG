import pygame
import random


class RandomEnemy:

    def __init__(self, level):
        enemy_types = [
            {
                "name": "Lobo_1",
                "hp": 30,
                "atk": 8,
                "exp": 20,
                "image": "assets/enemies/Lobo_1.png"
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

        # Ruta de imagen correspondiente
        img_file = enemy["image"]

        try:
            # IMPORTANTE:
            # pygame.display.set_mode(...) debe haberse ejecutado antes
            self.image = pygame.image.load(img_file).convert_alpha()
            print(f"Imagen cargada correctamente: {img_file}")

        except Exception as e:
            print(f"Error cargando imagen {img_file}: {e}")
            self.image = None
