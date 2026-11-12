# Parte visual do app (cores, fontes, css e cabecalho das telas)
# Visual de "jornal de dados": fundo cor de papel, titulos com serifa e menu no topo

import streamlit as st
import plotly.io as pio
import plotly.graph_objects as go

# paleta
TINTA = "#1F1A17"        # texto principal
PAPEL = "#FAF6EE"        # fundo
TERRACOTA = "#B4462F"    # cor de destaque
PETROLEO = "#1D4E5F"
MOSTARDA = "#D49A1A"
OLIVA = "#6B7F3A"
AMEIXA = "#7A3E65"
AREIA = "#E7DCC8"
CINZA = "#8C8279"

CORES = [PETROLEO, TERRACOTA, MOSTARDA, OLIVA, AMEIXA, "#3E7CB1", "#C26D3A", "#4F4A45"]

# cada dimensao tem sempre a mesma cor em todos os graficos
COR_DIMENSAO = {"Longevidade": OLIVA, "Educação": PETROLEO, "Renda": TERRACOTA, "Geral": TINTA}


def configurar_graficos():
    pio.templates["jornal"] = go.layout.Template(
        layout=dict(
            colorway=CORES,
            font=dict(family="IBM Plex Sans, Arial, sans-serif", color=TINTA, size=13),
            title=dict(font=dict(family="Fraunces, Georgia, serif", size=18)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor=AREIA, griddash="dot", zerolinecolor=CINZA, linecolor=TINTA, showline=True),
            yaxis=dict(gridcolor=AREIA, griddash="dot", zerolinecolor=CINZA),
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(gridcolor=AREIA, linecolor=CINZA, griddash="dot"),
                       angularaxis=dict(gridcolor=AREIA, linecolor=TINTA)),
            hoverlabel=dict(bgcolor=PAPEL, bordercolor=TINTA, font_size=13),
            margin=dict(t=40, l=10, r=10),
        )
    )
    pio.templates.default = "simple_white+jornal"


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

#MainMenu, footer, [data-testid="stAppDeployButton"], [data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stHeader"] {background: transparent;}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display: none;}
.block-container {padding-top: 1.2rem; max-width: 1240px;}

html, body, .stApp, .stMarkdown, p, li, label, input, textarea, button {
    font-family: 'IBM Plex Sans', Arial, sans-serif;
}
h1, h2, h3, h4 {font-family: 'Fraunces', Georgia, serif !important; color: #1F1A17; letter-spacing: -0.01em;}

/* faixa do topo com o nome da startup */
.topo {
    display: flex; justify-content: space-between; align-items: baseline;
    border-top: 6px solid #1F1A17; border-bottom: 1px solid #1F1A17;
    padding: 10px 0 8px 0; margin-bottom: 4px;
}
.topo .marca {font-family: 'Fraunces', Georgia, serif; font-size: 1.9rem; font-weight: 700; color: #1F1A17;}
.topo .marca span {color: #B4462F;}
.topo .info {font-size: .78rem; text-transform: uppercase; letter-spacing: .12em; color: #6B625B;}

/* menu de telas (segmented control) */
[data-testid="stButtonGroup"] button {border-radius: 0 !important; border-color: #1F1A17 !important;}
[data-testid="stButtonGroup"] button[aria-checked="true"], [data-testid="stButtonGroup"] button[kind="segmented_controlActive"] {
    background: #1F1A17 !important; color: #FAF6EE !important;
}

/* resumo dos filtros */
.filtros-ativos {font-size: .85rem; color: #6B625B; padding-top: 8px;}
.filtros-ativos b {color: #1F1A17;}

/* manchete de cada tela */
.manchete {border-bottom: 3px double #1F1A17; padding: 18px 0 14px 0; margin: 6px 0 22px 0;}
.manchete .chapeu {
    font-size: .8rem; font-weight: 600; text-transform: uppercase; letter-spacing: .14em; color: #B4462F;
}
.manchete h1 {font-size: 2.7rem; line-height: 1.1; margin: 4px 0 6px 0; padding: 0;}
.manchete p {font-size: 1.12rem; font-style: italic; color: #5A524C; margin: 0;}

/* subtitulos */
.block-container h3 {font-size: 1.45rem; border-bottom: 1px solid #D9CDB8; padding-bottom: 4px; margin-top: 1.4rem;}

/* numeros em destaque: sem caixa, so uma regua do lado */
[data-testid="stMetric"] {background: transparent; border-left: 3px solid #B4462F; padding: 2px 0 2px 14px;}
[data-testid="stMetricLabel"] p {font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; color: #6B625B;}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {font-family: 'Fraunces', Georgia, serif !important; font-size: 2rem; color: #1F1A17;}

/* tabelas com borda fina */
[data-testid="stDataFrame"] {border-top: 2px solid #1F1A17;}

/* avisos */
[data-testid="stAlert"] {border-radius: 0; border-left: 4px solid #1D4E5F;}
</style>
"""


def aplicar_estilo():
    st.markdown(CSS, unsafe_allow_html=True)


def topo():
    st.markdown(
        '<div class="topo"><div class="marca">Lupa<span>.</span>Social</div>'
        '<div class="info">Indicador 4 · IDHM · Atlas Brasil</div></div>',
        unsafe_allow_html=True,
    )


def cabecalho(titulo, descricao, etiqueta=""):
    html = '<div class="manchete">'
    if etiqueta:
        html += f'<div class="chapeu">{etiqueta}</div>'
    html += f"<h1>{titulo}</h1><p>{descricao}</p></div>"
    st.markdown(html, unsafe_allow_html=True)
