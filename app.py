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
if aporte <= 0:
    aporte = 0
    meta_atingida_sem_aporte = True
else:
    meta_atingida_sem_aporte = False

# atraso proporcional ao prazo
atraso = max(round(prazo * 0.2), 1)
prazo_atraso = max(prazo - atraso, 1)

aporte_atraso = calcular_aporte_mensal(
    patrimonio,
    prazo_atraso,
    taxa,
    capital
)

if aporte > 0 and aporte_atraso > 0:
    impacto_percentual = ((aporte_atraso / aporte) - 1) * 100
else:
    impacto_percentual = None


df_evolucao = evolucao_patrimonio(
    patrimonio,
    prazo,
    taxa,
    capital
)

if meta_atingida_sem_aporte:
    st.success(
        "Com o capital inicial informado e a rentabilidade estimada, "
        "você atinge o patrimônio desejado sem necessidade de aportes mensais."
    )
else:
    st.metric(
        label="Aporte mensal necessário",
        value=f"R$ {aporte:,.2f}"
    )


st.info(
    f"💡 **Efeito do tempo:** se você começasse **5 anos depois**, "
    f"o aporte mensal subiria para **R$ {aporte_atraso:,.2f}**, "
    f"um aumento de **{impacto_percentual:.1f}%**."
)


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
