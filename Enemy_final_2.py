import pygame


class Enemy2:
    def __init__(self, level):

        enemy = {
            "name": "Pica",
            "hp": 50,
            "atk": 12,
            "exp": 35
        }

        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        imagen = {
            "Pica": "assets/big_enemies/pica_lucha.png"
        }

        img_file = imagen.get(self.name, "assets/big_enemies/pica_lucha.png")

        try:
            self.imagen = pygame.image.load(img_file).convert_alpha()
            self.imagen = pygame.transform.scale(self.imagen, (200, 200))
        except Exception as e:
            print(e)
            self.imagen = None