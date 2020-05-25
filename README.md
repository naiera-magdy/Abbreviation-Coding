# **Abbreviation Encoding**
This is a text compression algorithm based on dictionary coding.

The main idea is about to replace frequently Repeated words or statements with their abbreviations
______________________________________________________________________________________________________

### **Example** 
**Text:** “twinkle twinkle little star how i wonder what you are twinkle twinkle little	 star twinkle twinkle little star”

**Dictionary:** {'T': 'twinkle', 'LS': 'little star'}

**Encoded:** “T T LS how i wonder what you are T T LS T T LS”

______________________________________________________________________________________________________
### **Before running this code you have to ensure that these packages are installed on your device**
* 	python
* 	bitstring
* 	heapq
* 	opencv
* 	numpy
* 	math
*	pathlib
* 	time

## **To run the code**
**1.** Write the following command
``````````````````````````````
python3 abbreviationCoding.py
``````````````````````````````
**2.** Enter text path as following for example:
``````````````````````````````
Enter text path : twinkle.txt
``````````````````````````````