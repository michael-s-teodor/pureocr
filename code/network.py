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

    def feedForward(self, a):
        
        # This function returns the output of the network when a is applied
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w,a) + b)
        return a
    
#### Helper functions
def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

def sigmoid_derivative(z):
    return np.exp(z) / (np.exp(z) + 1)**2
