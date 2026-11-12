# IDH x investimento publico (convenios federais pagos aos municipios)

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from layout import cabecalho, TERRACOTA
from estatisticas import fmt
from secoes.dados import carregar, COLUNA

COLUNAS_UPLOAD = ["municipio", "uf", "geral", "longevidade", "educacao", "renda", "pago_por_habitante"]


def mostrar(filtros, arquivo=None):
    comp = filtros["componente"]
    col = COLUNA[comp]
    cabecalho("O investimento chega onde o IDH é mais baixo?",
              "IDHM 2010 de cada município x valor pago em convênios federais por habitante", "Dispersão")

    df = carregar("dados/tratados/idhm_x_convenios.csv", arquivo, COLUNAS_UPLOAD)
    df = df[df["uf"].isin(filtros["ufs"]) & (df["pago_por_habitante"] > 0)].dropna(subset=[col])
    if len(df) < 5:
        st.warning("Poucos municípios com esses filtros.")
        return

    pearson = df[col].corr(df["pago_por_habitante"])
    # Spearman = correlacao de Pearson entre as posicoes (ranks); assim nao precisa do scipy
    spearman = df[col].rank().corr(df["pago_por_habitante"].rank())

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Municípios", fmt(len(df)))
    k2.metric("Mediana paga por habitante", f"R$ {fmt(df['pago_por_habitante'].median(), 2)}")
    k3.metric("Correlação (Pearson)", fmt(pearson, 2))
    k4.metric("Correlação (Spearman)", fmt(spearman, 2))

    fig = px.scatter(df, x="pago_por_habitante", y=col, color="uf", hover_name="municipio", log_x=True, opacity=0.65,
                     hover_data={"pago_por_habitante": ":.2f", col: ":.3f", "uf": False},
                     labels={"pago_por_habitante": "Pago em convênios federais por habitante (R$, escala log)",
                             col: f"IDHM {comp} 2010", "uf": "UF"})
    # linha de tendencia (minimos quadrados no log do valor)
    x = np.log10(df["pago_por_habitante"])
    a, b = np.polyfit(x, df[col], 1)
    xs = np.linspace(x.min(), x.max(), 50)
    fig.add_scatter(x=10 ** xs, y=a * xs + b, mode="lines", name="Tendência", line=dict(color=TERRACOTA, width=3))
    fig.update_layout(height=540, legend=dict(orientation="h", y=1.08))
    st.plotly_chart(fig, width="stretch")

    forca = abs(spearman)
    nivel = "fraca" if forca < 0.3 else "moderada" if forca < 0.6 else "forte"
    sentido = "negativa" if spearman < 0 else "positiva"
    st.markdown(
        f"A correlação é **{nivel} e {sentido}** (Spearman {fmt(spearman, 2)}). "
        + ("Ou seja, os municípios com IDHM mais baixo tendem a receber **mais** por habitante: o dinheiro está indo, em parte, para onde a necessidade é maior. "
           if spearman < 0 else
           "Ou seja, os municípios com IDHM mais alto tendem a receber **mais** por habitante: o dinheiro não está chegando primeiro onde a necessidade é maior. ")
        + "Correlação não é causa: um valor alto pode ser efeito de mais projetos aprovados, e não do índice."
    )

    st.subheader("Média por faixa de IDHM")
    df["Faixa"] = pd.cut(df[col], bins=[0, 0.5, 0.6, 0.7, 0.8, 1],
                         labels=["Muito baixo", "Baixo", "Médio", "Alto", "Muito alto"], right=False)
    faixas = df.groupby("Faixa", observed=True)["pago_por_habitante"].agg(Municípios="count", Mediana="median", Média="mean").round(2)
    st.dataframe(faixas.reset_index(), hide_index=True, width="stretch")
    st.caption("Base: convênios federais pagos (SICONV) para 3.232 municípios. É uma amostra, não todo o investimento público. "
               "O Spearman é mais confiável aqui porque os valores pagos têm outliers muito grandes.")
