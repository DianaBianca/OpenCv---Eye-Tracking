import cv2
import numpy as np

import os

def creatDir(name, path=''):
    # checando se a pasta existe
    if not os.path.exists(f'{path}/{name}'):
        #se ela nao existir, criar
        os.makedirs(f'{path}/{name}')

lastName = ''
cap = cv2.VideoCapture(0)# 0 = camera principal, se tiver uma webcam integrada no notebook, usar 1 

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))


# criando o diretório train
creatDir('train')
# perguntando o nome
print("Qual o seu nome?")
# salvando o nome
name = input()

lastName = name
# criando um diretório para a pessoa
creatDir(name,'train')
qtd = os.listdir(f'train/{lastName}')
# salvando 
out = cv2.VideoWriter(f'train/{lastName}/{lastName}.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

while(True): 
    ret, frame = cap.read()
    
    if ret == True: 
       out.write(frame)
       # mostrando o resultado    
       cv2.imshow('frame',frame)
    
       # pessione q para interromper a gravação
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    
    else:
        break
    
cap.release()
out.release()

cv2.destroyAllWindows() 
