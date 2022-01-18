#by Jakub Nowocień
import Library


def main():
    s = ""
    x = 0
    s = input("podaj tekst\n")
    x = int(input("podaj przesuniecie\n"))
    if (x > 25):
        print("błąd przesunięcia")
    else:
        textCode = Library.CodingCezar(s, x)
        Library.DecodingCezar(textCode, x)


main()
