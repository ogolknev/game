'''
Определение класса настроек
'''

import pygame
from enum import Enum



class Settings():

    '''
    Класс содержащий настройки и текущую конфигурацию большинства параметров
    '''

    def __init__(self, controls: dict = None):


        self.resolution = pygame.display.list_modes()[-3]
        self.screen = pygame.display.set_mode(self.resolution)

        self.running = True

        self.FPS = 120
        self.clock = pygame.time.Clock()


        # Задание клавишного контроллера
        self.k_control = KeyControl(self, controls)


        # Задание группы для текущего обзорщика
        self.viewer_group = pygame.sprite.Group()
        # Определение тукущего обзорщика и его групп
        self.c_viewer = None

        # Доступные обзорщики (тест)
        self.available_viewers = None


class Directions(Enum):
    '''
    Возможные направлений
    '''
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class KeyControl():

    '''
    Класс содержащий назначение клавиш и методы управления ими
    '''

    def __init__(self, settings: Settings, controls: dict = None):

        # Назначение клавиш
        self.controls = {

            'move_up': pygame.K_w,
            'move_down': pygame.K_s,
            'move_left': pygame.K_a,
            'move_right': pygame.K_d,

            'fullscreen': pygame.K_F11,

            'change_viewer': pygame.K_F1,

            'quit': pygame.K_ESCAPE

        } if not controls else controls

        # Текущие настройки
        self.settings = settings


    def control(self, k_pressed, event: pygame.event.Event):

        """
        Метод общего управления
        """

        # Отслежвание единичного нажатия
        if event.type == pygame.KEYDOWN:

            if k_pressed[self.controls['fullscreen']]:
                pygame.display.toggle_fullscreen()
                self.resolution = pygame.display.Info().current_w, pygame.display.Info().current_h

            if k_pressed[self.controls['quit']]:
                self.settings.running = False

            if k_pressed[self.controls['change_viewer']]:

                if self.settings.c_viewer == self.settings.available_viewers[0]:

                    self.settings.c_viewer.target.directions = set()
                    
                    self.settings.c_viewer = self.settings.available_viewers[1]
                    
                else:

                    self.settings.c_viewer.target.directions = set()

                    self.settings.c_viewer = self.settings.available_viewers[0]

        # Отслеживание продолжительного нажатия
        pass

    def creature_control(self, creature, k_pressed, event):

        """
        Метод управления существами
        """

        # Отслеживание единичного нажатия
        if event.type == pygame.KEYDOWN:
            pass

        # Отслеживание продолжительного нажатия
        creature.directions = set()

        if k_pressed[self.controls['move_up']]:
            creature.directions.add(Directions.UP)

        if k_pressed[self.controls['move_down']]:
            creature.directions.add(Directions.DOWN)

        if k_pressed[self.controls['move_left']]:
            creature.directions.add(Directions.LEFT)

        if k_pressed[self.controls['move_right']]:
            creature.directions.add(Directions.RIGHT)
