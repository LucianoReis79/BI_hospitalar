# utils.py

import re
from datetime import datetime


def limpar_texto(texto):

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def converter_moeda(valor):

    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    return float(valor)


def extrair_periodo(texto):

    match = re.search(
        r"Período considerado: De (\d{2}/\d{2}/\d{4}) até (\d{2}/\d{2}/\d{4})",
        texto
    )

    if match:

        data_inicial = match.group(1)

        data_final = match.group(2)

        data = datetime.strptime(
            data_final,
            "%d/%m/%Y"
        )

        return {

            "data_inicial":
            data_inicial,

            "data_final":
            data_final,

            "competencia":
            data.strftime("%Y-%m"),

            "ano":
            data.year,

            "mes":
            data.month
        }

    return {

        "data_inicial": None,
        "data_final": None,
        "competencia": None,
        "ano": None,
        "mes": None
    }
