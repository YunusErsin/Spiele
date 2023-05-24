import pygame
pygame.init()

class Settings:
    Breite = 900
    Hoehe = 600
    FPS = 60
    Window = pygame.display.set_mode((Breite, Hoehe))
    pygame.display.set_caption("Clapy")
    Punkte_zum_gewinnen = 7

class Farben:
    ROT = (255, 0, 0)
    Schwarz = (0, 0, 0)
    WEIß = (255,255,255)
 
Text = pygame.font.SysFont("Arial", 50)   

class Schlaeger:
    Schlaeger_breite  = 10
    Schlaeger_hoehe = 100
    Farbe_schlaeger = Farben.ROT
    geschwindigkeit_schlaeger = 8

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, window):
        pygame.draw.rect(window, self.Farbe_schlaeger, (self.x, self.y, self.width, self.height))

    def bewegung(self, hoch=True):
        if hoch:
            self.y -= self.geschwindigkeit_schlaeger # wenn y hoch geht, geht der Schläger runter
        else:
            self.y += self.geschwindigkeit_schlaeger

class Ball:
    
    BALL_RADIUS = 5
    geschwindigkeit_ball = 10
    Farbe_ball = Farben.WEIß

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_geschwindigkeit = self.geschwindigkeit_ball
        self.y_geschwindigkeit = 0

    def draw(self, win):
        pygame.draw.circle(win, self.Farbe_ball, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_geschwindigkeit
        self.y += self.y_geschwindigkeit

    def ball_anfang(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_geschwindigkeit = 0
        self.x_geschwindigkeit *= -1


def draw(window, linker_schläger, rechter_schläger, ball, punkte_links, punkte_rechts):
    window.fill(Farben.Schwarz)

    punktestand_links = Text.render(f"{punkte_links}", 1, Farben.ROT)   
    punktestand_rechts = Text.render(f"{punkte_rechts}", 1, Farben.ROT)
    window.blit(punktestand_links, (Settings.Breite//4 - punktestand_links.get_width()//2, 20))  # position
    window.blit(punktestand_rechts, (Settings.Breite * (3/4) - punktestand_rechts.get_width()//2, 20))
    
    linker_schläger.draw(window)
    rechter_schläger.draw(window)
    ball.draw(window)
    pygame.display.update()




def collision(ball, linker_schläger, rechter_schläger):
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= Settings.Hoehe: # radius damit die kanten vom ball erkannt werden, *= -1 ist richtung veränderung, fur oben und unten rand
        ball.y_geschwindigkeit *= -1 #ändert richtung

    if ball.x_geschwindigkeit < 0: # ball bewegt sich nach links, also wird die collision mit den linke schläger geprüft
        if ball.y + ball.radius >= linker_schläger.y and ball.y - ball.radius <= linker_schläger.y + linker_schläger.height:
            if ball.x - ball.radius <= linker_schläger.x + linker_schläger.width:  # x ist die linke kante vom linken schläger, + die breite vom linken schläger, - radius weil man nach links geh
                ball.x_geschwindigkeit *= -1 #ändert richtung
                ball.y_geschwindigkeit = (ball.y - (linker_schläger.y + linker_schläger.height / 2)) / (linker_schläger.height / 2) * ball.geschwindigkeit_ball  # der ball prallt in verschiedenen richtungen ab
     
    else:  # ball bewegt sich nach rechts, kollision mit rechten schläger wird geprüft
        if ball.y + ball.radius >= rechter_schläger.y and ball.y - ball.radius <= rechter_schläger.y + rechter_schläger.height:
            if ball.x + ball.radius >= rechter_schläger.x: # x ist die linke kante vom rechtn schläger, + radius weil man nacht rechts geht
                ball.x_geschwindigkeit *= -1 #ändert richtung
                ball.y_geschwindigkeit = (ball.y - (rechter_schläger.y + rechter_schläger.height / 2)) / (rechter_schläger.height / 2) * ball.geschwindigkeit_ball   # der ball prallt in verschiedenen richtungen ab

def schläger_bewegung(taste, linker_schläger, rechter_schläger):
    if taste[pygame.K_w]:
        linker_schläger.bewegung(hoch=True)
    if taste[pygame.K_s]: 
        linker_schläger.bewegung(hoch=False)

    if taste[pygame.K_UP]: 
        rechter_schläger.bewegung(hoch=True)
    if taste[pygame.K_DOWN]: 
        rechter_schläger.bewegung(hoch=False)

# wenn die w taste gedrückt wird, wird für den linken schläger up = True gesetzt und der Schläger bewegt sich

def main():
    running = True
    clock = pygame.time.Clock()  

    linker_schlaeger = Schlaeger(10, Settings.Hoehe/2 - Schlaeger.Schlaeger_hoehe / 2, Schlaeger.Schlaeger_breite, Schlaeger.Schlaeger_hoehe) # position der schläger 
    rechter_schlaeger = Schlaeger(Settings.Breite - 10 - Schlaeger.Schlaeger_breite, Settings.Hoehe / 2 - Schlaeger.Schlaeger_hoehe / 2, Schlaeger.Schlaeger_breite, Schlaeger.Schlaeger_hoehe)
    ball = Ball(Settings.Breite / 2, Settings.Hoehe / 2, Ball.BALL_RADIUS) # der ball spawnt in der mitte

    punkte_links = 0
    punkte_rechts = 0

    while running:
        clock.tick(Settings.FPS)
        draw(Settings.Window, linker_schlaeger, rechter_schlaeger, ball, punkte_links, punkte_rechts)

        taste = pygame.key.get_pressed()
        schläger_bewegung(taste, linker_schlaeger, rechter_schlaeger)

        ball.move()
        collision(ball, linker_schlaeger, rechter_schlaeger)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or taste[pygame.K_ESCAPE]:
                running = False

        if ball.x < 0:
            punkte_rechts += 1
            ball.ball_anfang()
        elif ball.x > Settings.Breite:
            punkte_links += 1
            ball.ball_anfang()
        
        
        won = False
        if punkte_links>= Settings.Punkte_zum_gewinnen:
            won = True
        elif punkte_rechts >= Settings.Punkte_zum_gewinnen:
            won = True
        if won:
            pygame.time.delay(2000)
            running = False
        
    
    pygame.quit()

if __name__ == "__main__":
    main()
