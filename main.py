import pygame
import pygame_menu
import subprocess

WIDTH = 1200
HEIGHT = 960

pygame.init()

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

def settengs():
    pass

def start_the_game():
    subprocess.call(['python', "strelba.exe"])

menu = pygame_menu.Menu('Добро Пожаловать', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Играть', start_the_game)
menu.add.button('Меню', settengs)
menu.add.button('Выйти', pygame_menu.events.EXIT)

menu.mainloop(surface)

