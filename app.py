# app.py

import streamlit as st
import pandas as pd
import tempfile
import os
import hashlib

from parser import processar_pdf

from analytics import (
    calcular_curva_abc
)

from sheets_manager import (

    ler_base_historica,

    substituir_dataframe,

    registrar_importacao,

    verificar_importacao

)


# =========================
# CONFIGURAÇÃO
# =========================

st.set_page_config(

    page_title="Inteligência Farmacêutica Hospitalar",

    layout="wide"

)

st.title(
    "Inteligência Farmacêutica Hospitalar"
)


# =========================
# UPLOAD PDFs
# =========================

uploaded_files = st.file_uploader(

    "Upload dos PDFs",

    type=["pdf"],

    accept_multiple_files=True

)


# =========================
# PROCESSAMENTO
# =========================

if uploaded_files:

    novos_dados = []

    progresso = st.progress(0)

    for i, arquivo in enumerate(uploaded_files):

        with st.spinner(

            f"Processando {arquivo.name}..."

        ):

            try:

                # BYTES DO ARQUIVO
                arquivo_bytes = arquivo.getvalue()

                # HASH MD5
                hash_arquivo = hashlib.md5(
                    arquivo_bytes
                ).hexdigest()

                # VERIFICA DUPLICIDADE
                if verificar_importacao(
                    hash_arquivo
                ):

                    st.warning(
                        f"{arquivo.name} já foi importado."
                    )

                    continue

                # ARQUIVO TEMP
                with tempfile.NamedTemporaryFile(

                    delete=False,

                    suffix=".pdf"

                ) as tmp:

                    tmp.write(
                        arquivo_bytes
                    )

                    caminho_pdf = tmp.name

                # PROCESSA PDF
                df = processar_pdf(
                    caminho_pdf
                )

                os.remove(caminho_pdf)

                # VALIDA
                if not df.empty:

                    novos_dados.append(df)

                    # REGISTRA IMPORTAÇÃO
                    registrar_importacao(

                        arquivo.name,

                        hash_arquivo

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

    # =========================
    # PROCESSA HISTÓRICO
    # =========================

    if novos_dados:

        # NOVOS PDFs
        df_novos = pd.concat(

            novos_dados,

            ignore_index=True

        )

        # HISTÓRICO ANTIGO
        df_historico = (
            ler_base_historica()
        )

        # CONCATENA
        if not df_historico.empty:

            df_final = pd.concat(

                [

                    df_historico,

                    df_novos

                ],

                ignore_index=True

            )

        else:

            df_final = df_novos

        # REMOVE DUPLICIDADE
        df_final = (
            df_final
            .drop_duplicates()
        )

        # NUMÉRICOS
        colunas_numericas = [

            "Quantidade",
            "Valor_Total",
            "Custo_Unitario"

        ]

        for coluna in colunas_numericas:

            if coluna in df_final.columns:

                df_final[coluna] = (

                    pd.to_numeric(

                        df_final[coluna],

                        errors="coerce"

                    )

                    .fillna(0)

                    .round(2)

                )

        # CURVA ABC
        df_abc = calcular_curva_abc(
            df_final
        )

        try:

            # BASE HISTÓRICA
            substituir_dataframe(

                df_final,

                "Base_Historica"

            )

            # CURVA ABC
            substituir_dataframe(

                df_abc,

                "Curva_ABC"

            )

            st.success(
                "Base histórica atualizada!"
            )

            st.write(

                f"Total histórico: "

                f"{len(df_final)} linhas"

            )

        except Exception as e:

            st.error(
                "Erro ao salvar na Google Sheets"
            )

            st.exception(e)