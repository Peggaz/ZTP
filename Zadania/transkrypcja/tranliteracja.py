import Zadania.Library.library as Library


print(Library.Transliteration("../ru.txt", "../transliteracja_ru.txt") + '\n================\n')

print(Library.LoadText("../ru.txt") + '\n================\n')

print(Library.Transcription("../ru.txt", "../transliteracja_ru.txt"))
