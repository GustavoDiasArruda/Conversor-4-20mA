import streamlit as st

st.set_page_config(page_title="Conversor de Instrumentação", page_icon="⚙️")

st.title("⚙️ Conversor de Instrumentação")

# --- PAINEL DE CONFIGURAÇÃO ---
st.sidebar.header("Configurações do Instrumento")
unidade = st.sidebar.text_input("Unidade (ex: °C, Bar, m³/h):", value="°C")
min_val_bruto = st.sidebar.number_input("Valor Bruto para 4mA:", value=1638)
max_val_bruto = st.sidebar.number_input("Valor Bruto para 20mA:", value=8191)

st.sidebar.subheader("Escala de Engenharia")
min_eng = st.sidebar.number_input("Valor mínimo (4mA):", value=0.0)
max_eng = st.sidebar.number_input("Valor máximo (20mA):", value=100.0)

faixa_bruta = max_val_bruto - min_val_bruto
faixa_eng = max_eng - min_eng

# --- ABAS DE CONVERSÃO ---
aba1, aba2 = st.tabs(["Bruto ➡️ Engenharia", "mA ➡️ Engenharia"])

with aba1:
    st.header("Conversão: Valor Bruto")
    val_bruto = st.number_input("Digite o Valor Bruto:", value=5500)
    if st.button("Calcular Valor em Engenharia"):
        # Primeiro acha a corrente, depois converte para engenharia
        ma = 4 + ((val_bruto - min_val_bruto) / faixa_bruta) * 16
        valor_eng = min_eng + ((ma - 4) / 16) * faixa_eng
        st.metric(label=f"Valor em {unidade}", value=f"{valor_eng:.2f} {unidade}")

with aba2:
    st.header("Conversão: Corrente (mA)")
    val_ma = st.number_input("Digite a Corrente (mA):", min_value=4.0, max_value=20.0, value=12.0)
    if st.button("Calcular Valor em Engenharia"):
        valor_eng = min_eng + ((val_ma - 4) / 16) * faixa_eng
        st.metric(label=f"Valor em {unidade}", value=f"{valor_eng:.2f} {unidade}")

# --- TABELA DE REFERÊNCIA ---
st.markdown("---")
st.subheader("Tabela de Referência")
referencias = {
    "4 mA": min_eng,
    "8 mA": min_eng + (faixa_eng * 0.25),
    "12 mA": min_eng + (faixa_eng * 0.50),
    "16 mA": min_eng + (faixa_eng * 0.75),
    "20 mA": max_eng
}

import pandas as pd
df = pd.DataFrame(list(referencias.items()), columns=["Corrente", f"Valor em {unidade}"])
st.table(df)
