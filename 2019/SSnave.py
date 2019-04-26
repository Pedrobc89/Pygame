import pygame
import math
from random import randint

def sin(angle):
    """Calculates the sine of the given angle in degrees"""
    return math.sin(math.radians(angle))

def cos(angle):
    """Calculates the cosine of the given angle in degrees"""
    return math.cos(math.radians(angle))

def update():
    screen.fill((0,0,0))  # Apaga tudo o que tem na tela pintando de cor preta
    # screen.blit(background_image, [0,0])
    Spaceship.updateAll()
    Shot.updateAll()
    pygame.display.update()

def randomEnimies():
    """Creates a random flying targets"""
    for i in range(0,10):
        w, h = screenSize
        x = randint(0, w)
        y = randint(0, h)
        vel = Vector(randint(1,3), randint(0,360))
        s = Spaceship(x, y, 20, vel.direction)
        s.velocity = vel
        s.color = (randint(0,255), randint(0,255), randint(0,255))

class Vector():
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction

    @property
    def x(self):
        """The x property."""
        return self.magnitude*cos(self.direction)
    @x.setter
    def x(self, value):
        self.magnitude = math.hypot(value, self.y)
        self.direction = math.degrees(math.atan2(self.y, value))

    @property
    def y(self):
        """The y property."""
        return self.magnitude*sin(self.direction)
    @y.setter
    def y(self, value):
        self.magnitude = math.hypot(value, self.x)
        self.direction = math.degrees(math.atan2(value, self.x))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        magnitude = math.hypot(x, y)
        direction = math.degrees(math.atan2(y, x))
        return Vector(magnitude, direction)

    def __iadd__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        self.magnitude = math.hypot(x, y)
        self.direction = math.degrees(math.atan2(y, x))
        return self

    def __str__(self):
        return "({}, {})".format(self.magnitude, self.direction)

class Shot():
    allShots = []
    def __init__(self, x, y, velocity, ship):
        self.id = Shot.allShots.append(self)
        self.x = x
        self.y = y
        self.length = 5
        self.velocity = velocity
        self.ship = ship
        self.color = ship.color
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("/Users/pato/Documents/Development/PyGame/2019/laser.wav"))
    
    @property
    def points(self):
        """The points property."""
        p1 = (self.x, self.y)
        vec = Vector(self.length, self.velocity.direction)
        p2 = (self.x+vec.x, self.y+vec.y)
        return [p1, p2]

    def updateAll():
        for shot in Shot.allShots:
            shot.update()

    def update(self):
        self.move()
        self.draw()

    def outBounds(self):
        w, h = screenSize
        if not 0 < self.x < w or not 0 < self.y < h:
            self.explode()

    def move(self):
        self.outBounds()
        for ship in Spaceship.allShips:
            if self.ship is not ship:
                if ship.collidepoint(self.x, self.y):
                    ship.takeDamage()
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound("/Users/pato/Documents/Development/PyGame/2019/laserBlast.wav"))
                    self.explode()
        self.x += self.velocity.x
        self.y += self.velocity.y

    def draw(self):
        pygame.draw.line(screen, self.color, self.points[0], self.points[1])

    def explode(self):
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("/Users/pato/Documents/Development/PyGame/2019/woosh.wav"))
        if Shot.allShots.count(self)>0: Shot.allShots.remove(self)
        del self
        
class Missile(Shot):
    def __init__(self, x, y, velocity, ship, target):
        super().__init__(x, y, velocity, ship)
        self.velocity.magnitude = 1
        self.target = target
    
    def move(self):
        self.velocity.magnitude+=0.001
        if self.velocity.magnitude > 3: self.explode()
        x = self.target.centerx - self.x
        y = self.target.centery - self.y
        self.velocity.direction = math.degrees(math.atan2(y, x))
        self.direction = self.velocity.direction
        super().move()

