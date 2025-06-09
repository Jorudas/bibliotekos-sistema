
class Knyga:
    def __init__(self, id, pavadinimas, autorius, leidimo_metai, kiekis, zanras):
        self.id = id
        self.pavadinimas = pavadinimas
        self.autorius = autorius
        self.leidimo_metai = leidimo_metai
        self.kiekis = kiekis
        self.zanras = zanras

    def to_dict(self):
        return {
            "id": self.id,
            "pavadinimas": self.pavadinimas,
            "autorius": self.autorius,
            "leidimo_metai": self.leidimo_metai,
            "kiekis": self.kiekis,
            "zanras": self.zanras
        }