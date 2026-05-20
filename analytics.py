# analytics.py

import pandas as pd


def calcular_curva_abc(df):

    df = df.sort_values(
        "Valor_Total",
        ascending=False
    )

    total = df["Valor_Total"].sum()

    df["Percentual_Valor"] = (
        df["Valor_Total"] / total
    )

    df["Percentual_Acumulado"] = (
        df["Percentual_Valor"].cumsum()
    )

    def classe(p):

        if p <= 0.80:
            return "A"

        elif p <= 0.95:
            return "B"

        return "C"

    df["Classe_ABC"] = (
        df["Percentual_Acumulado"]
        .apply(classe)
    )

    return df


def gerar_indicadores(df):

    return pd.DataFrame({

        "Indicador": [

            "Valor Total",
            "Quantidade Total",
            "Medicamentos",
            "Custo Médio"

        ],

        "Valor": [

            df["Valor_Total"].sum(),

            df["Quantidade"].sum(),

            df["Medicamento"].nunique(),

            df["Custo_Unitario"].mean()
        ]
    })


def top_custo(df):

    return (
        df.groupby("Medicamento")
        ["Valor_Total"]
        .sum()
        .reset_index()
        .sort_values(
            "Valor_Total",
            ascending=False
        )
        .head(10)
    )


def top_consumo(df):

    return (
        df.groupby("Medicamento")
        ["Quantidade"]
        .sum()
        .reset_index()
        .sort_values(
            "Quantidade",
            ascending=False
        )
        .head(10)
    )
