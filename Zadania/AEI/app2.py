#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
CLP_USE = False
if CLP_USE:
    from clp3 import clp
app = Flask(__name__)


sort_po_id = False
RULES_COLOR = {
    'Zdarzenie': "<a style='color:green'>",
    'Sprawca': "<a style='color:red'>",
    'Cel': "<a style='color:blue'>",
    'Obiekt': "<a style='color:yellow'>",
    'Narzędzie': "<a style='color:orange'>",
    'Miejsce': "<a style='color:magenta'>"
}

SEMANTICAL_RATING = {
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

MATCHING_RULES = {
    'Zdarzenie': ['zastosowanie', 'uczenie', 'learning', 'analiza'],
    'Sprawca': ['oprogramowanie', 'machine', 'maszyna'],
    'Cel': ['rozwiązanie', 'znalezienie', 'podejmowanie', 'decyzji', 'aplikacje'],
    'Obiekt': ['model', 'nadzorowane', 'nienadzorowane', 'dana', 'zbiór', 'maszynowy', 'neuron', 'wzorzec'],
    'Narzędzie': ['wzór', 'algorytm', 'reguła', 'neuronowe', 'funkcja', 'metoda', 'technologia'],
    'Miejsce': ['komputer', 'uniwersytet']
}


# @TODO:,Przeładować teksty od nowa

class TextAnalyzer:
    def replace_all(self, text, word, rule):
        text = text.replace(word + " ", RULES_COLOR[rule] + word + "</a>" + " ")
        text = text.replace(word + ",", RULES_COLOR[rule] + word + "</a>" + ",")
        text = text.replace(word + ".", RULES_COLOR[rule] + word + "</a>" + ".")
        text = text.replace(word + "(", RULES_COLOR[rule] + word + "</a>" + "(")
        text = text.replace(word + ")", RULES_COLOR[rule] + word + "</a>" + ")")
        text = text.replace(word + ":", RULES_COLOR[rule] + word + "</a>" + ":")
        return text

    def make_rating(self, list_role):
        if not list_role:
            return 0
        role_set = set(list_role)
        for roles, rating in SEMANTICAL_RATING.items():
            if set(roles) == role_set:
                return rating
        return 0

    def analyze_text(self, text):
        list_fined_word = []
        list_fined_role = []
        result_list = []
        word_list = text.split(" ")
        text_out = text
        unique_words = set()
        for rule in MATCHING_RULES:
            list_row = []
            for word in word_list:
                base_word = self.clpBasicWord(self.onlyLetter(word.lower()))
                if self.is_matching_rule(base_word, rule):
                    self.update_lists(base_word, rule, list_fined_word, list_fined_role)
                    text_out = self.replace_all(text_out, self.onlyLetter(word.lower()), rule)
                    self.add_to_list_row(base_word, rule, list_row, unique_words, list_fined_word)
            result_list.append(list_row)
        rating = int(self.make_rating(list_fined_role) * 100)
        return result_list, rating, text_out

    def is_matching_rule(self, base_word, rule):
        return base_word in MATCHING_RULES[rule]

    def update_lists(self, base_word, rule, list_fined_word, list_fined_role):
        if rule not in list_fined_role:
            list_fined_role.append(rule)
        list_fined_word.append(self.onlyLetter(base_word.lower()))

    def add_to_list_row(self, base_word, rule, list_row, unique_words, list_fined_word):
        if base_word not in unique_words:
            unique_words.add(base_word)

            if len(list_row) == 0:
                list_row.append(RULES_COLOR[rule] + rule + '</a>')
            list_row.append(base_word)

    def make_rating(self, list_role):
        if len(list_role) == 0:
            return 0
        semantic_ratings = {tuple(roles): rating for roles, rating in SEMANTICAL_RATING.items()}
        if tuple(list_role) in semantic_ratings:
            return semantic_ratings[tuple(list_role)]
        for roles, rating in semantic_ratings.items():
            if len(roles) == len(list_role) and all(role in roles for role in list_role):
                return rating
        return 0

    def onlyLetter(self, s):
        if isinstance(s, list):
            s = ''.join(s)
        s = s.replace("\n", " ").replace("  ", " ")
        return ''.join(x for x in s if x == " " or self.orALetter(x))

    def clpBasicWord(self, s):
        if CLP_USE:
            id = clp(s)
            if len(id) > 0:
                list_p = clp.forms(id[0])
                if len(list_p) > 0:
                    s = list_p[0]
        return s

    def orALetter(self, ch):
        if ch in "ąćęłńóśźż":
            return True
        z = ord(ch)
        if z >= ord("a") and z <= ord("z"):
            return True
        return False


class Text:
    def __init__(self, id, rating, text, list_result):
        self.text = text
        self.list = list_result
        self.rating = rating
        self.id = id


def make_text_out(text_analyzer):
    files = []
    for it in range(0, 100):
        files.append( open(f"../../teksty/AEI/{it}.txt", "r", encoding="utf-8").read().replace('\n', ' '))
    text_list = []
    for file_id in range(len(files)):
        list_result, rating, text = text_analyzer.analyze_text(files[file_id])
        text_list.append(Text(file_id, rating, text, list_result))
    return text_list

text_analyzer = TextAnalyzer()
text_list = make_text_out(text_analyzer)
text_list.sort(key=lambda e: -float(e.rating))
# Do something with the text_list


# TEXT = tabele, tekst,


@app.route("/", methods=['GET'])
def txts():
    return render_template("all.html", text_list=text_list, length=len(text_list))

    # return render_template("index_old.html")


@app.route("/roles", methods=['GET'])
def roles():
    semantyka = sorted(SEMANTICAL_RATING.items(), key=lambda kv: kv[1], reverse=True)
    return render_template("semantyki.html", semantyka=semantyka)


@app.route("/wght", methods=['GET'])
def wght():
    return render_template("wagi.html", wagi=MATCHING_RULES)


############################################

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)
    #app.run(host='wierzba.wzks.uj.edu.pl', debug=True, port=5334)
