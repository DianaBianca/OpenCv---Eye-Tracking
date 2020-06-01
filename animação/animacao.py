import pygame
import ctypes
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
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

inicio = 25

nextX = x - inicio 
nextY = y - inicio 
print(nextX)
print(nextY)

#nome da janela
pygame.display.set_caption("Calibração")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

i = 1
py = 25
px = 25
speed = 3
# -------- Main Program Loop -----------

while done == False:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Set the screen background
    screen.fill(BLACK)
    
    pygame.draw.circle(screen,GREEN, [px,py], 25)
    pygame.display.flip()
    
    if(i <= 3):    
        px += nextX
        #pygame.display.flip()
        clock.tick(0.5)
        print(px, py)
        
    if((i < 7) and (i > 3)):
        py = y
        px -= nextX
        #pygame.display.flip()
        clock.tick(0.5)
        print(px, py)

    if(i == 7):
        py = x
        px += 25
        print(px, py)
        
        clock.tick(0.5)
        
    if(i > 7):
        py = x
        px += nextX
        print(px, py)
        #pygame.display.flip()
        clock.tick(0.5)
    
    i = i+1
   
# Close the window and quit.
pygame.quit()
