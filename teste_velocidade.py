import pygame
import ctypes
import time
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
user32 = ctypes.windll.user32

#1366 768- tamanho da minha tela
sizeX = user32.GetSystemMetrics(0)
sizeY = user32.GetSystemMetrics(1) # tirando um pedaço que ultrapassa a tela

size = sizeX,sizeY
screen = pygame.display.set_mode(size)
#print(sizeY)
#print(sizeX)

x = int(sizeX/2)
y = int(sizeY/2)

nextX = x  
nextY = y 
print(nextX)
print(nextX * 2)
print(nextY)

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
    
    if(px == 0 and py == 0):
        #time.sleep(5)
        print('inicio')
        
    if(direita):
        px += velocity * dt
        print(int(px))
        
    elif(voltar):
        px -= velocity * dt
        
    else:
        py += velocity * dt
        
    
    if(int(px) >= (nextX -3) and int(px) <= (nextX)):
        print('metade')
        #time.sleep(5)
        
    if(int(px) >= (nextX * 2)- 40):
        #time.sleep(5)
        #print('fim primeira linha')
        direita = False

    if(py >= y - 2 and py <= y ):   
        #time.sleep(5)
        py = y
        #print('meio')
        voltar = True
        #time.sleep(5)
        
    

    

    

# Close the window and quit.
pygame.quit()

