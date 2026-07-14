import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Conversor Profissional", page_icon="⚙️")

st.title("⚙️ Conversor de Instrumentação")

# --- CONFIGURAÇÕES ---
st.sidebar.header("Configurações")
unidade = st.sidebar.text_input("Unidade:", value="°C")
min_b = st.sidebar.number_input("Valor PLC (4mA):", value=1638)
max_b = st.sidebar.number_input("Valor PLC (20mA):", value=8191)
min_e = st.sidebar.number_input("Engenharia Mínima:", value=0.0)
max_e = st.sidebar.number_input("Engenharia Máxima:", value=100.0)

faixa_b = max_b - min_b
faixa_e = max_e - min_e

# --- ABAS ---
tab1, tab2 = st.tabs(["Converter Valor PLC", "Converter Corrente (mA)"])

with tab1:
    val_b = st.number_input("Digite o Valor do PLC:", value=5500)
    if st.button("Calcular (PLC)"):
        ma = 4 + ((val_b - min_b) / faixa_b) * 16
        eng = min_e + ((ma - 4) / 16) * faixa_e
        st.metric(f"Resultado em {unidade}", f"{eng:.2f} {unidade}")
        st.metric("Corrente Resultante", f"{ma:.2f} mA")

with tab2:
    val_ma = st.number_input("Digite os mA:", min_value=4.0, max_value=20.0, value=12.0)
    if st.button("Calcular (mA)"):
        eng = min_e + ((val_ma - 4) / 16) * faixa_e
        plc = min_b + ((val_ma - 4) / 16) * faixa_b
        st.metric(f"Resultado em {unidade}", f"{eng:.2f} {unidade}")
        st.metric("Valor PLC Correspondente", f"{int(plc)}")

# --- TABELA E GRÁFICO ---
st.markdown("---")
st.subheader("Tabela de Referência")
df = pd.DataFrame({
    "Corrente": [4, 8, 12, 16, 20],
    f"Eng ({unidade})": [min_e, min_e+(faixa_e*0.25), min_e+(faixa_e*0.50), min_e+(faixa_e*0.75), max_e],
    "Valor PLC": [min_b, min_b+(faixa_b*0.25), min_b+(faixa_b*0.50), min_b+(faixa_b*0.75), max_b]
})
st.table(df)

st.subheader("Gráfico de Linearidade")
fig, ax = plt.subplots()
ax.plot(df["Corrente"], df[f"Eng ({unidade})"], marker='o', linestyle='-', color='b')
ax.set_xlabel("Corrente (mA)")
ax.set_ylabel(f"Engenharia ({unidade})")
ax.grid(True)
st.pyplot(fig)
