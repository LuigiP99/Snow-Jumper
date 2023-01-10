import pygame
from .config import *
import os

class Coin(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.images = (pygame.transform.scale(pygame.image.load(os.path.join(dir_images, 'Coin-1.png')), (70, 54)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'Coin-2.png')), (70, 54)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'Coin-3.png')), (70, 54)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'Coin-4.png')), (70, 54)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'Coin-5.png')), (70, 54)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'Coin-6.png')), (70, 54)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'Coin-7.png')), (70, 54)))

        self.count = 0
        self.index = 0
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.radius = 15
        self.current_vel = 0

        self.vel_x = SPEED

    def update(self):
        self.rect.left -= self.vel_x

        self.count += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        if self.count > 3:
            self.index += 1
            self.count = 0

    def stop(self):
        self.vel_x = 0
    
    def resume(self):
        self.vel_x = SPEED + self.current_vel