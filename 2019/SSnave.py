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
    for ship in Spaceship.allShips:
        ship.update()
    
    pygame.display.update()

def looping():
    """Main loop"""
    for event in pygame.event.get(): # captura eventos (teclado e mouse)
        if event.type == pygame.QUIT: # Clique no X da janela
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Apertada a tecla ESC
            return False

    update()
    return True

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
        p1 = (self.centerx+self.width/2*cos(self.direction), self.centery+self.width/2*sin(self.direction))
        p2 = (self.centerx+self.width/2*cos(self.direction+120), self.centery+self.width/2*sin(self.direction+120))
        p3 = (self.centerx+self.width/2*cos(self.direction-120), self.centery+self.width/2*sin(self.direction-120))
        return [p1, p2, self.center, p3]
    
    def draw(self):
        pygame.draw.polygon(screen, self.color, self.points)

    def update(self):
        # self.move()
        self.draw()
    
    def __repr__(self):
        return "corner: ({}, {}) size: {} direction: {}".format(self.xf, self.yf, self.width, self.direction)


if __name__ == "__main__":
# try:
    pygame.init()
    screenSize = (800, 600)
    screen = pygame.display.set_mode(screenSize)

    s = Spaceship(390,290,20,-90)

    while looping():
        print(s)
        pass

# except:
#     print("An error has ocurred")
# finally:
    pygame.quit()
    print("Closing App")

