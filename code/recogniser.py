#### Libraries
# Own libraries
from network import Network

#### Class
net = Network([10000, 10, 10, 94])

class Recogniser():

    def __init__(self):
        pass
    
    def retrieve_char(self, img):

        # Compute the output of the neural network   
        output = net.feed_forward(img)

        # Determine the most likely outcome and return its ASCII value
        max = 0
        char = 0
        for i in range(94):
            if (max < output[i]):
                max = output[i]
                char = i
        return chr(char + 33)

    def return_texts(self, data):
        texts = []
        for img in range(len(data)):
            texts.append(self.retrieve_char(img))
        return texts
    