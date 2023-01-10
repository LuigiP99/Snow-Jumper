import pygame
import os
from .config import *

class Player(pygame.sprite.Sprite):

    def __init__(self, left, bottom, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.count = 0
        self.index = 0
        self.images = (
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'walk\\sprite_1.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'walk\\sprite_2.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'walk\\sprite_4.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'walk\\sprite_13.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'walk\\sprite_14.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'walk\\sprite_15.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'player_skid.png')), (100, 80)),
        )

        self.jump_images = (pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'jump\\sprite_12.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'jump\\sprite_16.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'jump\\sprite_17.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'jump\\sprite_18.png')), (100, 80)),
        pygame.transform.scale(pygame.image.load(os.path.join(dir_images, r'jump\\sprite_19.png')), (100, 80)))

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom
        self.radius = 35

        self.pos_y = self.rect.bottom
        self.veloc_y = 0

        self.can_jump = False

        self.playing = True

    def collide_with(self, sprites):
        objects = pygame.sprite.spritecollide(self, sprites, False)
        for object in objects:
            if pygame.sprite.collide_circle(self, object):
                return object # return the object that collide with the player

    def collide_bottom(self, wall):
        return self.rect.colliderect(wall.rect_top)

    def skid(self, wall):
        self.pos_y = wall.rect.top
        self.veloc_y = 0
        self.can_jump = True

        self.image = self.images[6]

    def validate_platform(self, platform):
        result = pygame.sprite.collide_rect(self, platform)
        if result:
            self.veloc_y = 0
            self.pos_y = platform.rect.top 
            self.can_jump = True

        self.count += 1
        if self.index >= len(self.images[0:5]):
            self.index = 0
        self.image = self.images[self.index]
        if self.count > 4:
            self.index += 1
            self.count = 0

    def jump(self):
        if self.can_jump:
            self.veloc_y = -22
            self.can_jump = False

        if self.veloc_y < 0:
            self.count += 1
            if self.index >= len(self.jump_images):
                self.index = 0
            self.image = self.jump_images[self.index]

            if self.count > 5:
                self.index += 1
                self.count = 0

    def update_post(self):
        self.veloc_y += PLAYER_GRAV
        self.pos_y += self.veloc_y * PLAYER_GRAV

    def update(self):
        if self.playing:
            self.update_post()

            self.rect.bottom = self.pos_y
            
    def stop(self):
        self.playing = False

    def resume(self):
        self.playing = True
