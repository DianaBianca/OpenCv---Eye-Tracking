import cv2
import numpy as np
import functions as f 

points = []
cropping = False

def nothing(x):
    pass

#criar janela de trackbars
cv2.namedWindow('trackbars')

#criar as trackbars
cv2.createTrackbar('th','trackbars',1,255, nothing)#nome,onde sera criado, valor inicial, val final, função)
cv2.createTrackbar('dil','trackbars',1,255, nothing)
cv2.createTrackbar('tamanho','trackbars',1,255,nothing)
def click_and_drop(event, x, y, flags, param):
    global points, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        points = [[x, y]]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        points.append([x, y])
        cropping = False
        

video = cv2.VideoCapture("olhos.mp4")
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", click_and_drop)

while (True):
    retval, frame = video.read()
    
    #recuperar trackbar
    th = cv2.getTrackbarPos('th','trackbars')#nome,onde a track ta
    dil = cv2.getTrackbarPos('dil','trackbars')
    tamanho = cv2.getTrackbarPos('tamanho','trackbars')
    # checando se o frame é válido
    if not retval:
        # Restart video.
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
       
    cv2.imshow("frame", frame)
    
    #se existir os dois pontos selecionados no video
    if len(points) == 2:
        
        f.roi(frame, points, th, dil,tamanho)
                    
    cv2.waitKey(33)
    
cv2.destroyAllWindows()
