import library

print(library.nGram("ala ma kota // asd", 3))
print(library.nGram(library.ReadClearText("../teksty/eng1.txt").lower(), 3))
print(library.nGram(library.ReadClearText("../teksty/eng1.txt").lower(), 2))
print(library.nGram(library.ReadClearText("../teksty/eng1.txt").lower(), 1))