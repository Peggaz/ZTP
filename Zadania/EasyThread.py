import threading, queue
import datetime
import multiprocessing

class OnVariableThread(threading.Thread):
    '''
    SKUP SIĘ
    prosta klasa która musi współpracować z oppowiednio napisanmi metodami ale to python
    niestety przekazujemu zmienne do wątków za pomocą listy argówmentów
    i tu mamy dwa wyjścia:
        1 przekazujemy listę z jedną zmienna albo piszemy nowe wątki
        2 przekazujemy w liście zmiennych wiele wartości ale funkcja musi odbierać i przekształcać to
            z listy argumentow na operacyjne
            PATRZ wywołanie w "test"
    '''
    def __init__(self, id, tasks, function):
        '''
        koństruktor klasy dzołającej na wątku która analizuje tekst i wywołuje pojedyńczą funkcję z jedną zmienną
        :param id: id tekstu do analizy
        :param tasks: kolejka zapytań
        :param log: funkcja odpowiadająca za logowanie zdarzeń
        :param function: Funkcja obliczająca
        '''
        self.ID = id
        self.tasks = tasks
        self.function = function
        threading.Thread.__init__(self, name="WątekTF-%d" % (id,))

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
                varible, ret_queue = req
            except:
                break
            ret = self.function(varible)
            ret_queue.put(ret)
            self.tasks.task_done()

def EasyThread(list, function):
    '''
    :param list: lista zawierająca elementy do analizy przez wątek
    :param function: funkcja przez którą mają przejść wartości z wątku
    :return: wartości zwrócone przez wątek w formie listy
    '''
    request_queue = queue.Queue()
    resalt_queue = queue.Queue()
    x_thread = multiprocessing.cpu_count() * 2
    for it in range(x_thread):
        OnVariableThread(it, request_queue, function).start()
    for it in list:
        request_queue.put((it, resalt_queue))
    ret_list = []
    for it in range(len(list)):
        ret_list.append(resalt_queue.get())
    for i in range(x_thread):
        request_queue.put(None)
    request_queue.join()
    return ret_list