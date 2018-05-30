from pygame.locals import *
import pygame, os, random
from random import randint

#PRESS "d" to clear bricks

#Pygame skeleton "https://github.com/kidscancode/pygame_tutorials/blob/master/pygame%20template.py"
#consts for window
WIDTH = 800
HEIGHT = 600
FPS = 30

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BG = (135,206,250)


#drawText method "https://github.com/kidscancode/pygame_tutorials/blob/master/shmup/shmup-14.py" [line 34-40]
font_name = pygame.font.match_font("arial")
def drawText(surf, text, size, x ,y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text,True,YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface, text_rect)


#assets (os lib used to to join paths on every operating system)
game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder,"img")
sound_folder = os.path.join(game_folder,"sound")


class Paddle(pygame.sprite.Sprite):

    def __init__(self,paddlesize):
        pygame.sprite.Sprite.__init__(self)
        self.paddlesize = paddlesize
        image = pygame.image.load(os.path.join(image_folder, "paddle1.png")).convert()
        self.image=pygame.transform.scale(image,(paddlesize,20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT-HEIGHT/18)
        self.speedx = 0
        self.maxspeed = 10

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -self.maxspeed
        if keystate[pygame.K_RIGHT]:
            self.speedx = self.maxspeed
        self.rect.x +=self.speedx
        if self.rect.right>WIDTH:
            self.rect.right = WIDTH
        if self.rect.left<0:
            self.rect.left = 0

    def getXPos(self):
        return self.rect.center[0]
    def getYPos(self):
        return self.rect.center[1]


class Ball (pygame.sprite.Sprite):


    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_folder,"ball.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 8
        self.rect.center = (x, HEIGHT - HEIGHT / 10)
        self.x = x
        self.speedx = 0
        self.speedy = 0
        self.inScreen = True

    def launch(self):
        self.speedx = randint(-10, 10)*speedmuliplier
        self.speedy = randint(-10, -5)-level*speedmuliplier


    def changeDir(self):
        self.speedy = -self.speedy
        if self.speedx<=0:
            self.speedx = randint(-10,-5)-level
        if self.speedx>0:
            self.speedx = randint(5,10)+level

    def changeDirX(self):
        self.speedx = -self.speedx

    def changeDirY(self):
        self.speedy = -self.speedy

    def getYPos(self):
        return self.rect.center[1]

    def lefthit(self):
        self.speedx = randint(-10,-7)*speedmuliplier
        self.speedy = randint(-5,-3)*speedmuliplier

    def leftinnerhit(self):
        self.speedx = randint(-5,-3)*speedmuliplier
        self.speedy = randint(-10, -7)*speedmuliplier

    def rightinnerhit(self):
        self.speedx = randint(3, 5)*speedmuliplier
        self.speedy = randint(-10, -7)*speedmuliplier

    def righthit(self):
        self.speedx = randint(7, 10)*speedmuliplier
        self.speedy = randint(-10,-7)*speedmuliplier




    def update(self):
        if not ball_launched:
            self.rect.center =(paddle.getXPos(),HEIGHT-HEIGHT/10)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right>WIDTH:
            self.speedx=-self.speedx
        if self.rect.left<0:
            self.speedx=-self.speedx
        if self.rect.top < 0:
            self.speedy=-self.speedy
        if self.rect.bottom>HEIGHT:
            self.inScreen = False
            if lifes>0:
                self.rect.center = (paddle.getXPos(), HEIGHT - HEIGHT / 10)
                self.speedx = 0
                self.speedy = 0


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y,type):
        pygame.sprite.Sprite.__init__(self)
        if type==1:
            self.image = pygame.image.load(os.path.join(image_folder, "brick.png")).convert()
            self.radius = 30
        if type==2:
            self.image = pygame.image.load(os.path.join(image_folder, "brick2.png")).convert()
            self.radius = 30
        if type==3:
            self.image = pygame.image.load(os.path.join(image_folder, "brick3.png")).convert()
            self.radius = 27
        if type==4:
            self.image = pygame.image.load(os.path.join(image_folder, "brick4.jpg")).convert()
            self.radius = 22
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y


    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Life (pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_folder, "heart.png")).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Pow (pygame.sprite.Sprite): #"https://github.com/kidscancode/pygame_tutorials/blob/master/shmup/shmup-14.py" [line 192-200]

    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["life","death","bolt"])
        self.image = powup_images[self.type]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = randint(1,3)

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT-HEIGHT/12:
            self.kill()


# Settings
lifes = 3
score = 0
paddlesize = WIDTH/6
level = 1
paddletimer=15
brickscore = 10
ball_launched = False
running = True
settedBricks = False
gameStarted = False
gameOver = False
speedmuliplier = level+level/5


#init game and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BREAKOUT")
clock = pygame.time.Clock()
#sprites
sprites = pygame.sprite.Group()
paddle = Paddle(paddlesize)
ball = Ball(paddle.getXPos())
powerups = pygame.sprite.Group()
life1 = Life(10,20)
balls = pygame.sprite.Group()
lasers = pygame.sprite.Group()
balls.add(ball)
sprites.add(paddle,life1)
bricks = pygame.sprite.Group()

