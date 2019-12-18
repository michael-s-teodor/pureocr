#### Libraries
# Own libraries
from preprocessor import Preprocessor
from recogniser import Recogniser 
from network import Network

#### Main
img = Preprocessor("samples/2.jpg")
recogniser = Recogniser()
img.process_image()
img.convert_to_binary()
img.preview_image()
