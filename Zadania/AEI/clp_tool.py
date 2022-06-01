import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/Library')
import library


while(True):
    input_s = ""
    input_s = input("podaj słowo: ")
    print(library.CLPBasicWord(input_s))