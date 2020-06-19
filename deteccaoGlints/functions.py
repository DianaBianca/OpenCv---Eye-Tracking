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
    contours,hier = cv2.findContours = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

    for cnt in contours:
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<600) :  
            hull = cv2.convexHull(cnt)    
            hull = cv2.approxPolyDP(hull,0.1*cv2.arcLength(hull,True),True)
            if len(hull)==4:
                cv2.drawContours(roi,[hull],0,(0,255,0),2)
        
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
