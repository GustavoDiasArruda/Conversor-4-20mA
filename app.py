import streamlit as st

st.set_page_config(page_title="Conversor 4-20mA Pro", page_icon="⚡")

st.title("⚡ ALLAN GORDINHO GOSTOSO")

# --- PAINEL DE CONFIGURAÇÃO ---
st.sidebar.header("Configurações da Escala")
min_val = st.sidebar.number_input("Valor para 4mA:", value=1638)
max_val = st.sidebar.number_input("Valor para 20mA:", value=8191)

# --- ENTRADA DO USUÁRIO ---
valor_bruto = st.number_input("Digite o Valor Bruto a converter:", value=5500)

# --- CÁLCULO ---
faixa = max_val - min_val
if faixa == 0:
    st.error("O valor de 20mA deve ser maior que o de 4mA.")
else:
    resultado = 4 + ((valor_bruto - min_val) / faixa) * 16
    
    st.markdown("---")
    st.metric(label="Corrente Calculada", value=f"{resultado:.2f} mA")

    # --- TABELA DE REFERÊNCIA ---
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
