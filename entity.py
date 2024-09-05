import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.__frame_index = 0
        self.__animation_speed = 0.15
        self.__direction = pygame.math.Vector2()

    @property
    def frame_index(self):
        return self.__frame_index

    @frame_index.setter
    def frame_index(self, value):
        self.__frame_index = value

    @property
    def _animation_speed(self):
        return self.__animation_speed

    @_animation_speed.setter
    def animation_speed(self, value):
        self.__animation_speed = value

    @property
    def _direction(self):
        return self.__direction

    @_direction.setter
    def direction(self, value):
        self.__direction = value

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # mover direita
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # mover esquerda
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # mover para baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # mover para cima
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
