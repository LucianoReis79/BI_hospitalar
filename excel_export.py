# excel_export.py

import pandas as pd


def exportar_excel(df):

    arquivo = "inteligencia_farmaceutica.xlsx"

    with pd.ExcelWriter(
        arquivo,
        engine="xlsxwriter"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Base_Historica",
            index=False
        )

        abc = (
            df.groupby("Classe_ABC")
            ["Valor_Total"]
            .sum()
            .reset_index()
        )

        abc.to_excel(
            writer,
            sheet_name="Curva_ABC",
            index=False
        )

    return arquivo