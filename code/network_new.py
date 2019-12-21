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
    def __init__(self, x, y, sizes):
        self.layer_num = len(sizes)+2
        self.layer = [[]] * self.layer_num
        self.layer[0] = x # input layer
        self.weights = [[]] * self.layer_num
        # self.weights[1]= np.random.rand(self.layer[0].shape[1], 4) # considering we have 4 nodes in the hidden layer
        # self.weights[2] = np.random.rand(4, 1)
        self.weights[1]= np.random.rand(x.shape[1], sizes[0])
        for i in range(2, self.layer_num-1):
            self.weights[i] = np.random.rand(sizes[i-1], sizes[i])
        self.weights[self.layer_num-1] = np.random.rand(sizes[self.layer_num-3], y.shape[1])
        self.y = y
        self.output = np.zeros(y.shape)

    def feed_forward(self):
        for i in range(1, self.layer_num):
            self.layer[i] = sigmoid(np.dot(self.layer[i-1], self.weights[i]))
        return self.layer[self.layer_num-1]
    
    def back_prop(self):
        d_weights = [[]] * self.layer_num

        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights[2] = np.dot(self.layer[1].T, 2*(self.y -self.output)*sigmoid_derivative(self.output))
        d_weights[1] = np.dot(self.layer[0].T, np.dot(2*(self.y -self.output)*sigmoid_derivative(self.output), self.weights[2].T)*sigmoid_derivative(self.layer[1]))

        # update the weights with the derivative (slope) of the loss function
        for i in range(1, self.layer_num):
            self.weights[i] += d_weights[i]

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
    # input
    x = np.array(([0,0,1], 
                  [0,1,1],
                  [1,0,1],
                  [1,1,1]), dtype=float)
    
    # output
    y = np.array(([0],
                  [1],
                  [1],
                  [0]), dtype=float)

    # sizes of each hidden layer
    sizes = [4]

    NN = NeuralNetwork(x, y, sizes)
    for i in range(1500): # trains the NN 1,000 times
        if i % 100 ==0: 
            print ("for iteration # " + str(i) + "\n")
            print ("Input : \n" + str(x))
            print ("Actual Output: \n" + str(y))
            print ("Predicted Output: \n" + str(NN.feed_forward()))
            print ("Loss: \n" + str(np.mean(np.square(y - NN.feed_forward())))) # mean sum squared loss
            print ("\n")
    
        NN.train(x, y)
