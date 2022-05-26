#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request

from Zadania.Library import library

app = Flask(__name__)

semantyka_tab = []
teksty = []
tab_wagi = []
sort_po_id = False
def main():
    plik = library.LoadText("../../teksty/AEI/all_text.txt")

    plik = plik.replace('\n', ' ')
    plik_csv = library.LoadText("../../teksty/AEI/semantyka.csv")
    semantyka = plik_csv.split("\n")
    semantyka_tab.clear()

    plik_csv = wczytaj("wagi_id.csv")
    wiersze_wagi = plik_csv.split("\n")
    waga = []
    for wiersz in wiersze_wagi:
        waga.append(wiersz.split(","))


    for sem in range(len(semantyka)):
        semantyka_wiersz = []
        id = 0
        for it in semantyka[sem].split(","):
            if id == 0:
                semantyka_wiersz.append("<mark id=mark_" + str(sem) + ">" + it + "</mark>")
            else: semantyka_wiersz.append(it)
            id += 1
        semantyka_tab.append(semantyka_wiersz)
    semantyka_mark = []


    #eliminacja nazw wiersza tabeli

    for it in range(len(semantyka_tab)):
        semantyka_mark.append("<mark id=mark_" + str(it) + ">")

    lista_tekstow = plik.split("#0")

    class Tekst:
        def __init__(self, tekst="", tab=[]):
            self.tekst = tekst
            self.tab = tab
            self.id = ""
            self.ocena = ""
            self.ocena_int = 0
            self.id_int = 0
    teksty.clear()
    tab_wagi.clear()
    for wiersz in waga:
        local_tab = []
        iterator = 0
        for it in wiersz:
            if iterator:
                local_tab.append(semantyka[int(it)].split(",")[0])
            else: local_tab.append(it)
            iterator += 1
        tab_wagi.append(local_tab)
    for wiersz in range(len(semantyka)):
        semantyka[wiersz] = semantyka[wiersz].split(",")
        semantyka[wiersz] = semantyka[wiersz][1:]


    for tekst in lista_tekstow:
        tab_wynik = []
        waga_tekstu = []
        index_tekst = Tekst("", [])
        index_tekst.id_int = (tekst.split("\n")[0])[1:6]
        if int(index_tekst.id_int) < 50:
            index_tekst.id = "Tekst na temat nr: " + index_tekst.id_int
        else:
            index_tekst.id = "Tekst nie na temat nr: " + index_tekst.id_int
        index_tekst.id_int = int(index_tekst.id_int)
        txt = ""
        tekst.replace("\n", " ")
        naglowek = 0
        for slowo in tekst.split(" "):
            if naglowek < 3:
                naglowek += 1
            else:
                podstawowa_forma = library.CLPBasicWord(library.OnlyLetter(slowo))
                for sem in range(len(semantyka)):
                    if podstawowa_forma in semantyka[sem]:
                        if sem not in waga_tekstu:
                            waga_tekstu.append(str(sem))
                        if podstawowa_forma not in tab_wynik:
                            tab_wynik.append(podstawowa_forma)
                        slowo = semantyka_mark[sem] + slowo + "</mark>"
                index_tekst.tekst += slowo + " "
        licznik_tekstu = 0


        for it in waga:
            ok = True
            id = 0
            for wag in it:
                if id > 0 and wag not in waga_tekstu:
                    ok = False
                    break
                id += 1
            if ok:
                licznik_tekstu = float(it[0])
                break

        for semantyka_wiersz in semantyka_tab:
            local_tab = []
            czy_byl_wiersz = False
            for wynik in tab_wynik:
                if wynik in semantyka_wiersz:
                    if not czy_byl_wiersz:
                        local_tab.append(semantyka_wiersz[0])
                        czy_byl_wiersz = True
                    local_tab.append(wynik)
            index_tekst.tab.append(local_tab)

        if licznik_tekstu >= float(0.60):
            index_tekst.ocena = "<a style='color:green'>"
        elif licznik_tekstu >= float(0.50):
            index_tekst.ocena = "<a style='color:yellow'>"
        else:
            index_tekst.ocena = "<a style='color:red'>"
        index_tekst.ocena += "{:.2f}".format(licznik_tekstu) + "</a>"
        index_tekst.ocena_int = licznik_tekstu
        teksty.append(index_tekst)
@app.route("/", methods=['GET', 'POST'])
def index():
    main()
    if request.method == 'POST':
        if request.form['sort_value'] == 'Sortuj po ocenie':
            def key(e):
                return -e.ocena_int
            teksty.sort(key=key)
            pass

        elif request.form['sort_value'] == 'Sortuj po id':
            def key(e):
                return e.id_int
            teksty.sort(key=key)
            pass
    return render_template("index.html", semantyka=semantyka_tab, teksty=teksty, wagi=tab_wagi)


############################################

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5003)
    ##app.run(host='wierzba.wzks.uj.edu.pl', debug=True, port=5003)