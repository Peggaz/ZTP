import os

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'templates')
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Library')
try:
    import library
except:
    pass
try:
    from Zadania.Library import library
except:
    pass


class Answer:
    def __init__(self, nr_tekst=0, nr_zdania=-1, zdanie=''):
        self.zdanie = zdanie
        self.nr_tekst = nr_tekst
        self.nr_zdania = nr_zdania
    def __str__(self):
        if self.nr_zdania >= 0:
            return "tekst nr: " + str(self.nr_tekst) + " zdanie nr: " + str(self.nr_zdania) + " " + self.zdanie + "\n"
        return "tekst nr: " + str(self.nr_tekst) + " " + self.zdanie + "\n"

class Konkordancja:
    word = ""
    answer = []

    def __init__(self, file :str):
        self.setFile(file)

    def setFile(self, file:str):
        self.file = file

    def makeAnser(self):
        for it in range(0, 100):
            library.Log("rozpoczęcie wczytywania pliku z: " + "../../teksty/AEI/"+ str(it) + ".txt")
            file = library.LoadText("../../teksty/AEI/"+ str(it) + ".txt")
            mind_list = file.split(".")
            for mind_id in range(len(mind_list)):
                for word in library.OnlyLetter(mind_list[mind_id]).split(" "):
                    if self.word == library.CLPBasicWord(word):
                        self.answer.append(Answer(it, mind_id, mind_list[mind_id]))
                        break
            library.Log("zakończono budowe odpowiedzi 1")

    def makeAnserv2(self):
        file = ""
        for it in range(0, 100):
            library.Log("rozpoczęcie wczytywania pliku z: " + "../../teksty/AEI/" + str(it) + ".txt")
            file = library.LoadText("../../teksty/AEI/"+ str(it) + ".txt")
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
                    self.answer.append(Answer(it, -1, text))
            library.Log("zakończono budowe odpowiedzi 1")


    def printAnswer(self):

        for it in self.answer:
            print(it)

    def findWord(self):
        if library.CLP_ON:
            self.word = library.CLPBasicWord(input("Podaj słowo: "))
        else:
            self.word = input("Podaj słowo: ")
        self.makeAnser()
        self.printAnswer()
        self.makeAnserv2()
        self.printAnswer()



#k = Konkordancja()
#k.findWord()