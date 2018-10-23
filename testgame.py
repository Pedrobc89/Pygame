import math
import time
import pygame
from random import randint

pygame.init()

size = (800,600)
gravity = -0.1
mean_fps = 0
num = 1
pwr = 100
ang = 0
mass = 10

def fps_measure(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        elapsed_ts = end_ts - beg_ts
        fps = 1/elapsed_ts
        global mean_fps
        global num
        print("{}: fps= {:0.2f}\t".format(func.__name__, mean_fps/num), end="\r")
        mean_fps+=fps
        num +=1
        return retval
    return wrapper

def time_usage(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        elapsed_ts = end_ts - beg_ts
        # print("{}: time elapsed = {:0.2f}".format(func.__name__, elapsed_ts), end="\n")
        return retval
    return wrapper

# Cria uma janela do tamanho 800x600 pixels
screen = pygame.display.set_mode(size)
# Título da janela
pygame.display.set_caption('Olemac ed soluco')
background_image = pygame.image.load("bg.jpg").convert()
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)
image = pygame.image.load('Ball@2x.png').convert_alpha()
img_rect = image.get_rect()
# GameClock
clock = pygame.time.Clock()


# O jogo será de corrida, quando bater o carro você pede e o jogo desaparece
crashed = False

color = (0, 128, 255)
black = (0,0,0)
ax, ay = 0, 0
vx, vy = 0, 0
x, y, w, h = 30, 30, 60, 60
g = .9 # gravity
jumps = 2
objList = []

class Physics:
    def __init__(self):
        self.ax = 0
        self.vx = 0
        self.ay = -gravity
        self.vy = 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        objList.append(self)
        self.draw()
        pass

    def coords(self):
        return (self.x+400-self.w/2,
                300-self.h/2-self.y, self.w, self.h)

    def isOut(self):
        sw, sh = size
        if self.right() >= sw/2 :
             return True
        if self.left() <= -sw/2:
             return True
        if self.up() >= sh/2 :
             return True
        if self.down() <= -sh/2:
            return True
        return False

    def left(self): return self.x-self.w/2
    def right(self): return self.x+self.w/2
    def up(self): return self.y+self.h/2
    def down(self): return self.y-self.h/2
    def getRect(self): return pygame.Rect(self.x, self.y, self.w, self.h)
    

    def draw(self):
        self.erase()
        self.move()
        if self.image: screen.blit(self.image, pygame.Rect(self.coords()))
        else:  pygame.draw.rect(screen, self.color, pygame.Rect(self.coords()))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.coords()))
        # pygame.display.update(self.rect)
        pass

    def erase(self):
        # pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.coords()))
        # screen.blit(background_image, pygame.Rect(self.coords()))
        pass

    def moveby(self, step, func):
        x = self.x+step
        self.move_to(x,func(x))
        pass

    def move_to(self, x, y):
        self.x = x
        self.y = y
        pass

    def move(self):
        if not self.movable: return 
        # detect colision

        self.vx += self.ax
        self.vy += self.ay + gravity

        self.x += self.vx
        other = self.detect_colisions()
        if other:
            if other.movable:
                self.x -= self.vx
                vx1 = self.vx
                vx2 = other.vx
                self.vx = (vx1*(self.area-other.area)+2*vx2*other.area)/(self.area+other.area)
                other.vx = (vx2*(self.area-other.area)+2*vx1*other.area)/(self.area+other.area)
            else:
                self.x -= 2*self.vx
                self.vx = -self.vx

        if self.isOut(): 
            self.x -= 2*self.vx
            self.vx = -self.vx

        self.y += self.vy
        other = self.detect_colisions()
        if other:
            if other.movable:
                self.y -= self.vy
                vy1 = self.vy
                vy2 = other.vy
                self.vy = (vy1*(self.area-other.area)+2*vy2*other.area)/(self.area+other.area)
                other.vy = (vy2*(self.area-other.area)+2*vy1*other.area)/(self.area+other.area)
            else:
                self.y -= 2*self.vy
                self.vy = -self.vy+gravity

        if self.isOut(): 
            self.y -= 2*self.vy
            self.vy = -self.vy+gravity

        pass
        
    
    def set_move(self, ax, ay, vx, vy):
        self.ax = ax
        self.vx = vx
        self.ay = ay
        self.vy = vy
        pass

    # detect if there is a colision
    # return (xcolision, ycolision)
    def detect_colisions(self):
        if not self.collidable: return False
        xboom = False
        yboom = False
        for r in objList:
            if r != self and r.collidable:
                xboom = self.x_colision(r)
                yboom = self.y_colision(r)
                if xboom and yboom:
                    return r
        return None

    def x_colision(self, other):
        if self.right() < other.left(): return False
        if self.left() > other.right(): return False
        return True

    def y_colision(self, other):
        if self.up() < other.down(): return False
        if self.down() > other.up(): return False
        return True

class Rectao(Physics):
    def  __init__(self, x, y, w, h, color, image=None, collidable = True, movable = True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = self.w+self.h
        self.color = color
        self.movable = movable
        self.collidable = collidable
        if image: self.image = pygame.transform.scale(image, (self.w+5, self.h+5))
        else: self.image = None
        Physics.__init__(self)
        return

def f1(x):
    a, b = 0, 1
    return a*x+ b

def f2(x):
    a, b, c = -0.005, 0, 150
    return a*x*x+ b*x+c

# screen.fill((0,0,0))
# screen.blit(background_image, [0,0])
# ping  = Rectao(-200,-150,10,10, (0,255,255), image)
# chao = Rectao(0, -250, 800, 50, (255, 255, 255), None, True, False)
# eixox = Rectao(0,0, 800, 4, (255,255,255), None, False, False)
eixoy = Rectao(0,0, 4, 600, (255,255,255), None, False, False)
# bolax = Rectao(0,0, 4, 4, (0,255,0), None, False)
# bolay = Rectao(0,0, 4, 4, (0,0,255), None, False)
# pygame.display.update()

forward = True

def update():
    dirty_rect = []
    for r in objList:
        r.draw()
        dirty_rect.append(r.getRect())
    if len(dirty_rect) > 0: 
        pygame.display.update(dirty_rect) # Atualiza todos os objetos da janela
    else:
        pygame.display.update()
    
    # pygame.display.flip() # Atualiza todos os objetos da janela
    pass


# Game loop - toda a lógica do jogo estará aqui
def loop():
    global pwr
    global ang
    screen.blit(background_image, [0,0])
    for event in pygame.event.get():

        #  print event values, helps implementing new key entries
        #  print(event)

        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Rectao(-300,-20,20,20, (randint(0,255),randint(0,255),randint(0,255)), image)
            bullet.set_move(0,0,7*pwr/100*math.cos(math.radians(ang)),7*pwr/100*math.sin(math.radians(ang)))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and pwr < 100: pwr += 5
        if pressed[pygame.K_DOWN] and pwr > 0: pwr -= 5
        if pressed[pygame.K_LEFT] and ang < 90: ang += 5
        if pressed[pygame.K_RIGHT] and ang > 0: ang -=5
        print("Power: {:3d} Angle: {:3d}".format(pwr, ang), end="\r")

    # update()
    for r in objList: r.draw()
    pygame.display.update()
    clock.tick(120) # FPS - frames per second

    return True

objList.remove(eixoy)
while loop(): 
    pass

pygame.quit()