from flask import Flask, render_template
import json
CLP_USE = False
if CLP_USE:
    from clp3 import clp

import re

app = Flask(__name__)




class Color:
    def __init__(self, text):
        self.text = text
        self.colors = {
            'Zdarzenie': "<a style='color:green'>",
            'Sprawca': "<a style='color:red'>",
            'Cel': "<a style='color:blue'>",
            'Obiekt': "<a style='color:yellow'>",
            'Narzędzie': "<a style='color:orange'>",
            'Miejsce': "<a style='color:magenta'>"
        }

    def colored(self, word, key):
        for it in ' ,.():"':
            self.text = self.text.replace(f'{word}{it}', f" {self.colors[key]}{word}</a>{it}")
        return self.text

class Text:
    def __init__(self, text, id):
        self.text = text
        self.table = {}
        self.rating = 0
        self.id = id

    def setText(self, text):
        self.text = text

    def setList(self, list):
        self.list = list

    def setRating(self, rating):
        self.rating = rating

class Raitng:
    def __init__(self, text_obj):
        self.rules = {
            "Sprawca": ["artysta", "wokalista", "muzyk", "piosenkarz", "aktor"],
            "Zdarzenie": ["koncert", "sesja", "trasa", "występ", "premiera", "wywiad"],
            "Narzędzie": ["mikrofon", "głos", "moda"],
            "Obiekt": ["album", "marka", "pleasing", "outfit", "tekst", "styl", "muzyka"],
            "Cel": ["kariera", "rozwój", "inspiracja", "promocja", "wpływ"],
            "Miejsce": ["vogue", "scena", "stadion", "showbiznes"]
        }
        self.semantics = {
            ('Zdarzenie', 'Sprawca', 'Cel', 'Obiekt', 'Narzędzie', 'Miejsce'): 1
            , ('Zdarzenie', 'Sprawca', 'Cel', 'Obiekt', 'Narzędzie'): 0.95
            , ('Zdarzenie', 'Sprawca', 'Cel', 'Obiekt', 'Miejsce'): 0.95
            , ('Zdarzenie', 'Sprawca', 'Cel', 'Obiekt', 'Miejsce'): 0.95
            , ('Zdarzenie', 'Sprawca', 'Obiekt', 'Narzędzie', 'Miejsce'): 0.95
            , ('Zdarzenie', 'Cel', 'Obiekt', 'Narzędzie', 'Miejsce'): 0.95
            , ('Sprawca', 'Cel', 'Obiekt', 'Narzędzie', 'Miejsce'): 0.95
            , ('Zdarzenie', 'Sprawca', 'Cel', 'Narzędzie'): 0.9
            , ('Zdarzenie', 'Sprawca', 'Obiekt', 'Narzędzie'): 0.9
            , ('Zdarzenie', 'Cel', 'Obiekt', 'Narzędzie'): 0.9
            , ('Sprawca', 'Cel', 'Obiekt', 'Narzędzie'): 0.9
            , ('Zdarzenie', 'Sprawca', 'Cel', 'Obiekt'): 0.8
            , ('Zdarzenie', 'Sprawca', 'Cel', 'Miejsce'): 0.8
            , ('Zdarzenie', 'Sprawca', 'Obiekt', 'Miejsce'): 0.8
            , ('Zdarzenie', 'Cel', 'Narzędzie', 'Miejsce'): 0.8
            , ('Zdarzenie', 'Cel', 'Obiekt', 'Miejsce'): 0.75
            , ('Sprawca', 'Cel', 'Obiekt', 'Miejsce'): 0.75
            , ('Narzędzie', 'Cel', 'Obiekt', 'Miejsce'): 0.75
            , ('Narzędzie', 'Cel', 'Sprawca', 'Miejsce'): 0.75
            , ('Obiekt', 'Zdarzenie', 'Narzędzie', 'Miejsce'): 0.75
            , ('Zdarzenie', 'Sprawca', 'Narzędzie'): 0.7
            , ('Zdarzenie', 'Cel', 'Narzędzie'): 0.7
            , ('Sprawca', 'Cel', 'Narzędzie'): 0.7
            , ('Obiekt', 'Narzędzie', 'Miejsce'): 0.7
            , ('Cel', 'Obiekt', 'Narzędzie'): 0.6
            , ('Zdarzenie', 'Cel', 'Miejsce'): 0.65
            , ('Sprawca', 'Cel', 'Miejsce'): 0.65
            , ('Zdarzenie', 'Sprawca', 'Cel'): 0.65
            , ('Zdarzenie', 'Sprawca', 'Obiekt'): 0.65
            , ('Sprawca', 'Obiekt', 'Narzędzie'): 0.65
            , ('Zdarzenie', 'Cel', 'Obiekt'): 0.6
            , ('Sprawca', 'Cel', 'Obiekt'): 0.6
            , ('Zdarzenie', 'Sprawca', 'Miejsce'): 0.6
            , ('Zdarzenie', 'Narzędzie', 'Miejsce'): 0.6
            , ('Zdarzenie', 'Narzędzie', 'Obiekt'): 0.6
            , ('Zdarzenie', 'Narzędzie'): 0.4
            , ('Sprawca', 'Narzędzie'): 0.4
            , ('Zdarzenie', 'Sprawca'): 0.4
            , ('Cel', 'Narzędzie'): 0.4
            , ('Sprawca', 'Cel'): 0.4
            , ('Sprawca', 'Obiekt'): 0.3
            , ('Obiekt', 'Narzędzie'): 0.4
            , ('Sprawca', 'Miejsce'): 0.4
            , ('Zdarzenie', 'Cel'): 0.3
            , ('Zdarzenie', 'Obiekt'): 0.3
            , ('Zdarzenie', 'Miejsce'): 0.3
            , ('Narzędzie', 'Miejsce'): 0.3
            , ('Cel', 'Miejsce'): 0.3
            , ('Cel', 'Obiekt'): 0.3
            , ('Obiekt', 'Miejsce'): 0.3
            , ('Narzędzie',): 0.2
            , ('Sprawca',): 0.2
            , ('Cel',): 0.1
            , ('Zdarzenie',): 0.1
            , ('Miejsce',): 0.1
            , ('Obiekt',): 0.1
        }
        self.text_obj = text_obj

    def run(self):
        self.textAnalize()
        self.calculateRaiting()

    def textAnalize(self):
        color = Color(self.text_obj.text)
        clear_text = self.text_obj.text.replace(",", "").replace(".", "").replace("?", "").replace("!", "").replace(":", "").replace(";", "").replace("(", "").replace(")", "").replace("\"", "").replace("\'", "").replace("\n", "").replace('"', '')
        for word in clear_text.split(" "):
            for key, value in self.rules.items():
                base_word = word.lower()
                if CLP_USE:
                    id = clp(base_word)
                    if len(id) > 0:
                        list_p = clp.forms(id[0])
                        if len(list_p) > 0:
                            base_word = list_p[0]
                if base_word in value:
                    self.text_obj.text = color.colored(word, key)#tekst pokolorowany
                    self.text_obj.text = color.colored(base_word, key)  # tekst pokolorowany
                    if key in self.text_obj.table and word not in self.text_obj.table[key]:
                        self.text_obj.table[key].append(word)
                    else:
                        self.text_obj.table[key] = [word]

    def calculateRaiting(self):
        if len(self.text_obj.table) == 0:
            self.text_obj.rating = 0
            return
        if tuple(self.text_obj.table.keys()) in self.semantics:
            self.text_obj.rating = self.semantics[tuple(self.text_obj.table.keys())]
        else:
            for item in self.semantics:
                ok = True
                for it in item:
                    if it not in self.text_obj.table.keys():
                        ok = False
                        break
                if ok:
                    self.text_obj.rating = self.semantics[item]
                    return

class AllText:
    def __init__(self):
        files = open("../../teksty/AEI/all_text_app3.txt", "r", encoding="utf-8").read()
        self.files = files.split("#####")
        self.list_text = []

    def analize(self):
        id = 0
        for file in self.files:
            text = Text(file, id)
            id += 1
            raiting = Raitng(text)
            raiting.run()
            self.list_text.append(raiting.text_obj)



all_text = AllText()
all_text.analize()
reting = Raitng(all_text.list_text[0].text)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index3.html", list_text=all_text.list_text)

@app.route("/semantyka", methods=['GET'])
def semantyka():
    return render_template("semantyki.html", semantyka=reting.semantics)


@app.route("/wagi", methods=['GET'])
def wagi():
    return render_template("wagi.html", wagi=reting.rules)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)
    # app.run(host='wierzba.wzks.uj.edu.pl', debug=True, port=5335)
