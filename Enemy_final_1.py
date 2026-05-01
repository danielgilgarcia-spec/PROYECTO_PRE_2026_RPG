import pygame


class Enemy1:
    def __init__(self, level):

        enemy = {
            "name": "Mihawk",
            "hp": 30,
            "atk": 8,
            "exp": 20
        }

        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        imagen = {
            "Mihawk": "assets/big_enemies/mihawk_lucha.png"
        }

        img_file = imagen.get(self.name, "assets/big_enemies/mihawk_lucha.png")

        try:
            self.imagen = pygame.image.load(img_file).convert_alpha()
            self.imagen = pygame.transform.scale(self.imagen, (200, 200))
        except Exception as e:
            print(e)
            self.imagen = None
