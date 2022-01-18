import Library
import DamerauDistance
def TextCorection(src_corect_text):
    in_text = "ala ma kotz"#input().lower()
    correct_dic = Library.ReadClearText(src_corect_text).split(" ")
    ret = ""
    d_distance = DamerauDistance.DamerauDistance()
    for word in in_text.split(" "):
        if word in correct_dic:
            ret += " " + word
        else:
            correct_word= ""
            correct_weight = 100
            for it in correct_dic:
                weight = d_distance.MakeAndGetDistance(word, it)
                if correct_weight > weight:
                    correct_weight = weight
                    correct_word = it
                if weight <= 0.2:
                    correct_word = it
                    break
            ret += correct_word
    print(ret)


    print("hellow word")

TextCorection("../teksty/odm.txt")