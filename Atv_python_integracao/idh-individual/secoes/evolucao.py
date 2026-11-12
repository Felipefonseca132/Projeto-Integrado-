# Pergunta 2: evolucao do IDHM desde os anos 2000

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from layout import cabecalho, CORES
from estatisticas import fmt
from secoes.dados import base_uf, base_brasil, COLUNAS_UF

COLUNAS_UPLOAD = COLUNAS_UF


def mostrar(filtros, arquivo=None):
    comp = filtros["componente"]
    cabecalho("Como o IDHM evoluiu?", f"IDHM {comp.lower() if comp != 'Geral' else 'geral'} de cada estado ao longo dos anos", "Pergunta 2")

    uf = base_uf(arquivo)
    sel = uf[uf["uf"].isin(filtros["ufs"]) & (uf["componente"] == comp) & uf["ano"].isin(filtros["anos"])]
    if sel.empty:
        st.warning("Sem dados para os filtros.")
        return
    ano_ini, ano_fim = sel["ano"].min(), sel["ano"].max()

    # linhas
    fig = go.Figure()
    for i, (sigla, g) in enumerate(sel.sort_values("ano").groupby("uf")):
        fig.add_scatter(x=g["ano"], y=g["valor"], mode="lines+markers", name=sigla,
                        line=dict(color=CORES[i % len(CORES)], width=2.5))
    if comp == "Geral":
        br = base_brasil()
        br = br[br["ano"].isin(filtros["anos"])]
        fig.add_scatter(x=br["ano"], y=br["valor"], mode="lines", name="Brasil",
                        line=dict(color="#1F1A17", width=2, dash="dash"))
    if ano_ini <= 2010 < ano_fim:
        fig.add_vline(x=2011, line_dash="dot", line_color="#8C8279",
                      annotation_text="Censo | PNAD", annotation_position="top")
    for limite, nome in [(0.6, "médio"), (0.7, "alto"), (0.8, "muito alto")]:
        fig.add_hline(y=limite, line_width=1, line_color="#D9CDB8",
                      annotation_text=f"faixa {nome}", annotation_position="right", annotation_font_color="#8C8279")
    fig.update_layout(height=500, xaxis_title="Ano", yaxis_title=f"IDHM {comp}", legend=dict(orientation="h", y=1.08))
    st.plotly_chart(fig, width="stretch")
    st.caption("Até 2010 os valores vêm dos Censos; de 2012 em diante, da PNAD Contínua. A metodologia muda, "
               "então compare a tendência, não diferenças pequenas na virada.")

    # tabela de crescimento
    piv = sel.pivot_table(index="uf", columns="ano", values="valor")
    resumo = pd.DataFrame({
        f"IDHM {ano_ini}": piv[ano_ini],
        f"IDHM {ano_fim}": piv[ano_fim],
    })
    resumo["Ganho (pontos)"] = resumo[f"IDHM {ano_fim}"] - resumo[f"IDHM {ano_ini}"]
    resumo["Ganho (%)"] = resumo["Ganho (pontos)"] / resumo[f"IDHM {ano_ini}"] * 100
    resumo = resumo.sort_values("Ganho (pontos)", ascending=False).round(3)

    k1, k2, k3 = st.columns(3)
    k1.metric(f"Maior avanço {ano_ini}-{ano_fim}", resumo.index[0], f"+{fmt(resumo['Ganho (pontos)'].iloc[0], 3)}")
    k2.metric(f"Menor avanço {ano_ini}-{ano_fim}", resumo.index[-1], f"+{fmt(resumo['Ganho (pontos)'].iloc[-1], 3)}")
    k3.metric(f"Média dos estados em {ano_fim}", fmt(resumo[f"IDHM {ano_fim}"].mean(), 3))

    st.subheader(f"Quanto cada estado avançou de {ano_ini} a {ano_fim}")
    st.dataframe(resumo.reset_index().rename(columns={"uf": "UF"}), hide_index=True, width="stretch")

    if 2020 in piv.columns and 2021 in piv.columns:
        caiu = (piv[2021] < piv[2020]).sum()
        st.markdown(f"Entre 2020 e 2021, **{caiu} de {len(piv)}** estados selecionados tiveram queda, efeito da pandemia de covid-19 "
                    "(em geral, longevidade, educação e renda caíram). Depois disso o índice voltou a subir.")
    texto = f"O estado que mais avançou foi **{resumo.index[0]}** e o que menos avançou foi **{resumo.index[-1]}**. "
    if len(resumo) >= 3 and resumo[f"IDHM {ano_ini}"].corr(resumo["Ganho (pontos)"]) < 0:
        texto += "Quem começou mais atrás avançou mais, e por isso a distância entre esses estados diminuiu."
    st.markdown(texto)
