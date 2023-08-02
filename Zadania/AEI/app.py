from flask import Flask, render_template
import json
CLP_USE = False
if CLP_USE:
    from clp3 import clp

import re

app = Flask(__name__)

class Data:
    def __init__(self):
        self.json_data = None
        with open('data.json', 'r', encoding='utf-8') as f:
            json_data = f.read()
            self.json_data = json.loads(json_data)

    def convert(self):
        return self.json_data

    def getSematicalRaiting(self):
        return self.json_data['semantical_ratings']

    def getMatchingRules(self):
        return self.json_data['matching_rules']

class Text:
    def __init__(self, text, id_text):
        self.text = text
        self.id_text = id_text
        self.semantics_dict = {}
        self.value = None

    def getIs(self):
        return self.value > 0.5

    def makeSemantics(self, data):
        for word in self.text.split(" "):
            for key, value in data.getMatchingRules().items():
                for rule in value:
                    if self.clpBasicWord(word).lower() == self.clpBasicWord(rule):
                        try:
                            self.semantics_dict[key].append(rule)
                        except:
                            self.semantics_dict[key] = [rule]
                        self.replace_all(word, data, key)
        self.value = self.__calculateValue(data)

    def replace_all(self, word, data, key):
        self.text = self.text.replace(word, f"<span style='color: {data.json_data['colors'][key]}'>{word}</span>")
    def __calculateValue(self, data):
        sematicalRaiting = data.getSematicalRaiting()
        for item in sematicalRaiting:
            ok = True
            for it in item['semantical']:
                if it not in self.semantics_dict.keys():
                    ok = False
                    break
            if ok:
                return item['value']
        return 0

    def clpBasicWord(self, word):
        if CLP_USE:
            id = clp(word)
            if len(id) > 0:
                list_p = clp.forms(id[0])
                if len(list_p) > 0:
                    s = list_p[0]
        return word


class AllText:
    def __init__(self, data):
        self.list_text = []
        self.data = data
        self.data.convert()
        self.read_all()

    def read_all(self):
        for it in range(100):
            with open('../../teksty/AEI/' + str(it) + '.txt', 'r', encoding='utf-8') as f:
                file = re.sub(r'[^\w\s]', '', f.read().replace('\n', ' '))
                obj = Text(file, it)
                obj.makeSemantics(data)
                self.list_text.append(obj)

data = Data()
allText = AllText(data)
print("dupa")

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index_new.html", list_text=allText.list_text)

@app.route("/semantyka", methods=['GET'])
def semantyka():
    return render_template("semantyki.html", semantyka=data.getSematicalRaiting())


@app.route("/wagi", methods=['GET'])
def wagi():
    return render_template("wagi.html", wagi=data.getMatchingRules())


if __name__ == '__main__':
    app.run()
