import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
    def __init__(self):
        # superfície de exibição
        self.__display_surface = pygame.display.get_surface()
        self.__game_paused = False

        # configuração do grupo de sprites
        self.__visible_sprites = YSortCameraGroup()
        self.__obstacle_sprites = pygame.sprite.Group()

        # sprites de ataque
        self.__current_attack = None
        self.__attack_sprites = pygame.sprite.Group()
        self.__attackable_sprites = pygame.sprite.Group()

        # configuração do sprite
        self.create_map()

        # interface do usuário
        self.__ui = UI()
        self.__upgrade = Upgrade(self.player)

        # particulas
        self.__animation_player = AnimationPlayer()
        self.__magic_player = MagicPlayer(self.animation_player)

        self.__saved_score = self.load_score()

    @property
    def display_surface(self):
        return self.__display_surface

    @display_surface.setter
    def display_surface(self, value):
        self.__display_surface = value

    @property
    def game_paused(self):
        return self.__game_paused

    @game_paused.setter
    def game_paused(self, value):
        self.__game_paused = value

    @property
    def visible_sprites(self):
        return self.__visible_sprites

    @visible_sprites.setter
    def visible_sprites(self, value):
        self.__visible_sprites = value

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @obstacle_sprites.setter
    def obstacle_sprites(self, value):
        self.__obstacle_sprites = value

    @property
    def current_attack(self):
        return self.__current_attack

    @current_attack.setter
    def current_attack(self, value):
        self.__current_attack = value

    @property
    def attack_sprites(self):
        return self.__attack_sprites

    @attack_sprites.setter
    def attack_sprites(self, value):
        self.__attack_sprites = value

    @property
    def attackable_sprites(self):
        return self.__attackable_sprites

    @attackable_sprites.setter
    def attackable_sprites(self, value):
        self.__attackable_sprites = value

    def get_create_map(self):
        return self.create_map()

    def set_create_map(self, value):
        self.create_map = value

    @property
    def _ui(self):
        return self.__ui

    @_ui.setter
    def _ui(self, value):
        self.__ui = value

    @property
    def upgrade(self):
        return self.__upgrade

    @upgrade.setter
    def upgrade(self, value):
        self.__upgrade = value

    @property
    def animation_player(self):
        return self.__animation_player

    @animation_player.setter
    def animation_player(self, value):
        self.__animation_player = value

    @property
    def _magic_player(self):
        return self.__magic_player

    @_magic_player.setter
    def _magic_player(self, value):
        self.__magic_player = value

    @property
    def saved_score(self):
        return self.__saved_score

    @saved_score.setter
    def saved_score(self, value):
        self.__saved_score = value

    def load_score(self):
        try:
            with open("score.txt", "r") as arq:
                score = arq.read().split(": ")[-1]
                return int(score)
        except (IOError, ValueError) as e:
            print(f"Erro ao carregar o score: {e}")
            return 0

    def pontuacao(self):
        """Exibe o score do jogador na tela."""
        font = pygame.font.Font(None, 40)
        score_surface = font.render(
            f"Score do jogador: {self.player.exp}", True, (255, 255, 255)
        )
        score_rect = score_surface.get_rect(
            center=(
                self.display_surface.get_width() // 2,
                self.display_surface.get_height() // 2,
            )
        )

        overlay = pygame.Surface(self.display_surface.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.display_surface.blit(overlay, (0, 0))

        self.display_surface.blit(score_surface, score_rect)
        pygame.display.update()

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def save_score(self):
        """Salva o score do jogador em um arquivo."""
        try:
            with open("score.txt", "w") as arq:
                arq.write(f"Score do jogador: {self.player.exp}")
                self.saved_score = self.player.exp
        except IOError as e:
            print(f"Erro ao salvar o score: {e}")

    def create_map(self):
        layouts = {
            "boundary": import_csv_layout("map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("map/map_Grass.csv"),
            "object": import_csv_layout("map/map_LargeObjects.csv"),
            "entities": import_csv_layout("enemy/map_Entities.csv"),
        }
        graphics = {
            "grass": import_folder("graphics/tilemap/grass"),
            "objects": import_folder("graphics/tilemap/objects"),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile(
                                (x, y),
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites,
                                ],
                                "grass",
                                random_grass_image,
                            )

                        if style == "object":
                            surf = graphics["objects"][int(col)]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                surf,
                            )

                        if style == "entities":
                            if col == "394":
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                )
                            else:
                                if col == "390":
                                    monster_name = "bamboo"
                                elif col == "391":
                                    monster_name = "spirit"
                                elif col == "392":
                                    monster_name = "raccoon"
                                else:
                                    monster_name = "squid"
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_xp,
                                )

    def reset_level(self):

        self.save_score()

        self.player.exp = 0

        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.attack_sprites.empty()
        self.attackable_sprites.empty()

        self.create_map()

        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_attack(self):

        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites]
        )

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self._magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "flame":
            self._magic_player.flame(
                self.player, cost, [self.visible_sprites, self.attack_sprites]
            )

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset, [self.visible_sprites]
                                )
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type
                            )

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(
                attack_type, self.player.rect.center, [self.visible_sprites]
            )

            if self.player.health <= 0:
                self.pontuacao()
                self.reset_level()

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_xp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self._ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pontuacao()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # setup geral
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__half_width = self._display_surface.get_size()[0] // 2
        self.__half_height = self._display_surface.get_size()[1] // 2
        self.__offset = pygame.math.Vector2()

        # croação do pisp
        self.__floor_surf = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.__floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    @property
    def _display_surface(self):
        return self.__display_surface

    @_display_surface.setter
    def _display_surface(self, value):
        self.__display_surface = value

    @property
    def _half_width(self):
        return self.__half_width

    @_half_width.setter
    def _half_width(self, value):
        self.__half_width = value

    @property
    def _half_height(self):
        return self.__half_height

    @_half_height.setter
    def _half_height(self, value):
        self.__half_height = value

    @property
    def _offset(self):
        return self.__offset

    @_offset.setter
    def _offset(self, value):
        self.__offset = value

    @property
    def floor_surf(self):
        return self.__floor_surf

    @floor_surf.setter
    def floor_surf(self, value):
        self.__floor_surf = value

    @property
    def floor_rect(self):
        return self.__floor_rect

    @floor_rect.setter
    def floor_rect(self, value):
        self.__floor_rect = value

    def custom_draw(self, player):

        
        self._offset.x = player.rect.centerx - self._half_width
        self._offset.y = player.rect.centery - self._half_height

        
        floor_offset_pos = self.floor_rect.topleft - self._offset
        self._display_surface.blit(self.floor_surf, floor_offset_pos)

    
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self._offset
            self._display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
