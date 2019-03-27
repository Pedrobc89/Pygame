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
        self.x += value*m.sin(m.degrees(self.azimuth))
        self.y += value*m.cos(m.degrees(self.azimuth))
        pass

    def sidestep(self, value):
        """moves the point of view one step to the right (left if value is negative)"""
        self.x += value*m.cos(m.degrees(self.azimuth))
        self.y += value*m.sin(m.degrees(self.azimuth))
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
        """The center (x, y) of cube."""
        return (self.x, self.y)
    @center.setter
    def center(self, value):
        x, y = value
        self.x = x
        self.y = y
    
    @property
    def points(self):
        """The list of the vertices coordinates of the cube."""
        #TODO: calculate the vertices coordinates based on perspective
        topleft = (self.x-self.size/2, self.y-self.size/2)
        topright = (self.x+self.size/2, self.y-self.size/2)
        bottomleft = (self.x-self.size/2, self.y+self.size/2)
        bottomright = (self.x+self.size/2, self.y+self.size/2)

        topleft2 = (self.x-self.size/2, self.y-self.size/2)
        topright2 = (self.x+self.size/2, self.y-self.size/2)
        bottomleft2 = (self.x-self.size/2, self.y+self.size/2)
        bottomright2 = (self.x+self.size/2, self.y+self.size/2)

        return [topleft, topright, bottomright, bottomleft]

    def draw(self):
        pygame.draw.polygon(screen, (255,0,0), self.points, True)
    

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
cube = myCube(200, 200, 0, 40, 0)
lCube2 = myCube(100, 100, 0, 40, 0)

# Updates the screen and all objects in it
def update():
    screen.fill(pygame.Color('black'))  # Apaga tudo o que tem na tela pintando de cor preta
    dirty_rect = []
    for cube in myCube.allCubes:
        cube.draw()
    for r in myRect.allRects:
        r.draw()
    
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
        myCube.pov.sidestep(1)
    if pressed[pygame.K_q]: 
        myCube.pov.sidestep(-1)
    if pressed[pygame.K_UP]: 
        myCube.pov.elevation += 1
    if pressed[pygame.K_DOWN]: 
        myCube.pov.elevation -= 1

    print(myCube.pov)
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

    