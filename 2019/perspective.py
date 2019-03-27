import pygame # importa o modulo pygame
import math as m

def perspectiveChange(x, y, z, angle):
    x_ = (x-y)*m.cos(angle)
    y_ = z-(x+y)*m.sin(angle)
    return (x_, y_)

#Globals
gravity = -0.1 #pixels per frame
objList = []

#Init
pygame.init() # Inicialização do módulo pygame
clock = pygame.time.Clock() # Inicialização do clock do pygame

screen_size = (400,400) # Tamanbho da Janela
screen = pygame.display.set_mode(screen_size) # Cria a janela no OS

class myShape(p)

class myRect(pygame.Rect):
    def __init__(self, x, y, width, height, depth = 1, color = (255,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.depth = depth
        self.ax = 0
        self.vx = 0
        self.ay = -gravity
        self.vy = 0
        self.color = color
        objList.append(self)
        self.draw()
        pass

    def draw(self):
            # pygame.draw.circle(screen, self.color, self.center, int(self.width*1.41/2))
            #pygame.draw.rect(screen, self.color, self)
            pygame.draw.line(screen, self.color, self.topleft, self.topright)
            pygame.draw.line(screen, self.color, self.topright, self.bottomright)
            pygame.draw.line(screen, self.color, self.bottomright, self.bottomleft)
            pygame.draw.line(screen, self.color, self.bottomleft, self.topleft)
            points = [self.topleft, self.topright, self.bottomright, self.bottomleft]
            pygame.draw.lines(screen, , False, points, lineThickness)
            pass

rect = myRect(190,190,20,20)

def updateAll():
    dirty_rect = []
    for r in objList:
        r.draw()
        dirty_rect.append(r)
    if len(dirty_rect) > 0: 
        pygame.display.update(dirty_rect) # Atualiza todos os objetos da janela
    else:
        pygame.display.update()
    
    # pygame.display.flip() # Atualiza todos os objetos da janela
    pass

# Definição de uma função/método
# Loop principal do programa, aqui estará o que acontece com cada frame do Jogo
def looping():
    screen.fill((0, 0, 0))  # Apaga tudo o que tem na tela pintando de cor preta
    #screen.blit(background_image, [0,0]) # Apaga tudo o que tem na tela pintando o fundo com uma imagem
    for event in pygame.event.get(): # captura eventos (teclado e mouse)
        if event.type == pygame.QUIT: # Clique no X da janela
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Apertada a tecla ESC
            return False
    
    # print(p)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]: 
        rect.inflate_ip(2, 2)
    if pressed[pygame.K_s]: 
        rect.inflate_ip(-2, -2)
    if pressed[pygame.K_a]: rect.move_ip(-3,0)
    if pressed[pygame.K_d]: rect.move_ip(3,0)

    updateAll()
    #pygame.display.update() # Atualiza o frame na tela
    clock.tick(60) # FPS - frames per second / basicamente um delay
    return True
        

while looping():
    pass
pygame.quit()
