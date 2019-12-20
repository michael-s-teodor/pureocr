#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Mihnea S. Teodorescu & Moe Assaf, University of Groningen
"""

#### Libraries
# Third-party libraries
import numpy as np

#### Class
class Network(object):

    def __init__(self, sizes):
        # sizes = number of neurons per layer [input, hidden, ..., hidden, output]
        self.num_layers = len(sizes)
        self.sizes = sizes

        # Each neuron has one bias
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]

        # Each neuron from layer n has sizes[n-1] weights
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feed_forward(self, a):

        # This function returns the output of the network when a is applied
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w,a) + b)
        return a

    def back_propagation(self, input, output):
        a = self.feed_forward(input)
        d_cost = 2*(-1*a+output)
        d_sigmoid = sigmoid_derivative(a)
        d = d_cost * d_sigmoid

        dw = np.array(self.weights)

        for layer in range(len(self.weights), 4, -1):
            layer_out = sigmoid(np.dot(w,a) + b)
            dw[layer] = layer_out * d
        self.weights += dw


    def train(self, input, output, iterations):
        for i in range(iterations):
            if(iterations%100):
                print(self.feed_forward(input))
            self.back_propagation(input,output)

#### Helper functions
def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

def sigmoid_derivative(z):
    return z*(1-z) # Where z is the output = sigmoid(wx+b)

if __name__ == "__main__":
    print("Debugging starting..")
    inputs  = [[1,1],[0,1],[1,0],[0,0]]
    outputs = [1,0,0,0]
    network = Network([2,4,4,4,1])

    for input, output in zip(inputs, outputs):
        network.train(input,output,100)
