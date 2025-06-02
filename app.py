
import streamlit as st
from moduliai.knyga import Knyga
from moduliai.utils import nuskaityk_knygas, irasyt_knyga

# 🔧 Failo kelias
KNYGOS_FAILAS = "duomenys/knygos.json"

st.set_page_config(page_title="Bibliotekos valdymas", page_icon="📚")
st.title("📚 Knygos pridėjimas į biblioteką")

# 📋 Streamlit forma
with st.form("knygos_forma"):
    pavadinimas = st.text_input("Knygos pavadinimas")
    autorius = st.text_input("Autorius")
    metai = st.number_input("Leidimo metai", min_value=0, max_value=2025, step=1)
    kiekis = st.number_input("Kiekis", min_value=1, max_value=1000, step=1)

    pateikti = st.form_submit_button("➕ Pridėti knygą")

# 🧠 Kai paspausta „Pridėti“
if pateikti:
    if not pavadinimas.strip() or not autorius.strip():
        st.warning("⚠️ Pavadinimas ir autorius negali būti tušti.")
    elif metai > 2025:
        st.warning("📅 Leidimo metai negali būti iš ateities.")
    else:
        # Sugeneruojam naują ID (pagal esamų skaičių)
        esamos = nuskaityk_knygas(KNYGOS_FAILAS)
        naujas_id = len(esamos) + 1

        # Sukuriam objektą
        knyga = Knyga(naujas_id, pavadinimas, autorius, metai, kiekis)

        # Įrašom į failą kaip dict
        irasyt_knyga(knyga.to_dict(), KNYGOS_FAILAS)

        st.success("✅ Knyga sėkmingai pridėta į biblioteką!")

# 📖 Knygų sąrašas
st.subheader("📚 Visos bibliotekos knygos:")
knygos = nuskaityk_knygas(KNYGOS_FAILAS)

if knygos:
    st.table(knygos)
else:
    st.info("📭 Bibliotekoje dar nėra įrašytų knygų.")