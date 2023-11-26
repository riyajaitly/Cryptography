# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from math import floor
from codec import Codec, CaesarCypher, HuffmanCodes
import binascii

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None


    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)

        data = np.array(image)

        l = data.shape
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec(delimiter = self.delimiter) 
            #self.codec = Codec()  
        elif codec == 'caesar':
            self.codec = CaesarCypher(delimiter = self.delimiter, shift=3)
        elif codec == 'huffman':
            self.codec = HuffmanCodes(delimiter = self.delimiter)
        
        binary = self.codec.encode(message + self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary

            counter = 0
            r = 0

            bin_len = len(binary)
            
            #loops through array and saves image in new file  
            for r in range(l[0]):
                for j in range(l[1]):
                    for k in range(l[2]):
                        if counter < bin_len:
                            bin_char = binary[counter]
                            counter = counter + 1
                            if int(bin_char) == 0:
                                if data[r, j, k] % 2 == 1:
                                    if data[r, j, k] == 255:
                                        data[r, j ,k] = 0
                                    else:
                                        data[r, j, k] = data[r, j ,k] + 1
                            else:
                                if data[r, j, k] % 2 == 0:
                                    data[r, j , k] = data[r, j ,k] + 1
                        else:
                            break


        cv2.imwrite(fileout, data)

    #returns a decoded text message hidden in a given file using a specified codec               
    def decode(self, filein, codec):
        image = cv2.imread(filein)  

        data = np.array(image)

        l = data.shape 
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec(delimiter = self.delimiter) 
        elif codec == 'caesar':
            self.codec = CaesarCypher(delimiter = self.delimiter)
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False

        binary = ""

        for r in range(l[0]):
            for j in range(l[1]):
                for k in range(l[2]):
                    if data[r, j ,k] % 2 == 0:
                        binary = binary + str(0)
                    else:
                        binary = binary + str(1)
            
        binary_message = binary    
        decoded_message = self.codec.decode(binary)

        self.text = decoded_message
        self.binary = binary_message

            
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          
    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()
    
    