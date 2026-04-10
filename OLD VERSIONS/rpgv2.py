"""
RPG 
Controles: Flechas para moverse, ESPACIO para interactuar/atacar
"""

import pygame
import random
import sys

from Player import Player
from Enemy import Enemy
from maps import game_map_1, game_map_2
from text import INTRO_SCREENS
from menu import show_main_menu, add_player_record
from defined import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE



# Inicialización
pygame.init()

# Configuración de pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("EN BUSCA DE LA TRIPULACIÓN PERDIDA")
clock = pygame.time.Clock()


# Estados del juego
INTRO = "intro"
EXPLORING = "exploring"
BATTLE = "battle"
DIALOGUE = "dialogue"
EXIT = "exit"
NEXT = "next"

class Game:
    def __init__(self, player_name="Héroe", difficulty=None):
        self.player_name = player_name
        self.difficulty  = difficulty or {
            "name": "Normal", "enemy_mult": 1.0,
            "player_hp": 100, "player_atk": 10, "encounter_rate": 0.15
        }
        self.state = INTRO
        self.intro_screen = 0  # Índice de la pantalla de introducción actual
        self.intro_timer = 0  # Contador para efectos de transición
        self.player = Player()

        # Aplicar configuración de dificultad al jugador
        self.player.max_hp  = self.difficulty["player_hp"]
        self.player.hp      = self.player.max_hp
        self.player.attack  = self.difficulty["player_atk"]

        self.enemy = Enemy(self.player.level)
        self.message = f"¡Bienvenido, {self.player_name}! Usa las flechas para moverte."
        self.font = pygame.font.Font(None, 24)
        self.font_big = pygame.font.Font(None, 36)
        # Caché para imágenes de las pantallas de intro (si existen archivos)
        self.loaded_intro_images = {}
        self.battle_choice = 0  # 0=Atacar, 1=Huir
        # Mapa activo (permite cambiar de nivel fácilmente)
        self.current_map = game_map_1
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
            pygame.draw.rect(screen, COLORS["GREEN"], rect)
            # Detalles de pasto (relativos a pantalla)
            for i in range(3):
                px = screen_x + random.randint(5, 25)
                py = screen_y + random.randint(5, 25)
                pygame.draw.circle(screen,COLORS["DARK_GREEN"], (px, py), 2)
                
        elif tile_type == 1:  # Árbol
            pygame.draw.rect(screen, COLORS["DARK_GREEN"], rect)
            # Tronco
            trunk = pygame.Rect(screen_x + 12, screen_y + 18, 8, 10)
            pygame.draw.rect(screen, COLORS["BROWN"], trunk)
            
        elif tile_type == 2:  # Agua
            pygame.draw.rect(screen, COLORS["BLUE"], rect)
            
        elif tile_type == 3:  # Camino
            pygame.draw.rect(screen, COLORS["LIGHT_GRAY"], rect)
            
        elif tile_type == 4:  # Casa
                 pygame.draw.rect(screen, COLORS["BROWN"], rect)
                 roof = [(screen_x, screen_y + 10),
                     (screen_x + 16, screen_y),
                     (screen_x + 32, screen_y + 10)]
                 pygame.draw.polygon(screen, COLORS["RED"], roof)

        elif tile_type == 5:  # salida
            pygame.draw.rect(screen, COLORS["DARK_BLUE"], rect)

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
        stats_text = f"{self.player_name}  |  HP: {self.player.hp}/{self.player.max_hp}  |  Nv: {self.player.level}  |  EXP: {self.player.exp}  [{self.difficulty['name']}]"
        text_surface = self.font.render(stats_text, True, COLORS["WHITE"])
        screen.blit(text_surface, (10, SCREEN_HEIGHT - 70))
        
        # Mensaje
        msg_surface = self.font.render(self.message, True, COLORS["WHITE"])
        screen.blit(msg_surface, (10, SCREEN_HEIGHT - 40))

    def draw_exploring2(self):
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
        stats_text = f"{self.player_name}  |  HP: {self.player.hp}/{self.player.max_hp}  |  Nv: {self.player.level}  |  EXP: {self.player.exp}  [{self.difficulty['name']}]"
        text_surface = self.font.render(stats_text, True, COLORS["WHITE"])
        screen.blit(text_surface, (10, SCREEN_HEIGHT - 70))
        
        # Mensaje
        msg_surface = self.font.render(self.message, True, COLORS["WHITE"])
        screen.blit(msg_surface, (10, SCREEN_HEIGHT - 40))
    
    def draw_intro(self):
        """Dibuja la pantalla de introducción"""
        screen.fill(COLORS["BLACK"])
        
        # Obtener la pantalla actual
        if self.intro_screen >= len(INTRO_SCREENS):
            self.state = EXPLORING
            return
        
        current_screen = INTRO_SCREENS[self.intro_screen]
        
        # Dibujar fondo con degradado (efecto visual)
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(20 * (1 - color_factor))
            g = int(20 * (1 - color_factor))
            b = int(40 * (1 - color_factor))
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Título
        title_font = pygame.font.Font(None, 50)
        title_surface = title_font.render(current_screen["title"], True, current_screen["color"])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        
        # Efecto de desvanecimiento
        alpha = int(255 * min(1, self.intro_timer / 30))
        # Si la pantalla tiene una imagen asociada, cargarla (una vez) y mostrarla
        if current_screen.get("image_background"):
            img_bkg_path = current_screen.get("image_background")
            img_bkg = self.loaded_intro_images.get(self.intro_screen)
            img_path = current_screen.get("image")
            img = self.loaded_intro_images.get(self.intro_screen)            
            if img_bkg or img is None:
                try:
                    img_bkg = pygame.image.load(img_bkg_path).convert_alpha()
                    img = pygame.image.load(img_path).convert_alpha()
                    # Escalar imagen a un tamaño razonable (ancho máx 400)
                    w, h = img_bkg.get_size()
                    max_w = SCREEN_HEIGHT
                    if w > max_w:
                        scale = max_w / w
                        img_bkg = pygame.transform.scale(img_bkg, (int(w * scale), int(h * scale)))
                    self.loaded_intro_images[self.intro_screen] = img_bkg
                except Exception:
                    img_bkg = None
                    img = None
            if img_bkg or img:
                try:
                    if img_bkg:
                        img_bkg.set_alpha(alpha)
                        screen.blit(img_bkg, img_bkg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
                    if img:
                        img = pygame.transform.scale(img, (int(1024/4), int(1536/4)))
                        img.set_alpha(alpha)
                        screen.blit(img, img.get_rect(center=((SCREEN_WIDTH // 2) + 152, (SCREEN_HEIGHT // 2) + 33)))
                except Exception:
                    pass
        title_surface.set_alpha(alpha)
        screen.blit(title_surface, title_rect)
        
        # Texto de la pantalla
        text_lines = current_screen["text"].split("\n")
        line_height = 50
        start_y = SCREEN_HEIGHT // 2 - (len(text_lines) * line_height) // 2
        offset_x = 0
        if current_screen.get("image_background"):
            # Offset para mover el recuadro y el texto en X
            offset_x = -100  # Cambia este valor para mover más o menos a la derecha
            # Calcula el tamaño del bocadillo según el texto
            text_surfaces = [self.font_big.render(line, True, COLORS["WHITE"]) for line in text_lines]
            max_width = max(ts.get_width() for ts in text_surfaces)
            total_height = len(text_surfaces) * line_height
            padding_x = 40
            padding_y = 20
            box_width = max_width + padding_x * 2
            box_height = total_height + 3
            box_x = (SCREEN_WIDTH - box_width) // 2 + offset_x
            box_y = 398  # Puedes ajustar esta posición según prefieras
            # Dibuja el fondo del bocadillo
            bocadillo_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, COLORS["D_GREEN"], bocadillo_rect)  # Fondo verde oscuro
            pygame.draw.rect(screen, COLORS["DARK_GREEN"], bocadillo_rect, 4)  # Borde
            start_y = box_y + padding_y


        for i, line in enumerate(text_lines):
            text_surface = self.font_big.render(line, True, COLORS["WHITE"])
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2 + offset_x, start_y + i * line_height))
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, text_rect)
        
        # Indicador de avance
        instruction_font = pygame.font.Font(None, 24)
        instruction_text = instruction_font.render(
            #f"Pantalla {self.intro_screen + 1}/{len(INTRO_SCREENS)} - Pulsa ESPACIO para continuar",
            f"Pulsa ESPACIO para continuar",
            True,
            COLORS["GRAY"]
        )
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(instruction_text, instruction_rect)
        
        # Barra de progreso
        progress = (self.intro_screen + 1) / len(INTRO_SCREENS)
        bar_width = SCREEN_WIDTH - 100
        bar_height = 10
        bar_rect = pygame.Rect(50, SCREEN_HEIGHT - 50, bar_width, bar_height)
        fill_rect = pygame.Rect(50, SCREEN_HEIGHT - 50, int(bar_width * progress), bar_height)
        
        pygame.draw.rect(screen, COLORS["WHITE"], bar_rect, 2)
        pygame.draw.rect(screen, (100, 200, 100), fill_rect)
    
    def draw_battle(self):
        """Dibuja la pantalla de batalla"""
        screen.fill(COLORS["BLACK"])
        
        # Área de batalla
        battle_bg = pygame.Rect(50, 50, SCREEN_WIDTH - 100, 200)
        pygame.draw.rect(screen, COLORS["GRAY"], battle_bg)
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
            pygame.draw.circle(screen, COLORS["RED"], (enemy_x - 10, enemy_y - 10), 8)
            pygame.draw.circle(screen, COLORS["RED"], (enemy_x + 10, enemy_y - 10), 8)
        
        # Nombre del enemigo
        enemy_name = self.font_big.render(self.enemy.name, True, COLORS["WHITE"])
        screen.blit(enemy_name, (enemy_x - 50, enemy_y - 80))
        
        # Barra de HP del enemigo
        hp_bar_width = 150
        hp_percentage = self.enemy.hp / self.enemy.max_hp
        hp_bar_rect = pygame.Rect(enemy_x - 75, enemy_y + 50, hp_bar_width, 15)
        hp_fill_rect = pygame.Rect(enemy_x - 75, enemy_y + 50, int(hp_bar_width * hp_percentage), 15)
        pygame.draw.rect(screen, COLORS["LIGHT_GRAY"], hp_bar_rect)
        pygame.draw.rect(screen, COLORS["GREEN"] if hp_percentage > 0.3 else COLORS["RED"], hp_fill_rect)
        pygame.draw.rect(screen, COLORS["WHITE"], hp_bar_rect, 2)
        
        # HP texto
        hp_text = self.font.render(f"{self.enemy.hp}/{self.enemy.max_hp}", True, COLORS["WHITE"])
        screen.blit(hp_text, (enemy_x - 30, enemy_y + 52))
        
        # Jugador (pequeño)
        player_x = 120
        player_y = 200
        pygame.draw.circle(screen, COLORS["RED"], (player_x, player_y), 25)
        
        # Barra de HP del jugador
        player_hp_bar_width = 150
        player_hp_percentage = self.player.hp / self.player.max_hp
        player_hp_bar_rect = pygame.Rect(player_x - 75, player_y + 40, player_hp_bar_width, 15)
        player_hp_fill_rect = pygame.Rect(player_x - 75, player_y + 40, int(player_hp_bar_width * player_hp_percentage), 15)
        pygame.draw.rect(screen, COLORS["LIGHT_GRAY"], player_hp_bar_rect)
        pygame.draw.rect(screen, COLORS["GREEN"] if player_hp_percentage > 0.3 else COLORS["RED"], player_hp_fill_rect)
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
        attack_color = COLORS["WHITE"] if self.battle_choice == 0 else COLORS["GRAY"]
        flee_color = COLORS["WHITE"] if self.battle_choice == 1 else COLORS["GRAY"]
        
        attack_text = self.font_big.render("ATACAR" if self.battle_choice == 0 else "ATACAR", True, attack_color)
        flee_text = self.font_big.render("HUIR" if self.battle_choice == 1 else "HUIR", True, flee_color)
        
        screen.blit(attack_text, (70, 360))
        screen.blit(flee_text, (300, 360))
        
        hint_text = self.font.render("Flechas: Seleccionar  |  ESPACIO: Confirmar", True, COLORS["GRAY"])
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
            if random.random() < self.difficulty["encounter_rate"]:
                self.enemy = Enemy(self.player.level)
                # Aplicar multiplicador de dificultad al enemigo
                mult = self.difficulty["enemy_mult"]
                self.enemy.max_hp  = int(self.enemy.max_hp  * mult)
                self.enemy.hp      = self.enemy.max_hp
                self.enemy.attack  = int(self.enemy.attack  * mult)
                self.state = BATTLE
                self.message = f"¡Un {self.enemy.name} salvaje apareció!"
                self.battle_choice = 0

    def run(self):
        """Loop principal del juego"""
        running = True
        space_pressed = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            keys = pygame.key.get_pressed()
            
            if self.state == INTRO:
                self.intro_timer += 1
                
                # Avanzar pantalla con ESPACIO
                if keys[pygame.K_SPACE]:
                    if not space_pressed:
                        self.intro_screen += 1
                        self.intro_timer = 0
                        space_pressed = True
                        pygame.time.wait(200)
                else:
                    space_pressed = False
                
                self.draw_intro()
            
            elif self.state == EXPLORING:
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
                    if self.current_map is game_map_1:
                        self.current_map = game_map_2
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
                add_player_record(self.player_name, self.player.level, self.difficulty["name"])
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    result = show_main_menu(screen)          # Menú inicial: nombre + dificultad
    game = Game(player_name=result["name"], difficulty=result["difficulty"])
    game.run()