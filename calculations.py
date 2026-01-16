import pandas as pd
def calcular_aporte_mensal(fv, anos, taxa_anual, capital_inicial=0):
    n = anos * 12
    i = taxa_anual / 12

    if i == 0:
        return (fv - capital_inicial) / n

    pmt = (fv - capital_inicial * (1 + i)**n) * i / ((1 + i)**n - 1)
    return round(pmt, 2)

def evolucao_patrimonio(
    fv, anos, taxa_anual, capital_inicial=0
):
    n = anos * 12
    i = taxa_anual / 12

    patrimonio = capital_inicial
    aporte = calcular_aporte_mensal(
        fv, anos, taxa_anual, capital_inicial
    )

    dados = []

    for mes in range(1, n + 1):
        patrimonio = patrimonio * (1 + i) + aporte
        dados.append({
            "Mês": mes,
            "Patrimônio": patrimonio
        })

    return pd.DataFrame(dados)
