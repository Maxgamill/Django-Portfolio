#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:08:55 2019

@author: Maxgamill
"""
import numpy as np
from scipy.special import expit
import os

class neuralNetwork:
    
    #Initialise the NN
    def __init__(self, inputNodes, hiddenNodes, outputNodes, learningRate):
        self.inodes  = inputNodes
        self.hnodes = hiddenNodes
        self.onodes = outputNodes
        self.lr = learningRate
        
        #Link weights to matricies: W_input->hidden (Wih) and W_hidden->output
        # (Who)
        #Weights inside the arrays are w_i_j where the link is from i to j in
        # the next layer... w11 w12 -> w12 w22 etc
        #Using random numbers with a variance related to the No. of nodes
        self.Wih = np.random.normal(
                0.0, pow(self.hnodes, -0.5),(self.hnodes, self.inodes)
                )
        self.Who = np.random.normal(
                0.0, pow(self.onodes, -0.5),(self.onodes, self.hnodes)
                )
        #Decides the threshold for signals to be passed
        self.activation_function = lambda x: expit(x)
        pass
    
    #Train the NN
    def train(self, inputs_list, targets_list, save=False):
        inputs = np.array(inputs_list, ndmin=2) .T
        targets = np.array(targets_list, ndmin=2) .T
        
        #Calculates signals into the hidden layer
        hidden_inputs = np.dot(self.Wih, inputs)
        #Calculates signals emergig from the hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        
        #Calculates signals into final output layer
        final_inputs = np.dot(self.Who, hidden_outputs)
        #Calculates the signals emergin from the final output layer
        final_outputs = self.activation_function(final_inputs)
        
        #Need to evaluate the error to train the model
        #Error is target - actual
        output_errors = targets - final_outputs
        
        #Hidden layer error is the output_errors split by weights, recombined
        # at hidden nodes
        hidden_errors = np.dot(self.Who.T, output_errors)
        
        #Update the weights of the links between the input and hidden layers
        self.Who += self.lr * np.dot((output_errors * final_outputs * 
                                      (1 - final_outputs)), np.transpose(hidden_outputs))
        
        #Update the weights of the links between the output and final layers
        self.Wih += self.lr * np.dot((hidden_errors * hidden_outputs * 
                                      (1 - hidden_outputs)), np.transpose(inputs))
        if save == True:
            np.savetxt('trainedWih',self.Wih)
            np.savetxt('trainedWho',self.Who)
        else:
            pass
        pass
    
    #Query the NN
    def query(self, inputs_list, trainedNetwork=False):
        #Converts inputs_list into 2D array
        inputs = np.array(inputs_list, ndmin=2) .T
        if trainedNetwork==False: 
            #Calculate signals into hidden layer
            hidden_inputs = np.dot(self.Wih, inputs)
            #Calculate the signals emerging from hidden layer
            hidden_outputs = self.activation_function(hidden_inputs)
            
            #Calculate signals into final output layer
            final_inputs = np.dot(self.Who, hidden_outputs)
        else:
            #Opens 2 files to base NN weights off. Must be named as seen.
            Wih_file = open(os.getcwd()+'/maxSite/neuralNet/trainedWih','r')
            #Wih_file = open('/var/www/djangoSite/maxSite/neuralNet/trainedWih','r')
            Wih_list = Wih_file.readlines()
            Wih_file.close()
            Wih = []
            for i in range(len(Wih_list)):
                temp = list(Wih_list[i].split(' '))
                Wih.append(temp)
            Wih = np.array(Wih, dtype=np.float64)
            
            Who_file = open(os.getcwd()+'/maxSite/neuralNet/trainedWho','r')
            #Who_file = open('/var/www/djangoSite/maxSite/neuralNet/trainedWho','r')
            Who_list = Who_file.readlines()
            Who_file.close()
            Who = []
            for i in range(len(Who_list)):
                temp = list(Who_list[i].split(' '))
                Who.append(temp)
            Who = np.array(Who, dtype=np.float64)
            
            hidden_inputs = np.dot(Wih, inputs)
            #Calculate the signals emerging from hidden layer
            hidden_outputs = self.activation_function(hidden_inputs)
            
            #Calculate signals into final output layer
            final_inputs = np.dot(Who, hidden_outputs)
        #Calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs
        pass
    
class miscFunctions:    
    
    def compress(img_array,compressed_res):
        '''Compress a 2D square array into a smaller size'''
        img_list = []
        ratio = int(len(img_array[0])/compressed_res)
        
        for x in range(compressed_res):
            for y in range(compressed_res):
                comp_array = img_array[x*ratio:(x+1)*ratio,y*ratio:(y+1)*ratio]/ratio**2
                segment_val = np.sum(comp_array)
                img_list.append(segment_val)
            
        img_data = np.array(img_list)
        img_data= img_data.reshape(compressed_res,compressed_res)
        return img_data