from flask import Flask, render_template
try:
    from clp3 import clp
except:
    pass
import re

app = Flask(__name__)

weights = {
    ('Wydarzenie', 'Aktor', 'Cel', 'Obiekt', 'Narzędzie', 'Miejsce'): 1,
    ('Wydarzenie', 'Aktor', 'Cel', 'Obiekt', 'Narzędzie'): 0.95,
    ('Wydarzenie', 'Aktor', 'Cel', 'Obiekt', 'Miejsce'): 0.95,
    ('Wydarzenie', 'Aktor', 'Obiekt', 'Narzędzie', 'Miejsce'): 0.95,
    ('Miejsce', 'Cel', 'Wydarzenie', 'Aktor', 'Narzędzie'): 0.95,
    ('Wydarzenie', 'Cel', 'Obiekt', 'Narzędzie', 'Miejsce'): 0.95,
    ('Wydarzenie', 'Aktor', 'Obiekt', 'Narzędzie'): 0.9,
    ('Wydarzenie', 'Aktor', 'Obiekt', 'Miejsce'): 0.9,
    ('Wydarzenie', 'Aktor', 'Obiekt', 'Narzędzie'): 0.9,
    ('Wydarzenie', 'Aktor', 'Obiekt', 'Narzędzie'): 0.9,
    ('Wydarzenie', 'Aktor', 'Obiekt', 'Narzędzie'): 0.9,
    ('Wydarzenie', 'Aktor', 'Obiekt', 'Miejsce'): 0.9,
    ('Wydarzenie', 'Obiekt', 'Narzędzie', 'Miejsce'): 0.9,
    ('Wydarzenie', 'Cel', 'Obiekt', 'Narzędzie'): 0.9,
    ('Wydarzenie', 'Aktor', 'Cel'): 0.85,
    ('Wydarzenie', 'Aktor', 'Obiekt'): 0.85,
    ('Wydarzenie', 'Aktor', 'Miejsce'): 0.85,
    ('Wydarzenie', 'Obiekt', 'Narzędzie'): 0.85,
    ('Wydarzenie', 'Obiekt', 'Miejsce'): 0.85,
    ('Wydarzenie', 'Narzędzie', 'Miejsce'): 0.85,
    ('Wydarzenie', 'Cel', 'Obiekt'): 0.8,
    ('Wydarzenie', 'Cel', 'Miejsce'): 0.8,
    ('Wydarzenie', 'Narzędzie', 'Miejsce'): 0.8,
    ('Wydarzenie', 'Cel'): 0.75,
    ('Wydarzenie', 'Obiekt'): 0.75,
    ('Wydarzenie', 'Miejsce'): 0.75,
    ('Aktor', 'Cel', 'Obiekt'): 0.7,
    ('Aktor', 'Cel', 'Miejsce'): 0.7,
    ('Obiekt', 'Narzędzie', 'Miejsce'): 0.7,
    ('Cel', 'Obiekt', 'Narzędzie'): 0.7,
    ('Cel', 'Obiekt', 'Miejsce'): 0.7,
    ('Cel', 'Narzędzie', 'Miejsce'): 0.7,
    ('Wydarzenie',): 0.6,
    ('Aktor',): 0.6,
    ('Obiekt',): 0.6,
    ('Narzędzie',): 0.6,
    ('Cel',): 0.6,
    ('Miejsce',): 0.6,
}

formularz = {
    'Wydarzenie': ["wystawa", "wydarzenie", "pielęgnacja", "hodowla"],
    'Aktor': ["kot", "miłośnik", "goście", "pupil", "hodowcy", "kocięta", "sędziowie", "sędzia", "sędzina", "fife"],
    'Obiekt': ["nagroda", "Best in Show", "karma", "puchar", "dyplom", "klatka", "dokumenty"],
    'Narzędzie': ["pokaz", "doświadczenie", "wiedza", "stres", "wpłata", "opłata"],
    'Cel': ["wygrana", "prezentacja"],
    'Miejsce': ["miasta", "kraj", "Cat Show", "klub"],
}

colors = {
        'Wydarzenie': 'crimson',
        'Aktor': 'hotpink',
        'Obiekt': 'deepskyblue',
        'Narzędzie': 'indigo',
        'Cel': 'green',
        'Miejsce': 'darkgoldenrod',
    }
to_replace = ",.?!:;()[]{} "


marge_texts = []
all_texts = []
with open("../../teksty/AEI/merge.txt", "r", encoding='utf-8') as f:
    marge_texts = f.read().split("#####")

first_loop = True
lenght = 0
for key, value in formularz.items():
    id = 0
    for text in marge_texts:
        if first_loop:
            all_texts.append({'id': id, 'text': text, 'rating': 0, 'semantical_role': {}})
        for word in value:
            try:
                all_forms =  clp.forms(clp(word.lower())[0])
            except:
                all_forms = [word.lower()]
            for word_clp in all_forms:

                if word_clp in all_texts[id]['text'].lower():
                    if key not in all_texts[id]['semantical_role'] or all_forms not in all_texts[id]['semantical_role'][key]:
                        try:
                            all_texts[id]['semantical_role'][key].append(all_forms[0])
                        except:
                            all_texts[id]['semantical_role'][key] = [all_forms[0]]
                    for char in to_replace:
                        all_texts[id]['text'] = all_texts[id]['text'].replace(word_clp + char,
                                            "<mark style='color: "+ colors[key] +"; background-color: #eee;'>" + word_clp + "</mark>" + char)


        id+=1
    first_loop = False
    lenght = id


for it in all_texts:
    for key, value in weights.items():
        ok = True
        for role in key:
            if role not in it['semantical_role']:
                ok = False
        if ok and value > it['rating']:
            it['rating'] = value





@app.route("/")
def hello_world():
    # all_texts.sort(key=lambda x: x.rating, reverse=True)
    return render_template('all_texts.html', text_list=all_texts, length=lenght)


@app.route("/form")
def form():
    return render_template('form.html', form=formularz, length=len(formularz.keys()))


@app.route("/points")
def points():
    rating_list = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    return render_template('points.html', rating=rating_list, length=len(weights.keys()))


if __name__ == '__main__':
    #app.run(host='wierzba.wzks.uj.edu.pl', port=5335, debug=True)
    app.run(port=5335, threaded=True, debug=True)

