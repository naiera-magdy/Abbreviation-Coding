from cv2 import cv2
import numpy as np
from pathlib import Path
import heapq
from abbrev_utility import *

path = input("Enter text path : ")

with open(path, 'r') as file:
	inputText = file.read()

# sample = sample.lower()

print(inputText)

entropy = calculate_entropy(inputText)

# Apply abbriviation Encoding
abbriv_encode(inputText)

# Read the input file
with open('abbrevEncoded.txt', 'r') as file:
	sample = file.read()
	# Append a null terminator
	sample += '\0'

# Populate the frequency list
frequency = [0] * 0xFF
for symbol in sample:
	frequency[ord(symbol)] += 1

# Populate the heap
heap = []
for i in range(len(frequency)):
	# Check if the character is empty
	if frequency[i] == 0:
		continue

	# If the character is valid, create its node
	n = Node(chr(i), frequency[i])
	heapq.heappush(heap, n)

# Remove the two smallest nodes from the heap
# Combine them and re-insert them
while len(heap) > 1:
	left = heapq.heappop(heap)
	right = heapq.heappop(heap)
	parent = combine_nodes(left, right)
	heapq.heappush(heap, parent)

# Populate the encoding dictionary
encodingDictionary = {}
encode_tree(heap[0], '', encodingDictionary)

# Encode the sample into a byte array
encodedSample = encode_sample(sample, encodingDictionary)
encodedSample = string_to_bytes(encodedSample)

# Output the sample into a file
outputFile = open('encoded', 'w+b')
outputFile.write(encodedSample)
outputFile.close()

# Print encoding dictionary into file
with open('encodingDictionaryHuffman', 'w+') as file:
	file.write(str(encodingDictionary))

# =============================================================================
# Decode sample

# Read the input file
with open('encoded', 'r+') as file:
	sample = bitstring.Bits(file)

# Read encoding dictionary from file
with open('encodingDictionaryHuffman', 'r+') as file:
	encodingDictionary = file.read()
	encodingDictionary = eval(encodingDictionary)

decodedSample = decode_sample(sample, encodingDictionary)

# Output the decoded sample into a file
decodedSample = bytearray(decodedSample, 'utf-8')
outputFile = open('decodedHuffman', 'w+b')
outputFile.write(decodedSample)
outputFile.close()

with open('decodedHuffman','r+') as file:
    sample = file.read()
    file.close()

with open('encodingDic','r+') as file:
    encodingDic = file.read()
    encodingDic = eval(encodingDic)
    file.close()

print(type(encodingDic))
decoded = abbriv_decode(sample,encodingDic)

if inputText == decoded:
    print("\nSame")
else:
    print("\nDifferent")

outputFile = open('Abbrivdecoded.txt', 'w')
outputFile.write(decoded)
outputFile.close()

size1 = Path(path).stat().st_size
size2 = Path('encoded').stat().st_size
size3 = Path('encodingDic').stat().st_size
size4 = Path('encodingDictionaryHuffman').stat().st_size

print("compression ratio: ", size1/(size2+size3+size4))

# size5 = Path('D:/Multimedia/huffman/encoded').stat().st_size
# size6 = Path('D:/Multimedia/huffman/encodingDictionary').stat().st_size

# print("compression ratio Huffman: ", size1/(size5+size6))

print("entropy: ",entropy)
print("compression ratio entropy: ", 8/entropy)