#All assets downloaded from opengameart.org
#sounds
bounce = pygame.mixer.Sound(os.path.join(sound_folder, "bounce.ogg"))
bricksound = pygame.mixer.Sound(os.path.join(sound_folder, "bricksound.wav"))
itemsound = pygame.mixer.Sound(os.path.join(sound_folder, "item.wav"))
gameoversound = pygame.mixer.Sound(os.path.join(sound_folder, "applause.wav"))
introsound = pygame.mixer.Sound(os.path.join(sound_folder, "start.ogg"))
lvlup = pygame.mixer.Sound(os.path.join(sound_folder, "piano.wav"))
#images
powup_images ={}
powup_images["life"]=pygame.image.load(os.path.join(image_folder, "heart.png"))
powup_images["death"]=pygame.image.load(os.path.join(image_folder, "goldskull.gif"))
powup_images["bolt"]=pygame.image.load(os.path.join(image_folder, "bolt.png"))


def setBricks(level):
    if level==1:
        for x in range(30, WIDTH-80, 64): #interval=width&height from brickimg
            for y in range(0, 300, 24):
                bricks.add(Brick(x,y,1))
    if level==2:
        for x in range(30, WIDTH-80, 64):
            for y in range(0, 325, 24):
                bricks.add(Brick(x,y,2))
    if level==3:
        for x in range(30, WIDTH-80, 54):
            for y in range(0, 325, 19):
                bricks.add(Brick(x,y,3))
    if level==4:
        for x in range(30, WIDTH-80, 50):
            for y in range(0, 400 , 16):
                bricks.add(Brick(x,y,4))




#GameLoop
while running:

    paddletimer+=1                          #if ball hits groundline from the paddel it will change direction between bootom and top line of it
    clock.tick(FPS)
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[K_SPACE] and ball_launched==False:
        gameStarted=True
        ball.launch()
        ball_launched= True

    #kill all bricks
    if keystate[K_d]:
        for brick in bricks:
            brick.kill()





#BallSetup
    if ball.inScreen == False:
        ball_launched=False
        ball.inScreen=True
        lifes-=1
    if lifes == 0:
        ball.kill()
        for pow in powerups:
            pow.kill()
        gameOver=True

#SetupBricks
    if not settedBricks:
        setBricks(level)
        settedBricks=True
#levelcomplete
    if not bricks and not gameOver:
        if level<4:       #maxlevel play again untill death
            level+=1
        lifes+=1
        brickscore += 10
        lvlup.play()
        ball.inScreen=False
        settedBricks=False
        setBricks(level)
    #update
    bricks.update()
    sprites.update()
    balls.update()

    #draw
    screen.fill(BG)
    bricks.draw(screen)
    sprites.draw(screen)
    balls.draw(screen)


    #collisions
    ballbrickhit = pygame.sprite.spritecollide(ball,bricks,True,pygame.sprite.collide_circle)
    for hit in ballbrickhit:
        if(hit.rect.bottom>ball.getYPos()>hit.rect.top):        #sidehit
            ball.changeDirX()
        else:
            ball.changeDirY()                                    #normal hit
        bricksound.play()
        score += brickscore
        if random.random()>0.9:                                 # "https://github.com/kidscancode/pygame_tutorials/blob/master/shmup/shmup-14.py" [line 329-332]
            pow = Pow(hit.rect.center)
            itemsound.play()
            sprites.add(pow)
            powerups.add(pow)


    paddleball = pygame.sprite.spritecollide(paddle, balls,False)

    for hit in paddleball:
        if paddletimer>10:
            bounce.play()
            paddletimer = 0

            if hit.rect.center[0]<=paddle.getXPos()-paddlesize/4:
                ball.lefthit()
            if hit.rect.center[0]>paddle.getXPos()-paddlesize/4 and hit.rect.center[0]<paddle.getXPos():
                ball.leftinnerhit()
            if hit.rect.center[0]>paddle.getXPos() and hit.rect.center[0]<paddle.getXPos()+paddlesize/4:
                ball.rightinnerhit()
            if hit.rect.center[0]>=paddle.getXPos()+paddlesize/4:
                ball.righthit()


    powups = pygame.sprite.spritecollide(paddle,powerups,True)
    for hit in powups:
        if hit.type == "life":
            lifes+=1
        if hit.type == "death":
            lifes -=1
        if hit.type == "bolt":
            if paddle.maxspeed<30:
                paddle.maxspeed +=5


    if not gameStarted:
        drawText(screen, "WELCOME TO BREAKOUT", 50, WIDTH / 2, HEIGHT / 4)
        drawText(screen, "Arrow Keys to move left and right", 30, WIDTH / 2, HEIGHT / 4+70)
        drawText(screen, "Press SPACE to launch the ball", 30, WIDTH / 2, HEIGHT / 4+100)

    if gameOver:
        for brick in bricks:
            brick.kill()
        gameoversound.play()
        drawText(screen, "Game Over!", 50, WIDTH / 2, HEIGHT / 4)
        drawText(screen, "  Your Score was "+str(score), 50, WIDTH / 2, HEIGHT / 4+60)
        drawText(screen, "Press R to restart", 40, WIDTH / 2, HEIGHT / 4+110)
        if keystate[K_r]:
            lifes = 3
            score = 0
            level = 1
            paddlesize=3
            paddle.maxspeed=10
            brickscore = 10
            ball_launched = False
            running = True
            settedBricks = False
            gameStarted = False
            gameOver = False
            ball = Ball(paddle.getXPos())
            balls.add(ball)


    #drawScore
    drawText(screen,str(score),30,WIDTH/2,10)
    drawText(screen, str(lifes), 20, 26, 25)
    pygame.display.flip() #after drawing everything


pygame.quit()