class Spaceship(pygame.Rect):
    """Class for the spaceship"""
    allShips = []
    def __init__(self, x, y, size, direction, isMain = False):
        self.xf = x
        self.yf = y
        self.size = size
        self.direction = direction
        self.allShips.append(self)
        self.color = pygame.Color('white')
        self.velocity = Vector(0, direction)
        self.alive = True
        self.isMain = isMain
        self.shots = []
        self.maxShots = 5
        self.warpable = False
    
    @property
    def xf(self):
        """The xf property."""
        return self._xf
    @xf.setter
    def xf(self, value):
        self._xf = value
        self.x = int(self._xf)

    @property
    def yf(self):
        """The yf property."""
        return self._yf
    @yf.setter
    def yf(self, value):
        self._yf = value
        self.y = int(self._yf)

    @property
    def points(self):
        """List of points to draw the ship"""
        vec = Vector(self.width/2, self.direction)
        p1 = (self.centerx+vec.x, self.centery+vec.y)
        vec.direction+=120
        p2 = (self.centerx+vec.x, self.centery+vec.y)
        vec.direction+=120
        p3 = (self.centerx+vec.x, self.centery+vec.y)
        return [p1, p2, self.center, p3]
    
    @property
    def alive(self):
        """Is spaceship alive?"""
        return self._alive
    @alive.setter
    def alive(self, value):
        self._alive = value
        if not value:
            Spaceship.allShips.remove(self)

    @property
    def size(self):
        """Size of the ship"""
        return self._size
    @size.setter
    def size(self, value):
        self._size = value
        self.width = value
        self.height = value

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.points)

    def updateAll():
        for ship in Spaceship.allShips:
            ship.update()

    def update(self):
        self.move()
        self.draw()

    def outBounds(self):
        w, h = screenSize
        if not 0 < self.centerx < w or not 0 < self.centery < h:
            if self.isMain: 
                self.alive = False
            elif self.warpable:
                self.warp()
            else:
                self.bounce()

    def warp(self):
        w, h = screenSize
        if self.xf < 0:
            self.xf = w
        elif self.xf > w:
            self.xf = 0
        elif self.yf < 0:
            self.yf = h
        elif self.yf > h:
            self.yf = 0
    
    
    def bounce(self):
        w, h = screenSize
        if not 0 < self.x < w:
            self.velocity.x = -self.velocity.x
        elif not 0 < self.y < h:
            self.velocity.y = -self.velocity.y
        
        self.direction = self.velocity.direction
    
    def takeDamage(self, value = 10):
        self.size -= value
        if self.size <= 20:
            self.alive = False

    def move(self):
        # self.velocity.direction = self.direction
        self.outBounds()

        if self.isMain:
            for other in Spaceship.allShips:
                if other is not self:
                    if self.colliderect(other):
                        pygame.mixer.Channel(3).play(pygame.mixer.Sound("/Users/pato/Documents/Development/PyGame/2019/woosh.wav"))
                        self.alive = False
                        other.alive = False

        self.xf += self.velocity.x
        self.yf += self.velocity.y

    def accelerate(self, magnitude):
        self.velocity+=Vector(magnitude, self.direction)

    def __str__(self):
        return "corner: ({}, {}) size: {} direction: {}".format(self.xf, self.yf, self.width, self.direction)
    
    def shoot(self):
        # if len(self.shots) < self.maxShots:
        dir = self.direction
        x, y = self.points[0]
        a = Shot(x, y, Vector(5, dir), self)
        self.shots.append(a)

    def shootMissile(self, target):
        # if len(self.shots) < self.maxShots:
        dir = self.direction
        x, y = self.points[0]
        a = Missile(x, y, Vector(5, dir), self, target)
        self.shots.append(a)
        
