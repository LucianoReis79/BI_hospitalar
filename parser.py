# parser.py

import pdfplumber
import pandas as pd
import re
import logging
from utils import (
    limpar_texto,
    converter_moeda,
    extrair_periodo
)

logging.basicConfig(level=logging.INFO)

PADRAO_ITEM = re.compile(
    r"""
    (?P<ficha>[A-Z0-9\-]+)\s+
    (?P<codigo>\d+)\s+
    (?P<descricao>.+?)\s+
    (?P<unidade>Unidade|Ampola|Frasco|Bolsa|Bisnaga|LATA|Seringa)\s+
    (?P<quantidade>\d+)\s+
    R\$\s?(?P<valor>[\d\.\,]+)
    """,
    re.VERBOSE
)

REMOVER = [
    r"MINISTERIO DA DEFESA",
    r"EXERCITO BRASILEIRO",
    r"Página \d+ / \d+",
    r"Relatório emitido.*"
]


def remover_linhas_invalidas(texto):

    linhas_validas = []

    for linha in texto.split("\n"):

        ignorar = False

        for padrao in REMOVER:
            if re.search(padrao, linha):
                ignorar = True

        if not ignorar:
            linhas_validas.append(linha)

    return linhas_validas


def reconstruir_registros(linhas):

    registros = []

    buffer = ""

    for linha in linhas:

        linha = limpar_texto(linha)

        if re.match(r"^[A-Z0-9\-]+\s+\d+", linha):

            if buffer:
                registros.append(buffer)

            buffer = linha

        else:
            buffer += " " + linha

        if "R$" in linha:
            registros.append(buffer)
            buffer = ""

    return registros


def processar_pdf(caminho_pdf):

    registros_extraidos = []

    with pdfplumber.open(caminho_pdf) as pdf:

        texto_completo = ""

        for pagina in pdf.pages:

            texto = pagina.extract_text()

            if texto:
                texto_completo += "\n" + texto

        periodo = extrair_periodo(texto_completo)

        linhas = remover_linhas_invalidas(texto_completo)

        registros = reconstruir_registros(linhas)

        for registro in registros:

            match = PADRAO_ITEM.search(registro)

            if match:

                try:

                    dados = match.groupdict()

                    valor = converter_moeda(dados["valor"])

                    quantidade = float(dados["quantidade"])

                    custo_unitario = valor / quantidade

                    registros_extraidos.append({
                        "Competencia": periodo["competencia"],
                        "Ano": periodo["ano"],
                        "Mes": periodo["mes"],
                        "Data_Inicial": periodo["data_inicial"],
                        "Data_Final": periodo["data_final"],
                        "Ficha": dados["ficha"],
                        "Codigo": dados["codigo"],
                        "Medicamento": dados["descricao"],
                        "Unidade": dados["unidade"],
                        "Quantidade": quantidade,
                        "Valor_Total": valor,
                        "Custo_Unitario": custo_unitario
                    })

                except Exception as e:
                    logging.error(f"Erro ao processar: {registro}")

    return pd.DataFrame(registros_extraidos)