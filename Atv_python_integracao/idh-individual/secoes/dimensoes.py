# Pergunta 1: qual dimensao mais puxa o IDHM para baixo em cada estado?

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from layout import cabecalho, CORES, COR_DIMENSAO
from estatisticas import fmt
from secoes.dados import base_uf, COLUNAS_UF

COLUNAS_UPLOAD = COLUNAS_UF
DIMENSOES = ["Longevidade", "Educação", "Renda"]


def mostrar(filtros, arquivo=None):
    cabecalho("Qual dimensão puxa o IDH para baixo?", "Longevidade, educação e renda lado a lado em cada estado", "Pergunta 1")

    uf = base_uf(arquivo)
    uf = uf[uf["uf"].isin(filtros["ufs"])]
    anos_disp = sorted(set(uf["ano"]) & set(filtros["anos"]))
    if not anos_disp:
        st.warning("Nenhum ano disponível com esses filtros.")
        return
    ano = st.select_slider("Ano analisado", options=anos_disp, value=anos_disp[-1])
    sel = uf[uf["ano"] == ano]
    tab = sel.pivot_table(index="uf", columns="componente", values="valor").reindex(columns=["Geral"] + DIMENSOES)
    tab = tab.dropna()
    if tab.empty:
        st.warning("Sem dados para esse ano.")
        return

    tab["Pior dimensão"] = tab[DIMENSOES].idxmin(axis=1)
    tab["Melhor dimensão"] = tab[DIMENSOES].idxmax(axis=1)
    tab["Distância (melhor - pior)"] = tab[DIMENSOES].max(axis=1) - tab[DIMENSOES].min(axis=1)

    contagem = tab["Pior dimensão"].value_counts()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Estados analisados", len(tab))
    k2.metric("IDHM médio dos estados", fmt(tab["Geral"].mean(), 3))
    k3.metric("Pior dimensão mais comum", contagem.index[0], f"em {contagem.iloc[0]} de {len(tab)} estados", delta_color="off")
    k4.metric("Maior distância entre dimensões", fmt(tab["Distância (melhor - pior)"].max(), 3),
              tab["Distância (melhor - pior)"].idxmax(), delta_color="off")

    # radar
    st.subheader(f"Radar das três dimensões em {ano}")
    fig = go.Figure()
    for i, (sigla, linha) in enumerate(tab.iterrows()):
        valores = [linha[d] for d in DIMENSOES] + [linha[DIMENSOES[0]]]
        fig.add_trace(go.Scatterpolar(r=valores, theta=DIMENSOES + [DIMENSOES[0]], name=sigla,
                                      line=dict(color=CORES[i % len(CORES)], width=3), marker=dict(size=8)))
    # o eixo comeca perto do menor valor, senao as diferencas entre os estados somem
    minimo = max(0, tab[DIMENSOES].min().min() - 0.03)
    maximo = min(1, tab[DIMENSOES].max().max() + 0.02)
    fig.update_layout(polar=dict(radialaxis=dict(range=[minimo, maximo], tickformat=".2f", angle=90, tickangle=90)), height=520,
                      legend=dict(orientation="h", y=-0.08))
    c1, c2 = st.columns([3, 2])
    c1.plotly_chart(fig, width="stretch")

    mostrar_tab = tab.copy().reset_index().rename(columns={"uf": "UF", "Geral": "IDHM"})
    for c in ["IDHM"] + DIMENSOES + ["Distância (melhor - pior)"]:
        mostrar_tab[c] = mostrar_tab[c].round(3)
    mostrar_tab = mostrar_tab.rename(columns={"Longevidade": "Longev.", "Educação": "Educ.", "Pior dimensão": "Pior"})
    c2.dataframe(mostrar_tab[["UF", "IDHM", "Longev.", "Educ.", "Renda", "Pior"]],
                 hide_index=True, width="stretch")
    c2.caption("Quanto mais para dentro o ponto do radar, mais aquela dimensão puxa o IDHM para baixo.")

    # barras agrupadas
    st.subheader("Comparação das dimensões por estado")
    longo = tab[DIMENSOES].reset_index().melt(id_vars="uf", var_name="Dimensão", value_name="Índice")
    fig_b = px.bar(longo, x="uf", y="Índice", color="Dimensão", barmode="group", text_auto=".3f", color_discrete_map=COR_DIMENSAO,
                   labels={"uf": "UF"})
    fig_b.update_yaxes(range=[max(0, longo["Índice"].min() - 0.1), 1])
    fig_b.update_layout(height=420, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_b, width="stretch")

    piores = ", ".join(f"**{u}** ({d.lower()})" for u, d in tab["Pior dimensão"].items())
    texto = f"Em {ano}, a dimensão que mais puxa o IDHM para baixo é: {piores}. "
    if (tab["Melhor dimensão"] == "Longevidade").all():
        texto += "A longevidade é a dimensão mais alta em todos esses estados: o gargalo não é a saúde. "
    texto += f"A prioridade mais comum para o fundo regional é **{contagem.index[0].lower()}**."
    st.markdown(texto)
    if ano <= 2010:
        st.info("Nos Censos (1991 a 2010) a educação era a dimensão mais baixa em quase todo o país. "
                "Compare com 2024 mudando o ano acima.")
