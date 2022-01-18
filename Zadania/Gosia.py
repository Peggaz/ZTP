vowels = ['a', 'e', 'i', 'o', 'u', 'ó', 'y', 'ą', 'ę', 'a', 'o', 'и', 'у', 'ы', 'э']

transcriptionDic = \
    {
        'б': 'b',
        'в': 'w',
        'г': 'g',
        'д': 'd',
        'e': (('je', 1, ['S', 'ъ', 'ь'], [], 0), ('e', 0, ['ж', 'л', 'ц', 'ч', 'ш', 'щ'], [], 0), ['ie']),
        'ё': (('jo', 1, ['S', 'ъ', 'ь'], [], 0), ('o', 0, ['ж', 'л', 'ч', 'ш', 'щ'], [], 0), ['io']),
        'ж': 'ż',
        'з': 'z',
        'и': (('ji', 0, ['ь'], [], 0), ('y', 0, ['ж', 'ц', 'ш'], [], 0), ['i']),
        'й': 'j',
        'к': 'k',
        'л': (('l', 0, [], ['е', 'ё', 'и', 'ь', 'ю', 'я'], 0), ['ł']),
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'ch',
        'ц': 'c',
        'ч': 'cz',
        'ш': 'sz',
        'щ': 'szcz',
        'ъ': '',
        'ь': (('', 0, ['ж', 'ш', 'ч', 'щ'], ['S'], 0), ['´']),
        'э': 'e',
        'ю': (('u', 0, ['л'], [], 0), ('ju', 1, ['S', 'ъ', 'ь'], [], 0), ['iu']),
        'я': (('ja', 1, ['S', 'ъ', 'ь'], [], 0), ('a', 0, ['л'], [], 0), ['ia'])}

def LoadText(s):
    return open(s, "r", encoding="utf-8").read()

def LoadTransliterationDic(s):
    read = LoadText(s)
    ru = 2
    la = 2
    trans = {}
    cru = []
    cla = []
    for c in read:

        if c != '\n' and c != ' ' and c != '\t':
            if ru > 0:
                cru.append(c)
                ru -= 1
            elif la > 0:
                cla.append(c)
                la -= 1
            if la == 0 and ru == 0:
                la = 2
                ru = 2
    for x in range(len(cru) - 1):
        trans[cru[x]] = cla[x]
    return trans


def Transliteration(src_text, transliteriation_src):
    trans = LoadTransliterationDic(transliteriation_src)
    textIN = LoadText(src_text)
    textOut = ""
    for c in textIN:
        if c in trans:
            textOut += trans[c]
        else:
            textOut += c
    return textOut


def Transcription(src_text, transliteriation_src):
    text_in = LoadText(src_text).lower()
    dic_transliteration = LoadTransliterationDic(transliteriation_src)
    text_out = ''
    for idc in range(len(text_in)):
        c = text_in[idc]
        if c != " " and c != '\n' and c != '\t':
            if c in transcriptionDic:
                if type(transcriptionDic[c]) == tuple:
                    for t in transcriptionDic[c]:
                        if len(t) == 5:
                            con = False
                            if idc > 0:
                                if t[1] and text_in[idc - 1] == ' ' or text_in[idc - 1] == '\n':
                                    text_out += t[0]
                                    break
                                elif t[2]:
                                    if t[2][0] == 'S':
                                        t[2].extend(vowels)
                                    if text_in[idc - 1] in t[2]:
                                        text_out += t[0]
                                        break
                            if idc < len(text_in) - 1:
                                if t[3]:
                                    if t[3][0] == 'S':
                                        t[3].extend(vowels)
                                    if text_in[idc + 1] in t[3]:
                                        text_out += t[0]
                                        break
                                if t[4] and text_in[idc + 0] == ' ' or text_in[idc + 1] == '\n':
                                    text_out += t[0]
                                    break
                        else:
                            text_out += t[0]
                elif type(transcriptionDic[c]) == str:
                    text_out += transcriptionDic[c]
                else:
                    text_out += transcriptionDic[c[0]]
            elif c in dic_transliteration:
                text_out += dic_transliteration[c]
            else:
                text_out += c
        else:
            text_out += c
    return text_out

print(Transcription("../teksty/ru.txt", "../teksty/transliteracja_ru.txt"))