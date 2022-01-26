import Library
import DamerauDistance
import threading, queue
import datetime
import multiprocessing
import EasyThread

def MainTextCorection(src_corect_text):
    in_text = "ala ma kotz"#input().lower()
    text_correct = Library.ReadClearText(src_corect_text)
    d_distance = DamerauDistance.DamerauDistance()
    ret = ""
    #test przygotowany, rozpoczęcie korekty
    Library.Log("Zakończono czyszczenie tekstu, rozpoczęto korektę")
    task = []
    for word in in_text.split(" "):
        task.append(word, d_distance, text_correct)
    for it in EasyThread.EasyThread(task, TextCorection):
        ret += it
def TextCorection(*args):
    try:
        word = args[0]
        d_distance = args[1]
        text_correct = args[2]
        ret = ""
        if word in text_correct:
            ret += " " + word
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
        return ret
    except:
        pass


    print("hellow word")

print(MainTextCorection("../teksty/odm.txt"))