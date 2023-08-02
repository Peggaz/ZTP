import os  # Importowanie modułu os do operacji na plikach i folderach
import re  # Importowanie modułu re do pracy ze wzorcami regularnymi
from collections import Counter  # Importowanie klasy Counter z modułu collections

folder_path = "teksty4"  # Ścieżka do folderu "teksty"
file_list = [filename for filename in os.listdir(folder_path) if filename.endswith(".txt")]  # Tworzenie listy plików z rozszerzeniem ".txt" w folderze

cnt = Counter()  # Inicjalizacja licznika

for filename in file_list:  # Iteracja przez listę plików
    file_path = os.path.join(folder_path, filename)  # Pełna ścieżka do pliku
    with open(file_path, "rt") as file:  # Otwarcie pliku w trybie do odczytu tekstu
        stringFile = file.read()  # Odczytanie zawartości pliku

    word_list = stringFile.split()  # Podział tekstu na listę słów

    for word in word_list:  # Iteracja przez listę słów
        word = re.sub(r"[^a-zA-Ząćęłóśżź_]", '', word)  # Usunięcie znaków spoza zakresu a-zA-Ząćęłóśżź_ ze słowa
        if word:  # Jeśli słowo nie jest puste
            cnt[word] += 1  # Zwiększenie licznika dla danego słowa

myString = ''  # Inicjalizacja pustego łańcucha tekstowego
counter = 0  # Inicjalizacja licznika

for counter, key in enumerate(cnt.most_common(), start=1):  # Iteracja przez najczęstsze słowa w liczniku
    myString += "{} {}\n".format(counter, re.sub(r'[^a-zA-Ząćęłóśżź0-9_]', ' ', str(key)))

with open("frekwencyjna.csv", "w") as text_file:  # Otwarcie pliku wynikowego w trybie do zapisu
    text_file.write(myString)  # Zapisanie łańcucha tekstowego do pliku