class Enemy(Spaceship):
    def __init__(self, x, y, size, target, inteligence = 0):
        super().__init__(x, y, size, 0)
        self.target = target
        self.velocity.magnitude = randint(1, 3)
        self.inteligence = inteligence
        self.velocity.direction = randint(0,360)
        self.direction = self.velocity.direction
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.elapsed_time = 0
        self.ticks = 0
        # print(pygame.color.THECOLORS)

    def move(self):
        method_name = 'path' + str(self.inteligence)
        # Get the method from 'self'. Default to a lambda.
        path = getattr(self, method_name, lambda: "Invalid month")
        # Call the method as we return it
        path()
        newTicks = pygame.time.get_ticks()
        self.elapsed_time += newTicks - self.ticks
        self.ticks = newTicks 
        # print(self.elapsed_time)
        self.direction = self.velocity.direction
        super().move()

    def path0(self):
        pass

    def path1(self):
        self.velocity.direction+=1

    def path2(self):
        self.velocity.magnitude+=0.001
        if self.velocity.magnitude >= 4:
            self.velocity.magnitude = 4

    def path3(self):
        self.velocity.direction+=self.velocity.magnitude

    def path4(self):
        if self.elapsed_time/1000 > 1:
            self.elapsed_time = 0
            self.velocity.direction+=randint(10,45)*(-1+2*randint(0,1))
        pass

    def path5(self):
        if self.elapsed_time/1000 > 1:
            self.elapsed_time = 0
            self.velocity.direction+=45*(-1+2*randint(0,1))
        pass
        
    def path6(self):
        x = self.target.centerx - self.centerx  
        y = self.target.centery - self.centery  
        self.velocity.direction = math.degrees(math.atan2(y, x))
        pass

    def path7(self):
        self.warpable = True
        self.velocity.direction = math.degrees(sin(self.x))
        pass
        
    def path8(self):
        self.warpable = True
        self.velocity.direction = math.degrees(cos(self.y))+90
        pass

    def path9(self):
        self.velocity.magnitude = 0
        x = self.target.centerx - self.centerx  
        y = self.target.centery - self.centery  
        self.velocity.direction = math.degrees(math.atan2(y, x))
        if self.elapsed_time/1000 > 1:
            self.elapsed_time = 0
            self.shoot()
        pass

    def path10(self):
        self.velocity.magnitude = 0
        x = self.target.centerx - self.centerx  
        y = self.target.centery - self.centery  
        hip = math.hypot(x, y)/5
        x = self.target.centerx+hip*self.target.velocity.x - self.centerx  
        y = self.target.centery+hip*self.target.velocity.y - self.centery  
        self.velocity.direction = math.degrees(math.atan2(y, x))
        if self.elapsed_time/3000 > 1:
            self.elapsed_time = 0
            self.shoot()
        pass

    def path11(self):
        self.velocity.magnitude = 0
        x = self.target.centerx - self.centerx  
        y = self.target.centery - self.centery  
        self.velocity.direction = math.degrees(math.atan2(y, x))
        if self.elapsed_time/5000 > 1:
            self.elapsed_time = 0
            self.shootMissile(Spaceship.allShips[0])
        pass

        
        
if __name__ == "__main__":
    try:
        looping = True
        numEnemies = 1
        pygame.init()
        clock = pygame.time.Clock()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("/Users/pato/Documents/Development/PyGame/2019/background.wav"), -1)
        screenSize = (1200, 800)
        screen = pygame.display.set_mode(screenSize)

        background_image = pygame.image.load("/Users/pato/Documents/Development/PyGame/2019/background.jpg").convert()

        mainShip = Spaceship(390,290,20,-90, True)

        while mainShip.alive and looping:
            """Main loop"""
            for event in pygame.event.get(): # captura eventos (teclado e mouse)
                if event.type == pygame.QUIT: # Clique no X da janela
                    looping = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Apertada a tecla ESC
                    looping = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Apertada a tecla espaço
                    mainShip.shoot()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    if(buttons[0]): mainShip.shoot()
                
            # rx, ry = pygame.mouse.get_rel()
            # mainShip.direction += rx
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                mainShip.direction += 4
            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                mainShip.direction -= 4
            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                mainShip.accelerate(0.1)
            if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                mainShip.accelerate(-0.1)

            if len(Spaceship.allShips) < numEnemies+1:
                w, h = screenSize
                x = randint(0, w)
                y = randint(0, h)
                if not mainShip.colliderect(pygame.Rect(x, y, 200, 200)):
                    # e = Enemy(x, y, randint(10, 50), mainShip, randint(0,11))
                    e = Enemy(x, y, randint(10, 50), mainShip, 10)

            update()
            clock.tick(60) # FPS - frames per second

    except:
        print("An error has ocurred")
    finally:
        pygame.quit()
        print("Game Over")

