import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Conversor Profissional", page_icon="⚙️")

st.title("⚙️ Conversor de Instrumentação")

# --- DICIONÁRIO DE UNIDADES ---
opcoes_unidades = {
    "Pressão": ["bar", "psi", "kPa", "MPa", "Pa", "kgf/cm²", "mmH₂O", "mmHg"],
    "Temperatura": ["°C", "°F", "K"],
    "Nível": ["%", "mm", "cm", "m", "in", "ft", "L", "m³"],
    "Vazão Volumétrica": ["L/min", "L/h", "m³/h", "m³/s", "GPM", "kg/h", "t/h", "Nm³/h", "SCFM"],
    "Vazão Mássica": ["kg/s", "kg/min", "kg/h", "t/h"],
    "Velocidade": ["m/s", "mm/s", "km/h"],
    "Frequência/Rotação": ["Hz", "kHz", "RPM", "rps"]
}

# --- CONFIGURAÇÕES ---
st.sidebar.header("Configurações")
categoria = st.sidebar.selectbox("Escolha a Grandeza:", list(opcoes_unidades.keys()))
unidade = st.sidebar.selectbox("Escolha a Unidade:", opcoes_unidades[categoria])

min_b = st.sidebar.number_input("Valor PLC (4mA):", value=1638)
max_b = st.sidebar.number_input("Valor PLC (20mA):", value=8191)
min_e = st.sidebar.number_input(f"Engenharia Mínima ({unidade}):", value=0.0)
max_e = st.sidebar.number_input(f"Engenharia Máxima ({unidade}):", value=100.0)

faixa_b = max_b - min_b
faixa_e = max_e - min_e

# --- ABAS ---
tab1, tab2 = st.tabs(["Converter Valor PLC", "Converter Corrente (mA)"])

with tab1:
    val_b = st.number_input("Digite o Valor do PLC:", value=5500)
    if st.button("Calcular (PLC)"):
        ma = 4 + ((val_b - min_b) / faixa_b) * 16
        eng = min_e + ((ma - 4) / 16) * faixa_e
        col1, col2 = st.columns(2)
        col1.metric(f"Resultado ({unidade})", f"{eng:.2f}")
        col2.metric("Corrente (mA)", f"{ma:.2f}")

with tab2:
    val_ma = st.number_input("Digite os mA:", min_value=4.0, max_value=20.0, value=12.0)
    if st.button("Calcular (mA)"):
        eng = min_e + ((val_ma - 4) / 16) * faixa_e
        plc = min_b + ((val_ma - 4) / 16) * faixa_b
        col1, col2 = st.columns(2)
        col1.metric(f"Resultado ({unidade})", f"{eng:.2f}")
        col2.metric("Valor PLC", f"{int(plc)}")

# --- TABELA E GRÁFICO ---
st.markdown("---")
st.subheader("Tabela de Referência")
df = pd.DataFrame({
    "Corrente (mA)": [4, 8, 12, 16, 20],
    f"Engenharia ({unidade})": [min_e, min_e+(faixa_e*0.25), min_e+(faixa_e*0.50), min_e+(faixa_e*0.75), max_e],
    "Valor PLC": [min_b, min_b+(faixa_b*0.25), min_b+(faixa_b*0.50), min_b+(faixa_b*0.75), max_b]
})
st.table(df)

st.subheader("Gráfico de Linearidade")
fig = px.line(df, x="Corrente (mA)", y=f"Engenharia ({unidade})", 
              markers=True, template="plotly_dark", title="Curva de Calibração")
fig.update_traces(line_color='#00ccff', line_width=3)
st.plotly_chart(fig, use_container_width=True)
