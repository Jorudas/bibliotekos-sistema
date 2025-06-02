
class Knyga:
    def __init__(self, id, pavadinimas, autorius, leidimo_metai, kiekis):
        self.id = id
        self.pavadinimas = pavadinimas
        self.autorius = autorius
        self.leidimo_metai = leidimo_metai
        self.kiekis = kiekis

    def __str__(self):
        return f"{self.pavadinimas} ({self.autorius}, {self.leidimo_metai}) 📚 ID: {self.id}"

    def to_dict(self):
        return {
            "id": self.id,
            "pavadinimas": self.pavadinimas,
            "autorius": self.autorius,
            "leidimo_metai": self.leidimo_metai,
            "kiekis": self.kiekis
        }