import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Library')
import Library.Library as Library


def klasteryzacja():
    lista = []
    mapa_adresow = []
    plik = Library.LoadText("../../teksty/klasteryzacja.txt")
    adresy = plik.split('\n')
    lista.append(adresy[0])
    mapa_adresow.append(lista)
    lista = []
    Library.Log("zakończono przygotowanie do pracy")
    log_len = len(adresy)
    for it in adresy:  # iterujemy po adresach ktore odzielamy po entaerach
        znaleziono = False
        it_nGramy = Library.nGram(it, 3)
        for it1 in mapa_adresow:  # mapa adresow czyli posiada adres wzorcowy it[0] a w niem kilka adresow
            if Library.Cosinusowa(it_nGramy, Library.nGram(it1[0],
                                                           3)) < 0.3:  # rozniceNGramy(it, it1[0]):#czym mniejszy wynik tym wieksza zgodnosc
                # Library.Log(
                #    str(Library.Cosinusowa(Library.nGram(it, 3), Library.nGram(it1[0], 3))) + " "
                #    + str(it) +"\n"+ str(it1[0]))
                it1.append(it)  # dodajemy do listy adresow danej firmy dodatkowy adres
                znaleziono = True
                break
        if not znaleziono:
            lista.append(it)  # jezeli nie znaleziono to dodajemy nowa liste adresu
            mapa_adresow.append(lista)  # dodajemy liste do mapy
            lista = []
        log_len -= 1
        Library.Log("pozostało " + str(log_len) + " adresów")
    Library.Log("zakończono analize")

    # wypisanie tekstu
    tekst = ""

    Library.Log("rozpoczęcie zapisu")
    for it in mapa_adresow:
        for it1 in it:
            tekst += it1 + "\n"
        tekst += "\n##########\n"
    f = open("wyjscie.txt", "w")
    f.write(tekst)
    f.close()
    Library.Log("zakończenie zapisu")


klasteryzacja()
