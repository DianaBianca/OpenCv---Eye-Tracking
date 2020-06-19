import cv2
import numpy as np

def roi(frame,points,th,dil,tamanho):
    
    roi = frame[points[0][1]:points[1][1], points[0][0]:points[1][0]]
    
    kernel = np.ones((5,5),np.uint8)#matriz, tipo
    
    blur = cv2.GaussianBlur(roi,(5,5),10)
    
    ret, thresh = cv2.threshold(blur,th ,255,cv2.THRESH_TOZERO)#imagem, valor,luminosidade,como será o threshold
    
    dilatacao = cv2.dilate(thresh,kernel, iterations = dil )
    
    edged = cv2.Canny(dilatacao, 30, 200)
    rows, cols, _ = roi.shape
    contours, _ = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        area= cv2.contourArea(cnt)
        if area <= tamanho :
            cv2.rectangle(dilatacao, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #cv2.line(dilatacao, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
            #cv2.line(dilatacao, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
            print("COORDENADAS ------> ", x, " , " , y)

    
    cv2.imshow("roi", dilatacao)
    tamanho_frame(roi)   

def tamanho_frame(frame):
    
    # get dimensions of image
    dimensions = frame.shape
     
    # height, width, number of channels in image
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2]
    print('Image Dimension    : ',dimensions)
    print('Image Height       : ',height)
    print('Image Width        : ',width)
    print('Number of Channels : ',channels)
