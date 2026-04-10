
# Estados del juego

INTRO      = "intro"
EXPLORING  = "exploring"
BATTLE     = "battle"
DIALOGUE   = "dialogue"
EXIT       = "exit"
NEXT       = "next"


# Colores

COLORS = {
    "BLACK": (0,0,0),
    "WHITE": (255,255,255),
    "GRAY": (128,128,128),
    "LIGHT_GRAY": (210,180,140),
    "DARK_GRAY": (50,50,50),
    "GREEN": (34,139,34),
    "DARK_GREEN": (0,100,0),
    "RED": (220,20,60),
    "GOLD": (255,215,0),
    "BLUE": (30,144,255),
    "NAVY": (20,30,80),
    "CYAN": (0,200,220),
    "PURPLE": (120,0,180),
    "D_GREEN": (30, 60, 30),
    "BROWN": (139, 69, 19),
    "DARK_BLUE": (11, 22, 33)
}


DIFFICULTIES = [
    {
        "name": "Fácil",
        "desc": "Enemigos más débiles, más HP inicial",
        "color": COLORS["GREEN"],
        "enemy_mult": 0.7,
        "player_hp": 150,
        "player_atk": 15,
        "encounter_rate": 0.08,
    },
    {
        "name": "Normal",
        "desc": "Experiencia equilibrada",
        "color": COLORS["GOLD"],
        "enemy_mult": 1.0,
        "player_hp": 100,
        "player_atk": 10,
        "encounter_rate": 0.15,
    },
    {
        "name": "Difícil",
        "desc": "Enemigos poderosos, HP reducido",
        "color": COLORS["RED"],
        "enemy_mult": 1.5,
        "player_hp": 70,
        "player_atk": 8,
        "encounter_rate": 0.22,
    },
]

# Configuración de pantalla
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 560
TILE_SIZE = 48