import Library
import DamerauDistance
def BigFirstChar(word):
    if len(word) > 0:
        return word[0].upper() + word[1:]
    return word
def korekta(sentenc, src_file):
    file = Library.ReadClearText(src_file).split('\n')
    sentenc = sentenc.lower()
    sentenc = sentenc.split(" ")
    ifDot = True
    zdanie = ""
    new_word = ""
    result = 100
    _damerau = DamerauDistance.DamerauDistance()
    for it in sentenc:
        old_result = 1.5
        word = ""
        punctuation = ""
        nowe_slowo = ""
        if not Library.OrALetter(it[len(it)-1]):
            punctuation = it[len(it)-1]
            word = it[:-1]
        else:
            word = it
        if word in file:
            if ifDot:
                ifDot = False
                word = BigFirstChar(word)
            if punctuation == ".": ifDot = True
            zdanie += word + punctuation + " "
            continue
        else:
            for it1 in file:
                if abs(len(word) - len(it1)) >= 3:
                    continue
                if result < 0.5 : continue
                result = _damerau.MakeAndGetDistance(word, it1)

                if old_result > result:
                    old_result = result
                    new_word = it1
                    if result <= 0.5:
                        break
        if ifDot:
            ifDot = False
            new_word = BigFirstChar(nowe_slowo)
        sentenc += nowe_slowo + punctuation + " "
        if punctuation == ".": ifDot = True
    return zdanie
print("tekst przygotowany")
print(korekta("Koty to fajne zfieszęta", "../teksty/odm.txt"))
print(korekta("Smiehc to zdrowie. Ptaki mają pieże. Chóśtawka nie ytlko lda zdieic. Robic zlośliwosci.", "../teksty/odm.txt"))
