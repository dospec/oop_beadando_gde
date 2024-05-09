from datetime import datetime
import random
from abc import ABC, abstractmethod

class Szoba(ABC):

    @abstractmethod
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, tipus):
        super().__init__(szobaszam, 20000)
        self.tipus = tipus

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, bonusz):
        super().__init__(szobaszam, 35000)
        self.bonusz = bonusz

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Foglalaskezelo:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.foglalasok = []

    def foglalas(self, szobaszam, datum):
        for szoba in self.szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
                if foglalas_datum >= datetime.now() and self.szoba_szabad(szobaszam, foglalas_datum):
                    foglalas = Foglalas(szoba, foglalas_datum)
                    self.foglalasok.append(foglalas)
                    return f"A foglalás sikeres. Szoba: {szobaszam}, Dátum: {datum}, Ár: {szoba.ar}"
                else:
                    return "A foglalás nem lehetséges."
        return "A megadott szobaszám nem létezik."

    def szoba_szabad(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                return False
        return True

    def lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return "A foglalás sikeresen lemondva."
        return "A megadott foglalás nem létezik."

    def listaz_foglalasok(self):
        if self.foglalasok:
            return "\n".join([f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum.strftime('%Y-%m-%d')}" for foglalas in self.foglalasok])
        else:
            return "Nincsenek foglalások."

# Szálloda, szobák és foglalások létrehozása
szalloda = Szalloda("Példa Szálloda")
szalloda.uj_szoba(EgyagyasSzoba("101","Terasz"))
szalloda.uj_szoba(EgyagyasSzoba("102", "Minibár"))
szalloda.uj_szoba(KetagyasSzoba("201", "4K TV"))

foglalaskezelo = Foglalaskezelo(szalloda)


foglalaskezelo.foglalas("101", "2024-05-12")
foglalaskezelo.foglalas("102", "2024-05-12")
foglalaskezelo.foglalas("201", "2024-05-20")
foglalaskezelo.foglalas("101", "2024-05-23")
foglalaskezelo.foglalas("102", "2024-05-26")

# Felhasználói interfész
while True:
    print(f"\n {szalloda.nev} rendszer")
    print("\nVálassz műveletet:")
    print("1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Szobák listázása")
    print("5. Kilépés")

    valasztas = input("Művelet kiválasztása (1/2/3/4): ")

    if valasztas == "1":
        szobaszam = input("Adja meg a szobaszámot: ")
        datum = input("Adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN): ")
        print(foglalaskezelo.foglalas(szobaszam, datum))
    elif valasztas == "2":
        szobaszam = input("Adja meg a szobaszámot: ")
        datum = input("Adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN): ")
        print(foglalaskezelo.lemondas(szobaszam, datum))
    elif valasztas == "3":
        print(foglalaskezelo.listaz_foglalasok())
    elif valasztas == "4":
        print("A szálloda szobái:")
        for szoba in szalloda.szobak:
            if isinstance(szoba, EgyagyasSzoba):
                print(f"Egyágyas szoba: {szoba.szobaszam}, Ár: {szoba.ar}, Tipus: {szoba.tipus}")
            elif isinstance(szoba, KetagyasSzoba):
                print(f"Kétágyas szoba: {szoba.szobaszam}, Ár: {szoba.ar}, Bonusz: {szoba.bonusz}")
    elif valasztas == "5":
        break
    else:
        print("Hibás választás. Kérem válasszon újra.")
