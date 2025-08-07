import Activity
class Cas:
    Casy = []

    @staticmethod
    def readAllCas():
        for c in Cas.Casy:
            c.read()

    @staticmethod
    def findCasWithLP(LP):
        for c in Cas.Casy:
            if c.LP == LP:
                return c
        return None

    def __init__(self, LP, NumerPozycji, Dzielnica, Nazwa_Dzielnicy, Nazwa,
                 PodmiotProwadzacy, Ulica, NumerBudynku, NumerLokalu,
                 KodPocztowy, Miasto, Wojewodztwo, Kraj,
                 Kontakt1, Kontakt2, Uwagi, Adres):
        self.LP = LP
        self.NumerPozycji = NumerPozycji
        self.Dzielnica = Dzielnica
        self.Nazwa_Dzielnicy = Nazwa_Dzielnicy
        self.Nazwa = Nazwa
        self.PodmiotProwadzacy = PodmiotProwadzacy
        self.Ulica = Ulica
        self.NumerBudynku = NumerBudynku
        self.NumerLokalu = NumerLokalu
        self.KodPocztowy = KodPocztowy
        self.Miasto = Miasto
        self.Wojewodztwo = Wojewodztwo
        self.Kraj = Kraj
        self.Kontakt1 = Kontakt1
        self.Kontakt2 = Kontakt2
        self.Uwagi = Uwagi
        self.Adres = Adres
        self.Zajecia = []

    def addCas(self):
        if self not in Cas.Casy:
            Cas.Casy.append(self)

    def addZajecia(self,Zajecia):
        if Zajecia not in Zajecia.Activitivity_list:
            self.Zajecia.append(Zajecia)
            Zajecia.addZajecia()
    #        print("Cas dodal poloczenie z zajeciami")

    def read(self):
        print(
            f"LP: {self.LP}, "
            f"NumerPozycji: {self.NumerPozycji}, "
            f"Dzielnica: {self.Dzielnica}, "
            f"Nazwa_Dzielnicy: {self.Nazwa_Dzielnicy}, "
            f"Nazwa: {self.Nazwa}, "
            f"PodmiotProwadzacy: {self.PodmiotProwadzacy}, "
            f"Ulica: {self.Ulica}, "
            f"NumerBudynku: {self.NumerBudynku}, "
            f"NumerLokalu: {self.NumerLokalu}, "
            f"KodPocztowy: {self.KodPocztowy}, "
            f"Miasto: {self.Miasto}, "
            f"Wojewodztwo: {self.Wojewodztwo}, "
            f"Kraj: {self.Kraj}, "
            f"Kontakt1: {self.Kontakt1}, "
            f"Kontakt2: {self.Kontakt2}, "
            f"Email: {self.Email}, "
            f"Uwagi: {self.Uwagi}, "
            f"Adres: {self.Adres}"
        )