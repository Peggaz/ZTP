def changChar(word: str, id: int, char: str):
    ret = list(word)
    ret[id] = char
    return ''.join(ret)

def MakePolCHarDick():
    '''
    Tworzy słownik mający odpowiedniki polskich znaków dla liter alfabetu angielskiego
    :return: słownik zawierający odpowiedniki poskich znaków
    '''
    ret = {}
    pol = "acelnos"
    lat = "ąćęłńóś"
    for it in range(len(pol)):
        ret[pol[it]] = lat[it]
    return ret


def allWords(word):
    charDict = MakePolCHarDick()
    ret = [word]  # lista słów do wykorzystania
    def extendRet(word, char):
        word = changChar(word, it, char)  # helpWord[it] = charDict[helpWord[it]]
        for it2 in allWords(word[it:]): ret.append(word[:it] + it2)
    for it in range(len(word)):
        if word[it] in charDict:
            extendRet(word, charDict[word[it]])
        elif word[it] == 'z':
            extendRet(word, 'ż')
            extendRet(word, 'ź')
    return ret

print(allWords('zolc'))