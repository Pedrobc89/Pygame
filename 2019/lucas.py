import pygame

class Circle:
    pi = 3.1415

    def __init__(self, radius, center):
        self.radius = radius
        self.center = center
    
    @property
    def diameter(self):
        """The diameter property."""
        return self.radius*2
    @diameter.setter
    def diameter(self, value):
        self.radius = value/2

    @property
    def center(self):
        """The center property."""
        return self._center
    @center.setter
    def center(self, value):
        self._center = value

    
    def p(self):
        return 2*self.pi*self.radius

    def area(self):
        return self.pi*self.radius*self.radius
    
    def draw(self):
        pygame.draw.circle(screen, (155,0,0), self.center, self.radius)

    # def __repr__(self):
    #     return ("Circle radius = {}, center = {}, diameter = {}, perimeter = {},"
    #         " area = {}").format(self.radius, self.center, self.diameter self.p(), self.area())


class Rectangle:
    def __init__(self, center, w, h):
        self.center = center
        self.w = w
        self.h = h

    def p(self):
        return 2*self.w+2*self.h

    def area(self):
        return self.w*self.h
    
    def points(self):
        x, y = self.center
        left = x-self.w/2
        right = x+self.w/2
        top = y-self.h/2
        bottom = y+self.h/2
        return [(left, top), (right, top), (right, bottom), (left, bottom)]

    def draw(self):
        pygame.draw.polygon(screen, (0,0,155), self.points())

    def __repr__(self):
        return ("Rectangle  center = {}, width = {},"
            " height = {}, perimeter = {}, area = {}").format(self.center, self.w, self.h, self.p(), self.area())

class RegularPolygon:
    def __init__(self, center, lenght, nSides):
        self.center = center
        self.length = lenght
        self.nSides = nSides
    
    def perimeter(self):
        return self.nSides * self.length

    def internalAngle(self):
        return (self.nSides-2)*180/self.nSides

    def __repr__(self):
        return ("RegularPolygon  center = {}, length = {},"
            " number of sides = {}, perimeter = {}, internal angle = {}"
            "").format(self.center, self.w, self.h, self.perimeter(), self.internalAngle())


pygame.init()
clock = pygame.time.Clock() # Inicialização do clock do pygame

screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size) # Cria a janela no OS

c = Circle(30, (400,300))
r = Rectangle((20,20), 10,20)
ax, ay, vx, vy, g = [0, 0, 0, 0, 1]
def looping():
    global ax
    global ay
    global vx
    global vy
    global g
    for event in pygame.event.get(): # captura eventos (teclado e mouse)
        # print(event)
        if event.type == pygame.QUIT: # Clique no X da janela
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Tecla ESC pressionada
            return False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        ay = -2
    elif pressed[pygame.K_s]:
        ay = 1
    else:
        ay = 0

    if pressed[pygame.K_a]:
        ax = -1
    elif pressed[pygame.K_d]:
        ax = 1
    else:
        ax = 0

    screen.fill((85, 130, 170))  # Apaga tudo o que tem na tela pintando de cor preta
    x, y = c.center
    vx += ax
    vy += ay  + g
    x += vx
    y += vy

    if y+c.radius > 600:
        y = 600-c.radius-1
        vy = 0
    if y-c.radius < 0:
        y = c.radius+1
        vy = 0
        
    c.center = (x, y)
    c.draw()
    r.draw()
    pygame.display.update() # Atualiza o frame na tela
    clock.tick(60) # FPS - frames per second / basicamente um delay
    
    return True

while looping():
    
    pass
