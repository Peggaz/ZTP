import math
import datetime
CLP_ON = False#Bardzo ważna zmienna określa czy użwać słownika CLP działa on poprawnie jedynie na wierzbie
if CLP_ON:
    from clp3 import clp
    import clp_settings
#region clp
def CLPBasicWord(s):
    id = clp(s)
    if len(id) > 0:
        list_p = clp.forms(id[0])
        if len(list_p) > 0:
            s = list_p[0]
    return s
#endregion


# region Cezar
def DecodingCezar(text, x):
    ret = ""
    for c in text:
        int_c = ord(c)
        if c != " " and c != "\n":
            if IsInAlfabetCezar(int_c, -x):
                ret += chr(int_c - x)
            else:
                ret += chr(int_c - x + 26)
        else:
            ret += c
    print(ret)


def CodingCezar(text, x):
    ret = ""
    for c in text:
        int_c = ord(c)
        if c != " " and c != "\n":
            if IsInAlfabetCezar(int_c, x):
                ret += chr(int_c + x)
            else:
                ret += chr(int_c + x - 26)
        else:
            ret += c
    print("tekst zakodowany:  " + ret)
    return ret


def IsInAlfabetCezar(c, x):
    if type(c) != int: c = ord(c)

    if ord("A") <= c <= ord("Z"):
        if ord("A") <= c + x <= ord("Z"):
            return True
    elif ord("a") <= c <= ord("z"):
        if ord("a") <= c + x <= ord("z"):
            return True
    return False


# endregion
# region tekst
def ReadClearText(s):
    '''
    Funkcja odczytuje tekst i wyrzuca z niego wszystko co nie jest literą ani spacją
    :param s: sciężka do pliku
    :return: string zawierający jedynie małe litery i pojedńcze spacje
    '''
    return OnlyLetter(LoadText(s).lower())


def OnlyLetter(s):
    '''
    :param s: String który zawiera w sobie zadany tekst
    :return: zwraca przyjęty tekst zawierający jedynie litery oraz pojedyńcze spacje
    entery są zamienione na pojedyńcze spacje
    '''
    if type(s) == list:
        new_s = ""
        for it in s:
            new_s += it
        s = new_s
    ret = ""
    s = s.replace("\n", " ")
    while "  " in s:#usuwam puste spacje
        s = s.replace("  ", " ")
    for x in s:
        if x == " " or OrALetter(x):
            ret += x
    return ret


def OrALetter(ch):
    '''
    Sprawdza czy litera należy do języka polskiego
    :param ch: znak(mała litera) do analizy polskiego alfabetu
    :return: wartość binarna czy znak należy do polskiego alfabetu
    '''
    if ch in "ąćęłńóśźż":
        return True
    z = ord(ch)
    if z >= ord("a") and z <= ord("z"):
        return True
    return False


def OrAInt(ch):
    '''
    :param ch: pojedyńczy znak znak
    :return: wartość binarna określająca czy znak jest cyfrom
    '''
    return ch in "0123456789"


def Euklidesowa(x_gram, y_gram):
    '''
    Funkcja metryki euklidesowej ze wzoru odleglosc n-gramów
    @:param x_gram - pierwszy słownik do porównania
    @:param y_gram - drugi słownik do porównania
    @:return - wynik w postaci int
    '''
    licznik = 0
    for itr in x_gram:
        if itr in y_gram:
            x = x_gram[itr]
            y = y_gram[itr]
            licznik += ((x - y) * (x - y))
    return math.sqrt(licznik)


def Taksowkowa(x_gram, y_gram):
    '''
    Funkcja metryki teksówkarskiej ze wzoru odleglosc n-gramów
    @:param x_gram - pierwszy słownik do porównania
    @:param y_gram - drugi słownik do porównania
    @:return - wynik w postaci int
    '''
    licznik = 0
    for itr in x_gram:
        if itr in y_gram:
            x = x_gram[itr]
            y = y_gram[itr]
            licznik += math.fabs(x - y)
    return licznik


def Maksimum(x_gram, y_gram):
    '''
    Funkcja metryki maksimum ze wzoru odleglosc n-gramów
    @:param x_gram - pierwszy słownik do porównania
    @:param y_gram - drugi słownik do porównania
    @:return - wynik w postaci int
    '''
    licznik = []
    for itr in x_gram:
        if itr in y_gram:
            x = x_gram[itr]
            y = y_gram[itr]
            licznik.append(math.fabs(x - y))
    return max(licznik)


def Cosinusowa(x_gram, y_gram):
    '''
    Funkcja metryki cosinusowej ze wzoru odleglosc n-gramów
    @:param x_gram - pierwszy słownik do porównania
    @:param y_gram - drugi słownik do porównania
    @:return - wynik w postaci int
    '''
    licznik = 0
    for itr in x_gram:
        if itr in y_gram:
            x = x_gram[itr]
            y = y_gram[itr]
            licznik += x * y
    try:
        return 1 - (licznik / (len(x_gram) * len(y_gram)))
    except:
        return -1

