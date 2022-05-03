import Library

print(Library.nGram("ala ma kota // asd", 3))
print(Library.nGram(Library.ReadClearText("../teksty/eng1.txt").lower(), 3))
print(Library.nGram(Library.ReadClearText("../teksty/eng1.txt").lower(), 2))
print(Library.nGram(Library.ReadClearText("../teksty/eng1.txt").lower(), 1))