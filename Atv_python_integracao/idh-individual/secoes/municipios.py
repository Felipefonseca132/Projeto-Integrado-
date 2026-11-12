# Pergunta 3: menores e maiores IDHM municipais e dispersao entre os estados (Censo 2010)

import pandas as pd
import plotly.express as px
import streamlit as st

from layout import cabecalho, PETROLEO, MOSTARDA, TERRACOTA
from estatisticas import calcular_estatisticas, tabela_estatisticas, fmt
from secoes.dados import base_municipios, COLUNA, COLUNAS_MUN

COLUNAS_UPLOAD = COLUNAS_MUN


def mostrar(filtros, arquivo=None):
    comp = filtros["componente"]
    col = COLUNA[comp]
    cabecalho("Municípios: quem está no topo e quem está no fim?",
              f"IDHM {comp.lower() if comp != 'Geral' else 'geral'} dos municípios no Censo 2010 (último dado municipal completo)",
              "Pergunta 3")

    mun = base_municipios(arquivo)
    df = mun[mun["uf"].isin(filtros["ufs"])].dropna(subset=[col])
    if len(df) < 4:
        st.warning("Poucos municípios com esses filtros.")
        return

    est = calcular_estatisticas(df[col])
    k = st.columns(6)
    k[0].metric("Municípios", fmt(len(df)))
    k[1].metric("Média", fmt(est["media"], 3))
    k[2].metric("Mediana", fmt(est["mediana"], 3))
    k[3].metric("IQR", fmt(est["iqr"], 3))
    k[4].metric("Desvio padrão", fmt(est["desvio_padrao"], 3))
    k[5].metric("Amplitude", fmt(est["amplitude"], 3))

    # estatisticas + histograma
    st.subheader("Estatísticas do IDHM municipal")
    c1, c2 = st.columns([2, 3])
    c1.dataframe(tabela_estatisticas(est), hide_index=True, width="stretch", height=560)
    fig_h = px.histogram(df, x=col, nbins=40, color_discrete_sequence=[PETROLEO],
                         labels={col: f"IDHM {comp}"})
    fig_h.add_vline(x=est["media"], line_dash="dash", line_color=TERRACOTA, line_width=2.5, layer="above")
    fig_h.add_vline(x=est["mediana"], line_dash="dot", line_color=MOSTARDA, line_width=2.5, layer="above")
    fig_h.add_scatter(x=[None], y=[None], mode="lines", name=f"Média: {fmt(est['media'], 3)}", line=dict(color=TERRACOTA, dash="dash"))
    fig_h.add_scatter(x=[None], y=[None], mode="lines", name=f"Mediana: {fmt(est['mediana'], 3)}", line=dict(color=MOSTARDA, dash="dot"))
    fig_h.update_layout(height=560, yaxis_title="Quantidade de municípios", bargap=0.05, legend=dict(orientation="h", y=1.08))
    c2.plotly_chart(fig_h, width="stretch")

    if abs(est["media"] - est["mediana"]) < 0.005:
        leitura = "A média e a mediana estão quase iguais: a distribuição é praticamente simétrica."
    elif est["media"] < est["mediana"]:
        leitura = "A média é menor que a mediana: alguns municípios com índice muito baixo puxam a média para baixo."
    else:
        leitura = "A média é maior que a mediana: alguns municípios com índice muito alto puxam a média para cima."
    st.markdown(f"{leitura} Metade dos municípios está entre **{fmt(est['q1'], 3)}** e **{fmt(est['q3'], 3)}** (IQR de {fmt(est['iqr'], 3)}).")

    # boxplot por UF
    st.subheader("Dispersão entre os estados")
    fig_b = px.box(df, x="uf", y=col, color="uf", points="outliers", hover_name="municipio",
                   labels={"uf": "UF", col: f"IDHM {comp}"})
    fig_b.update_layout(showlegend=False, height=460)
    st.plotly_chart(fig_b, width="stretch")

    por_uf = df.groupby("uf")[col].agg(
        Municípios="count", Média="mean", Mediana="median", Q1=lambda s: s.quantile(0.25),
        Q3=lambda s: s.quantile(0.75), Desvio="std", Mínimo="min", Máximo="max")
    por_uf["IQR"] = por_uf["Q3"] - por_uf["Q1"]
    por_uf["Amplitude"] = por_uf["Máximo"] - por_uf["Mínimo"]
    por_uf = por_uf[["Municípios", "Média", "Mediana", "Q1", "Q3", "IQR", "Desvio", "Mínimo", "Máximo", "Amplitude"]]
    st.dataframe(por_uf.round(3).reset_index().rename(columns={"uf": "UF"}), hide_index=True, width="stretch")
    mais = por_uf["IQR"].idxmax()
    menos = por_uf["IQR"].idxmin()
    st.markdown(f"**{mais}** tem a maior dispersão (IQR {fmt(por_uf.loc[mais, 'IQR'], 3)}): os municípios do estado são muito diferentes entre si. "
                f"**{menos}** é o mais homogêneo (IQR {fmt(por_uf.loc[menos, 'IQR'], 3)}).")

    # rankings
    st.subheader("Menores e maiores índices")
    cols = ["municipio", "uf", col, "pior_dimensao"] if "pior_dimensao" in df.columns else ["municipio", "uf", col]
    nomes = {"municipio": "Município", "uf": "UF", col: f"IDHM {comp}", "pior_dimensao": "Pior dimensão"}
    c1, c2 = st.columns(2)
    c1.markdown("**10 menores**")
    c1.dataframe(df.nsmallest(10, col)[cols].rename(columns=nomes), hide_index=True, width="stretch")
    c2.markdown("**10 maiores**")
    c2.dataframe(df.nlargest(10, col)[cols].rename(columns=nomes), hide_index=True, width="stretch")

    out = df[(df[col] < est["lim_inferior"]) | (df[col] > est["lim_superior"])]
    st.markdown(f"Pela regra de 1,5 × IQR (limites {fmt(est['lim_inferior'], 3)} e {fmt(est['lim_superior'], 3)}), "
                f"há **{len(out)} municípios outliers** nos estados selecionados.")
    if len(out):
        with st.expander("Ver os outliers"):
            st.dataframe(out.sort_values(col)[cols].rename(columns=nomes), hide_index=True, width="stretch")
