#!/var/www/djangoSite/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 14:37:47 2020

@author: Maxgamill
"""
from matplotlib.pyplot import imread
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import numpy as np
import base64
import maxSite.project_scripts.neuralNet as NN
import maxSite.project_scripts.spread as sp
import maxSite.project_scripts.ising as mag

def test(message):
    return 'The message: "' + message + '" successfully made it to the server!'

def trainedNetwork(img_file):
    input_nodes = 784
    hidden_nodes = 450
    output_nodes = 10
    learning_rate = 0.1
    
    # Gets the image file and reads it as 2D array
    img_array_raw = imread(img_file,0)
    img_array = img_array_raw[:,:,0]
    
    # Turns 2D img_array into the 28x28 format
    if len(img_array[0])==len(img_array[1])==28:
        pass
    else:
        img_array=NN.miscFunctions.compress(img_array, 28)
    img_data = 1 - img_array.reshape(input_nodes)
    img_data = (img_data * 0.99) + 0.01
    n = NN.neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    outputs = n.query(img_data, trainedNetwork=True)
    #index of highest value corresponds to outputs
    label = str(np.argmax(outputs))

    return f"The neural network guesses: {label}"

def sod(pop,fract,recovr,infections,numd,reps,reinfect):
    #Set variable data types
    pop = int(pop)
    fract = float(fract)
    recovr = float(recovr)
    infections = int(infections)
    reps = int(reps)
    reinfect = int(reinfect)
    numd = int(numd)

    #Run project script
    data,sdata,rdata = sp.infection(pop,fract,recovr,infections,numd,reps,reinfect)
    if reinfect == 0:
        title = "The Spread of a Non-Mutating Infectious Disease"
    else:
        title = "The Spread of a Mutating Infectious Disease"
    #Create matplotlib graph using project result
    fig = plt.figure()
    plt.plot(range(numd),data,label='Infected')
    plt.plot(range(numd),sdata,label='Susceptible')
    plt.plot(range(numd),rdata,label='Total Infected')
    plt.title(title)
    plt.xlabel('Number of Days')
    plt.ylabel('Number of Students')
    plt.legend()
    return fig

def ising(N,Temp,B,m,c,p):
    #Set variable data types
    N = int(N)
    Temp = float(Temp)
    B = float(B)
    m = float(m)
    c = int(c)
    p = int(p)
    T = np.linspace(0.01,Temp,p)
    #Compute Ising model values and arrange into an array
    vals = np.zeros((len(T),6))
    for i in range(len(T)):
        vals[i]+=mag.BFieldSpinStates(N,T[i],B,m,c)
    #Build the graphs as a subplot
    fig = plt.figure(figsize=[6.4,18])
    plt.subplot(311)
    plt.plot(T,mag.magU(B,T),label='Theoretical')
    plt.plot(T,vals[:,2],'go',label='Monte Carlo')
    plt.title('Internal Energy of a Ferromagnetic Solid in a Magnetic Field of '+str(B)+' T')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Internal Energy (a.u.)')
    plt.legend()
    plt.subplot(312)
    plt.plot(T,mag.magCv(B,T),label='Theoretical')
    plt.plot(T,vals[:,4]*N,'go',label='Monte Carlo')
    plt.title('Heat Capacity of a Ferromagnetic Solid in a Magnetic Field of '+str(B)+' T')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Heat Capacity (a.u.)')
    plt.legend()
    plt.subplot(313)
    plt.plot(T,mag.magS(B,T),label='Theoretical')
    plt.plot(T,vals[:,5],'go',label='Monte Carlo')
    plt.title('Entropy of a Ferromagnetic Solid in a Magnetic Field of '+str(B)+' T')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Entropy (a.u.)')
    plt.legend()

    return fig

