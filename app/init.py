'''
Инициализация pygame и применение настроек
'''

import pygame

pygame.init()

from settings import *


# Установка настроек
settings_ = Settings()

from sprites import *
from map_ import *


# Создание карты
bg_map = pygame.image.load('textures/map_bg.png')


# Создание спрайтов
players = pygame.sprite.Group()
bariers = pygame.sprite.Group()
tangiables = pygame.sprite.Group()

    
player_texture = pygame.Surface((50,50))
player_texture.fill((0,0,0))
player = Creature(player_texture, settings_, 500, 500)
player.add(players, tangiables)


barier_texture = pygame.Surface((25,25))
barier_texture.fill((0,255,255))
barier_texture.set_alpha(200)
Barier(barier_texture, settings_, 200, 200).add(bariers, tangiables)
for x in range(25, 2000, 25):
    Barier(barier_texture, settings_, x, 0).add(bariers, tangiables)
    Barier(barier_texture, settings_, x, 2000).add(bariers, tangiables)
    Barier(barier_texture, settings_, 0, x).add(bariers, tangiables)
    Barier(barier_texture, settings_, 2000, x).add(bariers, tangiables)
barier_valya_texture = pygame.Surface((50,50))
barier_valya_texture.fill((255,0,200))
barier_valya = Creature(barier_valya_texture, settings_, 600, 500)
barier_valya.add(players, tangiables)


# Задание текущего обзорщика
settings_.c_viewer = player.viewer
settings_.available_viewers = (barier_valya.viewer, player.viewer)

k_controls = {

    'move_up': pygame.K_UP,
    'move_down': pygame.K_DOWN,
    'move_left': pygame.K_LEFT,
    'move_right': pygame.K_RIGHT,

}

settings__ = Settings(k_controls)

