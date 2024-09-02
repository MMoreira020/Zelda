import pygame
from settings import*

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.__sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.__image = surface
        if sprite_type == 'object':
            self.__rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.__rect = self.image.get_rect(topleft = pos)
        self.__hitbox = self.rect.inflate(0, y_offset)

    @property
    def sprite_type(self):
        return self.__sprite_type

    @sprite_type.setter
    def _sprite_type(self, value):
        self.__sprite_type = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def hitbox(self):
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, value):
        self.__hitbox = value
