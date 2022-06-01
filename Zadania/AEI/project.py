#!flask/bin/python
# -*- coding: utf-8 -*-

import os
template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'templates')
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/Library')
import library

from flask import Flask
from flask import render_template
from flask import request

import library

app = Flask(__name__)

semantyka_tab = []
text_list = []
tab_wagi = []
sort_po_id = False
RULES_COLOR = {
    'zdarzenie': "<a style='color:green'>",
    'Sprawca': "<a style='color:red'>",
    'Cel': "<a style='color:blue'>",
    'Obiekt': "<a style='color:yellow'>",
    'Narzędzie': "<a style='color:orange'>",
    'Miejsce': "<a style='color:magenta'>"
}

MATCHING_RULES = {
    'zdarzenie':    ['zastosowanie', 'uczenie', 'learning', 'analiza'],
    'Sprawca':      ['model', 'oprogramowanie', 'machine', 'maszyna'],
    'Cel':          ['rozwiązanie', 'znalezienie', 'podejmowanie', 'decyzji', 'aplikacje'],
    'Obiekt':       ['model', 'nadzorowane', 'nienadzorowane', 'dana', 'zbiór', 'maszynowy', 'neuron', 'wzorzec'],
    'Narzędzie':    ['wzór', 'algorytm', 'reguła', 'neuronowe', 'funkcja', 'metoda', 'technologia'],
    'Miejsce':      ['komputer', 'uniwersytet']
}

SEMANTICAL_RULES = {
    '1 dopasowanie': '10%',
    '2 dopasowanie': '30%',
    '3 dopasowanie': '50%',
    '4 dopasowanie': '70%',
    '5 dopasowanie': '90%',
    '6 dopasowanie': '100%'

}
#@TODO:,Przeładować teksty od nowa

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

def make_rating(rating):
    if rating == 0:
        rating = 10
    elif rating == 90:
        rating = 100
    else:
        rating += 20
    return rating


def tex_analize(text):
    list_fined_word = []
    list = []
    rating = 0
    text_out = text
    first_for = True
    for rule in MATCHING_RULES:
        list_row = []
        for word in text.split(" "):
            base_word = library.CLPBasicWord(library.OnlyLetter(word.lower()))
            if base_word in MATCHING_RULES[rule] and word not in list_fined_word:
                list_fined_word.append(library.OnlyLetter(word.lower()))
                text_out = replace_all(text_out, library.OnlyLetter(word.lower()), rule)
                if base_word not in list_row:
                    if len(list_row) == 0:
                        rating = make_rating(rating)
                        list_row.append(RULES_COLOR[rule] + rule + '</a>')
                    list_row.append(base_word)
        list.append(list_row)
    return list, rating, text_out
def make_text_out():
    files = library.LoadText("../../teksty/AEI/all_text.txt")
    files = files.replace('\n', ' ')
    files = files.split('#0')
    files.pop(0)
    for file_id in range(len(files)):
        list, rating, text = tex_analize(files[file_id][3:])
        text_list.append(Text(files[file_id][1:3], rating, text, list))

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
            else: text_list.sort(key=key)
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
            else: text_list.sort(key=key)
            pass
    return render_template("index.html", teksty=text_list, desc_id=DESC_id, desc_rating=DESC_rating )
    #return render_template("index_old.html")

@app.route("/semantyka", methods=['GET'])
def semantyka():
    return render_template("semantyki.html", semantyka=SEMANTICAL_RULES)

@app.route("/wagi", methods=['GET'])
def wagi():
    return render_template("wagi.html", wagi=MATCHING_RULES)

############################################

if __name__ == '__main__':
    #app.run(host='localhost', debug=True, port=5003)
    app.run(host='wierzba.wzks.uj.edu.pl', debug=True, port=5005)
