#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 00:57:23 2019

@author: welberth
"""

import matplotlib.pyplot as plt
import numpy as np

n_a = 5   # number of alternatives
n_q = 10   # number of questions
al = list(range(1,n_a))

gab = np.random.choice(al,n_q)

# Simulate extracting a random sample n times

n=2_000_000 #numero de vezes que o experimento é repetido

# Running the experiment

historico = []

for i in range(n):
    chute = np.random.choice(al,n_q)
    acerto = len([i for i, j in zip(gab, chute) if i == j])
    historico.append(acerto)
#ploting the histogram
    
plt.hist(historico)
