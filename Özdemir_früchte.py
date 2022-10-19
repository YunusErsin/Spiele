import os
import pygame
import time
import random


class Settings():                                   # Statische Klasse
    SCREENRECT = pygame.rect.Rect(0, 0, 1000, 500)
    FPS = 60
    PATHFILE = os.path.dirname(os.path.abspath(__file__))
    PATHIMG = os.path.join(PATHFILE, "Bilder")

    staticmethod
    def get_imagepath(filename):
        return os.path.join(Settings.PATHIMG, filename)


class Bomben(pygame.sprite.Sprite):
    def __init__(self, filename, colorkey=None) -> None:
        super().__init__()
        if colorkey is None:
            self.image = pygame.image.load(Settings.get_imagepath(filename)).convert_alpha()
        else:
            self.image = pygame.image.load(Settings.get_imagepath(filename)).convert()
            self.image.set_colorkey(colorkey)

        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.vel = [0, 0]

    def update(self) -> None:
        self.rect.left += self.vel[0]
        self.rect.top += self.vel[1]
        if self.rect.right >= Settings.SCREENRECT.width or self.rect.left < 0:
            self.vel[0] *= -1
        if self.rect.bottom >= Settings.SCREENRECT.height or self.rect.top < 0:
            self.vel[1] *= -1
        return super().update()


class Game():
    def __init__(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()                                   
        self.screen = pygame.display.set_mode(Settings.SCREENRECT.size)    
        self.clock = pygame.time.Clock()                     

        self.all_bombs = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()

    

        self.background = pygame.image.load(Settings.get_imagepath("background.jpg")).convert()
        self.background = pygame.transform.scale(self.background, Settings.SCREENRECT.size)

        bombe = Bomben("bombe.png")
        bombe.rect.topleft = (0, 0)
        bombe.vel = [8, 2]
        self.all_bombs.add(bombe)

        katana = Bomben("katana.png")
        katana.rect.right = Settings.SCREENRECT.width
        katana.rect.bottom = Settings.SCREENRECT.height
        katana.vel = [-5, -4]
        self.all_bombs.add(katana)

        erdbeere = Bomben("erdbeere.png")
        erdbeere.vel = [0,0]
        erdbeere.rect.right = 500
        erdbeere.rect.bottom = 500
        self.all_obstacles.add(erdbeere)

        himbeere= Bomben("himbeere.png")
        himbeere.vel = [0,0]
        himbeere.rect.right = 300
        himbeere.rect.bottom = 500
        self.all_obstacles.add(himbeere)

        orange= Bomben("orange.png")
        orange.vel = [0,0]
        orange.rect.right = 800
        orange.rect.bottom = 100
        self.all_obstacles.add(orange)

        wassermelone= Bomben("wassermelone.png")
        wassermelone.vel = [0,0]
        wassermelone.rect.right = 500
        wassermelone.rect.bottom = 150
        self.all_obstacles.add(wassermelone)

        zitrone= Bomben("zitrone.png")
        zitrone.vel = [0,0]
        zitrone.rect.right =800
        zitrone.rect.bottom = 400
        self.all_obstacles.add(zitrone)

        
        self.last_spawn = 0
        self.running = True                                  

    def start(self):
        while self.running:                                  
            self.clock.tick(Settings.FPS)                    
            self.watch_for_events()
            self.update()
            self.draw()
            self.spawm()
            self.dissapear()

        pygame.quit()                                  

    def watch_for_events(self):
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:           
                self.running = False                     
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.all_bombs.update()
        self.all_obstacles.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_bombs.draw(self.screen)
        self.all_obstacles.draw(self.screen)
        pygame.display.flip()
    
    def spawm(self):

        direction_bombe = [1,2,5,7,8]
        direction_dynamit = [-3,-5, -9]
        

        if int(time.time()) >= self.last_spawn +1:
            bombe = Bomben("bombe.png",)
            bombe.rect.topleft = (0, 0)
            bombe.vel = [5,random.choice(direction_bombe)]
            self.all_bombs.add(bombe)

            dynamit = Bomben("katana.png")
            dynamit.rect.bottom = Settings.SCREENRECT.height
            dynamit.vel = [8, random.choice(direction_dynamit)]
            self.all_bombs.add(dynamit)

            self.last_spawn = int(time.time())


    def dissapear(self):
        for sprite in self.all_bombs.sprites():
            if pygame.sprite.spritecollideany(sprite, self.all_obstacles):
                sprite.kill()


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
