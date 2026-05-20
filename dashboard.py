# dashboard.py

import streamlit as st
import plotly.express as px


def exibir_dashboard(
    df,
    indicadores,
    df_abc
):

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Valor Total",
        f'R$ {df["Valor_Total"].sum():,.2f}'
    )

    col2.metric(
        "Quantidade",
        f'{df["Quantidade"].sum():,.0f}'
    )

    col3.metric(
        "Medicamentos",
        df["Medicamento"].nunique()
    )

    st.subheader("Top 10 Custo")

    top10 = (
        df.groupby("Medicamento")
        ["Valor_Total"]
        .sum()
        .reset_index()
        .sort_values(
            "Valor_Total",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top10,
        x="Medicamento",
        y="Valor_Total"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Curva ABC")

    fig2 = px.line(
        df_abc,
        y="Percentual_Acumulado"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )
