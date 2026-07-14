import streamlit as st

st.set_page_config(page_title="Conversor 4-20mA Pro", page_icon="⚡")

st.title("⚡ Conversor Universal")

# --- PAINEL DE CONFIGURAÇÃO ---
st.sidebar.header("Configurações da Escala")
min_val = st.sidebar.number_input("Valor para 4mA:", value=1638)
max_val = st.sidebar.number_input("Valor para 20mA:", value=8191)
faixa = max_val - min_val

# --- ABAS DE CONVERSÃO ---
aba1, aba2 = st.tabs(["Bruto ➡️ mA", "mA ➡️ Bruto"])

with aba1:
    st.header("Converter Bruto para mA")
    val_bruto = st.number_input("Digite o Valor Bruto:", value=5500)
    if st.button("Calcular mA"):
        res_ma = 4 + ((val_bruto - min_val) / faixa) * 16
        st.metric(label="Corrente Resultante", value=f"{res_ma:.2f} mA")

with aba2:
    st.header("Converter mA para Bruto")
    val_ma = st.number_input("Digite a Corrente (mA):", min_value=4.0, max_value=20.0, value=12.0)
    if st.button("Calcular Bruto"):
        res_bruto = min_val + ((val_ma - 4) / 16) * faixa
        st.metric(label="Valor Bruto Calculado", value=f"{int(res_bruto)}")

# --- TABELA DE REFERÊNCIA ---
st.markdown("---")
st.subheader("Tabela de Referência")
referencias = {
    "4 mA": min_val,
    "8 mA": min_val + (faixa * 0.25),
    "12 mA": min_val + (faixa * 0.50),
    "16 mA": min_val + (faixa * 0.75),
    "20 mA": max_val
}

import pandas as pd
df = pd.DataFrame(list(referencias.items()), columns=["Corrente", "Valor Bruto"])
st.table(df)
