from flask import Flask, render_template, request
import os
import re
try:
    from clp3 import clp as clp#TODO: uncomment
except:
    pass
from typing import List, Tuple, Set
app = Flask(__name__)
# Słownik zawierający słowa kluczowe, wagi i kolory
keyword_dict = {
    'Cel': (['fryderyk', 'plebiscyt', 'nagroda','paszport', 'fryderyka', 'fryderykowi', 'fryderykiem',
             'fryderyku', 'fryderykowie', 'fryderyków', 'fryderyki', 'fryderykom', 'fryderykami'], 0.1, '#ff5f77'),
    'Zdarzenie': (['koncert', 'spektakl', 'trasa', 'zagrać', 'wygrać', 'zwyciężyć'], 0.25, '#e7859e'),
    'Obiekt': (['diamentowa', 'platynowa', 'klip'], 0.15, '#d3a0d3'),
    'Sprawca': (['artysta', 'wokalista', 'twórca'], 0.2, '#9eddff'),
    'Miejsce': (['pge','Górnicza','dąbrowa','chorzów', 'chorzowie', 'chorzowa', 'chorzowowi', 'chorzowem', 'dąbrowy',
                 'dąbrowie', 'dąbrowę', 'dąbrową', 'dąbrowo', 'górniczej', 'górniczą'], 0.2, '#1fb1ff'),
    'Narzędzie': (['bilet','tekst','scena','produkt', 'program', 'materiał' ], 0.1, '#8089ff'),
}
znaki = "`.,;~!?  "

class Text:
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.categories = []
        self.category_sum = 0

class AllTexts:
    def __init__(self):
        self.texts = []
        self.total_category_sum = 0
        self.total_categories = 0

    def run(self):
        self.read_text()
        self.make_categories()

    def read_text(self):

        for file in os.listdir('teksty4'):#TODO zmienić ścieżkę
            with open(f'teksty4/{file}', 'r', encoding='utf-8') as f:
                text = f.read()
                self.texts.append(Text(text, file))

    def make_categories(self):
        for text_object in self.texts:
            # print(text_object.text)
            clear_text = text_object.text
            for znak in znaki:
                clear_text = clear_text.replace(znak, " ")
            for word in clear_text.split(" "):
                for key, value in keyword_dict.items():
                    word_forms = [word.lower()]
                    clp_forms = []
                    try:
                        clp_forms = clp.forms(clp.rec(word.lower())[0])
                    except:
                        pass
                    if len(clp_forms) > 0:
                        word_forms = clp_forms
                    # if(word == "diamentową"):
                    #     print(word_forms)
                    for word_form in word_forms:  # TODO odkomontować Pobierz formy słowa
                        if word_form in value[0] or word in value[0]:
                            if key not in text_object.categories:
                                text_object.categories.append(key)
                                text_object.category_sum += value[1]
                            text_object.text = self.color_text(word, text_object.text, value[2])
                            # if text_object.filename == "94.txt":
                            #     print(word, key, value[1], text_object.text)


    def color_text(self, word, text, color):
        for znak in znaki:
            replacement = f'<span style="background-color: {color}; font-weight: bold;">{word}</span>{znak}'
            text = text.replace(word+znak, replacement)
        return text




allTexts = AllTexts()
allTexts.run()
allTexts.texts = sorted(allTexts.texts, key=lambda x: [x.category_sum, -int(x.filename[:-4])], reverse=True)



# Route do wyświetlania listy tekstów
@app.route('/')
def display_texts():
    return render_template('index.html', texts=allTexts.texts)

# Route do wyświetlania kategorii
@app.route("/category")
def category():
    return render_template('category.html', keyword_dict=keyword_dict)

# Route do wyświetlania listy frekwencyjnej
@app.route("/words")
def words():
        slowa = []
        with open('frekwencyjna_bazowa_odsiane.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                row = line.split()
                slowa.append(row)

        return render_template('words.html', slowa=slowa)


# Route do wyświetlania listy tekstów
if __name__ == '__main__':
    app.run()
   # app.run(host="wierzba.wzks.uj.edu.pl", port=5335, debug=True, use_reloader=True)

