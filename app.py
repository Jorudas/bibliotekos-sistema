
import streamlit as st
import json
import pandas as pd
from moduliai.knyga import Knyga
from moduliai.utils import (
    nuskaityk_knygas, irasyt_knyga,
    nuskaityk_skaitytojus, irasyt_skaitytoja,
    nuskaityk_isskolinimus, irasyt_isskolinima, pasalinti_isskolinima
)

# 🔧 Failai
KNYGOS_FAILAS = "duomenys/knygos.json"
ISSKOLINIMAI_FAILAS = "duomenys/isskolinimai.json"
SKAITYTOJAI_FAILAS = "duomenys/skaitytojai.json"

st.set_page_config(page_title="Bibliotekos valdymas", page_icon="📚")
st.title("📚 Knygos pridėjimas į biblioteką")

# ➕ Knygos pridėjimas
# Inicijuojam session_state, jei tuščias
if "pavadinimas" not in st.session_state:
    st.session_state.pavadinimas = ""
if "autorius" not in st.session_state:
    st.session_state.autorius = ""
if "metai" not in st.session_state:
    st.session_state.metai = 0
if "kiekis" not in st.session_state:
    st.session_state.kiekis = 1
if "zanras" not in st.session_state:
    st.session_state.zanras = ""

with st.form("knygos_forma"):
    pavadinimas = st.text_input("Knygos pavadinimas", key="pavadinimas")
    autorius = st.text_input("Autorius", key="autorius")
    metai = st.number_input("Leidimo metai", min_value=0, max_value=2025, step=1, key="metai")
    kiekis = st.number_input("Kiekis", min_value=1, max_value=1000, step=1, key="kiekis")
    zanras = st.text_input("Žanras", key="zanras")
    pateikti = st.form_submit_button("Pridėti knygą")

    if pateikti:
        if not pavadinimas.strip() or not autorius.strip():
            st.warning("Pavadinimas ir autorius negali būti tušti.")
        elif metai > 2025:
            st.warning("Leidimo metai negali būti iš ateities.")
        else:
            esamos = nuskaityk_knygas(KNYGOS_FAILAS)
            naujas_id = len(esamos) + 1
            knyga = Knyga(naujas_id, pavadinimas, autorius, metai, kiekis, zanras)
            irasyt_knyga(knyga.to_dict(), KNYGOS_FAILAS)
            st.success("Knyga sėkmingai pridėta į biblioteką!")
            # Išvalom laukus po įvedimo
            st.session_state.pavadinimas = ""
            st.session_state.autorius = ""
            st.session_state.metai = 0
            st.session_state.kiekis = 1
            st.session_state.zanras = ""

# 📖 Knygų sąrašas su paieška
with st.expander("Visos bibliotekos knygos"):
    paieskos_zodis = st.text_input("🔎 Ieškoti knygos pagal pavadinimą arba autorių")
    knygos = nuskaityk_knygas(KNYGOS_FAILAS)

    if paieskos_zodis:
        paieskos_zodis = paieskos_zodis.lower()
        knygos = [k for k in knygos if paieskos_zodis in k['pavadinimas'].lower() or paieskos_zodis in k['autorius'].lower()]

    if knygos:
        rodoma_knygos = [
            {
                "ID": k["id"],
                "Pavadinimas": k["pavadinimas"],
                "Autorius": k["autorius"],
                "Leidimo metai": k["leidimo_metai"],
                "Kiekis": k["kiekis"],
                "Žanras": k.get("zanras", "Nenurodyta")
            }
            for k in knygos
        ]
        df_knygos = pd.DataFrame(rodoma_knygos).sort_values(by="Pavadinimas")
        st.table(df_knygos)
    else:
        if paieskos_zodis:
            st.warning("Knygų su tokiu pavadinimu ar autoriumi nerasta.")
        else:
            st.info("Bibliotekoje dar nėra įrašytų knygų.")

# 🗑️ Pašalinti senas knygas
with st.expander("🗑️ Pašalinti senas knygas pagal leidimo metus"):
    metai_x = st.number_input("Įveskite metus (pašalins visas knygas, išleistas anksčiau nei šie metai):", min_value=0, max_value=2025, step=1)
    salinti = st.button("🗑️ Pašalinti senas knygas")

    if salinti:
        knygos = nuskaityk_knygas(KNYGOS_FAILAS)
        naujos_knygos = [k for k in knygos if k["leidimo_metai"] >= metai_x]

        if len(naujos_knygos) < len(knygos):
            from moduliai.utils import irasyt_knyga
            # Perrašom visą knygų sąrašą
            with open(KNYGOS_FAILAS, "w", encoding="utf-8") as f:
                import json
                json.dump(naujos_knygos, f, indent=4, ensure_ascii=False)

            st.success(f"✅ Pašalinta {len(knygos) - len(naujos_knygos)} knygų, išleistų anksčiau nei {metai_x}.")
        else:
            st.info("📚 Knygų, kurios būtų pašalintos, nerasta.")

