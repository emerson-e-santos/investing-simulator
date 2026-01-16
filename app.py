import streamlit as st
from calculations import (calcular_aporte_mensal, evolucao_patrimonio)
from scenarios import PERFIS

st.set_page_config(page_title="Simulador de Patrimônio", layout="wide")

st.title("Simulador de Patrimônio & Investimentos")

st.write(
    "Informe seu objetivo financeiro e veja quanto precisará investir por mês "
    "de acordo com diferentes perfis de risco."
)

with st.sidebar:
    patrimonio = st.number_input(
        "Patrimônio desejado (R$)",
        min_value=10000,
        max_value=10000000,
        value=1000000,
        step=10000
    )

    prazo = st.slider("Prazo (anos)", 1, 40, 20)

    capital = st.number_input(
        "Capital inicial (R$)",
        min_value=0,
        max_value=1000000,
        value=0,
        step=5000
    )

    perfil = st.selectbox("Perfil de risco", list(PERFIS.keys()))

taxa = PERFIS[perfil]
aporte = calcular_aporte_mensal(patrimonio, prazo, taxa, capital)

df_evolucao = evolucao_patrimonio(
    patrimonio,
    prazo,
    taxa,
    capital
)

st.subheader("Aporte mensal necessário")
st.metric("Valor mensal", f"R$ {aporte:,.2f}")

st.subheader("Evolução do patrimônio ao longo do tempo")

st.line_chart(
    data=df_evolucao,
    x="Mês",
    y="Patrimônio"
)
st.caption(
    "Nos primeiros anos, o crescimento é mais lento. "
    "Com o tempo, os juros compostos passam a ter um impacto cada vez maior."
)

st.caption(
    "Esta ferramenta tem caráter exclusivamente educacional. Não constitui recomendação de investimento. Rentabilidade passada não garante resultados futuros."
)
