# sheets_manager.py

import gspread

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


# CONECTA ABA
def conectar_planilha(nome_aba):

    return SPREADSHEET.worksheet(nome_aba)


# LIMPA ABA
def limpar_aba(nome_aba):

    sheet = conectar_planilha(nome_aba)

    sheet.clear()


# FORMATA BR
def formatar_brasileiro(df):

    df = df.copy()

    for coluna in df.columns:

        if str(df[coluna].dtype) in [
            "float64",
            "int64"
        ]:

            df[coluna] = (
                df[coluna]
                .map(
                    lambda x:
                    f"{x:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            )

    return df


# SALVA DATAFRAME
def salvar_dataframe(df, aba):

    sheet = conectar_planilha(aba)

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


# REGISTRA IMPORTAÇÃO
def registrar_importacao(nome_arquivo):

    sheet = conectar_planilha(
        "Importacoes"
    )

    sheet.append_row([
        nome_arquivo
    ])