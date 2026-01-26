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

    perfil = st.selectbox(
    "Perfil de risco",
    list(PERFIS.keys()),
    help=DESCRICOES_PERFIL.get("Conservador") + "\n\n" +
         DESCRICOES_PERFIL.get("Moderado") + "\n\n" +
         DESCRICOES_PERFIL.get("Agressivo")
    )

taxa = PERFIS[perfil]
aporte = calcular_aporte_mensal(patrimonio, prazo, taxa, capital)
aporte_exibido = max(aporte, 0)
mostrar_efeito_tempo = aporte > 0

if mostrar_efeito_tempo:
    prazo_atraso = max(prazo - 5, 1)

    aporte_atraso = calcular_aporte_mensal(
        patrimonio,
        prazo_atraso,
        taxa,
        capital
    )

    impacto_percentual = ((aporte_atraso / aporte) - 1) * 100



df_evolucao = evolucao_patrimonio(
    patrimonio,
    prazo,
    taxa,
    capital
)

st.subheader("Aporte mensal necessário")
st.metric("Valor mensal", f"R$ {aporte_exibido:,.2f}")

if aporte <= 0:
    st.success(
        "🎯 **Boa notícia!** Com o capital inicial informado, "
        "seu objetivo pode ser alcançado **sem necessidade de novos aportes mensais**. "
        "Aqui, o tempo e os juros compostos estão trabalhando a seu favor."
    )

if mostrar_efeito_tempo:
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
