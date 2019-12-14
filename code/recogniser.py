from network import Network

net = Network([10000,10,10,94])

class Recogniser():

    def __init__(self):
        pass
    
    def retrieveChar(self,img):    
        output = net.feedForward(img)

        max = 0
        char = 0
        for i in range(94):
            if (max < output[i]):
                max = output[i]
                char = i
        return chr(char + 33 )

    def returnTexts(self,data):
        texts = []
        for img in range(len(data)):
            texts.append(self.retrieveChar(img))
        return texts

        
    # Compute the output of the neural network

    # Determine the most likely outcome and return its ASCII value
    