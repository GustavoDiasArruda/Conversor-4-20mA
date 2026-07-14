import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conversor de Instrumentação", page_icon="⚙️")

st.title("⚙️ Conversor de Instrumentação")

# --- PAINEL DE CONFIGURAÇÃO (BARRA LATERAL) ---
st.sidebar.header("Configurações")
unidade = st.sidebar.text_input("Unidade:", value="°C")
min_bruto = st.sidebar.number_input("Valor Bruto (4mA):", value=1638)
max_bruto = st.sidebar.number_input("Valor Bruto (20mA):", value=8191)
min_eng = st.sidebar.number_input("Engenharia Mínima:", value=0.0)
max_eng = st.sidebar.number_input("Engenharia Máxima:", value=100.0)

faixa_b = max_bruto - min_bruto
faixa_e = max_eng - min_eng

# --- ABAS DE CONVERSÃO ---
tab1, tab2 = st.tabs(["Bruto ➡️ Eng", "mA ➡️ Eng"])

with tab1:
    val = st.number_input("Digite o Valor Bruto:", value=5500)
    if st.button("Calcular Valor"):
        ma = 4 + ((val - min_bruto) / faixa_b) * 16
        res = min_eng + ((ma - 4) / 16) * faixa_e
        st.success(f"Resultado: {res:.2f} {unidade}")

with tab2:
    val_ma = st.number_input("Digite a Corrente (mA):", min_value=4.0, max_value=20.0, value=12.0)
    if st.button("Calcular Engenharia"):
        res = min_eng + ((val_ma - 4) / 16) * faixa_e
        st.success(f"Resultado: {res:.2f} {unidade}")

# --- TABELA DE REFERÊNCIA (FAIXAS) ---
st.markdown("---")
st.subheader("Tabela de Referência")

dados = {
    "Corrente": ["4 mA", "8 mA", "12 mA", "16 mA", "20 mA"],
    f"Valor em {unidade}": [
        min_eng,
        min_eng + (faixa_e * 0.25),
        min_eng + (faixa_e * 0.50),
        min_eng + (faixa_e * 0.75),
        max_eng
    ],
    "Valor Bruto": [
        min_bruto,
        min_bruto + (faixa_b * 0.25),
        min_bruto + (faixa_b * 0.50),
        min_bruto + (faixa_b * 0.75),
        max_bruto
    ]
}

df = pd.DataFrame(dados)
st.table(df)
