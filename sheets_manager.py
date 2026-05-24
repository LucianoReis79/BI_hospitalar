# sheets_manager.py

import streamlit as st

import pandas as pd
import gspread

from google.oauth2.service_account import Credentials


# =========================
# CONFIGURAÇÃO GOOGLE
# =========================

SCOPES = [

    "https://www.googleapis.com/auth/spreadsheets",

    "https://www.googleapis.com/auth/drive"

]

import json

CREDS = Credentials.from_service_account_info(

    st.secrets["gcp_service_account"],

    scopes=SCOPES

)

client = gspread.authorize(CREDS)

SPREADSHEET = client.open(
    "Historico_Farmacia_Hospitalar"
)


# =========================
# CONECTA ABA
# =========================

def conectar_planilha(nome_aba):

    return SPREADSHEET.worksheet(nome_aba)


# =========================
# LIMPA ABA
# =========================

def limpar_aba(nome_aba):

    sheet = conectar_planilha(nome_aba)

    sheet.clear()


# =========================
# FORMATA PADRÃO BR
# =========================

def formatar_brasileiro(df):

    df = df.copy()

    colunas_numericas = [

        "Quantidade",
        "Valor_Total",
        "Custo_Unitario",
        "Consumo_Medio_Mensal",
        "Percentual_Valor",
        "Percentual_Acumulado"

    ]

    for coluna in colunas_numericas:

        if coluna in df.columns:

            df[coluna] = (

                pd.to_numeric(

                    df[coluna],

                    errors="coerce"

                )

                .fillna(0)

                .map(

                    lambda x:
                    f"{x:,.2f}"

                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")

                )
            )

    return df


# =========================
# SALVA DATAFRAME
# =========================

def salvar_dataframe(df, aba):

    sheet = conectar_planilha(aba)

    # FORMATA
    df = formatar_brasileiro(df)

    # CABEÇALHO
    sheet.append_row(
        df.columns.tolist()
    )

    # DADOS
    sheet.append_rows(

        df.astype(str)
        .values
        .tolist()

    )


# =========================
# REGISTRA IMPORTAÇÃO
# =========================

def registrar_importacao(nome_arquivo):

    try:

        sheet = conectar_planilha(
            "Importacoes"
        )

        sheet.append_row([
            nome_arquivo
        ])

    except Exception:

        pass


# =========================
# LER BASE HISTÓRICA
# =========================

def ler_base_historica():

    sheet = conectar_planilha(
        "Base_Historica"
    )

    dados = sheet.get_all_records()

    # VAZIO
    if not dados:

        return pd.DataFrame()

    # DATAFRAME
    df = pd.DataFrame(dados)

    # CONVERTE PADRÃO BR → FLOAT
    colunas_numericas = [

        "Quantidade",
        "Valor_Total",
        "Custo_Unitario"

    ]

    for coluna in colunas_numericas:

        if coluna in df.columns:

            df[coluna] = (

                df[coluna]

                .astype(str)

                .str.replace(
                    ".",
                    "",
                    regex=False
                )

                .str.replace(
                    ",",
                    ".",
                    regex=False
                )

            )

            df[coluna] = pd.to_numeric(

                df[coluna],

                errors="coerce"

            ).fillna(0)

    return df


# =========================
# SUBSTITUI ABA
# =========================

def substituir_dataframe(df, aba):

    sheet = conectar_planilha(aba)

    # LIMPA
    sheet.clear()

    # FORMATA
    df = formatar_brasileiro(df)

    # CABEÇALHO
    sheet.append_row(
        df.columns.tolist()
    )

    # DADOS
    sheet.append_rows(

        df.astype(str)
        .values
        .tolist()

    )