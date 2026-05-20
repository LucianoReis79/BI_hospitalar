# app.py

import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3
import tempfile
import os

from parser import processar_pdf
from data.database import (
    criar_banco,
    salvar_dataframe,
    carregar_historico
)
from analytics import (
    calcular_curva_abc,
    gerar_indicadores
)
from dashboard import (
    exibir_dashboard
)
from excel_export import exportar_excel

st.set_page_config(
    page_title="Inteligência Farmacêutica Hospitalar",
    layout="wide"
)

st.title("Sistema de Inteligência Farmacêutica Hospitalar")

criar_banco()

uploaded_files = st.file_uploader(
    "Upload dos PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    todos_dados = []

    progress = st.progress(0)

    for i, arquivo in enumerate(uploaded_files):

        with st.spinner(f"Processando {arquivo.name}..."):

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(arquivo.read())
                caminho_pdf = tmp.name

            df = processar_pdf(caminho_pdf)

            todos_dados.append(df)

            os.remove(caminho_pdf)

            progress.progress((i + 1) / len(uploaded_files))

    if todos_dados:

        df_final = pd.concat(todos_dados, ignore_index=True)

        df_final = calcular_curva_abc(df_final)

        salvar_dataframe(df_final)

        indicadores = gerar_indicadores(df_final)

        st.success("PDFs processados com sucesso!")

        exibir_dashboard(df_final, indicadores)

        arquivo_excel = exportar_excel(df_final)

        with open(arquivo_excel, "rb") as f:
            st.download_button(
                "Baixar Excel",
                data=f,
                file_name="inteligencia_farmaceutica.xlsx"
            )