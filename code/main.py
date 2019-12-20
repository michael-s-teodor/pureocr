#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Mihnea S. Teodorescu & Moe Assaf, University of Groningen
"""

#### Libraries
# Own libraries
from preprocessor import Preprocessor
from recogniser import Recogniser
from network import Network

#### Main
img = Preprocessor("../samples/3.jpg")
recogniser = Recogniser()
img.process_image()
img.convert_to_binary()
#img.preview_image()
img.preview_chars()
