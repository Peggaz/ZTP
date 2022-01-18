class DamerauDistance:
    def __init__(self):
        '''
        koństruktor
        '''
        self._polishDic = self.__MakeDamerauDic()
    def __MakeDamerauDic(self):
        '''
        Tworzy słownik mający odpowiedniki polskich znaków dla liter alfabetu angielskiego
        :return: słownik zawierający odpowiedniki poskich znaków
        '''
        ret = {}
        pol = "acelnosz"
        lat = "ąćęłńóśźż"
        for it in range(len(pol)):
            ret[lat[it]] = pol[it]
        ret["ż"] = "z"
        return ret

    def __CheckDamerauOrthography(self, s1, s2, id1, id2):
        '''
        sprawdza błędy ortograficzne takie jak rz i ch
        :param s1: ciąg znaków
        :param s2: ciąg znaków
        :param id1: id pierwszego ciągu
        :param id2: id drugiego ciągu
        :return: wartość binarna określająca czy są to podane błędy gramatyczne
        '''
        try:
            id1 += 1
            if s1[id1-2:id1] == "ch" and s2[id2] == "h":
                return True
            elif s1[id1-2:id1] == "rz" and s2[id2] == "ż":
                return True
          # elif s1[id1-2:id1] == "ci" and s2[id2] == "ć":
             #   return True
            #elif s1[id1-2:id1] == "si" and s2[id2] == "ś":
             #   return True
           # elif s1[id1-2:id1] == "om" and s2[id2] == "ą":
              #  return True
            #elif s1[id1-2:id1] == "ni" and s2[id2] == "ń":
              #  return True

        except:
            pass
        return False


    def __PolishChar(self, c, c2):
        '''
        analizuje dwa podane znaki i
        :param c:
        :param c2:
        :return:
        '''
        if c in self._polishDic and self._polishDic[c] == c2:
            return True
        elif c2 in self._polishDic and self._polishDic[c2] == c:
            return True
        return False


    def MakeAndGetDistance(self, s ,t):
        '''
        Funkcja metryki cosinusowej ze wzoru odleglosc n-gramów
        @:param s - słowo porównywane
        @:param t - słowo do porównania
        @:return - ilosc operacji które są wymagane do korekty
        '''
        s = s.lower()
        t = t.lower()
        n = len(t)
        m = len(s)
        ret = [[0] * n for i in range(m)]
        for i in range(m):
            for j in range(n):
                try:
                    if s[i] == t[j]:
                        r = 0
                    elif self.__CheckDamerauOrthography(s, t, i, j) or self.__CheckDamerauOrthography(t, s, j, i):
                        r = -0.5#odejmujemy 0.5 ponieważ kolejne operacje spowodują zmianę wartości
                    elif self.__PolishChar(s[i], t[j]):
                        r = 0.2#no wiadmo
                    elif s[i + 1] == t[j] and t[j + 1] == s[i]:
                        r = -0.5#zostawiamy 0 ponieważ następna operacja cofnie doda nam 0.5
                    elif s[i] in "óu" and t[j] in "óu":
                        r = 0.5
                    else:
                        r = 1
                except:
                    r = 1
                ret[i][j] = min(ret[i-1][j] + 1,   #usuwanie liter
                               ret[i][j-1] + 1,    #wstawianie
                               ret[i-1][j-1] + r)  #zamian
        return ret[m-1][n-1]


    def Test(self):
        ret = True
        ret &= self.MakeAndGetDistance('pierze', 'pieże') == 0.5
        ret &= self.MakeAndGetDistance('smiech', 'śmiech') == 0.2
        ret &= self.MakeAndGetDistance('piora', 'piórą') == 0.4
        ret &= self.MakeAndGetDistance('piura', 'pióra') == 0.5
        ret &= self.MakeAndGetDistance('człowiek', 'cłzoiwek') == 1.0
        ret &= self.MakeAndGetDistance('zrobić', 'rzobić') == 0.5
        ret &= self.MakeAndGetDistance('zima', 'źima') == 0.2
        ret &= self.MakeAndGetDistance('prosiłem', 'prsoilem') == 0.7
        ret &= self.MakeAndGetDistance('ćwok', 'wciok') == 1.2 #Godny coś pojebał
        return ret