def nGram(s, n):
    '''
    @:param s: tekst który mamy rozbić
    @:param n: długość n-grama
    @:return słownik zaiwerający ngram i jego ilość
    '''
    _nGram = {}
    for x in range(len(s) - (n-1)):
        _nGram[s[x:x + n]] = _nGram.get(s[x:x + n], 0) + 1
    return _nGram


def SortDic(dic):
    '''
    :param dic: słownik
    :return: posortowany słownik po kluczu
    '''
    def key_sort(e):  # definicja klucza sortujacego https://www.w3schools.com/python/ref_list_sort.asp
        return e.licznik


def LoadText(s):
    '''
    :param s: scieżka dostępu
    :return: tekst kodowany w utf-8
    '''
    return open(s, "r", encoding="utf-8").read()


def AttendanceListCLP(string, attendance_list = None):
    '''
    :param string: ciąg znaków do analizy
    :param attendance_list: lista frkefencyjna domyślnie pusta zawierająca
    :return: lista frekfencyjna danego ciągu znaków
    '''
    if attendance_list == None:
        attendance_list = {}
    for word in string.split(" "):
        if (word != ""):
            if (CLP_ON):
                word = CLPBasicWord(word)
            if word in attendance_list:
                attendance_list[word] += 1
            else:
                attendance_list[word] = 1
    return attendance_list

def LevenshteinDistance(s ,t):
    '''
    Funkcja metryki cosinusowej ze wzoru odleglosc n-gramów
    @:param s - słowo porównywane
    @:param t - słowo do porównania
    @:return - ilosc operacji które są wymagane do korekty
    '''
    n = len(t)
    m = len(s)
    ret = [[0] * n for i in range(m)]
    for i in range(m):
        for j in range(n):
            r = 1
            if s[i] == t[j]:
                r = 0
            ret[i][j] = min(ret[i-1][j] + 1,   #usuwanie liter
                           ret[i][j-1] + 1,    #wstawianie
                           ret[i-1][j-1] + r)  #zamiana
    return ret[m-1][n-1]

def Atergo(file):
    ret = []
    for line in file.split("\n"):
        for it in line.split(" "):
            ret.append(it)
    def RevertWord(word):
        return word[::-1]
    ret.sort(key = RevertWord)
    return ret[::-1]

def SaveFile(list, name, location = "../wyniki/"):
    '''
    Zapisuje do domyslnej wartości location
    @:param ist - lista elementów
    @:param name - nazwa zapisanego pliku
    @:param location - scieża zapisu domyślnie: "../wyniki"
    '''
    f = open(location + name, "w")  # otwarcie pliku
    for it in list:
        try:
            f.write(it + " ")
        except:
            print("błąd w zapisie")

# endregion

# region transcription
vowels = ['a', 'e', 'i', 'o', 'u', 'ó', 'y', 'ą', 'ę', 'a', 'o', 'и', 'у', 'ы', 'э']
def MakeTranscriptionDic():
    '''
    :return: zwraca słownik transkrypcji alfabetu - cyrylica -> polski
    '''
    transcriptionDic = {
            'б': 'b',
            'в': 'w',
            'г': 'g',
            'д': 'd',
            'e': (('je', 1, ['S', 'ъ', 'ь'], [], 0), ('e', 0, ['ж', 'л', 'ц', 'ч', 'ш', 'щ'], [], 0), ['ie']),
            'ё': (('jo', 1, ['S', 'ъ', 'ь'], [], 0), ('o', 0, ['ж', 'л', 'ч', 'ш', 'щ'], [], 0), ['io']),
            'ж': 'ż',
            'з': 'z',
            'и': (('ji', 0, ['ь'], [], 0), ('y', 0, ['ж', 'ц', 'ш'], [], 0), ['i']),
            'й': 'j',
            'к': 'k',
            'л': (('l', 0, [], ['е', 'ё', 'и', 'ь', 'ю', 'я'], 0), ['ł']),
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'ch',
            'ц': 'c',
            'ч': 'cz',
            'ш': 'sz',
            'щ': 'szcz',
            'ъ': '',
            'ь': (('', 0, ['ж', 'ш', 'ч', 'щ'], ['S'], 0), ['´']),
            'э': 'e',
            'ю': (('u', 0, ['л'], [], 0), ('ju', 1, ['S', 'ъ', 'ь'], [], 0), ['iu']),
            'я': (('ja', 1, ['S', 'ъ', 'ь'], [], 0), ('a', 0, ['л'], [], 0), ['ia'])}
    return transcriptionDic


def LoadTransliterationDic(s):
    '''
    metoda wczytuje predefiniowany słownik transliteracji zawarty w pliku txt
    :param s: cieżka
    :return: słownik transliteracji
    '''
    read = LoadText(s)
    ru = 2
    la = 2
    trans = {}
    cru = []
    cla = []
    for c in read:

        if c != '\n' and c != ' ' and c != '\t':
            if ru > 0:
                cru.append(c)
                ru -= 1
            elif la > 0:
                cla.append(c)
                la -= 1
            if la == 0 and ru == 0:
                la = 2
                ru = 2
    for x in range(len(cru) - 1):
        trans[cru[x]] = cla[x]
    return trans


