import Library
import DamerauDistance
def BigFirstChar(word):
    '''
    Zmienia pierwszy znak słowa na wielką litere
    :param word:słowo do edycji
    :return: słowo z wielką pierwszą literą
    '''
    if len(word) > 0:
        return word[0].upper() + word[1:]
    return word
def korekta(sentenc, src_file):
    '''
    Zmienia pierwszy znak słowa na wielką litere
    :param sentenc:sentencja do korekty
 ads   :param src_file:scieżka do pliku
    :return: słowo z wielką pierwszą literą
    '''
    file = Library.ReadClearText(src_file).split('\n')
    sentenc = sentenc.lower()
    sentenc = sentenc.split(" ")
    ifDot = True
    zdanie = ""
    new_word = ""

    _damerau = DamerauDistance.DamerauDistance()
    for it in sentenc:
        result = 100
        old_result = 100
        word = ""
        punctuation = ""
        if not Library.OrALetter(it[len(it)-1]):
            punctuation = it[len(it)-1]
            word = it[:-1]
        else:
            word = it
        if_continue = False
        for line in file:
            if word in line:
                if ifDot:
                    ifDot = False
                    word = BigFirstChar(word)
                if punctuation == ".": ifDot = True
                zdanie += word + punctuation + " "
                if_continue = True
                break
        if if_continue: continue
        else:
            for line in file:
                br = False
                for it1 in line.split(" "):
                    if abs(len(word) - len(it1)) >= 3:
                        continue
                    result = _damerau.MakeAndGetDistance(word, it1)
                    if old_result > result:
                        old_result = result
                        new_word = it1
                        if result <= 0.5:
                            br = True
                            break
                if br: break
        if ifDot:
            ifDot = False
            new_word = BigFirstChar(new_word)
        zdanie += new_word + punctuation + " "
        if punctuation == ".": ifDot = True
    return zdanie
print("tekst przygotowany")
print(korekta("Koty to fajne zfieszęta", "../teksty/test.txt"))
print(korekta("Smiehc to zdrowie. Ptaki mają pieże. Chóśtawka nie ytlko lda zdieic. Robic zlośliwosci.", "../teksty/test.txt"))
