#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from ..Library import Library
# from ..Library.Library import LoadText

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/Library')
import Library.Library as Library

class Anser:
    def __init__(self, nr_tekst=0, nr_zdania = -1, zdanie=''):
        self.zdanie = zdanie
        self.nr_tekst = nr_tekst
        self.nr_zdania = nr_zdania
    def __str__(self):
        if self.nr_zdania >= 0:
            return "tekst nr:" + str(self.nr_tekst) + "zdanie nr: " + str(self.nr_zdania) + " " + self.zdanie +"\n"
        return "tekst nr:" + str(self.nr_tekst) + " " + self.zdanie + "\n"

class Konkordancja:
    word = ""
    answer = []
    def MakeAnser(self):
        for it in range(0, 100):
            file = Library.LoadText("../../teksty/AEI/"+ str(it) + ".txt")
            mind_list = file.split(".")
            for mind_id in range(len(mind_list)):
                for word in Library.OnlyLetter(mind_list[mind_id]).split(" "):
                    if self.word == Library.CLPBasicWord(word):
                        self.answer.append(Anser(it, mind_id, mind_list[mind_id]))
                        break

    def MakeAnserv2(self):
        file = ""
        for it in range(0, 100):
            file = Library.LoadText("../../teksty/AEI/"+ str(it) + ".txt")
            word_list = file.split(" ")
            for word_id in range(len(word_list)):
                if self.word in word_list[word_id]:
                    beg = word_id - 4
                    end = word_id + 5
                    if beg < 0:
                        beg = 0
                    if end > len(word_list):
                        end = len(word_list) - 1
                    text = ""
                    for word in word_list[beg:end]:
                        text += word + " "
                    self.answer.append(Anser(it, -1, text ))


    def PrintAnswer(self):
        for it in self.answer:
            print(it)

    def findWord(self):
        if Library.CLP_ON:
            self.word = Library.CLPBasicWord(input("Podaj słowo: "))
        else:
            self.word = input("Podaj słowo: ")
        self.MakeAnser()
        self.PrintAnswer()
        self.MakeAnserv2()
        self.PrintAnswer()



k = konkordancja()
k.findWord()