import pygame
import random

TILE = 100
WIDTH = 1200
HEIGHT = 1200
FPS = 60

world = [ ]
cell = 1

def levels_play():
    with open('level/level.txt') as file:
        for line in file:
                line = line.rstrip()
                if line:
                    if line.startswith("LEVEL"):
                        level_num = line[6]
    return level_num

def saves(world, level):
    with open('level/level.txt', 'a') as file:
        file.write("\nLEVEL ")
        file.write(str(int(level)+1))
        file.write("\n")
        for line in world:
            str_line = list(map(str, line))
            lines = "".join(str_line)
            file.write(lines)
            file.write("\n")
        file.write("\nEND LEVEl") 

for i in range(0, WIDTH, TILE):
    line = []
    for j in range(0, HEIGHT, TILE):
        line.append(0)
    world.append(line)

running = True

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Редактор")
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos[1], event.pos[0]
                        Row, Col = mouse_x // TILE, mouse_y // TILE
                        world[Row][Col] = cell
                    elif event.button == 3:
                        mouse_x, mouse_y = event.pos[1], event.pos[0]
                        Row, Col = mouse_x // TILE, mouse_y // TILE
                        world[Row][Col] = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cell = 1
                elif event.key == pygame.K_RIGHT:
                    cell = "#"
                elif event.key == pygame.K_LSHIFT:
                    level = levels_play()
                    saves(world, level)
    
    
    screen.fill((0, 0, 0))
    
    for i in range(0, len(world)):
        for j in range(0, len(world[i])):
            x_rect, y_rect = j * TILE, i * TILE
            
            rects = pygame.Rect(x_rect, y_rect, TILE, TILE)
            if world[i][j] == 1:
                pygame.draw.rect(screen, (122, 122, 122), rects)
            elif world[i][j] == 0:
                pygame.draw.rect(screen, (122, 122, 122), rects, 1)
            elif world[i][j] == "#":
                pygame.draw.rect(screen, (255, 0, 0), rects)
            
    
    pygame.display.update()
    clock.tick(FPS)