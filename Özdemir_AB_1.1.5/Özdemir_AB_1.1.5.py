import os
import pygame
import random


class Settings():                                  
    SCREENRECT = pygame.rect.Rect(0, 0, 1000, 500)
    FPS = 60
    PATHFILE = os.path.dirname(os.path.abspath(__file__))
    PATHIMG = os.path.join(PATHFILE, "formen")

    @staticmethod
    def get_imagepath(filename):
        return os.path.join(Settings.PATHIMG, filename)


class objects(pygame.sprite.Sprite):
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
        self.all_test= pygame.sprite.Group()


    

        self.background = pygame.image.load(Settings.get_imagepath("background.png")).convert()
        self.background = pygame.transform.scale(self.background, Settings.SCREENRECT.size)

        kreis_1 = objects("kreis_1.png")
        kreis_1.vel = [0,0]
        kreis_1.rect.right = 900
        kreis_1.rect.bottom = 300
        self.all_obstacles.add(kreis_1)

        kreis_2 = objects("kreis_2.png")
        kreis_2.vel = [0,0]
        kreis_2.rect.right = 200
        kreis_2.rect.bottom = 200
        self.all_obstacles.add(kreis_2)


        Rechteck_1 = objects("Rechteck_1.png")
        Rechteck_1.vel = [0,0]
        Rechteck_1.rect.right = 500
        Rechteck_1.rect.bottom = 500
        self.all_obstacles.add(Rechteck_1)

        Rechteck_2 = objects("Rechteck_2.png")
        Rechteck_2.vel = [0,0]
        Rechteck_2.rect.right = 300
        Rechteck_2.rect.bottom = 500
        self.all_obstacles.add(Rechteck_2)

        zick_1 = objects("zick_1.png")
        zick_1.vel = [0,0]
        zick_1.rect.right = 800
        zick_1.rect.bottom = 100
        self.all_obstacles.add(zick_1)

        zick_2 = objects("zick_2.png")
        zick_2.vel = [0,0]
        zick_2.rect.right = 500 
        zick_2.rect.bottom = 150
        self.all_obstacles.add(zick_2)

        bombe = objects("bombe.png")
        bombe.rect.right = random.randint(200,500)
        bombe.rect.bottom = random.randint(200,500)
        self.all_bombs.add(bombe)

        bombe_2 = objects("bombe.png")
        bombe_2.vel = [0,0]
        bombe_2.rect.right = 300
        bombe_2.rect.bottom = 300
        self.all_test.add(bombe_2)


    

        self.last_spawn = 0
        self.running = True      


                              

    def start(self):
        while self.running:                                  
            self.clock.tick(Settings.FPS)                    
            self.watch_for_events()
            self.update()
            self.draw()
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
        for sprite in self.all_bombs.sprites():
                if pygame.sprite.spritecollideany(sprite, self.all_obstacles):
                    self.all_test.draw(self.screen)
                    print("neu")
        pygame.display.flip()


    def dissapear(self):
        for sprite in self.all_bombs.sprites():
            if pygame.sprite.spritecollideany(sprite, self.all_obstacles):
                sprite.kill()
                print("tot")
               

   
       

def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
