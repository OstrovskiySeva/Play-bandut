import pygame

TILE = 100
WIDTH = 1200
HEIGHT = 1200
FPS = 60

world = [ ]

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
    
    x_mouse, y_mouse = pygame.mouse.get_pos()
    b1, b2, b3 = pygame.mouse.get_pressed()
    
    mouseRow, mouseCol = y_mouse // TILE, x_mouse // TILE
    
    if b1:
        world[mouseRow][mouseCol] == 1
    elif b3:
        world[mouseRow][mouseCol] == 0
    
    screen.fill((0, 0, 0))
    
    for i in range(0, len(world)):
        for j in range(0, len(world[i])):
            x_rect, y_rect = j * TILE, i * TILE
            
            rects = pygame.Rect(x_rect, y_rect, TILE, TILE)
            if world[i][j] == 1:
                pygame.draw.rect(screen, (122, 122, 122), rects)
            elif world[i][j] == 0:
                pygame.draw.rect(screen, (122, 122, 122), rects, 1)
            
    
    pygame.display.update()
    clock.tick(FPS)