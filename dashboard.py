# dashboard.py

import streamlit as st
import plotly.express as px


def exibir_dashboard(df, indicadores):

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Valor Total",
        f'R$ {indicadores["valor_total"]:,.2f}'
    )

    col2.metric(
        "Quantidade",
        f'{indicadores["quantidade_total"]:,.0f}'
    )

    col3.metric(
        "Medicamentos",
        indicadores["medicamentos"]
    )

    col4.metric(
        "Classe A",
        indicadores["classe_a"]
    )

    st.subheader("Top 10 Medicamentos por Custo")

    top10 = (
        df.groupby("Medicamento")["Valor_Total"]
        .sum()
        .reset_index()
        .sort_values("Valor_Total", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top10,
        x="Medicamento",
        y="Valor_Total"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Curva ABC")

    fig2 = px.scatter(
        df,
        x=df.index,
        y="Percentual_Acumulado",
        color="Classe_ABC"
    )

    st.plotly_chart(fig2, use_container_width=True)