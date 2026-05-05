#IMPORT's

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb

#Importanto em forma de url
url = 'https://raw.githubusercontent.com/Ujeverson/datasets/main/Salary_Data.csv'

dt = pd.read_csv(url)
dt.head()
print(dt.head())
print("------------------------------------------------------------")


x = dt['YearsExperience']
y = dt['Salary']

plt.scatter(x,y, color = 'purple')

plt.show()


#Criando modelo preditivo aplicando fórmulas (manualmente)

#Somatório dos valores de x
xs = x.sum()
print(xs)
print("------------------------------------------------------------")

#Somatório dos valores de y
ys = y.sum()
print(ys)
print("------------------------------------------------------------")

#Produto entre valores x e y
xy = x*y
print(xy)
print("------------------------------------------------------------")

#Somatório do produto entre valores de x e y
xys = (x*y).sum()
print(xys)
print("------------------------------------------------------------")

# X ao quadrado
x2 = x**2
print(x2)
print("------------------------------------------------------------")

#Soma dos valores de x ao quadrado
x2s = (x**2).sum()
print(x2s)
print("------------------------------------------------------------")

#Quantidade de linhas do dataframe
n = len(dt)
print(n)
print("------------------------------------------------------------")

#Determinando o valor de a
a = (n*xys - xs*ys)/(n*x2s - (xs)**2)
print(a)
print(round(a,2))
print("------------------------------------------------------------")

#Determinando o valor de b
b = (ys - a*xs) / n
print(b)
print(round(b,2))
print("------------------------------------------------------------")

print("A PARTIR DAQUI O BAGULHO FICA DOIDO")
print("------------------------------------------------------------")

#Predição de 5 anos de experiência
xyears = 5
ysalary = a*xyears + b
print(ysalary)
print("------------------------------------------------------------")

print("CRIANDO UMA LISTA VAZIA PARA ARMAZENAR OS VALORES DAS PREVISÕES DE X")
print("------------------------------------------------------------")
#Criando a lista
previsoes = []

#loop para calcular todos os valores do dataset e inserir em 'previsoes'
for elemento in x:
    ypred = a*elemento + b
    previsoes.append(ypred)

print(y-previsoes)
print("------------------------------------------------------------")

#Inserir as previsões no DataFrame
dt['predicoes'] = previsoes


print("------------------------------------------------------------")
print("------------------------------------------------------------")
print("UTILIZANDO O MÉTODO STATSMODELS")
print("------------------------------------------------------------")
print("------------------------------------------------------------")

#IMPORT's

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import seaborn as sb



#Importanto em forma de url
url = 'https://raw.githubusercontent.com/Ujeverson/datasets/main/Salary_Data.csv'

dt2 = pd.read_csv(url)
dt2.head()
print(dt2.head())
print("------------------------------------------------------------")

previsoes2 = sb.regplot(x="YearsExperience", y="Salary", data=dt2, color = 'purple')
print(previsoes2)
#Mostrando gráficamente com a função: plt.show()
plt.show()


'''xyears2 = 5
model.predict({'YearsExperience':xyears2})''' #SEGUINDO O SLIDE DEU ERRO.


#Corrigido com IA
# --- CORREÇÃO DO FINAL ---

# 1. Preparando os dados para o Statsmodels
# O Statsmodels não adiciona o intercepto (b) automaticamente, precisamos do add_constant
X = sm.add_constant(dt2['YearsExperience']) 
y = dt2['Salary']

# 2. Criando e treinando o modelo (Ordinary Least Squares - OLS)
model = sm.OLS(y, X).fit()

# 3. Preparando o valor para predição
# Precisamos passar o valor 5 acompanhado da constante 1
entrada_predicao = [1, 5] 

# 4. Fazendo a predição
previsao = model.predict(entrada_predicao)

print(f"Resultado do Statsmodels para 5 anos: {previsao[0]}")
print("------------------------------------------------------------")
# Opcional: Ver o resumo estatístico completo do modelo
# print(model.summary())
