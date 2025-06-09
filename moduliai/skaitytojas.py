
class Skaitytojas:
    def __init__(self, id, vardas, pavarde, el_pastas, tel_nr):
        self.id = id
        self.vardas = vardas
        self.pavarde = pavarde
        self.el_pastas = el_pastas
        self.tel_nr = tel_nr

    def to_dict(self):
        return {
            "id": self.id,
            "vardas": self.vardas,
            "pavarde": self.pavarde,
            "el_pastas": self.el_pastas,
            "tel_nr": self.tel_nr
        }