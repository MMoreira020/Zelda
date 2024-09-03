import pygame 

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self._sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        # gráfico
        full_path = f'weapons/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        # colocação
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left': 
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))

    @property
    def sprite_type(self):
        return self._sprite_type

    @sprite_type.setter
    def sprite_type(self, value):
        self._sprite_type = value

    def get_image(self):
        return self.image

    def set_image(self, value):
        self.image = value

    def get_rect(self):
        return self.rect

    def set_rect(self, value):
        self.rect = value
