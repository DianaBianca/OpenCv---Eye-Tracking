import pygame
import ctypes
import time
import os
import sys
from PIL import Image

size=(800,600)
FORMAT = "RGBA"

def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)

def get_gif_frame(img, frame):
    img.seek(frame)
    return  img.convert(FORMAT)


def init():
    return pygame.display.set_mode(size)

def exit():
    pygame.quit()

def main(screen, path_to_image,px,py):
    gif_img = Image.open(path_to_image)
    
    current_frame = 0
    clock = pygame.time.Clock()
    while True:
        imagem = pil_to_game(get_gif_frame(gif_img, current_frame))
        # Recupera as dimensoes da imagem
        w, h = imagem.get_size()

        # Escalas da imagem
        scales = [ 300, 300 ]
        for s in scales:
            frame = pygame.transform.smoothscale( imagem, (w-s, h-s) )
            screen.blit(frame, (px, py))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        current_frame = (current_frame + 1) % gif_img.n_frames

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    try:
        screen = init()
        main(screen, sys.argv[0])
    finally:
        exit()

    
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
    #screen.fill(BLACK)
    # chamamos o tick do relógio para 30 fps
    # e armazenamos o delta de tempo
    dt = clock.tick(20)

    while i != 11 :

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        screen.fill(BLACK)
        
        main(screen, "giif.gif",px,py)
        time.sleep(5)#tempo para a calibração de cada ponto
        
        if( i < 4 ):        
            px += nextx            
            
        elif(i < 7):
            if(i == 4):
                print('i == 4')
                py += nexty - 20
               
            else:
                px -= nextx 
                         
        elif(i > 6) :            
            if(i == 7):
                py += nexty - 30
                print('i == 7')
                
            else:
                px += nextx 
        i += 1           

# Close the window and quit.
pygame.quit()
