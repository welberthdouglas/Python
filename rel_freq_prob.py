# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 21:15:22 2018

@author: Welberth
"""

import numpy as np
np.random.seed(8)



def aniver(n,t):
    ''' dá a probabilidade de se ter ao menos duas pessoas com aniversário no mesmo
    dia em um grupo de n pessoas com base em t testes'''
    
    sucesso=0
    for i in  range(t):
        test=np.random.randint(1,365,n)
        test_count =np.unique(test,return_counts=True)
        est=(test_count[1]>=2).sum()
        if est >= 1:
            sucesso +=1
    return sucesso/t
