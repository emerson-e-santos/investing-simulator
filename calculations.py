def calcular_aporte_mensal(fv, anos, taxa_anual, capital_inicial=0):
    n = anos * 12
    i = taxa_anual / 12

    if i == 0:
        return (fv - capital_inicial) / n

    pmt = (fv - capital_inicial * (1 + i)**n) * i / ((1 + i)**n - 1)
    return round(pmt, 2)
