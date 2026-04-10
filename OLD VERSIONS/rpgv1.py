"""
RPG estilo Pokémon Original - Versión Simplificada
Controles: Flechas para moverse, ESPACIO para interactuar/atacar
"""

import pygame
import random
import sys

# Inicialización
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 560
TILE_SIZE = 48
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini RPG")
clock = pygame.time.Clock()

# Colores
COLORS["BLACK"] = (0, 0, 0)
COLORS["WHITE"] = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BLUE = (30, 144, 255)
BROWN = (139, 69, 19)
RED = (220, 20, 60)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Estados del juego
EXPLORING = "exploring"
BATTLE = "battle"
DIALOGUE = "dialogue"
EXIT = "exit"
NEXT = "next"

class Player:
    def __init__(self):
        self.x = 5
        self.y = 5
        self.name = "Héroe"
        self.hp = 100
        self.max_hp = 100
        self.attack = 15
        self.level = 1
        self.exp = 0

        # Cargar imagen PNG con transparencia
        self.imagen = pygame.image.load("zoro.png").convert_alpha()
        # Opcional: redimensionar si es muy grande
        self.imagen = pygame.transform.scale(self.imagen, (32, 32))
        
    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy

        # Verificar límites y colisiones
        if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
            if game_map[new_y][new_x] != 1:  # 1 es árbol/obstáculo
                self.x = new_x
                self.y = new_y
                return True
        return False
    
    def heal(self):
        self.hp = self.max_hp

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

class Game:
    def __init__(self):
        self.state = EXPLORING
        self.player = Player()
        self.enemy = Enemy(self.player.level)
        self.message = "¡Bienvenido! Usa las flechas para moverte."
        self.font = pygame.font.Font(None, 24)
        self.font_big = pygame.font.Font(None, 36)
        
        # Mapa: 0=pasto, 1=árbol, 2=agua, 3=camino, 4=casa, 5=salida/siguiente nivel
        self.game_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 3, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 3, 1, 1, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 0, 0, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 5],
            [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
            [1, 0, 0, 0, 4, 3, 3, 3, 1, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        self.game_map2 = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 4, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 4, 0, 0, 1],
            [1, 0, 0, 0, 3, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 2, 2, 2, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 4, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 1],
            [1, 1, 1, 0, 0, 0, 3, 1, 1, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2, 0, 1],
            [1, 0, 0, 1, 1, 0, 0, 3, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 5],
            [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
            [1, 0, 0, 0, 0, 3, 3, 3, 1, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.battle_choice = 0  # 0=Atacar, 1=Huir
        # Mapa activo (permite cambiar de nivel fácilmente)
        self.current_map = self.game_map
        # Viewport / cámara: cantidad de tiles visibles (excluyendo HUD)
        self.view_w = (SCREEN_WIDTH) // TILE_SIZE
        self.view_h = (SCREEN_HEIGHT) // TILE_SIZE
        self.camera_x = 0
        self.camera_y = 0
        
    def draw_tile(self, tile_type, x, y):
        """Dibuja un tile en el mapa"""
        # Convertir coordenadas de mapa a pantalla usando cámara
        screen_x = (x - self.camera_x) * TILE_SIZE
        screen_y = (y - self.camera_y) * TILE_SIZE
        rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
        
        if tile_type == 0:  # Pasto
            pygame.draw.rect(screen, GREEN, rect)
            # Detalles de pasto (relativos a pantalla)
            for i in range(3):
                px = screen_x + random.randint(5, 25)
                py = screen_y + random.randint(5, 25)
                pygame.draw.circle(screen, DARK_GREEN, (px, py), 2)
                
        elif tile_type == 1:  # Árbol
            pygame.draw.rect(screen, DARK_GREEN, rect)
            # Tronco
            trunk = pygame.Rect(screen_x + 12, screen_y + 18, 8, 10)
            pygame.draw.rect(screen, COLORS["BROWN"], trunk)
            
        elif tile_type == 2:  # Agua
            pygame.draw.rect(screen, BLUE, rect)
            
        elif tile_type == 3:  # Camino
            pygame.draw.rect(screen, (210, 180, 140), rect)
            
        elif tile_type == 4:  # Casa
                 pygame.draw.rect(screen, (139, 69, 19), rect)
                 roof = [(screen_x, screen_y + 10),
                     (screen_x + 16, screen_y),
                     (screen_x + 32, screen_y + 10)]
                 pygame.draw.polygon(screen, RED, roof)

        elif tile_type == 5:  # salida
            pygame.draw.rect(screen, (11, 22, 33), rect)

    def draw_player(self):
        px = (self.player.x - self.camera_x) * TILE_SIZE
        py = (self.player.y - self.camera_y) * TILE_SIZE
        screen.blit(self.player.imagen, (px, py))

    def draw_enemy(self):
        px = (self.enemy.x - self.camera_x) * TILE_SIZE
        py = (self.enemy.y - self.camera_y) * TILE_SIZE
        screen.blit(self.enemy.imagen, (px, py))

    def update_camera(self):
        """Centra la cámara en el jugador y la limita a los bordes del mapa"""
        map_w = len(self.current_map[0])
        map_h = len(self.current_map)

        max_cam_x = max(0, map_w - self.view_w)
        max_cam_y = max(0, map_h - self.view_h)

        target_x = self.player.x - self.view_w // 2
        target_y = self.player.y - self.view_h // 2

        self.camera_x = max(0, min(target_x, max_cam_x))
        self.camera_y = max(0, min(target_y, max_cam_y))

    def draw_exploring(self):
        """Dibuja el modo exploración"""
        screen.fill(COLORS["BLACK"])

        # Actualizar cámara antes de dibujar
        self.update_camera()

        # Dibujar solo la porción visible del mapa
        start_y = self.camera_y
        end_y = min(self.camera_y + self.view_h, len(self.current_map))
        start_x = self.camera_x
        end_x = min(self.camera_x + self.view_w, len(self.current_map[0]))

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.draw_tile(self.current_map[y][x], x, y)

       
        # Dibujar jugador
        self.draw_player()
        
        # HUD
        hud_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(screen, COLORS["BLACK"], hud_rect)
        pygame.draw.rect(screen, COLORS["WHITE"], hud_rect, 2)
        
        # Estadísticas
        stats_text = f"HP: {self.player.hp}/{self.player.max_hp}  |  Nivel: {self.player.level}  |  EXP: {self.player.exp}"
        text_surface = self.font.render(stats_text, True, COLORS["WHITE"])
        screen.blit(text_surface, (10, SCREEN_HEIGHT - 70))
        
        # Mensaje
        msg_surface = self.font.render(self.message, True, COLORS["WHITE"])
        screen.blit(msg_surface, (10, SCREEN_HEIGHT - 40))

    def draw_exploring2(self):
        """Dibuja el modo exploración"""
        screen.fill(COLORS["BLACK"])
        
        # Dibujar mapa2
        for y in range(len(self.game_map2)):
            for x in range(len(self.game_map2[0])):
                self.draw_tile(self.game_map2[y][x], x, y)
        
        # Dibujar jugador
        self.draw_player()
        
        # HUD
        hud_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(screen, COLORS["BLACK"], hud_rect)
        pygame.draw.rect(screen, COLORS["WHITE"], hud_rect, 2)
        
        # Estadísticas
        stats_text = f"HP: {self.player.hp + 100}/{self.player.max_hp + 100}  |  Nivel: {self.player.level + 100}  |  EXP: {self.player.exp + 100}"
        text_surface = self.font.render(stats_text, True, COLORS["WHITE"])
        screen.blit(text_surface, (10, SCREEN_HEIGHT - 70))
        
        # Mensaje
        msg_surface = self.font.render(self.message, True, COLORS["WHITE"])
        screen.blit(msg_surface, (10, SCREEN_HEIGHT - 40))
    
    def draw_battle(self):
        """Dibuja la pantalla de batalla"""
        screen.fill(COLORS["BLACK"])
        
        # Área de batalla
        battle_bg = pygame.Rect(50, 50, SCREEN_WIDTH - 100, 200)
        pygame.draw.rect(screen, GRAY, battle_bg)
        pygame.draw.rect(screen, COLORS["WHITE"], battle_bg, 3)
        
        # Enemigo (imagen o círculo)
        enemy_x = SCREEN_WIDTH - 150
        enemy_y = 120
        if hasattr(self.enemy, 'imagen') and self.enemy.imagen is not None:
            # Si el enemigo es Mihawk, aumentar tamaño
            if self.enemy.name == "Mihawk":
                imagen_grande = pygame.transform.scale(self.enemy.imagen, (120, 120))
                rect = imagen_grande.get_rect(center=(enemy_x, enemy_y))
                screen.blit(imagen_grande, rect)
            else:
                rect = self.enemy.imagen.get_rect(center=(enemy_x, enemy_y))
                screen.blit(self.enemy.imagen, rect)
        else:
            pygame.draw.circle(screen, (100, 0, 100), (enemy_x, enemy_y), 40)
            pygame.draw.circle(screen, RED, (enemy_x - 10, enemy_y - 10), 8)
            pygame.draw.circle(screen, RED, (enemy_x + 10, enemy_y - 10), 8)
        
        # Nombre del enemigo
        enemy_name = self.font_big.render(self.enemy.name, True, COLORS["WHITE"])
        screen.blit(enemy_name, (enemy_x - 50, enemy_y - 80))
        
        # Barra de HP del enemigo
        hp_bar_width = 150
        hp_percentage = self.enemy.hp / self.enemy.max_hp
        hp_bar_rect = pygame.Rect(enemy_x - 75, enemy_y + 50, hp_bar_width, 15)
        hp_fill_rect = pygame.Rect(enemy_x - 75, enemy_y + 50, int(hp_bar_width * hp_percentage), 15)
        pygame.draw.rect(screen, LIGHT_GRAY, hp_bar_rect)
        pygame.draw.rect(screen, GREEN if hp_percentage > 0.3 else RED, hp_fill_rect)
        pygame.draw.rect(screen, COLORS["WHITE"], hp_bar_rect, 2)
        
        # HP texto
        hp_text = self.font.render(f"{self.enemy.hp}/{self.enemy.max_hp}", True, COLORS["WHITE"])
        screen.blit(hp_text, (enemy_x - 30, enemy_y + 52))
        
        # Jugador (pequeño)
        player_x = 120
        player_y = 200
        pygame.draw.circle(screen, RED, (player_x, player_y), 25)
        
        # Barra de HP del jugador
        player_hp_bar_width = 150
        player_hp_percentage = self.player.hp / self.player.max_hp
        player_hp_bar_rect = pygame.Rect(player_x - 75, player_y + 40, player_hp_bar_width, 15)
        player_hp_fill_rect = pygame.Rect(player_x - 75, player_y + 40, int(player_hp_bar_width * player_hp_percentage), 15)
        pygame.draw.rect(screen, LIGHT_GRAY, player_hp_bar_rect)
        pygame.draw.rect(screen, GREEN if player_hp_percentage > 0.3 else RED, player_hp_fill_rect)
        pygame.draw.rect(screen, COLORS["WHITE"], player_hp_bar_rect, 2)
        
        # HP texto jugador
        player_hp_text = self.font.render(f"{self.player.hp}/{self.player.max_hp}", True, COLORS["WHITE"])
        screen.blit(player_hp_text, (player_x - 30, player_y + 42))
        
        # Menú de combate
        menu_rect = pygame.Rect(50, 300, SCREEN_WIDTH - 100, 130)
        pygame.draw.rect(screen, COLORS["BLACK"], menu_rect)
        pygame.draw.rect(screen, COLORS["WHITE"], menu_rect, 3)
        
        # Mensaje de batalla
        msg_surface = self.font.render(self.message, True, COLORS["WHITE"])
        screen.blit(msg_surface, (70, 320))
        
        # Opciones
        attack_color = COLORS["WHITE"] if self.battle_choice == 0 else GRAY
        flee_color = COLORS["WHITE"] if self.battle_choice == 1 else GRAY
        
        attack_text = self.font_big.render("ATACAR" if self.battle_choice == 0 else "ATACAR", True, attack_color)
        flee_text = self.font_big.render("HUIR" if self.battle_choice == 1 else "HUIR", True, flee_color)
        
        screen.blit(attack_text, (70, 360))
        screen.blit(flee_text, (300, 360))
        
        hint_text = self.font.render("Flechas: Seleccionar  |  ESPACIO: Confirmar", True, GRAY)
        screen.blit(hint_text, (70, 400))
    
    def handle_battle_input(self, keys):
        """Maneja la entrada en batalla"""
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.battle_choice = 1 - self.battle_choice
            pygame.time.wait(150)
        
        if keys[pygame.K_SPACE]:
            if self.battle_choice == 0:  # Atacar
                damage = random.randint(self.player.attack - 3, self.player.attack + 5)
                self.enemy.hp -= damage
                self.message = f"¡Atacaste por {damage} de daño!"
                
                pygame.time.wait(800)
                
                if self.enemy.hp <= 0:
                    self.player.exp += self.enemy.exp_reward
                    self.message = f"¡Derrotaste a {self.enemy.name}! +{self.enemy.exp_reward} EXP"
                    
                    # Subir de nivel
                    if self.player.exp >= self.player.level * 100:
                        self.player.level += 1
                        self.player.max_hp += 20
                        self.player.hp = self.player.max_hp
                        self.player.attack += 3
                        self.message += f" | ¡SUBISTE AL NIVEL {self.player.level}!"
                    
                    pygame.time.wait(2000)
                    self.state = EXPLORING
                    return
                
                # Turno del enemigo
                pygame.time.wait(200)
                enemy_damage = random.randint(self.enemy.attack - 2, self.enemy.attack + 3)
                self.player.hp -= enemy_damage
                self.message += f" | {self.enemy.name} te atacó por {enemy_damage}!"
                
                if self.player.hp <= 0:
                    self.message = "¡Has sido derrotado! Volviendo al inicio..."
                    pygame.time.wait(2000)
                    self.player.hp = self.player.max_hp
                    self.player.x = 5
                    self.player.y = 5
                    self.state = EXPLORING
            
            else:  # Huir
                self.message = "¡Escapaste con éxito!"
                pygame.time.wait(1000)
                self.state = EXPLORING

                # SI QUIERES HACERLO MÁS DESAFIANTE, DESCOMENTA ESTE BLOQUE Y COMENTA EL DE ARRIBA, ASÍ HUIR NO SERÁ 100% SEGURO, SINO EL VALOR INDICADO
                """
                if random.random() > 0.5:
                    self.message = "¡Escapaste con éxito!"
                    pygame.time.wait(1000)
                    self.state = EXPLORING
                else:
                    enemy_damage = random.randint(self.enemy.attack - 2, self.enemy.attack + 3)
                    self.player.hp -= enemy_damage
                    self.message = f"¡No pudiste escapar! {self.enemy.name} te atacó por {enemy_damage}!"
                    
                    if self.player.hp <= 0:
                        self.message = "¡Has sido derrotado! Volviendo al inicio..."
                        pygame.time.wait(2000)
                        self.player.hp = self.player.max_hp
                        self.player.x = 5
                        self.player.y = 5
                        self.state = EXPLORING
                """
            pygame.time.wait(500)
    
    def check_random_encounter(self):
        """Verifica si ocurre un encuentro aleatorio"""
        # Solo en pasto del mapa activo
        if self.current_map[self.player.y][self.player.x] == 0:
            if random.random() < 0.15:
                self.enemy = Enemy(self.player.level)
                self.state = BATTLE
                self.message = f"¡Un {self.enemy.name} salvaje apareció!"
                self.battle_choice = 0

    def run(self):
        """Loop principal del juego"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            keys = pygame.key.get_pressed()
            
            if self.state == EXPLORING:
                moved = False
                # Mover usando el mapa activo
                if keys[pygame.K_UP]:
                    moved = self.player.move(0, -1, self.current_map)
                    pygame.time.wait(150)
                elif keys[pygame.K_DOWN]:
                    moved = self.player.move(0, 1, self.current_map)
                    pygame.time.wait(150)
                elif keys[pygame.K_LEFT]:
                    moved = self.player.move(-1, 0, self.current_map)
                    pygame.time.wait(150)
                elif keys[pygame.K_RIGHT]:
                    moved = self.player.move(1, 0, self.current_map)
                    pygame.time.wait(150)

                if moved:
                    self.check_random_encounter()

                # Curar en la casa (mapa activo)
                if self.current_map[self.player.y][self.player.x] == 4 and keys[pygame.K_SPACE]:
                    self.player.heal()
                    self.message = "¡Te curaste en la casa! HP restaurado."
                    pygame.time.wait(1000)

                # Salida / cambio de nivel
                if self.current_map[self.player.y][self.player.x] == 5:
                    # Si estamos en el primer mapa, pasamos al segundo
                    if self.current_map is self.game_map:
                        self.current_map = self.game_map2
                        # colocar al jugador en una posición segura del nuevo mapa
                        self.player.x = 5
                        self.player.y = 5
                        self.message = "¡Nivel 2 cargado!"
                        pygame.time.wait(800)
                    else:
                        # Si ya estábamos en el mapa 2, finalizar
                        self.message = f"¡Nivel completado!"
                        pygame.time.wait(800)
                        self.state = EXIT

                self.draw_exploring()
            
            elif self.state == BATTLE:
                self.handle_battle_input(keys)
                self.draw_battle()

            # not using NEXT state anymore; map switching ocurre al pisar la salida
                
            elif self.state == EXIT:
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    game = Game()
    game.run()