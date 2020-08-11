import numpy as np
# Trabalho 1

# Hidrelétrica 1

# K 
meses = 12
k = meses - 2

# Delta: valor que pode ser modificado, defalut = 1
delta = 1
# Rendimento do Conjunto Turbina-Gerador:
n = 0.88
# Limite Inferior e Superior para o volume d'aguá armazenado no reservatório (em 10^6 m³):
xMax = 21200
xMin = 12800
# Capacidade Mínima e Máxima de Engolimento das Turbinas(m³/seg):
uMax = 10000
uLimite = 7955
uMin = 1400
# Criação de Possíveis Valores para Xk e Uk
TamanhoXk = xMax-xMin
#TamanhoXk = int(TamanhoXk/10) # De 8400 para 840
delta = TamanhoXk
Xk = []
for i in range(meses):
    xka = []
    for j in range (TamanhoXk):
        xka.append(xMin+j)
    Xk.append(xka)

TamanhoUk = uMax-uMin
#TamanhoUk = int(TamanhoUk/10)
Uk = []
for i in range(meses):
    Uka = []
    for j in range(TamanhoUk):
        Uka.append(uMin+j)
    Uk.append(Uka)
# Criando F(Xn), onde tem todos os valores possíveis
Fxn = [[0]*TamanhoXk]*(k+1)
dezember = [1500]*TamanhoXk
#dezember = [15000]*TamanhoXk

print(dezember)
Fxn.append(dezember)
print(len(Fxn))
# Demanda Dk:
#dk = [280,250,230,250,260,280,280,260,260,280,300,310]
dk = [2800,2500,2300,2500,2600,2800,2800,2600,2600,2800,3000,3100]
# Vazão Média Mensal:
#vk = [91,76,93,67,43,35,28,25,21,22,35,41]
vk = [9107,7688,9358,6794,4303,3533,2867,2557,2171,2247,3517,4180]
# P:
p = n*9.82*0.001

# Criação da Matriz Pixk:

Pixk = []
for i in range(meses):
    pxk = []
    for j in range (TamanhoUk):
        pxk.append(0)
    Pixk.append(pxk)

# Função da geração hidroelétrica com defluências agregadas h(x,u):
def h(x,u):
    if u <= uLimite and u > uMin:
       h1eh2 = h1(x)-h2(u)
       defluencia = p*h1eh2*u
       return defluencia
    elif u > uLimite:
        h1eh2 = h1(x)-h2(u)
        defluencia = p*h1eh2*uLimite
        return defluencia
    else:
        return 0

# Função H1(x):
def h1(x):
    x1 = (0.15519*0.01)*x
    x2 = (0.17377*0.0000001)*x*x
    return 303.04 + x1 - x2

# Função H2(u):
def h2(u):
    u1 = (0.2213*0.001)*u
    return 279.84 + u1

# Função ek(xk,uk):
def ek(x,u,d):
    resultadoH = h(x,u)
    if resultadoH >= d:
        custo = c(0)
        return custo
    elif resultadoH < d:
        g = d - resultadoH
        custo = c(g)
        return custo

# Função de Usinas Térmicas que pode produzir energia a um custo c(g):
def c(g):
    return 64.8*g*g

# Função de Transição de Estados e(xk,uk)
def transicaoEstado(x,u,v):
    return x + (v - u)*2.6
    

# Função Fx(x+1):
def Fx(x, k):
    #print(x, ' ', k)
    if x >= 0 and x < TamanhoXk:
        return Fxn[k][x]
    else:
        return 0 
Faux = 0
u0Aux = 0
while(k >= 0):
    print('k = ', k)
    x = []
    x = Xk[k]
    for i in range(len(x)):
        #print(' Len x : ', i)
        Faux = 99999
        u = []
        u = Uk[k]
        for j in range(len(u)):
            xMaixUm = int(transicaoEstado(x[i],u[j],vk[k]))
            #index = int((xMaixUm-xMin)/delta)
            custo = ek(x[i],u[j],dk[k])
            #print(custo)
            final = Fx(xMaixUm,k+1)
            #print(final)
            FxuAux = custo + final
            #print('[LOG]: \n Custo = ', custo, '\n Final = ',final,'\n FxuAux = ',FxuAux )
            if FxuAux <= Faux:
                #print('sim', FxuAux)
                Faux = FxuAux
                u0Aux = u[j]
        Fxn[k][i] = Faux 
        Pixk[k][i] = u0Aux
    k = k-1

for i in range(len(Fxn)):
    linha = Fxn[i]
    print(linha)

for i in range(len(Fxn)):
    linha = Fxn[i]
    print('No mes ',i,'o custo de Fxn = ',min(linha))
