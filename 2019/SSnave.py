import pygame
import math

def sin(angle):
    """Calculates the sine of the given angle in degrees"""
    return math.sin(math.radians(angle))

def cos(angle):
    """Calculates the cosine of the given angle in degrees"""
    return math.cos(math.radians(angle))

def update():
    screen.fill((0,0,0))  # Apaga tudo o que tem na tela pintando de cor preta
    Spaceship.updateAll()
    Shot.updateAll()
    pygame.display.update()

def looping():
    """Main loop"""
    mainShip = Spaceship.allShips[0]
    for event in pygame.event.get(): # captura eventos (teclado e mouse)
        if event.type == pygame.QUIT: # Clique no X da janela
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Apertada a tecla ESC
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Apertada a tecla espaço
            a = Shot(mainShip.centerx, mainShip.centery, Vector(3, mainShip.direction))
            
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_d]:
        Spaceship.allShips[0].direction += 5
    if pressed[pygame.K_a]:
        Spaceship.allShips[0].direction -= 5
    if pressed[pygame.K_w]:
        Spaceship.allShips[0].accelerate(0.1)
    if pressed[pygame.K_s]:
        Spaceship.allShips[0].accelerate(-0.1)


    update()
    return True

        

class Vector():
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction

    @property
    def x(self):
        """The x property."""
        return self.magnitude*cos(self.direction)

    @property
    def y(self):
        """The y property."""
        return self.magnitude*sin(self.direction)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        magnitude = math.sqrt(x**2+y**2)
        direction = math.degrees(math.atan2(y, x))
        return Vector(magnitude, direction)

    def __iadd__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        self.magnitude = math.sqrt(x**2+y**2)
        self.direction = math.degrees(math.atan2(y, x))
        return self

    def __str__(self):
        return "({}, {})".format(self.magnitude, self.direction)

class Shot():
    allShots = []
    def __init__(self, x, y, velocity):
        self.id = Shot.allShots.append(self)
        self.x = x
        self.y = y
        self.length = 5
        self.velocity = velocity
        self.color = pygame.Color('blue')
    
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
        self.x += self.velocity.x
        self.y += self.velocity.y

    def draw(self):
        pygame.draw.line(screen, self.color, self.points[0], self.points[1])

    def explode(self):
        print('Shot exploded')
        Shot.allShots.remove(self)
        
class Spaceship(pygame.Rect):
    """Class for the spaceship"""
    allShips = []
    def __init__(self, x, y, size, direction):
        self.xf = x
        self.yf = y
        self.width = size
        self.height = size
        self.direction = direction
        self.allShips.append(self)
        self.color = pygame.Color('blue')
        self.velocity = Vector(0, direction)
    
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
    
    def draw(self):
        pygame.draw.polygon(screen, self.color, self.points)

    def updateAll():
        for ship in Spaceship.allShips:
            ship.update()

    def update(self):
        self.move()
        self.draw()

    def move(self):
        self.xf += self.velocity.x
        self.yf += self.velocity.y

    def accelerate(self, magnitude):
        self.velocity+=Vector(magnitude, self.direction)

    def __str__(self):
        return "corner: ({}, {}) size: {} direction: {}".format(self.xf, self.yf, self.width, self.direction)


if __name__ == "__main__":
# try:
    pygame.init()
    screenSize = (800, 600)
    screen = pygame.display.set_mode(screenSize)

    s = Spaceship(390,290,20,-90)

    while looping():
        # print(s.velocity)
        pass

# except:
#     print("An error has ocurred")
# finally:
    pygame.quit()
    print("Closing App")