def Transliteration(src_text, transliteriation_src):
    '''
    metoda dokonująca transliteracji
    :param src_text: scieżka dostępu
    :param transliteriation_src: ścieżka dostępu do pliku zawierającego tranliteracje
    :return: tekst po transliteracji
    '''
    trans = LoadTransliterationDic(transliteriation_src)
    textIN = LoadText(src_text)
    textOut = ""
    for c in textIN:
        if c in trans:
            textOut += trans[c]
        else:
            textOut += c
    return textOut


def Transcription(src_text, transliteriation_src):
    text_in = LoadText(src_text).lower()
    dic_transliteration = LoadTransliterationDic(transliteriation_src)
    transcriptionDic = MakeTranscriptionDic()
    text_out = ''
    for idc in range(len(text_in)):
        c = text_in[idc]
        if c != " " and c != '\n' and c != '\t':
            if c in transcriptionDic:
                if type(transcriptionDic[c]) == tuple:
                    for t in transcriptionDic[c]:
                        if len(t) == 5:
                            con = False
                            if idc > 0:
                                if t[1] and text_in[idc - 1] == ' ' or text_in[idc - 1] == '\n':
                                    text_out += t[0]
                                    break
                                elif t[2]:
                                    if t[2][0] == 'S':
                                        t[2].extend(vowels)
                                    if text_in[idc - 1] in t[2]:
                                        text_out += t[0]
                                        break
                            if idc < len(text_in) - 1:
                                if t[3]:
                                    if t[3][0] == 'S':
                                        t[3].extend(vowels)
                                    if text_in[idc + 1] in t[3]:
                                        text_out += t[0]
                                        break
                                if t[4] and text_in[idc + 0] == ' ' or text_in[idc + 1] == '\n':
                                    text_out += t[0]
                                    break
                        else:
                            text_out += t[0]
                elif type(transcriptionDic[c]) == str:
                    text_out += transcriptionDic[c]
                else:
                    text_out += transcriptionDic[c[0]]
            elif c in dic_transliteration:
                text_out += dic_transliteration[c]
            else:
                text_out += c
        else:
            text_out += c
    return text_out

def Log(message):
    '''
    Funkcja odpowiadająca za zalogowanie czynności o danym czasie
    :param self:
    :param message:
    :return:
    '''
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print ("%s %s" % (now, message))
# endregion

#region Old Damerau
def MakeDamerauDic(self):
    ret = {}
    pol = "acelnosz"
    lat = "ąćęłńóśźż"
    for it in range(len(pol)):
        ret[lat[it]] = pol[it]
    ret["ż"] = "z"
    return ret

def CheckDamerauOrthographyOld(s1, s2, id1, id2):
    try:
        if s1[id1:id1 + 2] == "ch" and s2[id2] == "h":
            return True
        elif s1[id1:id1 + 2] == "rz" and s2[id2] == "ż":
            return True
        elif s1[id1:id1 + 2] == "ci" and s2[id2] == "ć":
            return True
        elif s1[id1:id1 + 2] == "si" and s2[id2] == "ś":
            return True
        elif s1[id1:id1 + 2] == "om" and s2[id2] == "ą":
            return True
        elif s1[id1:id1 + 2] == "ni" and s2[id2] == "ń":
            return True
        elif s1[id1] == "u" and s2[id2] == "ń":
            return True
    except:
        pass
    return False

def PolishChar(self, c, c2):
    if c in self._polishDic and self._polishDic[c] == c2:
        return True
    elif c2 in self._polishDic and self._polishDic[c2] == c:
        return True
    return False

def DamerauOld(s, t):
    ret = 0.0
    if s == t:
        return 0
    polishDic = MakeDamerauDic()
    if len(s) < len(t):
        lenWord = len(s)
    else:
        lenWord = len(t)
    lenF = 0
    lenS = 0
    for id_c in range(lenWord):
        try:
            if s[id_c + lenF] == t[id_c + lenS]:
                continue
        except:
            ret += math.fabs((id_c + lenS) - (id_c + lenF))
            break
        # czeski błąd
        if len(s) > (id_c + lenF + 1) and len(t) > (id_c + lenS + 1) and s[id_c + lenF + 1] == t[id_c + lenS] and s[
            id_c + lenF] == t[id_c + lenS + 1]:
            ret += 0.5
            lenF += 1
            lenS += 1
            continue
        elif PolishChar(s[id_c + lenF], t[id_c + lenS], polishDic):
            ret += 0.2
            continue
        elif CheckDamerauOrthographyOld(s, t, id_c + lenF, id_c + lenS):
            lenF += 1
            ret += 0.5
        elif CheckDamerauOrthographyOld(t, s, id_c + lenS, id_c + lenF):
            lenS += 1
            ret += 0.5
        else:
            ret += 0.5
    return ret
#endregion

