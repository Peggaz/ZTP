import csv

import Library

import matplotlib.pyplot as plt


def SaveCSV(words_list, file_name):
    words_list = sorted(words_list.items(), key=lambda kv: kv[1], reverse=True)
    try:
        with open('../wyniki/' + str(file_name) + '.csv', 'w', encoding='utf-8', newline='') as plikcsv:
            tresc = csv.writer(plikcsv)
            pozycja = 0
            for wyraz, liczba in words_list:
                if Library.CLP_ON:
                    id = Library.clp(wyraz)
                    if len(id) > 0:
                        id = Library.clp(wyraz)[0]
                        czesc_mowy = Library.clp.label(id)
                    if len(czesc_mowy) > 0:
                        pozycja += 1
                        lista_frekwencyjna = (pozycja, wyraz, liczba, czesc_mowy[0])
                        tresc.writerow(lista_frekwencyjna)
                lista_frekwencyjna = (pozycja, wyraz, liczba, "")
                tresc.writerow(lista_frekwencyjna)
    except FileNotFoundError:
        print("plik: " + file_name + ".csv nie istnieje")

#SaveCSV(Library.AttendanceListCLP(Library.ReadClearText("../teksty/pol1.txt")), "Lista")

list = Library.AttendanceListCLP(Library.ReadClearText("../teksty/pol1.txt"))
list = Library.SortDic(list)

x = []
y = []
rank = 0
for it in list:
    if it[1] not in x:
        rank += 1
    x.append(it[1])
    y.append(rank)

plt.plot(y,x)
plt.autoscale()
plt.show()