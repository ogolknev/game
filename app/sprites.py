'''
Определение спрайтов
'''

import pygame
from settings import Settings
from viewer import Viewer
from aux_ import Directions


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

        # Начальное положение на экране без учета обзорщика
        self.rect.x = posx
        self.rect.y = posy

        self.settings = settings

        # Положение спрайта на карте
        self.posx, self.posy = posx, posy

        # Обзорщик
        self.viewer = Viewer(self, settings.resolution)

        # Физические свойства объекта
        self.speedmax = 0

        self.speedx = 0
        self.speedy = 0

        self.accelerationx = 0
        self.accelerationy = 0

        self.moveblock = set()

        self.pushed = set()
        self.push = set()

        # Направления в которых сущность пытается двигаться
        self.directions = set()


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
                 speedmax: int = 4):
        
        super().__init__(texture, settings, posx, posy)

        self.speedmax = speedmax

    
    def update(self, viewer, tangiables: list[Entity] = None, *args, **kwargs):

        # Сохранение текущих заблокированных направления и скорости перед сбросом
        self_speedx, self_speedy = self.speedx, self.speedy
        # self_accelerationx, self_accelerationy = self.accelerationx, self.accelerationy
        # print(self_speedx, self_speedy)

        # Сброс текущих заблокированных направления и скорости
        self.moveblock = set()
        self.speedx, self.speedy = 0, 0
        self.accelerationx, self.accelerationy = 0, 0
        self.push, self.pushed = set(), set()
        collide = False

        def tangibility(tangiables: list[Entity], self = self):

            '''
            Функция реализующая свойство осязаемости для двигающихся сущностей. \n
            Определяет множество заблокированных направлений {Directions.RIGHT, Directions.LEFT, Directions.UP, Directions.DOWN} и \n
            коректируюущие вертикальную и горизонтальную скорости.
            '''
            

            # Проверка есть ли в списке осязаемые сущности
            if tangiables:

                collide = False

                # Перебор всех осязаемых сущностей для проверки столкновения или пересечения
                for i in self.rect.collidelistall(tangiables):

                    tangiable = tangiables[i]

                    # Проверка на 'столкновение' с собой
                    if id(self) != id(tangiable):

                        collide = True

                        # # Определение толкающая (и)или толкаемая ли сущность
                        # if self.speedmax and (self.directions or self.pushed) and tangiable.speedmax:
                        #     self.push.add()
                        # if self.speedmax and tangiable.directions or tangiable.push:
                        #     self.pushed = True


                        # Вычисления расстояния между центрами проверяемых сущностями
                        delta_x = self.rect.centerx - tangiable.rect.centerx
                        delta_y = self.rect.centery - tangiable.rect.centery


                        # Значение амортизации для невыхода из блокировки после корректировки положения
                        amortization = -tangiable.speedmax + 1 if self.pushed and (self_speedx or self_speedy) else 1
                        if self.push and tangiable.push: amortization = 2


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

                                if self.speedmax:

                                    if Directions.RIGHT in tangiable.directions | tangiable.pushed:
                                        self.pushed.add(Directions.RIGHT)
                                    
                                    if Directions.LEFT in self.directions | self.pushed:
                                        self.push.add(Directions.LEFT)

                                # Коррекция применима только для не толкающей или толкаемой, или толкаемой в данном направлении сущности
                                if not (self.push or self.pushed) or Directions.RIGHT in self.pushed:
                                    self.speedx += right - amortization

                                # Блок применим только для не толкающей или толкаюещей пересекающейся с толкаемой сущностью
                                # на 2 амортизации в данном направлении
                                if not self.push or (self.push and self.pushed): self.moveblock.add(Directions.LEFT)
                            
                            elif delta_x < 0:

                                if self.speedmax:

                                    if Directions.LEFT in tangiable.directions | tangiable.pushed:
                                        self.pushed.add(Directions.LEFT)
                                    
                                    if Directions.RIGHT in self.directions | self.pushed:
                                        self.push.add(Directions.RIGHT)

                                if not (self.push or self.pushed) or Directions.LEFT in self.pushed:
                                    self.speedx += left + amortization

                                if not self.push or (self.push and self.pushed): self.moveblock.add(Directions.RIGHT)

                        elif abs(delta_x) <= abs(delta_y) and right > amortization and left < -amortization:

                            # Определение направления столкновения по вертикали снизу и сверху
                            if delta_y > 0:

                                if self.speedmax:

                                    if Directions.DOWN in tangiable.directions | tangiable.pushed:
                                        self.pushed.add(Directions.DOWN)
                                    
                                    if Directions.UP in self.directions | self.pushed:
                                        self.push.add(Directions.UP)

                                if not (self.push or self.pushed) or Directions.DOWN in self.pushed:
                                    self.speedy += bottom - amortization

                                if not self.push or not (self.push and self.pushed): self.moveblock.add(Directions.UP)

                            elif delta_y < 0:

                                if self.speedmax:

                                    if Directions.UP in tangiable.directions | tangiable.pushed:
                                        self.pushed.add(Directions.UP)
                                    
                                    if Directions.DOWN in self.directions | self.pushed:
                                        self.push.add(Directions.DOWN)

                                if not (self.push or self.pushed) or Directions.UP in self.pushed:
                                    self.speedy += top + amortization

                                if not self.push or not (self.push and self.pushed): self.moveblock.add(Directions.DOWN)
            return collide

        collide = tangibility(tangiables)

        # Движение существа
        if Directions.UP in self.directions:
            self.speedy -= self.speedmax
        if Directions.DOWN in self.directions:
            self.speedy += self.speedmax
        if Directions.LEFT in self.directions:
            self.speedx -= self.speedmax
        if Directions.RIGHT in self.directions:
            self.speedx += self.speedmax

        # Применение блокировки движения
        if self.speedy < 0 and Directions.UP in self.moveblock or self.speedy > 0 and Directions.DOWN in self.moveblock:
            self.speedy = 0
        if self.speedx < 0 and Directions.LEFT in self.moveblock or self.speedx > 0 and Directions.RIGHT in self.moveblock:
            self.speedx = 0

        print(' ====================================\n',
              f'id:         {str(id(self))[-3:]}\n',
              f'speed:      {self.speedx, self.speedy}\n',
              f'directions: {self.directions}\n',
              f'moveblock:  {self.moveblock}\n',
              f'pos:        {self.posx, self.posy}\n',
              f'collide:    {collide}\n',
              f'push:       {self.push}\n',
              f'pushed:     {self.pushed}\n',
              '====================================')

        # Изменение положения сущности
        self.posx += self.speedx
        self.posy += self.speedy

        # Обновление вида
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




