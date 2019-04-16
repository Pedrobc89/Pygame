import pygame # importa o modulo pygame
import math as m # importa modulo de calculos matematicos

#Globals
gravity = -0.1 #pixels per frame
objList = []

pygame.init() # Inicialização do módulo pygame
clock = pygame.time.Clock() # Inicialização do clock do pygame

screen_size = (400,400) # Tamanbho da Janela
screen = pygame.display.set_mode(screen_size) # Cria a janela no OS

class Pov:
    """Creates a pont of view for all the object"""
    def __init__(self, x, y, z, azimuth, elevation):
        self.x = x # x position of the point of view
        self.y = y # y position of the point of view
        self.z = z # z position of the point of view
        self.azimuth = azimuth # azimuth angle of the point of view (horizontal angle)
        self.elevation = elevation # elevation angle of the point of view (vertical angle)

    def forward(self, value):
        """moves the point of view one step forward (backwards if value is negative)"""
        self.x += value*m.sin(m.radians(self.azimuth))
        self.y += value*m.cos(m.radians(self.azimuth))
        pass

    def sidestep(self, value):
        """moves the point of view one step to the right (left if value is negative)"""
        self.x += value*m.cos(m.radians(self.azimuth))
        self.y += value*m.sin(m.radians(self.azimuth))
        
        pass
        
    def transform(self, x, y, z, p = False):
        """Transforms a 3D point into 2d coordinates"""
        
        x = (x-self.x)
        y = (y-self.y)
        z = (z-self.z)
        azimuth = m.degrees(m.atan2(y, x))
        elevation = -m.degrees(m.atan2(z, y))
        if p: print(azimuth, elevation)
        if 30 < azimuth < 150: azimuth = (90+self.azimuth-azimuth)
        else: return None
        x_ = 200+(azimuth/60)*200
        y_ = 200+(elevation/60)*200

        if x_ < 0 or x_ > 400 or y_ < 0 or y_ > 400: return None

        return (x_, y_)        

    def drawAxis(self):
        """Draw the 3D axis"""
        origin = self.transform(self.x, self.y, self.z)
        xaxis = self.transform(self.x+400, self.y, self.z)
        yaxis = self.transform(self.x, self.y+400, self.z)
        zaxis = self.transform(self.x, self.y, self.z+400)
        # print(xaxis)

        pygame.draw.line(screen, pygame.Color("blue"), (200,200), (200+x, 200+y))
        pygame.draw.line(screen, pygame.Color("green"), (200,200), (200-y,200+x))

        pygame.draw.line(screen, pygame.Color("white"), (200,200), zaxis)
        pygame.draw.line(screen, pygame.Color("blue"), (200,200), xaxis)
        pygame.draw.line(screen, pygame.Color("green"), (200,200), yaxis)
        pass

    def __repr__(self):
        return "x: {} y: {} z: {} azimuth: {} elevation: {}".format(self.x, self.y, self.z, self.azimuth, self.elevation)

class myCube():
    allCubes = []
    pov = Pov(0,0,0,0,0)

    def __init__(self, x, y, z, size, orientation):
        self.x = x
        self.y = y
        self.z = z
        self.size = size

        self.allCubes.append(self)

    @property
    def x(self):
        """The center x coordinate."""
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        
    @property
    def y(self):
        """The center y coordinate."""
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    
    @property
    def z(self):
        """The z property."""
        return self._z
    @z.setter
    def z(self, value):
        self._z = value

    @property
    def center(self):
        """The center (x, y, z) of cube."""
        return (self.x, self.y, self.z)
    @center.setter
    def center(self, value):
        x, y, z = value
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def points(self):
        """The list of the vertices coordinates of the cube."""
        #TODO: calculate the vertices coordinates based on perspective
        x, y, z = self.center
        hs = self.size/2
        _x = x-hs
        x = x+hs
        _y = y-hs
        y = y+hs
        _z = z-hs
        z = z+hs
        tl = self.pov.transform(_x, _y, z)
        tr = self.pov.transform(x, _y, z)
        bl = self.pov.transform(_x, _y, _z)
        br = self.pov.transform(x, _y, _z)

        tl2 = self.pov.transform(_x, y, z)
        tr2 = self.pov.transform(x, y, z)
        bl2 = self.pov.transform(_x, y, _z)
        br2 = self.pov.transform(x, y, _z)

        p1 = [br, bl, tl, tr, tr2, br2, br, tr]
        p2 = [bl2, bl, tl, tl2, tr2, br2, bl2, tl2]

        if p1.count(None) > 0: p1 = None
        if p2.count(None) > 0: p2 = None

        return (p1, p2)

    def draw(self):
        p1, p2 = self.points
        if p1: pygame.draw.polygon(screen, (255,0,0), p1, True)
        if p2: pygame.draw.polygon(screen, (255,0,0), p2, True)
    

