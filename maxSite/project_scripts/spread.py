#!/var/www/djangoSite/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:59:22 2020

@author: Maxgamill
"""

import numpy as np
import matplotlib.pyplot as plt


def infection(pop,fract,recovr,infections,numd,reps=1,reinfect=0):
    '''
    pop - population (int)
    fract - fraction of pop initialy immune (float)
    recovr - chance to recover each day (fraction) (float)
    infections - number of people the infection can spread to each day (int)
    numd - data range of epidemic (int)
    reps - number of simulation repeats (int)
    reinfect - model if the recovered can be infected again (1) or become immune (0) (int)
    
    This function simulates the spread of a disease within a population using the Monte Carlo Method. 
    
    Returns 3 numpy arrays:
    data - number of infected students each day.
    sdata - number of succeptable students each day.
    rdata - total number of people infected throughout the period of the epidemic.
    '''
    
    #set parameters
    seed = np.random.seed() # seed for random number generator
    data = np.zeros(numd) # 0's array for infected
    sdata = np.zeros(numd) # 0's array of susceptibles
    rdata = np.zeros(numd) # 0's array of removed
    
    
    # array P:0=immune, 1=susceptible, 2=infected
    for k in range(reps): # loop for repeat calc'n
        #set up P array with values 0, 1, and 2
        P=np.zeros(pop) # student array to zero     
        for i in range(len(P)): # choose susceptibles
            P[i]=1 # all susceptible
        fn = np.trunc(fract*pop) # make into integer
        n = 0
        while n < fn: # exact fract*pop immune
            ra = int(np.random.rand()*(pop-1)) # -1 as index from 0
            if P[ra] == 0: # <> not equal sign
                pass
            else:
                P[ra] = 0
                n = n+1
        n = 0
        while n < infections: # 1 succeptable becomes infected
            ra = int(np.random.rand()*(pop-1))
            if P[ra] == 1:
                P[ra] = 2
                n = 1
            else:
                pass
    
     #the main part of calculation follows
        remov=0 # number removed
        for j in range(numd): # loop over days
            for i in range(pop): # loop students
                if P[i] == 2: #spread infection
                    for ii in range(infections):
                        ra = int(np.random.rand()*(pop-1)) # infect new student
                        if P[ra]==1:
                            P[ra]=2
                            remov+=1 # number removed
                        else: 
                            pass
                else:
                    pass
                if np.random.rand() < recovr: # chance of recovery
                    ra = int(np.random.rand()*(pop-1))
                    if P[ra] == 2: 
                        P[ra] = reinfect 
                    else:
                        pass
                else:
                    pass
            # end loop i
            c=0
            s=0
            for i in range(pop): # find number infected
                if P[i] == 2: 
                    c += 1 
                else:
                    pass
                if P[i] == 1:
                    s += 1 
                else:
                    pass
            data[j] = data[j] + c # number infected
            sdata[j] = sdata[j] + s # number suscept
            rdata[j] = rdata[j] + remov
    num_infected = rdata*1.0/reps # total number of students infected in 40 days
    return data/reps,sdata/reps,rdata/reps








