'''
Определение обзорщика
'''
import pygame



class Viewer():
    '''
    Класс обзорщика
    '''
    def __init__(self, viewed_entity, resolution: tuple[int, int]):

        # Обозреваемая сущность
        self.target = viewed_entity

        # Смещение необозреваемых элементов относительно обзорщика
        self.delta_x = self.target.posx - resolution[0] // 2
        self.delta_y = self.target.posy - resolution[1] // 2


    def update(self, resolution: tuple[int, int]):
        '''
        Обновление смещения необозреваемых элементов относительно обзорщика
        '''
        self.delta_x = self.target.posx - resolution[0] // 2
        self.delta_y = self.target.posy - resolution[1] // 2