# 👤 Skaitytojo registracija
st.header("Naujo skaitytojo registracija")
with st.form("skaitytojo_forma"):
    vardas = st.text_input("Vardas")
    pavarde = st.text_input("Pavardė")
    el_pastas = st.text_input("El. paštas")
    prideti_skaitytoja = st.form_submit_button("Pridėti skaitytoją")

if prideti_skaitytoja:
    if not vardas.strip() or not pavarde.strip() or not el_pastas.strip():
        st.warning("Visi laukeliai privalomi.")
    else:
        skaitytojai = nuskaityk_skaitytojus(SKAITYTOJAI_FAILAS)
        if any(s["el_pastas"].lower() == el_pastas.lower() for s in skaitytojai):
            st.warning("Skaitytojas su tokiu el. paštu jau egzistuoja.")
        else:
            skaitytojas = {"vardas": vardas, "pavarde": pavarde, "el_pastas": el_pastas}
            irasyt_skaitytoja(skaitytojas, SKAITYTOJAI_FAILAS)
            st.success("Skaitytojas pridėtas sėkmingai!")

# 👥 Skaitytojų sąrašas
with st.expander("Visi skaitytojai"):
    paieska_s = st.text_input("Ieškoti skaitytojo pagal vardą arba pavardę")
    skaitytojai = nuskaityk_skaitytojus(SKAITYTOJAI_FAILAS)

    if skaitytojai:
        filtruoti = skaitytojai
        if paieska_s:
            filtruoti = [s for s in skaitytojai if paieska_s.lower() in s["vardas"].lower() or paieska_s.lower() in s["pavarde"].lower()]

        rodoma = [{"Vardas": s["vardas"], "Pavardė": s["pavarde"], "El. paštas": s["el_pastas"]} for s in filtruoti]
        st.table(pd.DataFrame(rodoma).sort_values(by="Vardas"))
    else:
        st.info("📭 Bibliotekoje dar nėra įrašytų skaitytojų.")

# 📦 Knygos paskolinimas
st.header("Knygos paskolinimas")
knygos = nuskaityk_knygas(KNYGOS_FAILAS)
skaitytojai = nuskaityk_skaitytojus(SKAITYTOJAI_FAILAS)

if knygos and skaitytojai:
    with st.form("paskolinimo_forma"):
        pasirinktas_skaitytojas = st.selectbox("Pasirinkite skaitytoją", options=skaitytojai, format_func=lambda x: f"{x['vardas']} {x['pavarde']}")
        pasirinkta_knyga = st.selectbox("Pasirinkite knygą", options=knygos, format_func=lambda x: f"{x['pavadinimas']} ({x['autorius']})")
        paskolinti = st.form_submit_button("Paskolinti")

    if paskolinti:
        from moduliai.utils import nuskaityk_isskolinimus, irasyt_isskolinima
        from datetime import datetime, timedelta

        isskolinimai = nuskaityk_isskolinimus(ISSKOLINIMAI_FAILAS)

        # ⛔ Patikrinam, ar skaitytojas turi vėluojančių knygų
        dabartine_data = datetime.today().date()
        skaitytojo_vardas_pavarde = f"{pasirinktas_skaitytojas['vardas']} {pasirinktas_skaitytojas['pavarde']}"

        turi_veluojanciu = False
        for irasas in isskolinimai:
            if irasas["skaitytojas"] == skaitytojo_vardas_pavarde:
                try:
                    terminas = datetime.strptime(irasas["grazinimo_terminas"], "%Y-%m-%d").date()
                    if terminas < dabartine_data:
                        turi_veluojanciu = True
                        break
                except:
                    continue

        if turi_veluojanciu:
            st.error("Šis skaitytojas turi vėluojančių knygų. Negalima paskolinti naujos knygos.")
            st.stop()




        jau_paskolinta = any(
            i["knyga"] == pasirinkta_knyga["pavadinimas"] and i["skaitytojas"] == f"{pasirinktas_skaitytojas['vardas']} {pasirinktas_skaitytojas['pavarde']}"
            for i in isskolinimai
        )

        viso_kiekis = pasirinkta_knyga["kiekis"]
        paskolinta_kiekis = sum(
            1 for i in isskolinimai if i["knyga"] == pasirinkta_knyga["pavadinimas"]
        )
        likutis = viso_kiekis - paskolinta_kiekis

        if likutis == 0:
            st.warning("⚠️ Šios knygos visos kopijos jau paskolintos – nėra likučio.")
        elif jau_paskolinta:
            st.warning("⚠️ Ši knyga jau yra paskolinta šiam skaitytojui.")
        else:
            today = datetime.today().date()
            terminas = today + timedelta(days=14)

            irasyt_isskolinima(
                {
                    "vardas": pasirinktas_skaitytojas["vardas"],
                    "pavarde": pasirinktas_skaitytojas["pavarde"],
                    "el_pastas": pasirinktas_skaitytojas["el_pastas"]
                },
                {
                    "pavadinimas": pasirinkta_knyga["pavadinimas"],
                    "autorius": pasirinkta_knyga["autorius"]
                },
                ISSKOLINIMAI_FAILAS,
                today.strftime("%Y-%m-%d"),
                terminas.strftime("%Y-%m-%d")
            )

            st.success(f"✅ Knyga „{pasirinkta_knyga['pavadinimas']}“ paskolinta iki {terminas}")

