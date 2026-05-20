# app.py

import streamlit as st
import pandas as pd
import tempfile
import os

from parser import processar_pdf
from analytics import (
    calcular_curva_abc,
    gerar_indicadores,
    top_custo,
    top_consumo
)

from sheets_manager import (
    conectar_planilha,
    salvar_base_historica,
    salvar_curva_abc,
    salvar_indicadores,
    salvar_top_custo,
    salvar_top_consumo,
    verificar_importacao
)

from dashboard import exibir_dashboard

st.set_page_config(
    page_title="Inteligência Farmacêutica Hospitalar",
    layout="wide"
)

st.title("Inteligência Farmacêutica Hospitalar")

uploaded_files = st.file_uploader(
    "Upload dos PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    todos_dados = []

    progresso = st.progress(0)

    for i, arquivo in enumerate(uploaded_files):

        with st.spinner(f"Processando {arquivo.name}..."):

            if verificar_importacao(arquivo.name):

                st.warning(
                    f"{arquivo.name} já importado."
                )

                continue

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(arquivo.read())

                caminho_pdf = tmp.name

            df = processar_pdf(caminho_pdf)

            todos_dados.append(df)

            os.remove(caminho_pdf)

            progresso.progress(
                (i + 1) / len(uploaded_files)
            )

    if todos_dados:

        df_final = pd.concat(
            todos_dados,
            ignore_index=True
        )

        df_abc = calcular_curva_abc(df_final)

        indicadores = gerar_indicadores(df_final)

        df_top_custo = top_custo(df_final)

        df_top_consumo = top_consumo(df_final)

        salvar_base_historica(df_final)

        salvar_curva_abc(df_abc)

        salvar_indicadores(indicadores)

        salvar_top_custo(df_top_custo)

        salvar_top_consumo(df_top_consumo)

        st.success("Dados enviados para Google Sheets!")

        exibir_dashboard(
            df_final,
            indicadores,
            df_abc
        )
