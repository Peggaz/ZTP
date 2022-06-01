import random

from Zadania.Library import library

losowy = list(range(100))
random.shuffle(losowy)

text_out = ""

for it in losowy:
    text_out += "\n#00" + str(it) + "\n" + library.LoadText("../../teksty/AEI/" + str(it) + ".txt") + "\n"
library.SaveFile(text_out, "all_text.txt", "../../teksty/AEI/")
