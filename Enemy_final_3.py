import pygame


class Enemy3:
    def __init__(self, level):

        enemy = {
            "name": "King",
            "hp": 60,
            "atk": 15,
            "exp": 50
        }

        self.name = enemy["name"]
        self.max_hp = enemy["hp"] + (level * 5)
        self.hp = self.max_hp
        self.attack = enemy["atk"] + level
        self.exp_reward = enemy["exp"]

        imagen = {
            "King": "assets/big_enemies/king_lucha.png"
        }

        img_file = imagen.get(self.name, "assets/big_enemies/king_lucha.png")

        try:
            self.imagen = pygame.image.load(img_file).convert_alpha()
            self.imagen = pygame.transform.scale(self.imagen, (200, 200))
        except Exception as e:
            print(e)
            self.imagen = None
