
from Zadania.Library import library


def klasteryzacja():
    lista = []
    mapa_adresow = []
    plik = library.LoadText("../../teksty/klasteryzacja.txt")
    adresy = plik.split('\n')
    lista.append(adresy[0])
    mapa_adresow.append(lista)
    lista = []
    library.Log("zakończono przygotowanie do pracy")
    log_len = len(adresy)
    for it in adresy:  # iterujemy po adresach ktore odzielamy po entaerach
        znaleziono = False
        it_nGramy = library.nGram(it, 3)
        for it1 in mapa_adresow:  # mapa adresow czyli posiada adres wzorcowy it[0] a w niem kilka adresow
            if library.Cosinusowa(it_nGramy, library.nGram(it1[0],
                                                           3)) < 0.3:  # rozniceNGramy(it, it1[0]):#czym mniejszy wynik tym wieksza zgodnosc
                # library.Log(
                #    str(library.Cosinusowa(Library.nGram(it, 3), Library.nGram(it1[0], 3))) + " "
                #    + str(it) +"\n"+ str(it1[0]))
                it1.append(it)  # dodajemy do listy adresow danej firmy dodatkowy adres
                znaleziono = True
                break
        if not znaleziono:
            lista.append(it)  # jezeli nie znaleziono to dodajemy nowa liste adresu
            mapa_adresow.append(lista)  # dodajemy liste do mapy
            lista = []
        log_len -= 1
        library.Log("pozostało " + str(log_len) + " adresów")
    library.Log("zakończono analize")

    # wypisanie tekstu
    tekst = ""

    library.Log("rozpoczęcie zapisu")
    for it in mapa_adresow:
        for it1 in it:
            tekst += it1 + "\n"
        tekst += "\n##########\n"
    f = open("wyjscie.txt", "w")
    f.write(tekst)
    f.close()
    library.Log("zakończenie zapisu")


klasteryzacja()
