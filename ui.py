import pygame
from settings import *

class UI:
    def __init__(self):

        # geral
        self.__display_surface = pygame.display.get_surface()
        self.__font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # configuração de barra
        self.__health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.__energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # converte arma em dicionário
        self.__weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pygame.image.load(path).convert_alpha()
            self._weapon_graphics.append(weapon)

        # converte mágica em dicionário
        self.__magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic["graphic"]).convert_alpha()
            self._magic_graphics.append(magic)

    @property
    def _display_surface(self):
        return self.__display_surface

    @_display_surface.setter
    def _display_surface(self, value):
        self.__display_surface = value

    @property
    def _font(self):
        return self.__font

    @_font.setter
    def _font(self, value):
        self.__font = value

    @property
    def _health_bar_rect(self):
        return self.__health_bar_rect

    @_health_bar_rect.setter
    def _health_bar_rect(self, value):
        self.__health_bar_rect = value

    @property
    def _energy_bar_rect(self):
        return self.__energy_bar_rect

    @_energy_bar_rect.setter
    def _energy_bar_rect(self, value):
        self.__energy_bar_rect = value

    @property
    def _weapon_graphics(self):
        return self.__weapon_graphics

    @_weapon_graphics.setter
    def _weapon_graphics(self, value):
        self.__weapon_graphics = value

    def get_weapon_graphics(self):
        return self.weapon_graphics

    def set_weapon_graphics(self, value):
        self.weapon_graphics = value

    @property
    def _magic_graphics(self):
        return self.__magic_graphics

    @_magic_graphics.setter
    def _magic_graphics(self, value):
        self.__magic_graphics = value

    def get_magic_graphics(self):
        return self.magic_graphics

    def set_magic_graphics(self, value):
        self.magic_graphics = value

    def show_bar(self, current, max_amount, bg_rect, color):

        pygame.draw.rect(self._display_surface, UI_BG_COLOR, bg_rect)

        # estatística em pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # desenhando a barra
        pygame.draw.rect(self._display_surface, color, current_rect)
        pygame.draw.rect(self._display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self._font.render(str(int(exp)), False, TEXT_COLOR)
        x = self._display_surface.get_size()[0] - 20
        y = self._display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self._display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self._display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self._display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3
        )

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self._display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self._display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self._display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self._weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self._display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 635, has_switched)
        magic_surf = self._magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self._display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats["health"], self._health_bar_rect, HEALTH_COLOR
        )
        self.show_bar(
            player.energy, player.stats["energy"], self._energy_bar_rect, ENERGY_COLOR
        )

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
