import pygame
import ctypes
import time

# tela cheia 
import os 
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
 
# Define algumas cores colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
 
# Set the width and height of the screen [width, height]
user32 = ctypes.windll.user32

#1366 768- tamanho da minha tela
sizeX = user32.GetSystemMetrics(0)
sizeY = user32.GetSystemMetrics(1) 

size = sizeX,sizeY
screen = pygame.display.set_mode(size)
#print(sizeY)
#print(sizeX)

x = int(sizeX/2)
y = int(sizeY/2)


print(x)
print(x * 2)
print(y)

#nome da janela
pygame.display.set_caption("Calibração")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

i = 1
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
    dt = clock.tick(30)

    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        break
    
    screen.fill(BLACK)
    
    pygame.draw.rect(screen, WHITE, [px, py, 40, 40])
    pygame.display.flip()
    
    if(int(px) >= 0 and int(px) <= 1 ):
        time.sleep(3)
        
        i += 1
        if(i > 1):
            voltar = False
            
    if(direita):
        px += velocity * dt
        print(int(px))
        
    elif(voltar):
        px -= velocity * dt
        
    else:
        py += velocity * dt
        
    
    if(int(px) >= (x - 10) and int(px) <= (x)):
        print('metade')
        time.sleep(5)
        
    if(int(px) >= int(x * 2)- 40 and int(py) == 0):
        time.sleep(3)
        direita = False
        

    if(int(py) == y and  ((px) >= int(x * 2)- 100 or (px) <= int(x * 2)- 150 )):   
        time.sleep(3)
        #print('meio')
        py = y
        voltar = True
        
    
    if(int(py) >= x  and int(py)<= x + 5):
        direita = True
        
        
        

# Close the window and quit.
pygame.quit()

