import pygame # importa o modulo pygame
import random

pygame.init() # Inicialização do módulo pygame
clock = pygame.time.Clock() # Inicialização do clock do pygame

screen_size = (400,300) # Tamanbho da Janela
screen = pygame.display.set_mode(screen_size) # Cria a janela no OS

def colorPicker(name):
    try:
        return pygame.Color(name)
    except:
        print('Could find color with name {}. Returning Red.'.format(name))
        return pygame.Color('red')
    finally:
        pass

shape = pygame.Rect(0,0,20,20)
color = colorPicker('red')
ax, ay, vx, vy = [0,0,1,1]

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Apertada a tecla Space
            color = random.choice(list(pygame.color.THECOLORS.values()))
            # color = pygame.Color('gold')
        

    shape.x += vx
    shape.y += vy

    pygame.draw.rect(screen, color, shape )
    pygame.display.update() # Atualiza o frame na tela
    clock.tick(60) # FPS - frames per second / basicamente um delay
    return True
        
try:
    while looping():
        pass
except Exception as e:
    print("An unexpected error occurred. See below for error message:")
    print(e)
finally:
    pygame.quit()

    