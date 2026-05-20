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

    return {
        "valor_total": df["Valor_Total"].sum(),
        "quantidade_total": df["Quantidade"].sum(),
        "medicamentos": df["Medicamento"].nunique(),
        "classe_a": (
            df[df["Classe_ABC"] == "A"]
            ["Medicamento"]
            .nunique()
        )
    }