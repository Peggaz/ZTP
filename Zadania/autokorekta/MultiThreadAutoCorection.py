import Zadania.Library.library as Library
from Zadania.autokorekta import DamerauDistance
from Zadania.Library import EasyThread


def MainTextCorection(sentence, src_corect_text):
    Library.Log("rozpoczynanie wczytania oraz czyszczenia słownika")
    text_correct = Library.ReadClearText(src_corect_text).split(" ")
    print(text_correct)
    d_distance = DamerauDistance.DamerauDistance()
    ret = ""
    #test przygotowany, rozpoczęcie korekty
    Library.Log("Zakończono czyszczenie tekstu, rozpoczęto korektę")
    task = []
    id = 0
    for word in sentence.split(" "):
        task.append((id, word, d_distance, text_correct))
        id += 1
    dic_correct = {}
    for word, id in EasyThread.EasyThread(task, TextCorection):
        if word:
            dic_correct[word] = id
    dic_correct = Library.SortDic(dic_correct)[::-1]

    for it in range(len(dic_correct)):
        if it == 0 or dic_correct[it-1][0][-1] == '.':
            ret += BigFirstChar(dic_correct[it][0]) + " "
        else:
            ret += dic_correct[it][0] + " "
    Library.Log("zakończono korektę tekstu")
    return ret

def BigFirstChar(word):
    if len(word) > 0:
        return word[0].upper() + word[1:]
    return word

def TextCorection(args):
    try:
        word = args[1]
        d_distance = args[2]
        text_correct = args[3]
        ret = ""
        if word in text_correct:
            ret += word
        else:
            correct_word= ""
            correct_weight = 100
            for it in text_correct:
                weight = d_distance.MakeAndGetDistance(word, it)
                if correct_weight > weight:
                    correct_weight = weight
                    correct_word = it
                if weight <= 0.2:
                    correct_word = it
                    break
            ret += correct_word
            if word[-1] == ',' or word[-1] == '.':
                ret += word[-1]
        return ret, args[0]
    except:
        pass