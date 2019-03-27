import pygame
import math

pygame.init()
s_size = (400,300)
screen = pygame.display.set_mode(s_size)
done = False
is_blue = True
x = 30
y = 30
p1 = None
p2 = None 
gravity = (0.1, -math.pi/2)
elasticity = 0.75
r_list = []

clock = pygame.time.Clock()


class nRect(pygame.Rect):
        def __init__(self, *args, **kwargs):
                self.hp = 1000
                self.color = (0,0,255) #Default Color Blue
                self.movable = True #Default movable
                if 'movable' in kwargs:
                    self.movable = kwargs['movable']
                if 'image' in kwargs:
                    self.image = kwargs['image']
                if 'color' in kwargs:
                    self.color = kwargs['color']

                self.speed = 0
                self.angle = 0
                r_list.append(self)
                super().__init__(*args, **kwargs)
                self.x_f = float(self.x)
                self.y_f = float(self.y)
                pass
        
        def bounce(self):
            w, h = s_size
            bounce = False
            if self.x_f >= w-self.width:
                self.x_f = w - self.width
                self.angle = math.pi-self.angle
                bounce = True
            elif self.x_f <= 0:
                self.x_f = 0
                self.angle = math.pi-self.angle
                bounce = True
            
            if self.y_f >= h-self.h:
                self.y_f = h - self.height
                self.angle = -self.angle
                bounce = True

            elif self.y_f <= 0:
                self.y_f = 0
                self.angle = -self.angle
                bounce = True
            
            if bounce:
                self.speed*=.75
                self.hp -= 50
            return bounce

        def move_to(self, x, y):
                self.center = (x, y)
                pass

        def move_vector(self):
            if self.movable:
                if self.hp <= 0: 
                    r_list.remove(self)
                    return
                self.speed, self.angle = addVector((self.speed, self.angle), gravity)
                x, y = getXYCoordinates((self.speed, self.angle))
                # print(self.speed)
                self.x_f += x
                self.y_f += y 
                self.x = self.x_f
                self.y = self.y_f
                self.bounce()
                self.collide()
            self.draw()
            pass
        
        def collide(self):
            for other in r_list:
                if self == other:
                    return False
                if self.colliderect(other):
                    self.hp -= 60
                    other.hp -= 100
                    # print("self.speed: {:0.2f} self.angle: {:0.2f} other.speed: {:0.2f} other.angle: {:0.2f}".format(self.speed, math.degrees(self.angle), other.speed, math.degrees(other.angle)))
                    distance, tangent = find_vector(self.center, other.center) 
                    self.angle = 2 * tangent - self.angle
                    other.angle = 2 * tangent - other.angle
                    (self.speed, other.speed) = (other.speed*elasticity, self.speed*elasticity)
                    angle = 0.5 * math.pi + tangent
                    self.x += 10*math.sin(angle)
                    self.y -= 10*math.cos(angle)
                    other.x -= 10*math.sin(angle)
                    other.x += 10*math.cos(angle)

                    
                

        def set_move(self, speed, angle):
            self.movable = True
            self.angle = angle
            self.speed = speed
            pass

        def move_x_axis(self):
                self.vx += self.ax
                self.centerx += self.vx
                if self.colliderect(otherRect):
                    print("Colide X")
                pass

        def move_y_axis(self):
                self.vy += self.ay
                self.centery += self.vy
                if self.colliderect(otherRect):
                    print("Colide Y")
                pass

        def draw(self):
                pygame.draw.circle(screen, self.color, self.center, int(self.width*1.41/2))
                # pygame.draw.rect(screen, (255,0,0), self)
                pass

drag = False

def addVector(v1, v2):
    p1 = getXYCoordinates(v1)
    p2 = getXYCoordinates(v2)
    return find_vector(p1, p2)
    

def getXYCoordinates(vector):
    m, a = vector
    x = math.cos(a) * m
    y = math.sin(a) * m
    return x, y

def find_vector(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x = x1 - x2
    y = y1 - y2
    m = math.hypot(y, x)
    a = math.atan2(y, x)
    return m, a

while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bullet = nRect(40, 240,20,20)
                    bullet.set_move(0, math.pi/2)
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # if myRect.collidepoint(event.pos): 
                            # Enable Drag
                            # drag = True
            # elif drag and event.type == pygame.MOUSEMOTION:
            #         x, y = event.pos
            #         myRect.move_to(x, y)
            # elif drag and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            #         drag = False
            elif  event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    p1 = event.pos
                    bullet = nRect(40, 240,20,20, movable=False)
            elif event.type == pygame.MOUSEMOTION:
                    p2 = event.pos
                    # if p1 is not None:
                        # print(find_vector(p1, p2))

            elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    p2 = event.pos
                    x, y = p2
                    x0, y0 = p1
                    pwr, ang = find_vector(p1, p2)
                    bullet.set_move(.07*pwr,ang)
                    p1 = None
            else:
                    # print(event)
                    pass
    
    pressed = pygame.key.get_pressed()
    # if pressed[pygame.K_UP]: myRect.move_ip(0,-3)
    # if pressed[pygame.K_DOWN]: myRect.move_ip(0,3)
    # if pressed[pygame.K_LEFT]: myRect.move_ip(-3,0)
    # if pressed[pygame.K_RIGHT]: myRect.move_ip(3,0)
    
    screen.fill((0, 0, 0))
    if is_blue: color = (0, 128, 255)
    else: color = (255, 100, 0)
    if p1 is not None and p2 is not None:
            x1, y1 = p1
            x2, y2 = p2
            p3 = (50, 250)
            p4 = (50-(x1-x2), 250-(y1-y2))
            pygame.draw.line(screen, (255,255,255), p3, p4)
    for r in r_list:
        r.move_vector()

        
        pygame.display.flip()
        clock.tick(60)