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
        self.layer_num = len(sizes)+1
        self.layer = [[]] * self.layer_num
        self.input = x
        self.weights = [[]] * self.layer_num
        self.weights[0]= np.random.rand(self.input.shape[1], sizes[0])
        for i in range(1, self.layer_num-1):
            self.weights[i] = np.random.rand(sizes[i-1], sizes[i])
        self.weights[self.layer_num-1] = np.random.rand(sizes[self.layer_num-2], y.shape[1])
        self.y = y
        self.output = np.zeros(y.shape)

    def feed_forward(self):
        self.layer[0] = sigmoid(np.dot(self.input, self.weights[0]))
        for i in range(1, self.layer_num):
            self.layer[i] = sigmoid(np.dot(self.layer[i-1], self.weights[i]))
        return self.layer[self.layer_num-1]
    
    def rec_back_prop(self, d_weights, index):
        # d_weights[1] = np.dot(self.layer[0].T, 2*(self.y - self.output)*sigmoid_derivative(self.output))
        # d_weights[0] = np.dot(self.input.T, np.dot(2*(self.y - self.output)*sigmoid_derivative(self.output), self.weights[1].T)*sigmoid_derivative(self.layer[0]))
        
        # base case
        if (index == 0):
            return

        # recursive case
        self.rec_back_prop(d_weights, index-1)
    
    def back_prop(self):
        d_weights = [[]] * self.layer_num
        
        # recursive application of the chain rule to find derivative of the loss function with respect to each weight
        self.rec_back_prop(d_weights, self.layer_num-1)

        # update the weights with the derivative (slope) of the loss function
        for i in range(0, self.layer_num):
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

    # size of each hidden layer
    sizes = [4]

    NN = NeuralNetwork(x, y, sizes)
    for i in range(1001): # trains the NN 1,000 times
        if i % 100 ==0: 
            print ("for iteration # " + str(i) + "\n")
            print ("Input : \n" + str(x))
            print ("Actual Output: \n" + str(y))
            print ("Predicted Output: \n" + str(NN.feed_forward()))
            print ("Loss: \n" + str(np.mean(np.square(y - NN.feed_forward())))) # mean sum squared loss
            print ("\n")
    
        NN.train(x, y)
