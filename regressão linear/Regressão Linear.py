import numpy as np
import matplotlib.pyplot as plt

x = np.array([0,1,2,3,4,5,6,7]) # vetor com os valores de x
y = np.array([0.32,0.12,0.21,0.47,1,0.76,2,7]) # vetor com os valores de y

p1 = np.polyfit(x,y,2) # fornece os valores do intercepto e a inclinação

yfit = p1[0] * x + p1[1] # calcula os valores preditos
yresid = y - yfit # resíduo = valor real - valor ajustado (valor predito)
SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
SQtotal = len(y) * np.var(y) # número de elementos do vetor y vezes a variância de y
R2 = 1 - SQresid/SQtotal # coeficiente de determinação

print(p1) # imprime o intercepto e a inclinação
print(R2) # imprime coeficiente de determinação

plt.plot(x,y,'o')
plt.plot(x,np.polyval(p1,x),'g--')
plt.xlabel("x")
plt.ylabel("y")
plt.show()

