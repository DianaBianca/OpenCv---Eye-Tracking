import cv2
import numpy as np
import matplotlib.pyplot as plt

points = np.array([[0,0,1],
                  [0.5,0,1],
                  [1,0,1],
                  [0,0.5,1],
                  [0.5,0.5,1],
                  [1,0.5,1],
                  [0,1,1],
                  [0.5,1,1],
                  [1,1,1]])

eyes = np.array([ [0,0,1],
                  [0.25,0,1],
                  [0.5,0,1],
                  [0,0.25,1],
                  [0.25,0.25,1],
                  [0.5,0.25,1],
                  [0,0.50,1],
                  [0.25,0.50,1],
                  [0.5,0.50,1]])

tamanhofixo=60 #tamanho dos targets

#plt.scatter(eyes[:,0],eyes[:,1], color='blue', s=tamanhofixo)
plt.scatter(points[:,0],points[:,1], color='red', s=tamanhofixo)


equation = np.ones((9, 6))#6 equações e 9 alvos

#pegar cada coordenada do olho e realizar a equação
for i, eye in enumerate(eyes):
    
    equation[i, :-1] = [eye[0]**2, eye[1]**2, eye[0]*eye[1], eye[0], eye[1]]
    
coeffsX = np.linalg.pinv(equation).dot(points[:, 0])
coeffsY = np.linalg.pinv(equation).dot(points[:, 1])

M = np.vstack((coeffsX, coeffsY))

eye = np.array([0.25, 0.15])
#Gaze estimation method
gaze = M.dot([eye[0]**2, eye[1]**2, eye[0]*eye[1], eye[0], eye[1], 1])

print(gaze)

a = gaze[0]
b = gaze[1]

plt.scatter(a,b, color='black', s=200)

plt.xlabel("x")
plt.ylabel("y")
plt.show()
