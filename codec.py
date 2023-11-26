# codecs
import numpy as np

class Codec():
    
    def __init__(self, delimiter):
        self.name = 'binary'
        #self.delimiter = '#'
        self.delimiter = delimiter

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')
    # convert binary data into text
    def decode(self, data):
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter):
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte,2))       
        return text 

class CaesarCypher(Codec):
    def __init__(self, delimiter, shift=3):
        self.name = 'caesar'
        self.delimiter = '#'  
        self.shift = shift    
        self.chars = 256      # total number of characters
    # convert text into binary form
    # your code should be similar to the corresponding code used for Codec
    def encode(self, text):
        data = ''
        #CODE THIS PART
        for char in text:
            data += chr((ord(char) + self.shift) % 256)

        return ''.join([format(ord(i), "08b") for i in data])

    
    # convert binary data into text
    # your code should be similar to the corresponding code used for Codec
    
    def decode(self, data): 
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter):
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte,2))  
         

        #CODE THIS PART
        dataText = ""
        for char in text:
            dataText += chr((ord(char) - self.shift) % 256)

        return dataText


# a helper class used for class HuffmanCodes that implements a Huffman tree

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''
        
class HuffmanCodes(Codec):
    def __init__(self, delimiter):
        self.nodes = None
        self.data = {}
        self.name = 'huffman'
        self.delimiter = '#'

    # make a Huffman Tree    
    def make_tree(self, data):
        # make nodes
        nodes = []
        for char, freq in data.items():
            nodes.append(Node(freq, char))
            
        # assemble the nodes into a tree
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)

            # pick two nodes with the lowest frequencies
            left = nodes[0]
            right = nodes[1]

            # assign codes
            left.code = '0'
            right.code = '1'

            # combine the nodes into a tree
            root = Node(left.freq+right.freq, left.symbol+right.symbol,
                        left, right)

            # remove the two nodes and add their parent to the list of nodes
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(root)
        return nodes

    # traverse a Huffman tree
    def traverse_tree(self, node, val, modify):
        next_val = val + node.code
        if (node.left):
            self.traverse_tree(node.left, next_val, modify)
        if (node.right):
            self.traverse_tree(node.right, next_val, modify)
        if (not node.left and not node.right):
            # modifies code, is store it in dictionary that we use later
            modify[node.symbol] = next_val

    # convert text into binary form
    def encode(self, text):
        data = ''
        # create a dictionary named d and store character their frequecy in it.
        d = dict()
        # loop to set values of dictionary.
        for letter in text:
            d.setdefault(letter, 0)
            d[letter] += 1
        # call make_tree function it will create nodes for us and we can take its first value since
        # returned will contain only one element.
        self.nodes = self.make_tree(d)[0]
        # this will create a dictionary that store character and their encoded form.
        modify = dict()
        self.traverse_tree(self.nodes,'', modify)

        #create binary text and return it using dictionary modify
        for letter in text:
            data += modify[letter] 
        return data

     #convert binary data into text
    def decode(self, data):
        text = ""
        # get the nodes
        update = self.nodes
        #loop through it using length of data
        for i in range(len(data)):
            # move to the left if equal to 0
            if data[i] == '0':
                update = update.left
            #move right
            else:
                update = update.right
            #add text and set update equal to nodes
            if (update.left==None and update.right==None):
                text += update.symbol
                update = self.nodes
        
        #formats output correctly
        dataText = ""
        for char in text:
            if char == "#":
                break
            else:
                dataText = dataText + str(char)

        # return the decoded text
        return dataText

"""
# driver program for codec classes
if __name__ == '__main__':
    text = 'hello'
    #text = 'Casino Royale 10:30 Order martini'
    print('Original:', text)

    c = Codec()
    binary = c.encode(text + c.delimiter)
    print('Binary:',binary)
    data = c.decode(binary)
    print('Text:',data)

    cc = CaesarCypher()
    binary = cc.encode(text + cc.delimiter)
    print('Binary:',binary)
    data = cc.decode(binary)
    print('Text:',data)

    h = HuffmanCodes()
    binary = h.encode(text + h.delimiter)
    print('Binary:',binary)
    data = h.decode(binary)
    print('Text:',data) 
"""