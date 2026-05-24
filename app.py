# app.py

import streamlit as st
import pandas as pd
import tempfile
import os

from parser import processar_pdf

from analytics import (
    calcular_curva_abc
)

from sheets_manager import (
    salvar_dataframe,
    limpar_aba,
    registrar_importacao
)


# CONFIGURAÇÃO
st.set_page_config(
    page_title="Inteligência Farmacêutica Hospitalar",
    layout="wide"
)

st.title(
    "Inteligência Farmacêutica Hospitalar"
)


# UPLOAD PDFs
uploaded_files = st.file_uploader(
    "Upload dos PDFs",
    type=["pdf"],
    accept_multiple_files=True
)


# PROCESSAMENTO
if uploaded_files:

    todos_dados = []

    progresso = st.progress(0)

    for i, arquivo in enumerate(uploaded_files):

        with st.spinner(
            f"Processando {arquivo.name}..."
        ):

            try:

                # ARQUIVO TEMPORÁRIO
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(
                        arquivo.read()
                    )

                    caminho_pdf = tmp.name

                # PROCESSA PDF
                df = processar_pdf(
                    caminho_pdf
                )

                os.remove(caminho_pdf)

                if not df.empty:

                    todos_dados.append(df)

                    # REGISTRA IMPORTAÇÃO
                    registrar_importacao(
                        arquivo.name
                    )

                    st.success(
                        f"{arquivo.name} → "
                        f"{len(df)} linhas"
                    )

                else:

                    st.warning(
                        f"Nenhum dado encontrado "
                        f"em {arquivo.name}"
                    )

            except Exception as e:

                st.error(
                    f"Erro ao processar "
                    f"{arquivo.name}"
                )

                st.exception(e)

            progresso.progress(
                (i + 1)
                / len(uploaded_files)
            )

    # CONSOLIDA
    if todos_dados:

        df_final = pd.concat(
            todos_dados,
            ignore_index=True
        )

        # REMOVE DUPLICIDADES
        df_final = (
            df_final
            .drop_duplicates()
        )

        # ARREDONDAMENTO
        colunas_numericas = [

            "Quantidade",
            "Valor_Total",
            "Custo_Unitario"

        ]

        for coluna in colunas_numericas:

            if coluna in df_final.columns:

                df_final[coluna] = (
                    df_final[coluna]
                    .astype(float)
                    .round(2)
                )

        # CURVA ABC
        df_abc = calcular_curva_abc(
            df_final
        )

        try:

            # LIMPA ABAS
            limpar_aba("Base_Historica")
            limpar_aba("Curva_ABC")

            # SALVA NOVAMENTE
            salvar_dataframe(
                df_final,
                "Base_Historica"
            )

            salvar_dataframe(
                df_abc,
                "Curva_ABC"
            )

            st.success(
                "Dados enviados para "
                "Google Sheets!"
            )

        except Exception as e:

            st.error(
                "Erro ao salvar "
                "na Google Sheets"
            )

            st.exception(e)
