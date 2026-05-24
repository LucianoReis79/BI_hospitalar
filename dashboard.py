# dashboard.py

import streamlit as st
import plotly.express as px


def formatar_brl(valor):

    return (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def exibir_dashboard(df, df_abc):

    # KPIs
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Valor Total",
        f'R$ {formatar_brl(df["Valor_Total"].sum())}'
    )

    col2.metric(
        "Quantidade Total",
        formatar_brl(
            df["Quantidade"].sum()
        )
    )

    col3.metric(
        "Medicamentos",
        df["Medicamento"].nunique()
    )

    # CURVA ABC
    st.subheader("Curva ABC")

    fig = px.line(
        df_abc,
        x="Ranking",
        y="Percentual_Acumulado",
        hover_data=[
            "Medicamento",
            "Classe_ABC"
        ]
    )

    fig.update_traces(
        mode="lines"
    )

    fig.update_layout(
        xaxis_title="Ranking",
        yaxis_title="% Acumulado"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )