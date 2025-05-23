import pygame
import random
import math

import scripts.utils.constants as c
import scripts.utils.tools as tools


class Scenery():
    def __init__(self):
        self.backgrounds = tools.get_sprites('scenery', 'background', 4, 0, 0, 512, 300)
        self.trees = tools.get_sprite('scenery', 'trees', 0, 0, 512, 300)
        self.frontleaves = tools.get_sprite('scenery', 'frontleaves', 0, 0, 512, 300)
        self.bushes = tools.get_sprite('scenery', 'bushes', 0, 0, 512, 300)
        self.tiles = math.ceil(c.SCREEN_WIDTH / 512) + 1
        self.layers = [SceneLayer(self.backgrounds[layer], index, self.tiles) for index, layer in enumerate(range(3, 0, -1))]
        self.layers.append(SceneLayer(self.trees, 4, self.tiles))
        self.layers.append(SceneLayer(self.frontleaves, 4, self.tiles))
        self.layers.append(SceneLayer(self.bushes, 5, self.tiles))
        self.speed = 1.0
        
    def update(self, speed: float):
        self.speed = speed
        if not self.speed or self.speed < 1:
            self.speed = 1.0
        [layer.update(self.speed) for layer in self.layers]

    def adjust_position(self):
        for layer in self.layers:
            layer_speed = max(1, round(self.speed * layer.speed_factor))
            layer.rect.x -= layer_speed
            if layer.rect.x < -c.SCREEN_WIDTH:
                # Reset Position
                layer.rect.x = 0

    def draw(self, screen):
        for layer in self.layers:
            # Double Image for Seamless Transition
            screen.blit(layer.image, (layer.rect.x, 0))
            screen.blit(layer.image, (layer.rect.x + c.SCREEN_WIDTH, 0))


class SceneLayer(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, layer: int, tiles: int):
        super().__init__()
        self.image = image
        self.layer = layer
        self.tiles = tiles
        self.rect = self.image.get_rect()
        self.speed_factor = self.layer * 0.1