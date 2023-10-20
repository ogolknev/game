'''
Определение спрайтов
'''
from typing import Any
import pygame
from viewer import Viewer
from init import settings_, Directions



class Entity(pygame.sprite.Sprite):
    '''
    Родительский класс всех сущностей
    '''
    def __init__(self, texture: pygame.Surface, posx: int = 0, posy: int = 0):

        pygame.sprite.Sprite.__init__(self)

        self.image = texture
        self.rect = texture.get_rect()

        # Положение спрайта на карте
        self.posx, self.posy = posx, posy

        # Обзорщик
        self.viewer = Viewer(self, settings_.resolution)


        self.max_speed = None
        self.speedx = None
        self.speedy = None
        self.directions = None
        self.move_block = None
        self.pushed = None
        self.push = None


    def view_update(self, viewer):

        '''
        Обновление положения с учетом основного обзорщика
        '''

        # Учитывание основного обзорщика в положении спрайта на экране
        self.rect.centerx = self.posx - viewer.delta_x
        self.rect.centery = self.posy - viewer.delta_y



class Creature(Entity):

    '''
    Класс существа
    '''

    def __init__(self, texture: pygame.Surface,
                 posx: int = 0, posy: int = 0,
                 max_speed: int = 4):
        
        super().__init__(texture, posx, posy)

        self.max_speed = max_speed
        self.directions = set()

    
    def update(self, viewer, tangiables = None, *args, **kwargs):

        self.move_block = set()
        self.speedx, self.speedy = 0, 0

        def tangibility(self, tangiables):

            '''
            Функция реализующая свойство осязаемости для двигающихся сущностей. \n
            Возвращает множество заблокированных направлений {'r', 'l', 't', 'b'} и \n
            коректируюущие вертикальную и горизонтальную скорости.
            '''
            

            # Проверка есть ли в списке осязаемых предметов
            if tangiables:

                # Перебор всех осязаемых сущностей для проверки столкновения или пересечения
                for i in self.rect.collidelistall(tangiables):

                    tangiable = tangiables[i]

                    if self != tangiable:

                        self.pushed = True if self.max_speed and tangiable.max_speed and tangiable.directions else False
                        self.push = True if self.max_speed and self.directions and tangiable.max_speed else False

                        # Вычисления расстояния между центрами обозреваемой и проверяемой сущностями
                        delta_x = self.rect.centerx - tangiable.rect.centerx
                        delta_y = self.rect.centery - tangiable.rect.centery

                        # Значение амортизации для невыхода из блокировки после корректировки положения
                        amortization = 1 if not self.push else 0

                        # Определение расстояния от граней обозреваемой и проверяемой сущностями
                        right = tangiable.rect.right - self.rect.left
                        left = tangiable.rect.left - self.rect.right
                        bottom = tangiable.rect.bottom - self.rect.top
                        top = tangiable.rect.top - self.rect.bottom

                        
                        # Определение направления корректировки в зависимости от направления столкновения
                        # по горизонтали или по вертикали
                        if abs(delta_x) > abs(delta_y) and bottom > amortization and top < -amortization:

                            # Определение направления столкновения по горизонтали справа и слева
                            if delta_x > 0:
                                if not self.push: self.speedx = right - amortization
                                if not self.push: self.move_block.add('r')
                                # print(f'right: {self.speedx}')
                            
                            if delta_x < 0:
                                if not self.push: self.speedx = left + amortization
                                if not self.push: self.move_block.add('l')
                                # print(f'left: {self.speedx}')

                        elif abs(delta_x) <= abs(delta_y) and right > amortization and left < -amortization:

                            # Определение направления столкновения по вертикали снизу и сверху
                            if delta_y > 0:
                                if not self.push: self.speedy = bottom - amortization
                                if not self.push: self.move_block.add('b')
                                print(f'bottom: {self.speedy}')
                                # print(f'dx: {delta_x}')
                                # print(f'dy: {delta_y}')

                            if delta_y < 0:
                                if not self.push: self.speedy = top + amortization
                                if not self.push: self.move_block.add('t')
                                print(f'top: {self.speedy}')
                                # print(f'dx: {delta_x}')
                                # print(f'dy: {delta_y}')
                                
                return self.move_block, self.speedx, self.speedy

        self.move_block, self.speedx, self.speedy = tangibility(self, tangiables)

        # Движение существа
            
        if Directions.UP in self.directions and 'b' not in self.move_block:
            self.speedy -= self.max_speed
        if Directions.DOWN in self.directions and 't' not in self.move_block:
            self.speedy += self.max_speed
        if Directions.LEFT in self.directions and 'r' not in self.move_block:
            self.speedx -= self.max_speed
        if Directions.RIGHT in self.directions and 'l' not in self.move_block:
            self.speedx += self.max_speed


        if self.speedy < 0 and 'b' in self.move_block or self.speedy > 0 and 't' in self.move_block:
            self.speedy = 0
        if self.speedx < 0 and 'r' in self.move_block or self.speedx > 0 and 'l' in self.move_block:
            self.speedx = 0

        self.posx += self.speedx
        self.posy += self.speedy


        viewer.update(settings_.resolution)
        super().view_update(viewer=viewer)

        
        


class Barier(Entity):
    '''
    Класс барьера
    '''
    def __init__(self, texture: pygame.Surface, posx: int = 0, posy: int = 0):

        super().__init__(texture, posx, posy)


    def update(self, viewer, *args, **kwargs):

        super().view_update(viewer=viewer)




