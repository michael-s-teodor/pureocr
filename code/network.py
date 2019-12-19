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

    def backPropagation(self, input, output):
        a = self.feedForward(input)
        dCost = 2*(-1*a+output)
        dSigmoid = sigmoidDerivative(a)
        d = dCost*dSigmoid

        dw = np.array(self.weights)

        for layer in range(len(self.weights),4,-1):
            layerOut = sigmoid(np.dot(w,a) + b)
            dw[layer] = layerOut*d
        self.weights += dw


    def train(self, input, output, iterations):
        for i in range(iterations):
            if(iterations%100):
                print(self.feedForward(input))
            self.backPropagation(input,output)

#### Helper functions
def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

def sigmoidDerivative(z):
    #Where z is the output = sigmoid(wx+b)
    return z*(1-z)

if __name__ == "__main__":
    print("Debugging starting..")
    inputs  = [[1,1],[0,1],[1,0],[0,0]]
    outputs = [1,0,0,0]
    network = Network([2,4,4,4,1])

    for input, output in zip(inputs, outputs):
        network.train(input,output,100)
