import pygame
import os
import random
from .config import *

class Wall(pygame.sprite.Sprite):

    def __init__(self, left, bottom, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.new_height = random.randint(110, 220)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'wall.png')), (80, bottom - self.new_height))

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom
        self.current_vel = 0

        self.veloc_x = SPEED

        self.rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1)

    def update(self):
        self.rect.left -= self.veloc_x

        self.rect_top.x = self.rect.x

    def stop(self):
        self.veloc_x = 0

    def resume(self):
        self.veloc_x = SPEED + self.current_vel