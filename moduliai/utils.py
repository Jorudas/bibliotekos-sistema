
import json
import os

def nuskaityk_knygas(is_failo):
    """
    Nuskaito knygas iš JSON failo.
    Jei failas neegzistuoja – grąžina tuščią sąrašą.
    """
    if not os.path.exists(is_failo):
        return []

    with open(is_failo, 'r', encoding='utf-8') as failas:
        try:
            duomenys = json.load(failas)
        except json.JSONDecodeError:
            duomenys = []

    return duomenys

def irasyt_knyga(knyga, i_faila):
    """
    Prideda vieną knygą prie esamų JSON faile.
    'knyga' turi būti dict tipo (ne objektas).
    """
    knygos = nuskaityk_knygas(i_faila)
    knygos.append(knyga)

    with open(i_faila, 'w', encoding='utf-8') as failas:
        json.dump(knygos, failas, indent=4, ensure_ascii=False)

def nuskaityk_skaitytojus(failas):
    """
    Nuskaito skaitytojus iš JSON failo.
    Jei failas neegzistuoja arba tuščias – grąžina tuščią sąrašą.
    """
    if not os.path.exists(failas):
        return []

    with open(failas, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def irasyt_skaitytoja(skaitytojas, failas):
    """
    Prideda naują skaitytoją į JSON failą.
    'skaitytojas' turi būti dict tipo.
    """
    sarasas = nuskaityk_skaitytojus(failas)
    sarasas.append(skaitytojas)

    with open(failas, 'w', encoding='utf-8') as f:
        json.dump(sarasas, f, indent=4, ensure_ascii=False)

from datetime import date

def irasyt_isskolinima(skaitytojas, knyga, i_faila):
    """
    Įrašo knygos paskolinimą į JSON failą.
    """
    naujas_irasas = {
        "skaitytojas": f"{skaitytojas['vardas']} {skaitytojas['pavarde']}",
        "knyga": knyga["pavadinimas"],
        "data": date.today().isoformat()
    }

    if not os.path.exists(i_faila):
        visi_irasai = []
    else:
        with open(i_faila, 'r', encoding='utf-8') as f:
            try:
                visi_irasai = json.load(f)
            except json.JSONDecodeError:
                visi_irasai = []

    visi_irasai.append(naujas_irasas)

    with open(i_faila, 'w', encoding='utf-8') as f:
        json.dump(visi_irasai, f, indent=4, ensure_ascii=False)

def nuskaityk_isskolinimus(failas):
    """
    Nuskaito knygų išdavimus iš JSON failo.
    Jei failas neegzistuoja ar tuščias – grąžina tuščią sąrašą.
    """
    if not os.path.exists(failas):
        return []

    with open(failas, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def irasyt_isskolinima(skaitytojas, knyga, failas, data_isdavimo, data_grazinimo):
    if not os.path.exists(failas):
        isskolinimai = []
    else:
        with open(failas, 'r', encoding='utf-8') as f:
            try:
                isskolinimai = json.load(f)
            except json.JSONDecodeError:
                isskolinimai = []

    irasas = {
        "skaitytojas": f"{skaitytojas['vardas']} {skaitytojas['pavarde']}",
        "knyga": knyga["pavadinimas"],
        "isdavimo_data": data_isdavimo,
        "grazinimo_terminas": data_grazinimo
    }

    isskolinimai.append(irasas)

    with open(failas, 'w', encoding='utf-8') as f:
        json.dump(isskolinimai, f, indent=4, ensure_ascii=False)

def pasalinti_isskolinima(indeksas, failas):
    """
    Pašalina paskolintą knygą pagal sąrašo indeksą.
    """
    duomenys = nuskaityk_knygas(failas)
    if 0 <= indeksas < len(duomenys):
        del duomenys[indeksas]
        with open(failas, 'w', encoding='utf-8') as f:
            json.dump(duomenys, f, indent=4, ensure_ascii=False)