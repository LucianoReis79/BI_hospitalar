# analytics.py

import pandas as pd


def calcular_curva_abc(df):

    # =========================
    # CONSOLIDA DADOS
    # =========================

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

    # =========================
    # MESES COM CONSUMO
    # =========================

    meses_consumo = (

        df.groupby("Medicamento")

        ["Competencia"]

        .nunique()

        .reset_index()

        .rename(columns={

            "Competencia":
            "Meses_CMM"

        })

    )

    abc = abc.merge(

        meses_consumo,

        on="Medicamento",

        how="left"

    )

    # =========================
    # CMM
    # =========================

    abc["Consumo_Medio_Mensal"] = (

        abc["Quantidade"]

        / abc["Meses_CMM"]

    )

    # =========================
    # CUSTO UNITÁRIO
    # =========================

    abc["Custo_Unitario"] = (

        abc["Valor_Total"]

        / abc["Quantidade"]

    )

    # =========================
    # ORDENA
    # =========================

    abc = abc.sort_values(

        "Valor_Total",

        ascending=False

    )

    # =========================
    # TOTAL GERAL
    # =========================

    total = abc["Valor_Total"].sum()

    # =========================
    # PERCENTUAL
    # =========================

    abc["Percentual_Valor"] = (

        abc["Valor_Total"]

        / total

    ) * 100

    # =========================
    # PERCENTUAL ACUMULADO
    # =========================

    abc["Percentual_Acumulado"] = (

        abc["Percentual_Valor"]

        .cumsum()

    )

    # =========================
    # CLASSE ABC
    # =========================

    def classe(p):

        if p <= 80:

            return "🔴 Classe A"

        elif p <= 95:

            return "🟡 Classe B"

        return "🟢 Classe C"

    abc["Classe_ABC"] = (

        abc["Percentual_Acumulado"]

        .apply(classe)

    )

    # =========================
    # RANKING
    # =========================

    abc["Ranking"] = range(

        1,

        len(abc) + 1

    )

    # =========================
    # ARREDONDAMENTO
    # =========================

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

    # =========================
    # FORMATA PERCENTUAIS BR
    # =========================

    abc["Percentual_Formatado"] = (

        abc["Percentual_Valor"]

        .map(

            lambda x:

            f"{x:,.2f}%"

            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")

        )

    )

    abc["Percentual_Acumulado_Formatado"] = (

        abc["Percentual_Acumulado"]

        .map(

            lambda x:

            f"{x:,.2f}%"

            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")

        )

    )

    # =========================
    # COLUNAS FINAIS
    # =========================

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

        "Classe_ABC"

    ]]

    return abc