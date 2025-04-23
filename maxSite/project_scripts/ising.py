#!/var/www/djangoSite/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 14:26:07 2020

@author: Maxgamill
"""
import matplotlib.pyplot as plt
import numpy as np
import math

def magU(B,T,m=3.63,k=1):
    return -m*B*(np.exp(m*B/(k*T))-np.exp(-m*B/(k*T)))/(np.exp(m*B/(k*T))+np.exp(-m*B/(k*T)))

def magCv(B,T,m=3.63,k=1):
    return k*(m*B/(k*T)*2*(np.exp(m*B/(k*T))+np.exp(-m*B/(k*T)))**-1)**2

def magS(B,T,m=3.63,k=1):
    return k*np.log(np.exp(m*B/(k*T))+1) - (m*B/(k*T)*np.exp(m*B/(k*T))/(np.exp(m*B/(k*T))+1))

def BFieldSpinStates(N,T,B,m=3.63,c=2000):
    '''
    N - Number of sites
    T - Temperature
    B - Magnetic Field Strength
    m - Magnetic Moment
    c - Calculations per site
    '''
    L = int(N*c) # 2000 calcs / site
    k = 1.0 # Boltzmann const, in a.u.
    spin = np.zeros(N)
    # deltaE can take values ( -2mB, 0, 2mB), however, only the
    # positive value is used in the metropolis test, hence we define
    # probability P for the Metropolis test outside the loop.
    P = np.exp(-2*m*B/(k*T)) # prob’lty in Metropolis test.
    
    for k in range(N):
        spin[k] = -1 # initial distribution
    Enrg = -m*B*N # all spins aligned initially
    tot_Enrg = 0
    tot_Enrg2 = 0
    for num in range(L): # start Metropolis
        i = int(np.random.rand()*N) # choose spin at random
        DeltaE = -2*m*B*spin[i]
        # Metropolis test next
        if DeltaE <= 0 or np.random.rand() < P: # rand between 0 and 1
            spin[i] = -spin[i] # flip spin
            Enrg = Enrg + DeltaE # add in energy
        else:
            pass
        tot_Enrg = tot_Enrg + Enrg
        tot_Enrg2 = tot_Enrg2 + Enrg**2
        # end metropolis loop
    
    avE = tot_Enrg/L # total <E > , N sites
    avE2 = tot_Enrg2/L # total <E2> , N sites
    EnergyPerSpin= avE/N
    EnergySquaredPerSpin= avE2/N
    Cv = 1/(k*T**2)*(avE2 - avE**2)/N
    c=1
    for i in range(len(spin)-1):
        if spin[i] == spin[i+1]:
            pass
        else:
            c+=1 # count for number of spin groups
    states = math.factorial(N)/(math.factorial(c)*math.factorial(N-c))
    EntropyPerSpin = k*np.log(states)/N**2

    return avE,avE2,EnergyPerSpin,EnergySquaredPerSpin,Cv,EntropyPerSpin