# Noticias sobre superacao da pobreza e indices sociais

import os
import streamlit as st

from layout import cabecalho


NOTICIAS = [
    {"titulo": "Brasil alcança pela primeira vez patamar de muito alto desenvolvimento humano",
     "fonte": "PNUD Brasil", "link": "https://www.undp.org/pt/node/585556",
     "resumo": "Com dados do Radar IDHM 2024, o país passa para a faixa de muito alto desenvolvimento humano."},
    {"titulo": "Nordeste lidera maiores avanços estaduais no IDHM entre 2012 e 2024",
     "fonte": "PNUD Brasil", "link": "https://www.undp.org/pt/brazil/news/nordeste-lidera-maiores-avancos-estaduais-no-idhm-entre-2012-e-2024",
     "resumo": "Os estados do Nordeste estão entre os que mais avançaram no índice no período."},
    {"titulo": "Educação, longevidade e retomada da renda impulsionam avanço do IDHM brasileiro",
     "fonte": "PNUD Brasil", "link": "https://www.undp.org/pt/node/586216",
     "resumo": "Análise de quais dimensões explicam a melhora recente do IDHM."},
    {"titulo": "Maranhão avança no IDHM e entra na faixa de alto desenvolvimento humano em 2024",
     "fonte": "O Imparcial", "link": "https://oimparcial.com.br/brasil/2026/05/maranhao-avanca-no-idhm-e-entra-na-faixa-de-alto-desenvolvimento-humano-em-2024/",
     "resumo": "O estado, um dos clientes do cenário, chega à faixa alta do índice."},
    {"titulo": "Brasil sai do mapa da fome após três anos",
     "fonte": "O Povo (jul/2025)", "link": "https://www.opovo.com.br/noticias/brasil/2025/07/28/brasil-sai-do-mapa-da-fome-anuncia-onu.html",
     "resumo": "Relatório da ONU retira o Brasil do Mapa da Fome."},
    {"titulo": "Brasil tem maior índice de desenvolvimento humano da história, aponta ONU",
     "fonte": "CNN Brasil", "link": "https://www.cnnbrasil.com.br/nacional/brasil/brasil-tem-maior-indice-de-desenvolvimento-humano-da-historia-aponta-onu/",
     "resumo": "Reportagem sobre o recorde do índice brasileiro."},
]


def mostrar(filtros, arquivo=None):
    cabecalho("Na imprensa", "Superação da extrema pobreza e índices sociais no Brasil", "Conteúdo adicional")

    imagens = ["imagens/infografico_dimensoes.png", "imagens/infografico_evolucao.png", "imagens/infografico_faixas.png"]
    cols = st.columns(3)
    for col, img in zip(cols, imagens):
        if os.path.exists(img):
            col.image(img, width="stretch")

    pasta = "imagens/fotos"
    if os.path.isdir(pasta):
        fotos = sorted(f for f in os.listdir(pasta) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
        if fotos:
            cols = st.columns(min(len(fotos), 3))
            for i, foto in enumerate(fotos):
                cols[i % len(cols)].image(os.path.join(pasta, foto), caption=os.path.splitext(foto)[0], width="stretch")

    for i in range(0, len(NOTICIAS), 2):
        cols = st.columns(2)
        for col, n in zip(cols, NOTICIAS[i:i + 2]):
            with col.container(border=True):
                st.markdown(f"**{n['titulo']}**")
                st.caption(n["fonte"])
                st.write(n["resumo"])
                st.markdown(f"[Ler a matéria]({n['link']})")
