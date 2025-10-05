import pygame
import moviepy.editor
import time, datetime, threading
from copy import *
#Переменные
WIDTH = 1200
HEIGHT = 960
BACKGROUND_COLOR = (64, 64, 64)
VICTORY_OVERLAY_COLOR = (0, 192, 64)
DEFEAT_OVERLAY_COLOR = (205, 100, 0)

FILENAME = "level/level.txt"
TILE_SIZE = 50
FPS = 30

clock = pygame.time.Clock()

class Play:

    def __init__(self):
        pygame.init()
        self.video()
        self.music_end_event = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.music_end_event)
        self.font_button = pygame.font.SysFont('arial', 35)
        self.font_arial = pygame.font.SysFont('arial', 30)
        self.HP_font = pygame.font.SysFont('gothic', 30)
        self.font_menu = pygame.font.SysFont('arial', 50)
        self.initialize_screen()
        self.initialize_images()
        self.initialize_sound()
        self.HP_player = 20
        self.Armor_player = 100
        self.damage_polica = 5
        self.HP_polica = 20
        self.bullets = []
        self.pol_bullets = []
        self.hp_pos = 190
        self.armor_pos = 190
        self.bullet_speed = 0.1
        self.print_bomba = False
        self.defeat_polica = False
        self.levels = self.load_levels()
        self.selected_level = 1
        self.victory = False
        self.defeat = False
        self.dir = "down"
        self.move = None
        self.running = True
        self.bool_shoot = False
        self.polica_bool_shoot = False
        self.kit_bool = True
        self.music_ended = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.music_ended)
        self.sound_index = 0
        self.previous_time = pygame.time.get_ticks()
        clock.tick(FPS)

    def video(self):
        video = moviepy.editor.VideoFileClip("assets/video/large.mpg")
        video.preview()

    def initialize_screen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Бандит")
        icon = pygame.image.load("assets/image/1676683508.png")
        pygame.display.set_icon(icon)

    def initialize_images(self):
        self.wall_img = pygame.image.load("assets/image/IMG_20250216_104054_(50_x_50_пиксель).png").convert_alpha()
        self.wall_img = pygame.transform.smoothscale(self.wall_img, (TILE_SIZE, TILE_SIZE))
        self.floor_img = pygame.image.load("assets/image/IMG_20250216_104112_(50_x_50_пиксель).jpg").convert_alpha()
        self.floor_img = pygame.transform.smoothscale(self.floor_img, (TILE_SIZE, TILE_SIZE))
        self.bomba_img = pygame.image.load("assets/image/gold_PNG11000-4188514696.png").convert_alpha()
        self.bomba_img = pygame.transform.smoothscale(self.bomba_img, (TILE_SIZE, TILE_SIZE))
        self.player_up_img = pygame.image.load("assets/image/IMG_20250216_101641_(50_x_50_пиксель).png").convert_alpha()
        self.player_up_img = pygame.transform.smoothscale(self.player_up_img, (TILE_SIZE, TILE_SIZE))
        self.player_down_img = pygame.image.load("assets/image/IMG_20250216_101712_(50_x_50_пиксель).png").convert_alpha()
        self.player_down_img = pygame.transform.smoothscale(self.player_down_img, (TILE_SIZE, TILE_SIZE))
        self.player_left_img = pygame.image.load("assets/image/IMG_20250216_101658_(50_x_50_пиксель).png").convert_alpha()
        self.player_left_img = pygame.transform.smoothscale(self.player_left_img, (TILE_SIZE, TILE_SIZE))
        self.player_right_img = pygame.image.load("assets/image/IMG_20250216_101648_(50_x_50_пиксель).png").convert_alpha()
        self.player_right_img = pygame.transform.smoothscale(self.player_right_img, (TILE_SIZE, TILE_SIZE))
        self.x_img = pygame.image.load("assets/image/7462596.png").convert_alpha()
        self.x_img = pygame.transform.smoothscale(self.x_img, (TILE_SIZE, TILE_SIZE))
        self.polica_up_img = pygame.image.load("assets/image/polica_up.png").convert_alpha()
        self.polica_up_img = pygame.transform.smoothscale(self.polica_up_img, (TILE_SIZE, TILE_SIZE))
        self.polica_down_img = pygame.transform.rotate (self.polica_up_img, -180)
        self.polica_right_img = pygame.transform.rotate (self.polica_up_img, -90)
        self.polica_left_img = pygame.transform.rotate (self.polica_up_img, -270)
        self.polica_death_img = pygame.image.load("assets/image/polica_tryp.png").convert_alpha()
        self.polica_death_img = pygame.transform.smoothscale(self.polica_death_img, (TILE_SIZE, TILE_SIZE))
        self.bullet_right_img = pygame.image.load("assets/image/00e5a8660c772f2-787509045.png").convert_alpha()
        self.bullet_right_img = pygame.transform.smoothscale(self.bullet_right_img, (TILE_SIZE, TILE_SIZE))
        self.bullet_up_img = pygame.transform.rotate(self.bullet_right_img, -270)
        self.bullet_down_img = pygame.transform.rotate(self.bullet_right_img, -90)
        self.bullet_left_img = pygame.transform.rotate(self.bullet_right_img, -180)
        self.hp_img = pygame.image.load("assets/image/HP.png").convert_alpha()
        self.hp_img = pygame.transform.smoothscale(self.hp_img, (70, 70))
        self.kit_img = pygame.image.load("assets/image/kit.png").convert_alpha()
        self.kit_img = pygame.transform.smoothscale(self.kit_img, (TILE_SIZE, TILE_SIZE))
        self.shit_img = pygame.image.load("assets/image/shit.png").convert_alpha()
        self.shit_img = pygame.transform.smoothscale(self.shit_img, (30, 30))
        self.paket0_img = pygame.image.load("assets/image/paket0.png").convert_alpha()
        self.paket0_img = pygame.transform.smoothscale(self.paket0_img, (100, 100))
        self.paket1_img = pygame.image.load("assets/image/paket1.png").convert_alpha()
        self.paket1_img = pygame.transform.smoothscale(self.paket1_img, (100, 100))
        

    def initialize_sound(self):
        pygame.mixer.init()
        self.step_sound = pygame.mixer.Sound("assets/sound/medlennyiy-otchtlivyiy-korotkiy-zvuk-hodbyi-po-parketu.mp3")
        self.step_sound.set_volume(0.7)
        self.bomba_sound = pygame.mixer.Sound("assets/sound/891413a9af11a3b.mp3")
        self.bomba_sound.set_volume(0.7)
        self.shoot_sound = pygame.mixer.Sound("assets/sound/ab38330fcafc02e.mp3")
        self.shoot_sound.set_volume(0.5)
        self.pol_shoot_sound = pygame.mixer.Sound("assets/sound/shoot_pol_sound.mp3")
        self.pol_shoot_sound.set_volume(0.5)
        self.sounds = ['assets/sound/fon.mp3', 'assets/sound/veil-of-darkness_93700.mp3', 'assets/sound/fon1.mp3']
        self.kit_sound = pygame.mixer.Sound("assets/sound/kit.mp3")
        self.kit_sound.set_volume(0.7)

    def load_levels(self):
        with open(FILENAME) as file:
            levels = []
            for line in file:
                line = line.rstrip()
                if line:
                    if line.startswith("LEVEL"):
                        level = {"map": [], "player": [], "bomba": [], "polica": [], "dop_polica": []}
                    elif line.startswith("p: "):
                        x, y = map(int, line[3:].split(","))
                        level["player"].append((x, y))
                    elif line.startswith("b: "):
                            crates = line[3:].split()
                            for crate in crates:
                                x, y = map(int, crate.split(","))
                                level["bomba"].append((x, y))
                    elif line.startswith("m: "):
                        polica = line[3:].split()
                        for polic in polica:
                            x, y = map(int, polic.split(","))
                            level["polica"].append((x, y))
                    elif line.startswith("d: "):
                        dop_polica = line[3:].split()
                        for dop_polic in dop_polica:
                            dir_pol, hp_pol = map(int, dop_polic.split(","))
                            level["dop_polica"].append((dir_pol, hp_pol))
                    elif line == "END LEVEL":
                        levels.append(level)
                    else:
                        level["map"].append(line)
        return tuple(levels)
        
    def launch(self):
        pygame.mixer.music.load(self.sounds[self.sound_index])
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        self.sound_index += 1
        if self.sound_index > len(self.sounds)+1:
            self.sound_index = 0
        self.level_copy = self.copy_level()
        while self.running:
            self.handle_event()
            self.update_logic()
            self.update_screen()

    def copy_level(self):
        level_copy = deepcopy(self.levels[self.selected_level - 1])
        return level_copy

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.victory:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.selected_level < len(self.levels):
                            self.selected_level += 1
                        self.level_copy = self.copy_level()
                        self.victory = False
                        self.defeat_polica = False
                        self.kit_bool = True
                        self.hp_pos = 190
                        self.HP_player = 20
                        self.Armor_player = 100
                        self.HP_polica = 20
                        if self.print_bomba:
                            self.print_bomba = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.selected_level < len(self.levels):
                            self.selected_level += 1
                        self.level_copy = self.copy_level()
                        self.victory = False
                        self.defeat_polica = False
                        self.hp_pos = 190
                        self.HP_player = 20
                        self.Armor_player = 100
                        self.HP_polica = 20
                        if self.print_bomba:
                            self.print_bomba = False
                            
            elif self.defeat:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.level_copy = self.copy_level()
                        self.defeat = False
                        self.kit_bool = True
                        self.defeat_polica = False
                        self.hp_pos = 190
                        self.HP_player = 20
                        self.Armor_player = 100
                        self.HP_polica = 20
                        if self.print_bomba:
                            self.print_bomba = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.level_copy = self.copy_level()
                        self.defeat = False
                        self.defeat_polica = False
                        self.hp_pos = 190
                        self.HP_player = 20
                        self.Armor_player = 100
                        self.HP_polica = 20
                        if self.print_bomba:
                            self.print_bomba = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move = "up"
                    elif event.key == pygame.K_DOWN:
                        self.move = "down"
                    elif event.key == pygame.K_LEFT:
                        self.move = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.move = "right"
                    elif event.key == pygame.K_SPACE:
                        if self.bool_shoot == False:
                            self.time_shoot = time.time()
                            self.bool_shoot = True
                        if self.bool_shoot:
                            self.time_shoot_fin = time.time()
                            if self.time_shoot_fin - self.time_shoot > 0.8:
                                self.bool_shoot = False
                                self.shoot()
                        self.polica_ui()
                    elif event.key == pygame.K_q:
                        self.polica_shoot()
                    elif event.key == pygame.K_ESCAPE:
                        self.level_copy = self.copy_level()
                        self.dir = "down"
                        self.print_bomba = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y =  self.level_copy["player"][0]
                        get_player_x = self.start_x + x * TILE_SIZE
                        get_player_y = self.start_y + y * TILE_SIZE
                        if self.paytha.collidepoint((event.pos[0]-10, event.pos[1]-10)):
                            self.running = False
                        if event.pos[1]-10 < get_player_x - 50:
                            self.move = "up"
                        elif event.pos[1]-10 > get_player_x + 50:
                            self.move = "down"
                        elif event.pos[0]-10 < get_player_y - 50:
                            self.move = "left"
                        elif event.pos[0]-10 > get_player_y + 50:
                            self.move = "right"
                    elif event.button == 3:
                        if self.bool_shoot == False:
                            self.time_shoot = time.time()
                            self.bool_shoot = True
                        if self.bool_shoot:
                            self.time_shoot_fin = time.time()
                            if self.time_shoot_fin - self.time_shoot > 0.8:
                                self.bool_shoot = False
                                self.shoot()
                        self.polica_ui()
                elif event.type == self.music_ended:
                    pygame.mixer.music.load(self.sounds[self.sound_index])
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()

    def update_logic(self):
        if self.move:
            self.step_sound.play()
            if self.move == "up":
                self.dir = "up"
                self.update_move_up()
            elif self.move == "down":
                self.dir = "down"
                self.update_move_down()
            elif self.move == "left":
                self.dir = "left"
                self.update_move_left()
            elif self.move == "right":
                self.dir = "right"
                self.update_move_right()
            self.move = None
            self.check_victory()
        for bullet in self.bullets:
            if bullet["dir"] == "up":
                bullet["y"] -= self.bullet_speed
            elif bullet["dir"] == "down":
                bullet["y"] += self.bullet_speed
            elif bullet["dir"] == "left":
                bullet["x"] -= self.bullet_speed
            elif bullet["dir"] == "right":
                bullet["x"] += self.bullet_speed
        self.bullets = [bullet for bullet in self.bullets if 0 <= bullet["x"] < len(self.level_copy["map"][self.selected_level]) and 0 <= bullet["y"] < len(self.level_copy["map"])]

        for pol_bullet in self.pol_bullets:
            if pol_bullet["dir"] == "up":
                pol_bullet["y"] -= self.bullet_speed
            elif pol_bullet["dir"] == "right":
                pol_bullet["x"] += self.bullet_speed
            elif pol_bullet["dir"] == "down":
                pol_bullet["y"] += self.bullet_speed
            elif pol_bullet["dir"] == "left":
                pol_bullet["x"] -= self.bullet_speed
        self.pol_bullets = [pol_bullet for pol_bullet in self.pol_bullets if 0 <= pol_bullet["x"] < len(self.level_copy["map"][0]) and 0 <= pol_bullet["y"] < len(self.level_copy["map"])]
        
        self.bullet_collisions()

    def bullet_collisions(self):
        id = len(self.level_copy["dop_polica"])

        for bullet in self.bullets:
            x, y = int(round(bullet["x"], 0)), int(round(bullet["y"], 0))
            if self.level_copy["map"][y][x] == "#":
                self.bullets.remove(bullet)
            for i in range(0, len(self.level_copy["polica"])):
                if (x, y) == self.level_copy["polica"][i]:
                    self.dir_pol, self.hp_pol = self.level_copy["dop_polica"][i]
                    self.hp_pol -= 5
                    self.level_copy["dop_polica"].pop(i)
                    self.level_copy["dop_polica"].insert(i, (self.dir_pol, self.hp_pol))
            if (x, y) in self.level_copy["polica"]:
                self.bullets.remove(bullet)
                if self.HP_polica > 0:
                    self.HP_polica -= 3
                elif self.HP_polica <= 0:
                    self.defeat_polica = True
                    

        for pol_bullet in self.pol_bullets:
            pol_x, pol_y = int(round(pol_bullet["x"], 0)), int(round(pol_bullet["y"], 0))
            pos_pol = (pol_x, pol_y)
            if self.level_copy["map"][pol_y][pol_x] == "#":
                self.pol_bullets.remove(pol_bullet)
            elif pos_pol == self.level_copy["player"][0]:
                armor = self.Armor_player
                damage_armor = armor / 125
                self.Armor_player -= damage_armor * 100
                damage_in_player = 1 - damage_armor
                self.HP_player -= self.damage_polica * damage_in_player
                self.hp_pos -= self.damage_polica * damage_in_player * 8
                self.pol_bullets.remove(pol_bullet)
                self.check_defeat()
            

    def update_move_up(self):
        x, y = self.level_copy["player"][0]
        if self.level_copy["map"][y - 1][x] in ["-", "X", "%"] and (x, y - 1) not in self.level_copy["polica"]:
            if not ((x, y - 1) in self.level_copy["bomba"] and self.print_bomba):
                self.level_copy["player"].pop()
                self.level_copy["player"].append((x, y - 1))
        self.check_bomba()
        self.check_kit()

    def update_move_down(self):
        x, y = self.level_copy["player"][0]
        if self.level_copy["map"][y + 1][x] in ["-", "X", "%"] and (x, y + 1) not in self.level_copy["polica"]:
            if not ((x, y + 1) in self.level_copy["bomba"] and self.print_bomba):
                self.level_copy["player"].pop()
                self.level_copy["player"].append((x, y + 1))
        self.check_bomba()
        self.check_kit()

    def update_move_left(self):
        x, y = self.level_copy["player"][0]
        if self.level_copy["map"][y][x - 1] in ["-", "X", "%"] and (x - 1, y) not in self.level_copy["polica"]:
            if not ((x - 1, y) in self.level_copy["bomba"] and self.print_bomba):
                self.level_copy["player"].pop()
                self.level_copy["player"].append((x - 1, y))
        self.check_bomba()
        self.check_kit()

    def update_move_right(self):
        x, y = self.level_copy["player"][0]
        if self.level_copy["map"][y][x + 1] in ["-", "X", "%"] and (x + 1, y) not in self.level_copy["polica"]:
            if not ((x + 1, y) in self.level_copy["bomba"] and self.print_bomba):
                self.level_copy["player"].pop()
                self.level_copy["player"].append((x + 1, y))
        self.check_bomba()
        self.check_kit()

    def check_kit(self):
        x, y = self.level_copy["player"][0]
        if self.level_copy["map"][y][x] in "%":
            self.HP_player += 15
            self.hp_pos += 150
            if self.hp_pos > 190:
                self.hp_pos = 190
            if self.HP_player > 20:
                self.HP_player = 20
            if self.kit_bool:
                self.kit_sound.play()
            self.kit_bool = False

    def polica_ui(self):
        if len(self.level_copy["polica"]) > 0:
            player_x, player_y = self.level_copy["player"][0]
            for i in range(0, len(self.level_copy["polica"])):
                polica_x, polica_y = self.level_copy["polica"][i]
                dir_pol, hp_pol = self.level_copy["dop_polica"][i]
                if hp_pol > 0:
                    if player_x == polica_x or player_y == polica_y:
                        if self.polica_bool_shoot == False:
                            self.polica_shoot_time_nach = time.time()
                            self.polica_bool_shoot = True
                        if self.polica_bool_shoot:
                            self.polica_shoot_time_fin = time.time()
                            if self.polica_shoot_time_fin - self.polica_shoot_time_nach > 0.4:
                                self.polica_bool_shoot = False
                                self.polica_shoot(i)
                    
    def shoot(self):
        if self.bool_shoot == False:
            self.time_shoot = time.time()
            self.bool_shoot = True
        x, y = self.level_copy["player"][0]
        if self.dir == "up":
            bullet_dir = "up"
        elif self.dir == "down":
            bullet_dir = "down"
        elif self.dir == "left":
            bullet_dir = "left"
        elif self.dir == "right":
            bullet_dir = "right"

        self.bullets.append({"x": x, "y": y, "dir": bullet_dir})
        self.shoot_sound.play()

    def polica_shoot(self, count):
        positions = self.level_copy["polica"][count]
        x, y = positions
        dopolnutelno = self.level_copy["dop_polica"][count]
        dir, hp_polica = dopolnutelno
        if dir == 1:
            dir_clovo = "up"
        elif dir == 2:
            dir_clovo = "right"
        elif dir == 3:
            dir_clovo = "down"
        elif dir == 4:
            dir_clovo = "left"
                
        self.pol_bullets.append({"x": x, "y": y, "dir": dir_clovo})
        self.pol_shoot_sound.play()
            
    def check_bomba(self):
        x, y = self.level_copy["player"][0]
        if (x, y) in self.level_copy["bomba"] and not self.print_bomba:
            self.print_bomba = True
            self.level_copy["bomba"].remove((x, y))
            self.bomba_sound.play()
        if self.level_copy["map"][y][x] == "X" and self.print_bomba:
            self.print_bomba = False
            self.bomba_sound.play()
            self.level_copy["bomba"].append((x, y))
            self.move_ot_bomba()
        self.text_bomba()

    def move_ot_bomba(self):
        x, y = self.level_copy["player"][0]
        if self.level_copy["map"][y - 1][x] in ["-", "X"] and (x, y - 1) not in self.level_copy["polica"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x, y - 1))
        elif self.level_copy["map"][y + 1][x] in ["-", "X"] and (x, y + 1) not in self.level_copy["polica"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x, y + 1))
        elif self.level_copy["map"][y][x - 1] in ["-", "X"] and (x - 1, y) not in self.level_copy["polica"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x - 1, y))
        elif self.level_copy["map"][y][x + 1] in ["-", "X"] and (x + 1, y) not in self.level_copy["polica"]:
            self.level_copy["player"].pop()
            self.level_copy["player"].append((x + 1, y))

    def text_bomba(self):
        if not self.print_bomba:
            text_bomba = self.font_arial.render('Подбири золото', True, (0, 0, 255))
        else:
            text_bomba = self.font_arial.render('Отнеси на отмеченное место золото', True, (0, 0, 255))
        self.screen.blit(text_bomba, (WIDTH // 2, 0))
    
    def check_victory(self):
        self.victory = True
        for y in range(len(self.level_copy["map"])):
            for x in range(len(self.level_copy["map"][y])):
                if self.level_copy["map"][y][x] == 'X' and (x, y) not in self.level_copy["bomba"]:
                    self.victory = False

    def check_defeat(self):
        self.defeat = True
        if self.HP_player >= 0:
            self.defeat = False

    def update_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.update_game_screen()
        if self.victory:
            self.draw_victory_overlay()
        elif self.defeat:
            self.draw_defeat_overlay()
        pygame.display.flip()

    def update_game_screen(self):
        self.draw_game_board()
        self.print_level()
        self.text_bomba()
        self.polica_ui()

    def draw_game_board(self):
        rows =  len(self.level_copy["map"])
        self.start_x = (WIDTH - max(len(line) for line in self.level_copy["map"]) * TILE_SIZE) // 2 
        self.start_y = (HEIGHT - rows * TILE_SIZE) // 2
        i, j, n, i1= 0, 0, -1, 0
        for y in range(self.start_y, self.start_y + rows * TILE_SIZE, TILE_SIZE):
            colums = len(self.level_copy["map"][j])
            for x in range(self.start_x, self.start_x + colums * TILE_SIZE, TILE_SIZE):
                s = self.level_copy["map"][j][i]
                if s == "#":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.wall_img, (x, y))
                elif s == "-":
                    self.screen.blit(self.floor_img, (x, y))
                elif s == "X":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.x_img, (x, y))
                elif s == "%":
                    if self.kit_bool:
                        self.screen.blit(self.floor_img, (x, y))
                        self.screen.blit(self.kit_img, (x, y))
                    else:
                        self.screen.blit(self.floor_img, (x, y))
                if (i, j) in self.level_copy["player"]:
                    if self.dir == "up":
                        self.screen.blit(self.player_up_img, (x, y))
                    elif self.dir == "down":
                        self.screen.blit(self.player_down_img, (x, y))
                    elif self.dir == "left":
                        self.screen.blit(self.player_left_img, (x, y))
                    elif self.dir == "right":
                        self.screen.blit(self.player_right_img, (x, y))
                if (i, j) in self.level_copy["bomba"]:
                    self.screen.blit(self.bomba_img, (x, y))
                if (i, j) in self.level_copy["polica"]:
                    self.dir_pol, self.hp_pol = self.level_copy["dop_polica"][i1]
                    i1 += 1
                    if self.hp_pol > 0:
                        if self.dir_pol == 1:
                            self.screen.blit(self.polica_up_img, (x, y))
                        elif self.dir_pol == 2:
                            self.screen.blit(self.polica_right_img, (x, y))
                        elif self.dir_pol == 3:
                            self.screen.blit(self.polica_down_img, (x, y))
                        elif self.dir_pol == 4:
                            self.screen.blit(self.polica_left_img, (x, y))
                    else:
                        self.screen.blit(self.polica_death_img, (x, y))
                            
                i += 1
            i = 0
            j += 1
        i1 = 0

        text_HP_player = self.HP_font.render("HP:", True, (255, 0, 0))
        self.screen.blit(text_HP_player, (10, 10))
        hp_edging = pygame.Rect((10, 30), (200, 50))
        pygame.draw.rect(self.screen, (255, 0, 0), hp_edging, 5)
        hp_bar = pygame.Rect((15, 35), (round(self.hp_pos, 0), 40))
        pygame.draw.rect(self.screen, (255, 0, 0), hp_bar)
        self.paytha = pygame.Rect((1100, 0, 100, 50))
        pygame.draw.rect(self.screen, (0, 255, 255), self.paytha)
        text_Paytha = self.font_button.render('Выход', True, (1, 1, 1))
        self.screen.blit(text_Paytha, (1100, 0))
        self.screen.blit(self.hp_img, (210, 20))
        text_armor_player = self.HP_font.render("Броня:", True, (155, 155, 155))
        self.screen.blit(text_armor_player, (10, 90))
        armor_edging = pygame.Rect((10, 110), (200, 50))
        pygame.draw.rect(self.screen, (155, 155, 155), armor_edging, 5)
        armor_bar = pygame.Rect((15, 115), (round(self.Armor_player*1.9, 0), 40))
        pygame.draw.rect(self.screen, (155, 155, 155), armor_bar)
        self.screen.blit(self.shit_img, (230, 120))
        if not self.print_bomba:
            self.screen.blit(self.paket0_img, (WIDTH-100, HEIGHT-100))
        else:
            self.screen.blit(self.paket1_img, (WIDTH-100, HEIGHT-100))
        
        
            
        for bullet in self.bullets:
            if self.bullets[0]['dir'] == "up":
                bullet_x = self.start_x + bullet["x"] * TILE_SIZE
                bullet_y = self.start_y + bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_up_img, (bullet_x, bullet_y))
            elif self.bullets[0]['dir'] == "down":
                bullet_x = self.start_x + bullet["x"] * TILE_SIZE
                bullet_y = self.start_y + bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_down_img, (bullet_x, bullet_y))
            elif self.bullets[0]['dir'] == "left":
                bullet_x = self.start_x + bullet["x"] * TILE_SIZE
                bullet_y = self.start_y + bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_left_img, (bullet_x, bullet_y))
            elif self.bullets[0]['dir'] == "right":
                bullet_x = self.start_x + bullet["x"] * TILE_SIZE
                bullet_y = self.start_y + bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_right_img, (bullet_x, bullet_y))

        for pol_bullet in self.pol_bullets:
            if self.pol_bullets[0]['dir'] == 'up':
                pol_bullet_x = self.start_x + pol_bullet["x"] * TILE_SIZE
                pol_bullet_y = self.start_y + pol_bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_up_img, (pol_bullet_x, pol_bullet_y))
            elif self.pol_bullets[0]['dir'] == 'right':
                pol_bullet_x = self.start_x + pol_bullet["x"] * TILE_SIZE
                pol_bullet_y = self.start_y + pol_bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_right_img, (pol_bullet_x, pol_bullet_y))
            elif self.pol_bullets[0]['dir'] == 'down':
                pol_bullet_x = self.start_x + pol_bullet["x"] * TILE_SIZE
                pol_bullet_y = self.start_y + pol_bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_down_img, (pol_bullet_x, pol_bullet_y))
            elif self.pol_bullets[0]['dir'] == 'left':
                pol_bullet_x = self.start_x + pol_bullet["x"] * TILE_SIZE
                pol_bullet_y = self.start_y + pol_bullet["y"] * TILE_SIZE
                self.screen.blit(self.bullet_left_img, (pol_bullet_x, pol_bullet_y))

    def print_level(self):
        pass

    def draw_victory_overlay(self):
        self.screen.fill(VICTORY_OVERLAY_COLOR)
        text_menu = self.font_menu.render('Уровень закончен ты выйграл. Нажми ENTER', True, (0, 255, 255))
        self.screen.blit(text_menu, (WIDTH // 4, HEIGHT // 2))

    def draw_defeat_overlay(self):
        self.screen.fill(DEFEAT_OVERLAY_COLOR)
        text_menu = self.font_menu.render('Ты проиграл. Нажми ENTER', True, (0, 255, 255))
        self.screen.blit(text_menu, (WIDTH // 4, HEIGHT // 2))

    def __del__(self):
        pygame.quit()

def main():
    game = Play()
    game.launch()

if __name__ == "__main__":
    main()
