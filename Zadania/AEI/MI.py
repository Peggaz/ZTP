import math

from Zadania.Library import library
WIDNDOW_SIZE = 5

def POkno(x, y, windows):
    count = 0
    for it in windows:
        if x in it and y in it:
            count += 1
    return count/(len(windows) * 10)

def MainMIFun():
    text =""


    for file_id in range(100):
        ixy = {}
        windows = []
        text = library.ReadClearText("../../teksty/AEI/" + str(file_id) + ".txt")
        attendaceList = library.AttendanceListCLP(text)
        words = text.split(" ")
        for word_id in range(len(words) - WIDNDOW_SIZE):
            windows.append(words[word_id:word_id+WIDNDOW_SIZE])
        attendaceList = library.SortDic(attendaceList)
        sum_all_words = 0
        for it in attendaceList:
            sum_all_words += it[1]
        #print(attendaceList[0:1])
        for word1_id in range(len(attendaceList)):
            for word2_id in range(word1_id+1, len(attendaceList)):
                pxy = POkno(attendaceList[word1_id][0], attendaceList[word2_id][0], windows)
                px = attendaceList[word1_id][1]/sum_all_words
                py = attendaceList[word2_id][1]/sum_all_words

                ##print(attendaceList[word2_id][1], sum_all_words, py)
                #exit()

                odp = 0
                try:
                    if pxy > 0:
                        odp = math.log2(pxy / (px*py))
                        ixy[attendaceList[word1_id][0] + " " + attendaceList[word2_id][0]] = odp
                        #print(attendaceList[word1_id][0], "  ", attendaceList[word2_id][0], " ", odp)
                except:
                    print("ERORpxy", pxy, " px", px, " py", py)
                #print("ok")

        print(library.SortDic(ixy))


MainMIFun()