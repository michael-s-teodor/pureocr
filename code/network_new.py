#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Mihnea S. Teodorescu & Moe Assaf, University of Groningen
"""

#### Libraries
# Third-party libraries
import numpy as np

#### Class declaration
class NeuralNetwork:
    def __init__(self, x, y):
        self.layer = [[]] * 3
        self.layer[0] = x # input layer
        self.weights = [[]] * 3
        self.weights[1]= np.random.rand(self.layer[0].shape[1],4) # considering we have 4 nodes in the hidden layer
        self.weights[2] = np.random.rand(4,1)
        self.y = y
        self.output = np. zeros(y.shape)

    def feed_forward(self):
        for i in range(1,3):
            self.layer[i] = sigmoid(np.dot(self.layer[i-1], self.weights[i]))
        return self.layer[2]
        
    def back_prop(self):
        d_weights = [[],[],[]]

        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights[2] = np.dot(self.layer[1].T, 2*(self.y -self.output)*sigmoid_derivative(self.output))
        d_weights[1] = np.dot(self.layer[0].T, np.dot(2*(self.y -self.output)*sigmoid_derivative(self.output), self.weights[2].T)*sigmoid_derivative(self.layer[1]))

        # update the weights with the derivative (slope) of the loss function
        self.weights[1] += d_weights[1]
        self.weights[2] += d_weights[2]

    def train(self, x, y):
        self.output = self.feed_forward()
        self.back_prop()

#### Helper functions
def sigmoid(t):
    return 1/(1+np.exp(-t))

def sigmoid_derivative(p):
    return p * (1 - p)

#### Local main
if __name__ == "__main__":
    # Input
    x = np.array(([0,0,1],[0,1,1],[1,0,1],[1,1,1]), dtype=float)
    y = np.array(([0],[1],[1],[0]), dtype=float)

    NN = NeuralNetwork(x, y)
    for i in range(1500): # trains the NN 1,000 times
        if i % 100 ==0: 
            print ("for iteration # " + str(i) + "\n")
            print ("Input : \n" + str(x))
            print ("Actual Output: \n" + str(y))
            print ("Predicted Output: \n" + str(NN.feed_forward()))
            print ("Loss: \n" + str(np.mean(np.square(y - NN.feed_forward())))) # mean sum squared loss
            print ("\n")
    
        NN.train(x, y)
