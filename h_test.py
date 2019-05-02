import matplotlib.pyplot as plt
import numpy as np


all_samples=[]

# Simulate extracting a random sample n times

p=0.0106 # probabilidade de ocorrer 1 na população
s=21548 #tamanho da amostra
pop=433213 #tamanho da população
n=1000 #numero de vezes que o experimento é repetido


# Creating the null hipothesis population

p1=np.ones((int(round(pop*p)),), dtype=int)
p2=np.zeros(int(pop-round(pop*p),), dtype=int)
population=np.append(p1,p2)

# Running the experiment

for i in range(n):
    sample=np.random.choice(population,s,replace=False)
    prob=float(sum(sample))/len(sample)
    all_samples.append(prob)
    
#ploting the histogram
    
plt.hist(all_samples,20)
