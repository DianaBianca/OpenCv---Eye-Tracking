import pygame
import ctypes
import time
import os

# tela cheia 
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
 
# Define algumas cores colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Seta a largura e a altura da tela utilizada [width, height](só funciona para windows)
user32 = ctypes.windll.user32

#1366 768- tamanho da minha tela
sizeX = user32.GetSystemMetrics(0)
sizeY = user32.GetSystemMetrics(1) 

size = sizeX,sizeY
screen = pygame.display.set_mode(size)

nextx = int(sizeX/2) - 20
nexty = int(sizeY/2)

print(nextx)
print(nextx * 2)
print(nexty)

#nome da janela
pygame.display.set_caption("Calibração")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

i = 2
py = 0
px = 0
direita = True
voltar = False
# como o relógio do pygame trabalha
# em milissegundos, dividimos por 1000
# para manter os 100 pixels por segundo
velocity = 0.05


# criamos uma instância do relógio
clock = pygame.time.Clock()

# -------- Main Program Loop -----------

while done == False:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Set the screen background
    screen.fill(BLACK)
    # chamamos o tick do relógio para 30 fps
    # e armazenamos o delta de tempo
    dt = clock.tick(20)

    while i != 10 :

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, [px, py, 40, 40])
        pygame.display.flip()
        
        print('                  ')
        print('                  ')
        print('X ------------->',int(px))
        print('Y ------------->',int(py))
        print('valor de I : ', i)
        
        time.sleep(3)
        
        if( i < 4 ):            
            print('primeiro if')
            px += nextx            
            
        elif(i < 7):
            print('segundo if ***********')
            if(i == 4):
                print('i == 4')
                py += nexty
               
            else:
                px -= nextx 
                         
        elif(i < 10):
            print('terceiro if')
            
            if(i == 7):
                py += nexty
                print('i == 7')
                
            else:
                px += nextx 
        i += 1           

# Close the window and quit.
pygame.quit()
