import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.__animation_player = animation_player
        self.__sounds = {
            'heal': pygame.mixer.Sound('som/audio/heal.wav'),
            'flame': pygame.mixer.Sound('som/audio/Fire.wav')
        }
        
    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.__sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.__animation_player.create_particles('aura', player.rect.center, groups)
            self.__animation_player.create_particles('heal', player.rect.center, groups)
    
    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.__sounds['flame'].play()
            
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0,1)
            
            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.__animation_player.create_particles('flame', (x, y), groups)
                else:  # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.__animation_player.create_particles('flame', (x, y), groups)

    @property
    def animation_player(self):
        return self.__animation_player

    @animation_player.setter
    def animation_player(self, value):
        self.__animation_player = value

    @property
    def sounds(self):
        return self.__sounds

    @sounds.setter
    def sounds(self, value):
        self.__sounds = value

    def get_sound_heal(self):
        return self.__sounds['heal']

    def set_sound_heal(self, value):
        self.__sounds['heal'] = value

    def get_sound_flame(self):
        return self.__sounds['flame']

    def set_sound_flame(self, value):
        self.__sounds['flame'] = value
