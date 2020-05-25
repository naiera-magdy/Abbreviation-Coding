import bitstring
import math as math

# Node class
class Node:
	# Constructor magic
	# 
	# Arguments:
	#   symbol {str} -- The node's key
	#   freq {int} -- The number of occurences
	#
	def __init__(self, symbol, freq):
		self.symbol = symbol
		self.freq = freq
		self.left = None
		self.right = None

	# Comparison magic
	def __lt__(self, other):
		return self.freq < other.freq

#
# Combines two nodes into a new node
# (no value)
# 
# Arguments:
# 	left {Node} -- The first node
# 	right {Node} -- The second node
# 
# Returns:
# 	Node -- The combined node
#
def combine_nodes(left, right):
	parent = Node(None, left.freq + right.freq)
	parent.left = left
	parent.right = right
	return parent

#
# Populates the encoding dictionary
# 
# Arguments:
# 	node {Node} -- The current node being processed
# 	code {str} -- The current code being accumulated
# 	sampleCode {dict} -- The encoding dictionary
#
def encode_tree(node, code, sampleCode):
	# If the node doesn't exist, return
	if node is None:
		return

	# If the node is a leaf, store the code
	if node.symbol is not None:
		sampleCode[node.symbol] = code
		return

	# Process left and right subtrees
	encode_tree(node.left, code + '0', sampleCode)
	encode_tree(node.right, code + '1', sampleCode)
	return

#
# Encodes a string given an encoding dictionary
# 
# Arguments:
# 	sample {str} -- The string that will be encoded
# 	sampleCode {dict} -- The encoding dictionary
# 
# Returns:
# 	str -- The encoded string
#
def encode_sample(sample, sampleCode):
	encodedSample = ''
	for symbol in sample:
		encodedSample += sampleCode[symbol]
	return encodedSample

#
# Turns a string of binary digits into a bytearray
# (zero-padded)
# 
# Arguments:
# 	sample {string} -- A string of binary digits
# 
# Returns:
# 	bytearray -- The corresponding bytearray
#
def string_to_bytes(sample):
	idx = 0
	resultBytes = bytearray()
	while idx + 8 <= len(sample):
		b = sample[idx:idx + 8]
		b = int(b, 2)
		resultBytes.append(b & 0xff)
		idx += 8

	remainingLength = len(sample) - idx
	if remainingLength == 0:
		return resultBytes

	b = sample[idx:]
	b += '0' * (8 - remainingLength)
	b = int(b, 2)
	resultBytes.append(b & 0xff)
	return resultBytes

#
# Decodes a bitstring given an encoding dictionary
# 
# Arguments:
# 	sample {bitstring} -- The encoded bitstring
# 	sampleCode {dict} -- The encoding dictionary
# 
# Returns:
# 	string -- The decoded string
#
def decode_sample(sample, sampleCode):
	decodedSample = ''

	# Swap keys and values for the encoding dictionary
	swappedCode = { value: key for key, value in sampleCode.items() }

	# Read bit-by-bit
	# Accumulate key bitstring
	# Once a key is located,
	# append the value and reset the key
	currentBits = ''
	for b in sample:
		currentBits += '1' if b else '0'
		if currentBits in swappedCode:
			# Halt on a null terminator
			if swappedCode[currentBits] == '\0':
				return decodedSample

			decodedSample += swappedCode[currentBits]
			currentBits = ''

	return decodedSample

#
# Encode Given sample and save the encoded in file and its dictionary in file
# 
# Arguments:
# 	sample {string} -- A string to be encoded
#
def abbriv_encode(sample):
	# Split Sample to individual words
	sample = sample.split(" ") 

	encodedSample = ""
	encodingDic = {}
	code = ""
	i = 0
	j = 1

	while i < len(sample):

		# Check if this word is a single character
		if len(sample[i]) == 1:
			encodedSample += sample[i] + " "
			i+=1
			j = i+1
			continue
		
		# Check if this word or its statement is already stored in the dictionary
		skip = False
		for key in encodingDic:
			if encodingDic[key].find(sample[i]) == 0:
				match = True
				n = i
				dic = encodingDic[key].split(" ")
				for word in dic:
					if word != sample[n]:
						match = False
					n += 1
					if n >= len(sample):
						if word != dic[len(dic)-1]:
							match = False
						break
				if match == True:
					skip = True
					i += len(encodingDic[key].split(" "))
					encodedSample += key + " "
					break

		# Search for matching words or statements
		if skip == False:    
			found = False   
			while j < len(sample):
				if sample[j] == sample[i]:
					found = True
					code = sample[i][0].upper()
					count = 1
					while (i+count < j and j+count < len(sample)):
						if sample[j+count] != sample[i+count]:
							break
						code += sample[i+count][0].upper()
						count += 1
					
					k = 1
					putasit = False
					same = True

					# Make sure that this code is unique. If not so, make it unique
					while k < len(sample[i+count-1]) and same == True:
						same = False
						for key in encodingDic:
							if key == code and encodingDic[key] != " ".join(sample[i : i+count]):
								code = sample[i+count-1][k].upper()
								k +=1
								same = True
								break
				
					if k >= len(sample[i+count-1] ):
						putasit = True
					
					if(putasit == False):
						encodingDic[code] = " ".join(sample[i : i+count])
						encodedSample += code + " "
					else:
						# If can't make it unique so put it as it is 
						encodedSample += " ".join(sample[i : i+count]) + " "
					i += count 
					break
				else:
					j += 1
			# If this word isn't repeated put it as it is
			if found == False:
				encodedSample += sample[i] + " "
				i+=1
		j = i+1

	# Save Encoded text and the dictionary in files
	with open('abbrevEncoded.txt', 'w+') as file:
		file.write(encodedSample)
	with open('encodingDic', 'w+') as file:
		file.write(str(encodingDic))
		
#
# Decode a given sample to its original form
# 
# Arguments:
# 	sample		{string} -- A string to be decoded
# 	encodingDic {dict}	 -- dictionary of codes
# 
# Returns:
# 	string -- the decoded string
#
def abbriv_decode(sample,encodingDic):
	sample = sample.split(" ")
	i = 0
	decodedSample = ""
	while i < len(sample):
		founded = False
		for key in encodingDic:
			if key == sample[i]:
				decodedSample += encodingDic[key] + " "
				founded = True
			
		if founded == False:
			decodedSample += sample[i] + " "
		i += 1
	return decodedSample.strip()

#
# Calculate the entropy of a given text
# 
# Arguments:
# 	inputText {string} -- A string to calculate its entropy
# 
# Returns:
# 	float -- The entropy
#
def calculate_entropy(inputText):
	frequency = [0.0] * 0xFF
	for symbol in inputText:
		frequency[ord(symbol)] += 1
	entropy = 0
	for i in range(0,len(frequency)-1):
		if frequency[i] == 0:
			continue
		frequency[i] /= len(inputText)
		frequency[i] *= math.log2(1.0/float(frequency[i]))
		entropy += frequency[i]
	return entropy