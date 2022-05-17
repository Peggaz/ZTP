import Zadania.Library.library as Library
from Zadania.autokorekta.DamerauDistance import DamerauDistance

de = DamerauDistance().MakeAndGetDistance("ala ma kota", "kota ma ale")
print(de)
print(Library.Euklidesowa(Library.nGram(Library.ReadClearText("../teksty/pol1.txt"), 3), Library.nGram(Library.ReadClearText("../teksty/eng1.txt"), 3)))
#Library.SaveFile(Library.Atergo(Library.LoadText("../teksty/papk.txt")), "odm_atergo.txt")