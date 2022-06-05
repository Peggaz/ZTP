#!flask/bin/python
# -*- coding: utf-8 -*-

import os

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'templates')
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Library')
try:
    import library
except:
    pass
try:
    from Zadania.Library import library
except:
    pass
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

semantyka_tab = []
text_list = []
tab_wagi = []
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

class Text:
    def __init__(self, id, rating, text="", list=[]):
        self.text = text
        self.list = list
        self.rating = rating
        self.id = id


def replace_all(text, word, rule):
    if word[0] in 'ABCDEFGHIJKLMNOPRSTUWXYZ' or word[0] == " ":
        text = text.replace(word + " ", RULES_COLOR[rule] + word + "</a>" + " ")
        text = text.replace(word + ",", RULES_COLOR[rule] + word + "</a>" + ",")
        text = text.replace(word + ".", RULES_COLOR[rule] + word + "</a>" + ".")
        text = text.replace(word + "(", RULES_COLOR[rule] + word + "</a>" + "(")
        text = text.replace(word + ")", RULES_COLOR[rule] + word + "</a>" + ")")
        text = text.replace(word + ":", RULES_COLOR[rule] + word + "</a>" + ":")
    else:
        text = replace_all(text, " " + word, rule)
        word = word[0].upper() + word[1:]
        text = replace_all(text, word, rule)
    return text


def make_rating_old(rating):
    if rating == 0:
        rating = 10
    elif rating == 90:
        rating = 100
    else:
        rating += 20
    return rating


def make_rating(list_role):
    if len(list_role) == 0:
        return 0
    if tuple(list_role) in SEMANTICAL_RATING:
        return SEMANTICAL_RATING[tuple(list_role)]
    for it in SEMANTICAL_RATING:
        yes = True
        if len(it) != len(list_role):
            continue
        for role in list_role:
            if role not in it:
                yes = False
                break
        if yes:
            return SEMANTICAL_RATING[it]
    return 0


def tex_analize(text):
    list_fined_word = []
    list_fined_role = []
    list = []
    rating = []
    text_out = text
    first_for = True
    for rule in MATCHING_RULES:
        list_row = []
        for word in text.split(" "):
            base_word = library.CLPBasicWord(library.OnlyLetter(word.lower()))
            if base_word in MATCHING_RULES[rule] and word not in list_fined_word:
                if not rule in list_fined_role:
                    list_fined_role.append(rule)
                list_fined_word.append(library.OnlyLetter(word.lower()))
                text_out = replace_all(text_out, library.OnlyLetter(word.lower()), rule)
                if base_word not in list_row:
                    if len(list_row) == 0:
                        list_row.append(RULES_COLOR[rule] + rule + '</a>')
                    list_row.append(base_word)
        list.append(list_row)
    rating = int(make_rating(list_fined_role)*100)
    return list, rating, text_out


def make_text_out():
    files = library.LoadText("../../teksty/AEI/all_text.txt")
    files = files.replace('\n', ' ')
    files = files.split('#0')
    files.pop(0)
    for file_id in range(len(files)):
        list, rating, text = tex_analize(files[file_id][3:])
        text_list.append(Text(int(files[file_id][1:3]), rating, text, list))


def main():
    make_text_out()


main()


@app.route("/", methods=['GET', 'POST'])
def index():
    DESC_id = 1
    DESC_rating = 1
    if request.method == 'POST':

        if 'Sortuj po ocenie' in request.form['sort_value']:
            if 'malejąco' in request.form['sort_value']:
                DESC_rating = 0

            def key(e):
                return -float(e.rating)

            def key_desc(e):
                return float(e.rating)

            if DESC_rating:
                text_list.sort(key=key_desc)
            else:
                text_list.sort(key=key)
            pass

        elif 'Sortuj po id' in request.form['sort_value']:
            if 'malejąco' in request.form['sort_value']:
                DESC_id = 0

            def key(e):
                return int(e.id)

            def key_desc(e):
                return -int(e.id)

            if DESC_id:
                text_list.sort(key=key_desc)
            else:
                text_list.sort(key=key)
            pass
    return render_template("index.html", teksty=text_list, desc_id=DESC_id, desc_rating=DESC_rating)
    # return render_template("index_old.html")


@app.route("/semantyka", methods=['GET'])
def semantyka():
    return render_template("semantyki.html", semantyka=library.SortDic(SEMANTICAL_RATING))


@app.route("/wagi", methods=['GET'])
def wagi():
    return render_template("wagi.html", wagi=MATCHING_RULES)


############################################

if __name__ == '__main__':
    #app.run(host='localhost', debug=True, port=5003)
    app.run(host='wierzba.wzks.uj.edu.pl', debug=True, port=5010)
