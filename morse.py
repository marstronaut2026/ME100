from board import LED
from machine import Pin
import time
led = Pin(LED, mode=Pin.OUT)
BRate=0.25


def morse_dash():
    led(1)
    time.sleep(4*BRate)
    led(0)
    time.sleep(BRate)

def morse_pause():
    time.sleep(BRate)

def morse_dot():
    led(1)
    time.sleep(BRate)
    led(0)
    time.sleep(BRate)

CODE = {' ': '_', 
"'": '.----.', 
'(': '-.--.-', 
')': '-.--.-', 
',': '--..--', 
'-': '-....-', 
'.': '.-.-.-', 
'/': '-..-.', 
'0': '-----', 
'1': '.----', 
'2': '..---', 
'3': '...--', 
'4': '....-', 
'5': '.....', 
'6': '-....', 
'7': '--...', 
'8': '---..', 
'9': '----.', 
':': '---...', 
';': '-.-.-.', 
'?': '..--..', 
'A': '.-', 
'B': '-...', 
'C': '-.-.', 
'D': '-..', 
'E': '.', 
'F': '..-.', 
'G': '--.', 
'H': '....', 
'I': '..', 
'J': '.---', 
'K': '-.-', 
'L': '.-..', 
'M': '--', 
'N': '-.', 
'O': '---', 
'P': '.--.', 
'Q': '--.-', 
'R': '.-.', 
'S': '...', 
'T': '-', 
'U': '..-', 
'V': '...-', 
'W': '.--', 
'X': '-..-', 
'Y': '-.--', 
'Z': '--..', 
'_': '..--.-'}

def convertToMorseCode(sentence):
    sentence = sentence.upper()
    encodedSentence = ""
    for character in sentence:
        encodedSentence += CODE[character] + " " 
    return encodedSentence

while True:

    sentence = input("Enter sentence: ")
    encodedSentence = convertToMorseCode(sentence)
    print(encodedSentence)
    for i in encodedSentence:
        if i == ".":
            morse_dot()
        elif i == "-":
            morse_dash()
        else:
            morse_pause()