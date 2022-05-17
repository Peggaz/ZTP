import Zadania.Library.library as Library
import time
import datetime
import threading, queue
#Library.TFIDF("../teksty/papk.txt")
def log(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print("%s %s" % (now, message))

def oblicz(x):
    time.sleep(x)
    return x * x

# Watki w puli oczekujace na zadania w kolejce ``kolejka_zadan``
class WatekOblicz(threading.Thread):
    def __init__(self, id, kolejka_zadan):
        threading.Thread.__init__(self, name="WatekOblicz-%d" % (id,))
        self.kolejka_zadan = kolejka_zadan
    def run(self):
        while True:
            # watek sie blokuje w oczekiwaniu az cos trafi do kolejki
            req = self.kolejka_zadan.get()
            if req is None:
                # Nie ma nic wiecej do przetwarzania, wiec konczymy
                self.kolejka_zadan.task_done()
                break
            value, kolejka_rezultatow = req
            result = oblicz(value)
            log("%s %s -> %s" % (self.getName(), value, result))
            kolejka_rezultatow.put(result)
            self.kolejka_zadan.task_done()



def threaded_sum(values, kolejka_zadan):
    nsum = 0.0
    kolejka_rezultatow = queue.Queue()
    for value in values:
        kolejka_zadan.put((value, kolejka_rezultatow))
    # pobieramy wyniki; kolejnosc odpowiedzi nie musi byc identyczna jak zadan!
    # uzycie "_" jest konwencja oznaczajaca "wartosc tej zmiennej mnie nie interesuje"
    for _ in values:
        nsum += kolejka_rezultatow.get()
    return nsum

def main():
    kolejka_zadan = queue.Queue()
    log("uruchamiam watek glowny")
    # inicjalizujemy pule watkow z trzema watkami "obliczeniowymi"
    N_liczba_watkow = 3
    for i in range(N_liczba_watkow):
        WatekOblicz(i, kolejka_zadan).start()

    # wrzucamy 5 zadan
    result = threaded_sum( (4, 5, 3, 1.5, 2.2), kolejka_zadan )
    log("suma wynosi: %f" % (result,))

    # wysylamy zadania zakonczenia przetwarzania do wszystkich watkow
    for i in range(N_liczba_watkow):
        kolejka_zadan.put(None)
    kolejka_zadan.join()
    log("koniec watku glownego.")

if __name__ == "__main__":
    main()