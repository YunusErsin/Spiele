import pygame
pygame.init()

class Settings:
    WIDTH = 900
    HEIGHT = 600
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clapy")


ROT = (255, 0, 0)
Schwarz = (0, 0, 0)
WEIß = (255,255,255)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 7

Text = pygame.font.SysFont("Arial", 50)
Punkte_zum_gewinnen = 7

class Schläger:
    Farbe_paddle = ROT
    geschwindigkeit_schläger = 8

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(win, self.Farbe_paddle, (self.x, self.y, self.width, self.height))

    def bewegung(self, hoch=True):
        if hoch:
            self.y -= self.geschwindigkeit_schläger 
        else:
            self.y += self.geschwindigkeit_schläger

class Ball:
    max_geschwindigkeit_ball = 5
    Farbe_ball = WEIß

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_geschwindigkeit = self.max_geschwindigkeit_ball
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
    window.fill(Schwarz)

    punktestand_links = Text.render(f"{punkte_links}", 1, ROT)
    punktestand_rechts = Text.render(f"{punkte_rechts}", 1, ROT)
    window.blit(punktestand_links, (Settings.WIDTH//4 - punktestand_links.get_width()//2, 20))
    window.blit(punktestand_rechts, (Settings.WIDTH * (3/4) - punktestand_rechts.get_width()//2, 20))
    linker_schläger.draw(window)
    rechter_schläger.draw(window)

    ball.draw(window)
    pygame.display.update()

def collision(ball, linker_schläger, rechter_schläger):
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= Settings.HEIGHT:
        ball.y_geschwindigkeit *= -1

    if ball.x_geschwindigkeit < 0:
        if ball.y + ball.radius >= linker_schläger.y and ball.y - ball.radius <= linker_schläger.y + linker_schläger.height:
            if ball.x - ball.radius <= linker_schläger.x + linker_schläger.width:
                ball.x_geschwindigkeit *= -1
                ball.y_geschwindigkeit = (ball.y - (linker_schläger.y + linker_schläger.height / 2)) / (linker_schläger.height / 2) * ball.max_geschwindigkeit_ball
    else:
        if ball.y + ball.radius >= rechter_schläger.y and ball.y - ball.radius <= rechter_schläger.y + rechter_schläger.height:
            if ball.x + ball.radius >= rechter_schläger.x:
                ball.x_geschwindigkeit *= -1
                ball.y_geschwindigkeit = (ball.y - (rechter_schläger.y + rechter_schläger.height / 2)) / (rechter_schläger.height / 2) * ball.max_geschwindigkeit_ball


def schläger_bewegung(taste, linker_schläger, rechter_schläger):
    if taste[pygame.K_w]:
        linker_schläger.bewegung(hoch=True)
    if taste[pygame.K_s]: 
        linker_schläger.bewegung(hoch=False)

    if taste[pygame.K_UP]: 
        rechter_schläger.bewegung(hoch=True)
    if taste[pygame.K_DOWN]: 
        rechter_schläger.bewegung(hoch=False)




def main():
    running = True
    clock = pygame.time.Clock() 

    linker_schläger = Schläger(10, Settings.HEIGHT/2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    rechter_schläger = Schläger(Settings.WIDTH - 10 - PADDLE_WIDTH, Settings.HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(Settings.WIDTH / 2, Settings.HEIGHT / 2, BALL_RADIUS) 
    punkte_links = 0
    punkte_rechts = 0

    while running:
        clock.tick(Settings.FPS)
        draw(Settings.WIN, linker_schläger, rechter_schläger, ball, punkte_links, punkte_rechts)

        taste = pygame.key.get_pressed()
        schläger_bewegung(taste, linker_schläger, rechter_schläger)

        ball.move()
        collision(ball, linker_schläger, rechter_schläger)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball.move()
        collision(ball, linker_schläger, rechter_schläger)

        if ball.x < 0:
            punkte_rechts += 1
            ball.ball_anfang()
        elif ball.x > Settings.WIDTH:
            punkte_links += 1
            ball.ball_anfang()
        
        
        won = False
        
        if punkte_links>= Punkte_zum_gewinnen:
            won = True

        elif punkte_rechts >= Punkte_zum_gewinnen:
            won = True
        
        if won:
            pygame.time.delay(2000)
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()