# 📄 Paskolintų knygų sąrašas
with st.expander("Paskolintų knygų sąrašas"):
    isskolinimai = nuskaityk_isskolinimus(ISSKOLINIMAI_FAILAS)
    if isskolinimai:
        df = pd.DataFrame(isskolinimai)
        st.table(df)
        for i, irasas in enumerate(isskolinimai):
            sugrąžinti = st.button(f"Grąžinti: {irasas['knyga']} ({irasas['skaitytojas']})", key=f"grąžinti_{i}")
            if sugrąžinti:
                pasalinti_isskolinima(i, ISSKOLINIMAI_FAILAS)
                st.success(f"Knyga „{irasas['knyga']}“ grąžinta sėkmingai.")
                st.experimental_rerun()
    else:
        st.info("Dar nėra paskolintų knygų.")

# 📊 Bibliotekos statistika
with st.expander("📊 Bibliotekos statistika", expanded=True):
    if not knygos:
        st.warning("📭 Dar nėra įrašytų knygų – likučių nėra ką skaičiuoti.")
    else:
        st.markdown("### 📦 Knygų likučiai")

        # Skaičiuojam paskolintų knygų kiekius
        paskolinti_kiekiai = {}
        for irasas in isskolinimai:
            knygos_pavadinimas = irasas['knyga']
            paskolinti_kiekiai[knygos_pavadinimas] = paskolinti_kiekiai.get(knygos_pavadinimas, 0) + 1

        # Formuojam lentelę
        likuciu_lentele = []
        for knyga in knygos:
            pavadinimas = knyga["pavadinimas"]
            kiekis = knyga["kiekis"]
            paskolinta = paskolinti_kiekiai.get(pavadinimas, 0)
            likutis = kiekis - paskolinta

            likuciu_lentele.append({
                "Pavadinimas": pavadinimas,
                "Iš viso": kiekis,
                "Paskolinta": paskolinta,
                "Likutis": likutis
            })

        # Atvaizduojam, jei yra likučių
        if likuciu_lentele:
            df = pd.DataFrame(likuciu_lentele)
            st.table(df)
        else:
            st.info("📭 Šiuo metu likučių lentelė tuščia.")

        # 📈 Santrauka
        st.markdown("### 📈 Santrauka")
        kol1, kol2, kol3 = st.columns(3)
        kol1.metric("Knygų skaičius", len(knygos))
        kol2.metric("Skaitytojų skaičius", len(skaitytojai))
        kol3.metric("Paskolintų knygų", len(isskolinimai))

        st.markdown("#### 📌 Pastaba:")
        st.info("Skaičiavimai atliekami remiantis dabartiniais JSON failų duomenimis.")

# 📄 Vėluojančių knygų sąrašas
with st.expander("📄 Vėluojančių knygų sąrašas", expanded=False):
    from datetime import datetime

    isskolinimai = nuskaityk_isskolinimus(ISSKOLINIMAI_FAILAS)
    dabar = datetime.today().date()

    veluojancios = []
    for irasas in isskolinimai:
        try:
            terminas = datetime.strptime(irasas["grazinimo_terminas"], "%Y-%m-%d").date()
            if terminas < dabar:
                veluojancios.append({
                    "Knyga": irasas["knyga"],
                    "Skaitytojas": irasas["skaitytojas"],
                    "Išdavimo data": irasas["isdavimo_data"],
                    "Grąžinimo terminas": irasas["grazinimo_terminas"]
                })
        except Exception:
            continue

    if veluojancios:
        df_veluojancios = pd.DataFrame(veluojancios)
        st.warning(f"📚 Iš viso vėluojančių knygų: {len(veluojancios)}")
        st.table(df_veluojancios)
    else:
        st.success("Šiuo metu nėra vėluojančių knygų.")

#VELUOJANCIOS KNYGOS
from datetime import datetime

st.subheader("Vėluojančios knygos")

dabar = datetime.today().date()
veluojancios = []

for irasas in isskolinimai:
    try:
        terminas = datetime.strptime(irasas["grazinimo_terminas"], "%Y-%m-%d").date()
        if terminas < dabar:
            veluojancios.append(irasas)
    except Exception:
        continue

if veluojancios:
    st.warning(f"📚 Vėluoja {len(veluojancios)} knygos!")
    st.table(veluojancios)
else:
    st.info("✅ Šiuo metu nėra vėluojančių knygų.")