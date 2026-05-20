# database.py

import sqlite3
import pandas as pd

DB = "database.db"


def criar_banco():

    conn = sqlite3.connect(DB)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS historico_consumo (
        Competencia TEXT,
        Ano INTEGER,
        Mes INTEGER,
        Data_Inicial TEXT,
        Data_Final TEXT,
        Ficha TEXT,
        Codigo TEXT,
        Medicamento TEXT,
        Unidade TEXT,
        Quantidade REAL,
        Valor_Total REAL,
        Custo_Unitario REAL,
        Classe_ABC TEXT
    )
    """)

    conn.close()


def salvar_dataframe(df):

    conn = sqlite3.connect(DB)

    df.to_sql(
        "historico_consumo",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()


def carregar_historico():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM historico_consumo",
        conn
    )

    conn.close()

    return df