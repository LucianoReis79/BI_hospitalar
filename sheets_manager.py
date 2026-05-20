# sheets_manager.py

import gspread
import pandas as pd

from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(CREDS)

SPREADSHEET = client.open(
    "Historico_Farmacia_Hospitalar"
)


def conectar_planilha(nome_aba):

    return SPREADSHEET.worksheet(nome_aba)


def salvar_dataframe(df, aba):

    sheet = conectar_planilha(aba)

    valores = df.astype(str).values.tolist()

    sheet.append_rows(valores)


def salvar_base_historica(df):

    salvar_dataframe(
        df,
        "Base_Historica"
    )


def salvar_curva_abc(df):

    salvar_dataframe(
        df,
        "Curva_ABC"
    )


def salvar_indicadores(df):

    salvar_dataframe(
        df,
        "Indicadores"
    )


def salvar_top_custo(df):

    salvar_dataframe(
        df,
        "Top_Custo"
    )


def salvar_top_consumo(df):

    salvar_dataframe(
        df,
        "Top_Consumo"
    )


def verificar_importacao(nome_arquivo):

    sheet = conectar_planilha(
        "Importacoes"
    )

    registros = sheet.col_values(1)

    if nome_arquivo in registros:

        return True

    sheet.append_row([nome_arquivo])

    return False
