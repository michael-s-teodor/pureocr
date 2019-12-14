from preprocessor import PreProcessor
from recogniser import Recogniser 
from network import Network


img = PreProcessor("samples/2.jpg")
recogniser = Recogniser()
#======================================#
img.processImage()
img.convertToBinary()
img.previewImg()
#======================================#