class myRect(pygame.Rect):
    allRects = []
    def __init__(self, x, y, w, h, depth = 1, color = (255,0,0)):
        super().__init__(x, y, w, h)
        self.depth = depth
        self.ax = 0
        self.vx = 0
        self.ay = -gravity
        self.vy = 0
        self.color = color

        self.allRects.append(self)
        pass

    def move_ip(self, x, y):
        pygame.Rect.move_ip(self, x, y)
        pass

    def inflate_ip(self, x, y):
        if self.width + x  >= 2 and self.height + y >= 2:
            pygame.Rect.inflate_ip(self, x, y)
        pass

    def draw(self):
        """ Docstring for draw() """
        points = [self.topleft, self.topright, self.bottomright, self.bottomleft]
        pygame.draw.lines(screen, self.color, True, points)
        pass


# rect = myRect(190,190,20,20)
cube = myCube(0, 10, 0, 10, 0)
# lCube2 = myCube(100, 100, 0, 40, 0)

# Updates the screen and all objects in it
def update():
    screen.fill(pygame.Color('black'))  # Apaga tudo o que tem na tela pintando de cor preta
    dirty_rect = []
    for cube in myCube.allCubes:
        cube.draw()
    for r in myRect.allRects:
        r.draw()
    
    x = 200*m.cos(m.radians(myCube.pov.azimuth))
    y = 200*m.sin(m.radians(myCube.pov.azimuth))
    print(myCube.pov)

    pygame.display.update()
    
    # pygame.display.flip() # Atualiza todos os objetos da janela
    pass

# Definição de uma função/método
# Loop principal do programa, aqui estará o que acontece com cada frame do Jogo
def looping():
    #screen.blit(background_image, [0,0]) # Apaga tudo o que tem na tela pintando o fundo com uma imagem
    for event in pygame.event.get(): # captura eventos (teclado e mouse)
        if event.type == pygame.QUIT: # Clique no X da janela
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Apertada a tecla ESC
            return False
    
    # print(p)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]: 
        myCube.pov.forward(1)
    if pressed[pygame.K_s]: 
        myCube.pov.forward(-1)
    if pressed[pygame.K_a]:
        myCube.pov.azimuth -= 1
    if pressed[pygame.K_d]: 
        myCube.pov.azimuth += 1
    if pressed[pygame.K_e]: 
        myCube.pov.sidestep(.3)
    if pressed[pygame.K_q]: 
        myCube.pov.sidestep(-.3)
    if pressed[pygame.K_UP]: 
        myCube.pov.elevation += 1
    if pressed[pygame.K_DOWN]: 
        myCube.pov.elevation -= 1
    if pressed[pygame.K_SPACE]: 
        myCube.pov.z += 1
    if pressed[pygame.K_v]: 
        myCube.pov.z -= 1

    update()
    #pygame.display.update() # Atualiza o frame na tela
    clock.tick(60) # FPS - frames per second / basicamente um delay
    return True

while looping():
    pass

# try:
#     while looping():
#         pass
# except Exception as e:
#     print("An unexpected error occurred. See below for error message:")
#     print(e)
#     print(e.file)
# finally:
#     pygame.quit()

    