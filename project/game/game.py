import os
import pygame
import sys
import random
from pathlib import Path

from .config import *
from .game_platform import Platform
from .player import Player
from .wall import Wall
from .coin import Coin

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption(TITLE)

        self.running = True

        self.clock = pygame.time.Clock()

        if getattr(sys, 'frozen', False):
            self.dir = os.path.dirname(sys.executable)
        else:
            self.dir = os.path.dirname(os.path.abspath(__file__))
        self.dir_sounds = os.path.join(self.dir, 'sources\\sounds')
        self.dir_images = os.path.join(self.dir, 'sources\\sprites')
        self.dir_music = os.path.join(self.dir, 'sources\\sounds\\music')
        self.fonts = os.path.join(self.dir, 'sources\\fonts')
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load(os.path.join(self.dir_images, 'walk\\sprite_1.png')), (16, 16)))

    def start(self):
        self.menu()
        self.new()

    def new(self):
        self.score = 0
        self.level = 0
        self.playing = True
        self.winned = False
        self.paused = False
        self.current_veloc = 0
        self.background = pygame.image.load( os.path.join(self.dir_images, 'background.png') )

        self.generate_elements()
        self.run()

    def generate_elements(self):
        self.platform = Platform()
        self.player = Player(100, self.platform.rect.top - 200, self.dir_images)

        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.sprites.add(self.platform)
        self.sprites.add(self.player)

        self.generate_walls()

    def generate_walls(self):

        last_position = WIDTH + 100

        if not len(self.walls) > 0:
            
            self.level += 1
            self.current_veloc += 0.5

            for w in range(0, MAX_WALLS):
                
                left = random.randrange(last_position + 400, last_position + 500)
                wall = Wall(left, self.platform.rect.top, self.dir_images)

                last_position = wall.rect.right 

                self.sprites.add(wall)
                self.walls.add(wall)

                if self.level > 1:
                    wall.current_vel += self.current_veloc
                    wall.veloc_x += self.current_veloc

                # if self.level == 2:
                #     wall.veloc_x += 3
                # elif self.level == 3:
                #     wall.veloc_x += 5
                # elif self.level == 4:
                #     wall.veloc_x += 7
                # elif self.level == 5:
                #     wall.veloc_x += 9

            self.generate_coins()
            self.music()

    def generate_coins(self):

        last_position = WIDTH + 100

        self.current_veloc += 0.5

        for c in range(0, MAX_COINS):
            pos_x = random.randrange(last_position + 120, last_position + 400)

            coin = Coin(pos_x, 70, self.dir_images)

            last_position = coin.rect.right

            self.sprites.add(coin)
            self.coins.add(coin)

            if self.level > 1:
                coin.current_vel += self.current_veloc
                coin.vel_x += self.current_veloc

            # if self.level == 2:
            #     coin.vel_x += 3
            # elif self.level == 3:
            #     coin.vel_x += 5
            # elif self.level == 4:
            #     coin.vel_x += 7
            # elif self.level == 5:
            #     coin.vel_x += 9

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.player.jump()

        if key[pygame.K_r] and not self.playing:
            self.new()

        if key[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
            
        
        if key[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)

        if key[pygame.K_ESCAPE]:
            self.pause()
            self.paused = True
            
        if key[pygame.K_l] and self.paused:
            self.resume()
            self.paused = False



    def draw(self):
        self.surface.blit(self.background, (0,0))

        self.sprites.draw(self.surface)

        self.draw_text()

        pygame.display.flip()

    def update(self):
        if not self.playing:
            return

        wall = self.player.collide_with(self.walls)
        if wall:
            if self.player.collide_bottom(wall):
                self.player.skid(wall)
            else:
                self.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.stop()

        if self.level > 10:
            self.win()
            pygame.mixer.music.unload()
            pygame.mixer.music.stop()

        coin = self.player.collide_with(self.coins)
        if coin:
            self.score +=1
            coin.kill()

            sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'coin.mp3'))
            sound.set_volume(0.2)
            sound.play()
            
        self.sprites.update()

        self.player.validate_platform(self.platform)

        self.update_elements(self.walls)
        self.update_elements(self.coins)

        self.generate_walls()

    def update_elements(self, elements):
        for element in elements:
            if not element.rect.right > 40:
                element.kill()

    def pause(self):
        pygame.mixer.music.pause()

        self.player.stop()
        self.stop_elements(self.walls)
        self.stop_elements(self.coins)

        self.playing = False

    def stop(self):
        sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'lose.mp3'))
        sound.play()

        self.player.stop()
        self.stop_elements(self.walls)

        self.playing = False

    def win(self):
        sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'fanfare-triumphal.mp3'))
        sound.play()

        self.player.stop()
        self.stop_elements(self.walls)

        self.winned = True
        self.playing = False

    def resume(self):
        pygame.mixer.music.unpause()

        self.player.resume()
        self.resume_elements(self.walls)
        self.resume_elements(self.coins)

        self.playing = True

    def resume_elements(self, elements):
        for element in elements:
            element.resume()

    def stop_elements(self, elements):
        for element in elements:
            element.stop()

    def score_format(self):
        return f'Score : {self.score}'

    def level_format(self):
        return f'Level : {self.level}'

    def draw_text(self):
        if self.playing:
            self.display_text( self.score_format(), 20, BLACK, WIDTH // 2, 30, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( self.level_format(), 20, BLACK, 100, TEXT_POSY, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( 'Press ESCAPE to pause', 10, BLACK, 680, 30, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( '\'9\' Volume down or \'0\' Volume up', 10, BLACK, 600, 380, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )

        if not self.playing and not self.winned and not self.paused:
            self.display_text( 'You lose...', 60, BLACK, WIDTH // 2, HEIGHT // 2, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( 'Press \'R\' to try again', 35, BLACK, WIDTH // 2, 65, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )

        if not self.playing and self.paused:
            self.display_text( self.score_format(), 20, BLACK, WIDTH // 2, 30, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( self.level_format(), 20, BLACK, 100, TEXT_POSY, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( 'Press \'L\' to continue', 35, BLACK, WIDTH // 2, 65, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( 'PAUSED', 60, BLACK, WIDTH // 2, HEIGHT // 2, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )

        if self.winned:
            self.display_text( 'You Win!', 60, BLACK, WIDTH // 2, HEIGHT // 2 + 75, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            self.display_text( f'Your score was {self.score}', 35, BLACK, WIDTH // 2, 150, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )
            if self.score <= 130 and self.score < 155:
                self.display_text( f'Poor', 50, BLACK, WIDTH // 2, 215, os.path.join(self.fonts, 'ARCADE.TTF') )
            elif self.score >= 155 and self.score < 180:
                self.display_text( f'Acceptable', 50, BLACK, WIDTH // 2, 215, os.path.join(self.fonts, 'ARCADE.TTF') )
            elif self.score >= 180 and self.score < 200:
                self.display_text( f'Master', 50, BLACK, WIDTH // 2, 215, os.path.join(self.fonts, 'ARCADE.TTF') )
            elif self.score >= 200:
                self.display_text( f'Super Pro', 50, BLACK, WIDTH // 2, 215, os.path.join(self.fonts, 'ARCADE.TTF') )
            self.display_text( 'Press \'R\' to play again', 35, BLACK, WIDTH // 2, 75, os.path.join(self.fonts, 'PressStart2P-Regular.ttf') )

    def display_text(self, text, size, color, pos_x, pos_y, font):

        letter_font = pygame.font.Font(font, size)

        text = letter_font.render(text, True, color)
        rect = text.get_rect()
        rect.midtop = (pos_x, pos_y)

        self.surface.blit(text, rect)

    def menu(self):
        self.background = pygame.image.load( os.path.join(self.dir_images, 'background.png') )
        self.surface.blit(self.background, (0,0))
        self.display_text('Welcome to', 36, BLACK, WIDTH // 2, 10, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))
        self.display_text('Snow Jumper', 80, BLUE, WIDTH // 2, 80, os.path.join(self.fonts, 'ARCADE.TTF'))
        self.display_text('Press a key to start', 36, BLACK, WIDTH // 2, 170, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))
        self.display_text('Beat level 10 to win!', 20, BLACK, WIDTH // 2, 225, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))
        self.display_text('Score Table:', 15, BLACK, WIDTH // 2, 270, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))
        self.display_text('130 or less: Poor', 15, BLACK, WIDTH // 2 - 45, 300, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))
        self.display_text('155 or less: Acceptable', 15, BLACK, WIDTH // 2, 320, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))
        self.display_text('180 or less: Master', 15, BLACK, WIDTH // 2 - 30, 340, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))
        self.display_text('200 or higher: Super Pro', 15, BLACK, WIDTH // 2 + 10, 360, os.path.join(self.fonts, 'PressStart2P-Regular.ttf'))

        pygame.display.flip()

        self.wait()

    def wait(self):
        wait = True

        while wait:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP:
                    wait = False

    def music(self):
        if self.level == 1:
            pygame.mixer.music.load(os.path.join(self.dir_music, r'12 Something in The Way.mp3'))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(0, 56.5)

        if self.level == 3:
            pygame.mixer.music.load(os.path.join(self.dir_music, r'04 Boulevard of Broken Dreams.mp3'))
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
            pygame.mixer.music.play(0, 12)

        if self.level == 5:
            pygame.mixer.music.load(os.path.join(self.dir_music, r'15 - Mothers Day.mp3'))
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
            pygame.mixer.music.play()

        if self.level == 7:
            pygame.mixer.music.load(os.path.join(self.dir_music, r'07 Territorial Pissings.mp3'))
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
            pygame.mixer.music.play(0, 85)

        if self.level == 9:
            pygame.mixer.music.load(os.path.join(self.dir_music, r'06 - Chop Suey!.mp3'))
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
            pygame.mixer.music.play(0, 150)