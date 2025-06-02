
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