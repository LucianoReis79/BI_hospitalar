# analytics.py

import pandas as pd


def calcular_curva_abc(df):

    # QUANTIDADE DE MESES
    meses = df["Competencia"].nunique()

    if meses == 0:
        meses = 1

    # CONSOLIDA MEDICAMENTOS
    abc = (
        df.groupby(
            "Medicamento",
            as_index=False
        )
        .agg({

            "Quantidade": "sum",

            "Valor_Total": "sum"

        })
    )

    # CONSUMO MÉDIO MENSAL
    abc["Consumo_Medio_Mensal"] = (
        abc["Quantidade"] / meses
    )

    # MESES UTILIZADOS
    abc["Meses_CMM"] = meses

    # CUSTO UNITÁRIO
    abc["Custo_Unitario"] = (
        abc["Valor_Total"]
        / abc["Quantidade"]
    )

    # ORDENA
    abc = abc.sort_values(
        "Valor_Total",
        ascending=False
    )

    # TOTAL GERAL
    total = abc["Valor_Total"].sum()

    # PERCENTUAL
    abc["Percentual_Valor"] = (
        abc["Valor_Total"] / total
    ) * 100

    # PERCENTUAL ACUMULADO
    abc["Percentual_Acumulado"] = (
        abc["Percentual_Valor"]
        .cumsum()
    )

    # CLASSE ABC
    def classe(p):

        if p <= 80:
            return "A"

        elif p <= 95:
            return "B"

        return "C"

    abc["Classe_ABC"] = (
        abc["Percentual_Acumulado"]
        .apply(classe)
    )

    # COR DA CLASSE
    def cor_classe(c):

        if c == "A":
            return "🔴 Classe A"

        elif c == "B":
            return "🟡 Classe B"

        return "🟢 Classe C"

    abc["Classe_Formatada"] = (
        abc["Classe_ABC"]
        .apply(cor_classe)
    )

    # RANKING
    abc["Ranking"] = range(
        1,
        len(abc) + 1
    )

    # ARREDONDAMENTO
    colunas_numericas = [

        "Quantidade",
        "Valor_Total",
        "Consumo_Medio_Mensal",
        "Custo_Unitario",
        "Percentual_Valor",
        "Percentual_Acumulado"

    ]

    abc[colunas_numericas] = (
        abc[colunas_numericas]
        .round(2)
    )

    # PERCENTUAL FORMATADO
    abc["Percentual_Formatado"] = (
        abc["Percentual_Valor"]
        .astype(str)
        + "%"
    )

    abc["Percentual_Acumulado_Formatado"] = (
        abc["Percentual_Acumulado"]
        .astype(str)
        + "%"
    )

    # COLUNAS FINAIS
    abc = abc[[

            "Ranking",

            "Medicamento",

            "Quantidade",

            "Meses_CMM",

            "Consumo_Medio_Mensal",

            "Valor_Total",

            "Custo_Unitario",

            "Percentual_Formatado",

            "Percentual_Acumulado_Formatado",

            "Classe_Formatada"

    ]]

    return abc
