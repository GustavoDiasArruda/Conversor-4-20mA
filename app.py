import streamlit as st

st.set_page_config(page_title="Conversor 4-20mA", page_icon="⚡")

st.markdown("""
    <style>
    .big-font { font-size:40px !important; font-weight: bold; color: #0066cc; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Conversor Universal")
valor_bruto = st.number_input("Digite o Valor Bruto:", min_value=0, max_value=16383, value=5500)

MIN_VALOR = 1638
MAX_VALOR = 8191

if valor_bruto < MIN_VALOR:
    resultado = 4.0
elif valor_bruto > MAX_VALOR:
    resultado = 20.0
else:
    resultado = 4 + ((valor_bruto - MIN_VALOR) / (MAX_VALOR - MIN_VALOR)) * 16

st.markdown("---")
st.write("### Corrente Calculada:")
st.markdown(f'<p class="big-font">{resultado:.2f} mA</p>', unsafe_allow_html=True)
