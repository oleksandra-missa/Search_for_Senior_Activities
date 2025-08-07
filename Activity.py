import Cas
class Activity:
    Activitivity_list = []

    @staticmethod
    def readAllZajecia():
        for z in Activity.Activitivity_list:
            z.read()

    def __init__(self, Id, Name, Category, Start, End, Price, On_offline, Description, Id_Cas):
        self.Id = Id
        self.Name = Name
        self.Kategoria = Category
        self.Start = Start
        self.End = End
        self.Price = Price
        self.On_offline = On_offline
        self.Description = Description
        self.Id_Cas = Id_Cas
        self.Cas = -1

    def addZajecia(self):
        if self not in Activity.Activitivity_list:
            Activity.Activitivity_list.append(self)

    def addCas(self, CasGiven):
        if self.Cas != Cas:
            self.Cas = CasGiven
            CasGiven.addZajecia(self)
    #        print("Zajecia dodaly polonczenie z Cas")

    def read(self):
        print(
            f"Id: {self.Id}, "
            f"Nazwa: {self.Name}, "
            f"Kategoria: {self.Kategoria}, "
            f"Start: {self.Start}, "
            f"Koniec: {self.End}, "
            f"Oplata: {self.Price}, "
            f"Tryb: {self.On_offline}, "
            f"Opis: {self.Description}, "
            f"Id_Cas: {self.Id_Cas}"
        )

    def return_string(self):
        return (
            f"Nazwa: {self.Name}, "
            f"Kategoria: {self.Kategoria}, "
            f"Start: {self.Start}, "
            f"Koniec: {self.End}, "
            f"Oplata: {self.Price}, "
            f"Tryb: {self.On_offline}, "
            f"Opis: {self.Description}, "
            f"Id_Cas: {self.Id_Cas}"
        )