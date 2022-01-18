import Library
import threading, queue
import datetime
import multiprocessing
import math

class TFIDF:
    def __Log(self, message):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print ("%s %s" % (now, message))

    class __TFThread(threading.Thread):
        '''
        Klasa obsługująca wątek wyliczający tf dla każdego tekstu
        '''

        def __init__(self, id, tasks, log):
            '''
            koństruktor klasy dzołającej na wątku która analizuje tekst i oblicza słownik TF
            :param id: id tekstu do analizy
            :param tasks: kolejka zapytań
            :param log: funkcja odpowiadająca za logowanie zdarzeń
            '''
            self.ID = id
            self.tasks = tasks
            self.log = log
            threading.Thread.__init__(self, name="WątekTF-%d" % (id,))

        def __TF(self, file):
            '''
            Obliczenie słownika TF dla pliku wejściowego
            :param file: plik wejściowy w formie ciągu znaków
            :return: słownik TF dla danych słów
            '''
            TF_for_words = {}
            self.log("przeanalizowano plik o id: " + file[1:6])
            file = Library.OnlyLetter(file)
            attendance_list = Library.AttendanceListCLP(file, {})
            for word, value in attendance_list.items():
                TF_for_words[word] = value / len(attendance_list)
            return TF_for_words

        def run(self):
            '''
            funkcja główna startująca wątek
            '''
            while True:
                req = self.tasks.get()
                if req == None:
                    self.tasks.task_done()
                    break
                try:
                    file, ret_queue = req
                except:
                    break
                ret = self.__TF(file)
                ret_queue.put(ret)
                self.tasks.task_done()

    def __init__(self, src):
        '''
            koństruktor
        '''
        self.__file = Library.LoadText(src).lower()
        self.__file = self.__file.split("#0")

    def MakeAndSaveTFIDF(self):
        '''
           wczutuję tekst i dzieli go po # jest to specyfika pliku wsadowego
           :param s: ściężka do pliku domyślnie "pop.txt"
       '''
        self.TF_list = []
        self.__Log("Przygotowano " + str(len(self.__file)) + " do analizy")
        request_queue = queue.Queue()
        resalt_queue = queue.Queue()
        x_thread = multiprocessing.cpu_count() * 2  # liczba wątków robocza ustawiona na 15 jak uda mi się znaleźć funkcję zliczającą wątki procesora to ustawie liczbę wątków * 2
        self.__Log("rozpoczęto towrznie " + str(x_thread) + "wątków")
        for it in range(x_thread):
            self.__TFThread(it, request_queue, self.__Log).start()

        # for file in ret:
        # self.resalt_queue.put(TFThread(file.split(("\n"))[1:], file.split("\n")[0]).start())
        for it in self.__file:
            request_queue.put((it, resalt_queue))

        for it in range(len(self.__file)):
            self.TF_list.append(resalt_queue.get())

            # wysylamy zadania zakonczenia przetwarzania do wszystkich watkow
        for i in range(x_thread):
            request_queue.put(None)
        request_queue.join()
        self.__Log("zakonczono alalize, następuje zapis TF")
        self.__SaveTF(self.TF_list)
        self.__Log("zakonczono zapis TF, rozpoczęto obliczanie IDF")
        self.IDF_dict = self.__IDF(self.TF_list)
        self.__Log("zakonczono obliczanie IDF, rozpoczęto zapis IDF")
        self.__IDF(self.IDF_dict)
        self.__Log("zakończono zapis IDF")

    def __IDF(self, TF_list):
        '''
        :return: słownik IDF gdzie do każdego słowa przypisana jest wartość jego IDF dla całego zbioru tekstów
        '''
        dict1 = {}
        IDF_dict = {}
        for it in TF_list:
            for key in it:
                dict1[key] = dict1.get(key, 0) + 1
        for it in dict1:
            IDF_dict[it] = math.log10(100 / float(dict1[it]))
        return IDF_dict

    def NewSentence(self):
        '''
        Funkcja pozwala na dodanie nowego słowa bądź słów i obliczenie TF i idf dla danej senctecji
        '''
        TFIDF_dicts_list = []
        for TF_dict in self.TF_list:
            TFIDF_dict_for_file = {}
            for key in TF_dict:
                if key not in self.IDF_dict:
                    print(key)
                TFIDF_dict_for_file[key] = TF_dict[key] * self.IDF_dict[key]
            TFIDF_dicts_list.append(TFIDF_dict_for_file)
        new_word = input("podaj frazę bądz 0 aby wyjsc\n->")
        if new_word == "0":
            return True
        new_word_dict = Library.AttendanceListCLP(new_word)

        TF_dict_for_new_word = {}
        TFIDF_dict_for_new_word = {}
        for slowo in new_word_dict:
            TF_dict_for_new_word[slowo] = new_word_dict[slowo] / len(new_word_dict)
            if slowo not in self.IDF_dict:
                self.IDF_dict[slowo] = math.log10(100 / float(1))
            TFIDF_dict_for_new_word[slowo] = TF_dict_for_new_word[slowo] * self.IDF_dict[slowo]
        numer_tesktu = 0
        for slownikTFIDF in TFIDF_dicts_list:
            mnozenie = 0
            vector1 = 0
            vector2 = 0
            for slowo in new_word_dict:
                liczba = 0
                if slowo in slownikTFIDF: liczba = slownikTFIDF[slowo]
                mnozenie += TFIDF_dict_for_new_word[slowo] * liczba
                vector1 += liczba
                vector2 += TFIDF_dict_for_new_word[slowo]

            if vector1 > 0 and vector2 > 0:
                # print("w tekscie " + str(numer_tesktu) + " podobienstwo frazy \n" + str(mnozenie/(math.sqrt(vector1)) * (math.sqrt(vector2))))
                print("w tekscie " + str(numer_tesktu) + " podobienstwo frazy \n" + str(
                    vector1 * vector2 / (len(TFIDF_dict_for_new_word) * len(slownikTFIDF))))

            numer_tesktu += 1

        # vector_slownikow.append(slownilTFIDF_frazy)
        return False

    def __SaveTF(self, TF_list):
        out_file = open('../wyniki/' + "TF" + '.txt', 'w', encoding='utf-8', newline='')
        numer_plikow = 0
        for it in TF_list:
            out_file.write("slowo\t\t\t\t\t| TF\n")
            out_file.write("------ " + str(numer_plikow) + " -------\n")
            numer_plikow += 1
            for key, value in it.items():
                out_file.write(key + "\t\t\t\t\t| " + str(value) + "\n")

    def __SaveIDF(self, slownikIDF):
        tresc = open('../wyniki/' + "IDF" + '.txt', 'w', encoding='utf-8', newline='')
        tresc.write("slowo\t\t\t\t\t| IDF\n")
        tresc.write("------  -------\n")
        for it in slownikIDF:
            tresc.write(it + "\t\t\t\t\t| " + str(slownikIDF[it]) + "\n")

tf = TFIDF("../teksty/papk.txt")
tf.MakeAndSaveTFIDF()