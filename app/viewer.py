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



# Задание основного обзорщика
def set_viewer(viewer: Viewer, group: pygame.sprite.Group, pre_viewer: Viewer = None, pre_groups: list[pygame.sprite.Group] = None):
    if pre_viewer:
        pre_viewer.target.kill()
        pre_viewer.target.add(pre_groups)
    c_viewer = viewer
    c_viewer_groups = viewer.target.groups()
    viewer.target.kill()
    viewer.target.add(group)
    return c_viewer, c_viewer_groups
