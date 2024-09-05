import pygame
from settings import *


class Upgrade:
    def __init__(self, player):
        self.__display_surface = pygame.display.get_surface()
        self.__player = player
        self.__attribute_nr = len(player.stats)
        self.__attribute_names = list(player.stats.keys())
        self.__max_values = list(player.max_stats.values())
        self.__font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.__height = self._display_surface.get_size()[1] * 0.8
        self.__width = self._display_surface.get_size()[0] // 6
        self.create_items()

        self.__selection_index = 0
        self.__selection_time = None
        self.__can_move = True

    @property
    def _display_surface(self):
        return self.__display_surface

    @_display_surface.setter
    def _display_surface(self, value):
        self.__display_surface = value

    @property
    def _player(self):
        return self.__player

    @_player.setter
    def _player(self, value):
        self.__player = value

    @property
    def _attribute_nr(self):
        return self.__attribute_nr

    @_attribute_nr.setter
    def _attribute_nr(self, value):
        self.__attribute_nr = value

    @property
    def _attribute_names(self):
        return self.__attribute_names

    @_attribute_names.setter
    def _attribute_names(self, value):
        self.__attribute_names = value

    @property
    def _max_values(self):
        return self.__max_values

    @_max_values.setter
    def _max_values(self, value):
        self.__max_values = value

    @property
    def _font(self):
        return self.__font

    @_font.setter
    def _font(self, value):
        self.__font = value

    @property
    def _height(self):
        return self.__height

    @_height.setter
    def _height(self, value):
        self.__height = value

    @property
    def _width(self):
        return self.__width

    @_width.setter
    def _width(self, value):
        self.__width = value

    def get_create_items(self):
        return self.create_items()

    def set_create_items(self, value):
        self.create_items()  # Corrigir aqui. Você não deve atribuir um valor ao método

    @property
    def _selection_index(self):
        return self.__selection_index

    @_selection_index.setter
    def _selection_index(self, value):
        self.__selection_index = value

    @property
    def _selection_time(self):
        return self.__selection_time

    @_selection_time.setter
    def _selection_time(self, value):
        self.__selection_time = value

    @property
    def _can_move(self):
        return self.__can_move

    @_can_move.setter
    def _can_move(self, value):
        self.__can_move = value

    def input(self):
        keys = pygame.key.get_pressed()

        if self._can_move:
            if keys[pygame.K_d] and self._selection_index < self._attribute_nr - 1:
                self._selection_index += 1
                self._can_move = False
                self._selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_a] and self._selection_index >= 1:
                self._selection_index -= 1
                self._can_move = False
                self._selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self._can_move = False
                self._selection_time = pygame.time.get_ticks()
                self._item_list[self._selection_index].trigger(self._player)

    def selection_cooldown(self):
        if not self._can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self._selection_time >= 300:
                self._can_move = True

    def create_items(self):
        self._item_list = []

        for item, index in enumerate(range(self._attribute_nr)):
            # pos horizontal
            full_width = self._display_surface.get_size()[0]
            increment = full_width // self._attribute_nr
            left = (item * increment) + (increment - self._width) // 2

            # pos vertical
            top = self._display_surface.get_size()[1] * 0.1

            item = Item(left, top, self._width, self._height, index, self._font)
            self._item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self._item_list):

            name = self._attribute_names[index]
            value = self._player.get_value_by_index(index)
            max_value = self._max_values[index]
            cost = self._player.get_cost_by_index(index)
            item.display(
                self._display_surface, self._selection_index, name, value, max_value, cost
            )

class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # título
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(
            midtop=self.rect.midtop + pygame.math.Vector2(0, 20)
        )

        cost_surf = self.font.render(f"{int(cost)}", False, color)
        cost_rect = cost_surf.get_rect(
            midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20)
        )

        # desenhar
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):

        # desenho
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # desenhar elementos
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if (
            player.exp >= player.upgrade_cost[upgrade_attribute]
            and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]
        ):
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)
