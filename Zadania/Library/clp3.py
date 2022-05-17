# -*- coding: utf-8 -*-
# Author:   Paweł Chrząszcz, p.chrzaszcz@uj.edu.pl
# Contents: Unicode Python wrapper for the CLP library

from ctypes import *

def changChar(word: str, id: int, char: str):
    ret = list(word)
    ret[id] = char
    return ''.join(ret)

CLP_ENC = 'iso-8859-2'

class CLP:
    "Wrapper for CLP library."

    def __init__(self):
        self.lib = CDLL('libclp.so')
        self.lib.clp_ver.restype = c_char_p
        self.lib.clp_init()

    #--------------------------------------------------------------------------
    # Basic API
        
    def ver(self):
        "Returns CLP version string"
        return self.lib.clp_ver().decode(CLP_ENC)
    
    def rec(self, word):
        "Returns a list of ID's for the given string"
        try:
            inp = word.lower().encode(CLP_ENC)
            out = (c_int * 16)()
            num = c_int()
            self.lib.clp_rec(inp, out, byref(num))
            return out[:num.value]
        except UnicodeError:
            return []
    
    def label(self, id):
        "Returns the CLP label for the given ID"
        out = create_string_buffer(16)
        self.lib.clp_label(c_int(id), out)
        return out.value.decode(CLP_ENC)

    def bform(self, id):
        "Returns the base word form (string) for the given ID"
        out = create_string_buffer(64)
        self.lib.clp_bform(c_int(id), out)
        return out.value.decode(CLP_ENC)

    def forms(self, id):
        "Returns a list of all forms (strings) for the given ID"
        out = create_string_buffer(2048)
        self.lib.clp_forms(c_int(id), out)
        tmp = out.value.decode(CLP_ENC)
        return tmp.split(':')[:-1]

    def vec(self, id, word):
        "Returns a list of all form numbers for the given ID and string"
        inp = word.lower().encode(CLP_ENC)
        out = (c_int * 50)()
        num = c_int()
        self.lib.clp_vec(c_int(id), inp, out, byref(num))
        return out[:num.value]

    def __call__(self, word):
        return self.rec(word)
    
    def __getitem__(self, id):
        return self.bform(id)

    #--------------------------------------------------------------------------
    # Advanced API (additional utilities)
    def labels(self, w):
        "Creates a list of all CLP labels for the given string"
        l = [self.label(i) for i in self(w)]
        return list(set(l))

    def word(self, id, formid):
        "Returns a string for the given word ID and form ID"
        for f in self.forms(id):
            if formid in self.vec(id, f):
                return f

    def MakePolCHarDick(self):
        '''
        Tworzy słownik mający odpowiedniki polskich znaków dla liter alfabetu angielskiego
        :return: słownik zawierający odpowiedniki poskich znaków bez ż oraz ź
        '''
        ret = {}
        pol = "acelnos"
        lat = "ąćęłńóś"
        for it in range(len(pol)):
            ret[pol[it]] = lat[it]
        return ret

    def allWords(self, word, prefix=""):
        charDict = self.MakePolCHarDick()
        ret = [prefix + word]  # lista słów do wykorzystania

        def extendRet(word, char):
            word = changChar(word, it, char)  # helpWord[it] = charDict[helpWord[it]]
            ret.extend(self.allWords(word[it:], prefix + word[:it]))

        for it in range(len(word)):
            if word[it] in charDict:
                extendRet(word, charDict[word[it]])
            elif word[it] == 'z':
                extendRet(word, 'ż')
                extendRet(word, 'ź')
        return ret

    def newRec(self, word):
        ret = []
        for it_word in self.allWords(word):
            ret.append(self.rec(it_word))
        return ret

clp = CLP()

