'''
Определение спрайтов
'''

import pygame
from settings import Directions, Settings
from viewer import Viewer



class Entity(pygame.sprite.Sprite):
    '''
    Родительский класс всех сущностей
    '''
    def __init__(self, texture: pygame.Surface,
                 settings: Settings,
                 posx: int = 0, posy: int = 0):

        pygame.sprite.Sprite.__init__(self)

        self.image = texture
        self.rect = texture.get_rect()

        self.settings = settings

        # Положение спрайта на карте
        self.posx, self.posy = posx, posy

        # Обзорщик
        self.viewer = Viewer(self, settings.resolution)


        self.max_speed = 0
        self.speedx = 0
        self.speedy = 0
        self.directions = set()
        self.move_block = set()
        self.pushed = False
        self.push = False


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
                 settings: Settings,
                 posx: int = 0, posy: int = 0,
                 max_speed: int = 4):
        
        super().__init__(texture, settings, posx, posy)

        self.move_block = set()
        self.max_speed = max_speed
        self.directions = set()

    
    def update(self, viewer, tangiables: list[Entity] = None, *args, **kwargs):

        # Сохранение текущих заблокированных направления и скорости перед сбросом
        self_move_block = self.move_block
        self_speedx, self_speedy = self.speedx, self.speedy

        # Сброс текущих заблокированных направления и скорости
        self.move_block = set()
        self.speedx, self.speedy = 0, 0
        self.push, self.pushed = False, False

        def tangibility(tangiables: list[Entity], self = self):

            '''
            Функция реализующая свойство осязаемости для двигающихся сущностей. \n
            Определяет множество заблокированных направлений {'r', 'l', 't', 'b'} и \n
            коректируюущие вертикальную и горизонтальную скорости.
            '''
            

            # Проверка есть ли в списке осязаемые сущности
            if tangiables:

                # Перебор всех осязаемых сущностей для проверки столкновения или пересечения
                for i in self.rect.collidelistall(tangiables):

                    tangiable = tangiables[i]

                    # Проверка на 'столкновение' с собой
                    if id(self) != id(tangiable):

                        # Определение толкающая (и)или толкаемая ли сущность
                        if self.max_speed and (self.directions or self.pushed) and tangiable.max_speed:
                            self.push = True
                        if self.max_speed and tangiable.push:
                            self.pushed = True
                        
                        if self.push or self.pushed:
                            print(f'{str(id(self))[-3:]}: {'push' if self.push else 'pushed'}\n')

                        # Вычисления расстояния между центрами проверяемых сущностями
                        delta_x = self.rect.centerx - tangiable.rect.centerx
                        delta_y = self.rect.centery - tangiable.rect.centery


                        # Значение амортизации для невыхода из блокировки после корректировки положения
                        amortization = -tangiable.max_speed + 1 if self.pushed and (self_speedx or self_speedy) else 1
                        if self.push and tangiable.push: amortization = 0


                        # Определение расстояния от граней обозреваемой и проверяемой сущностями
                        right = tangiable.rect.right - self.rect.left
                        left = tangiable.rect.left - self.rect.right
                        bottom = tangiable.rect.bottom - self.rect.top
                        top = tangiable.rect.top - self.rect.bottom

                        
                        # Определение направления корректировки в зависимости от направления столкновения
                        # по горизонтали или по вертикали
                        if abs(delta_x) > abs(delta_y):

                            # Определение направления столкновения по горизонтали справа и слева
                            if delta_x > 0:

                                # Коррекция применима только для не толкающей или толкаемой, или толкаемой в данном направлении сущности
                                if not (self.push or self.pushed) or self.pushed and Directions.RIGHT in tangiable.directions:
                                    self.speedx = right - amortization
                                # Блок применим только для не толкающей или толкаюещей пересекающейся с толкаемой сущностью
                                # на 2 амортизации в данном направлении
                                if not self.push or right > 2 * amortization: self.move_block.add('r')
                            
                            elif delta_x < 0:
                                if not (self.push or self.pushed) or self.pushed and Directions.LEFT in tangiable.directions:
                                    self.speedx = left + amortization
                                if not self.push or left < 2 * -amortization: self.move_block.add('l')

                        elif abs(delta_x) <= abs(delta_y):

                            # Определение направления столкновения по вертикали снизу и сверху
                            if delta_y > 0:
                                if not (self.push or self.pushed) or self.pushed and Directions.DOWN in tangiable.directions:
                                    self.speedy = bottom - amortization
                                if not self.push or bottom > 2 * amortization: self.move_block.add('b')

                            elif delta_y < 0:
                                if not (self.push or self.pushed) or self.pushed and Directions.UP in tangiable.directions:
                                    self.speedy = top + amortization
                                if not self.push or top < 2 * -amortization: self.move_block.add('t')

        tangibility(tangiables)

        # Движение существа
        if Directions.UP in self.directions:
            self.speedy -= self.max_speed
        if Directions.DOWN in self.directions:
            self.speedy += self.max_speed
        if Directions.LEFT in self.directions:
            self.speedx -= self.max_speed
        if Directions.RIGHT in self.directions:
            self.speedx += self.max_speed

        # Применение блокировки движения
        if self.speedy < 0 and 'b' in self.move_block or self.speedy > 0 and 't' in self.move_block:
            self.speedy = 0
        if self.speedx < 0 and 'r' in self.move_block or self.speedx > 0 and 'l' in self.move_block:
            self.speedx = 0

        # Изменение положения сущности 
        self.posx += self.speedx
        self.posy += self.speedy


        viewer.update(self.settings.resolution)     
        super().view_update(viewer=viewer)

        
        


class Barier(Entity):
    '''
    Класс барьера
    '''
    def __init__(self, texture: pygame.Surface,
                 settings: Settings,
                 posx: int = 0, posy: int = 0):

        super().__init__(texture, settings, posx, posy)


    def update(self, viewer, *args, **kwargs):

        super().view_update(viewer=viewer)




