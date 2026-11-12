import streamlit as st

from secoes import inicio, dimensoes, evolucao, municipios, investimento, noticias
from layout import aplicar_estilo, configurar_graficos, topo

st.set_page_config(page_title="Lupa Social | IDH", page_icon="🔎", layout="wide", initial_sidebar_state="collapsed")
aplicar_estilo()
configurar_graficos()

REGIOES_UF = {
    "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
    "Centro-Oeste": ["DF", "GO", "MS", "MT"],
}
# estados dos governadores do cenario
UFS_PERSONAS = ["AC", "BA", "MA", "MG", "PA"]
ANOS = [1991, 2000, 2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

PAGINAS = {
    "Início": inicio,
    "Dimensões": dimensoes,
    "Evolução": evolucao,
    "Municípios": municipios,
    "Investimento": investimento,
    "Na imprensa": noticias,
}

# ---------------- topo ----------------
topo()

def _manter_pagina():
    # clicar de novo na tela marcada desmarcaria o botao; aqui ele continua na mesma tela
    if st.session_state["pagina"] is None:
        st.session_state["pagina"] = st.session_state.get("ultima_pagina", "Início")
    st.session_state["ultima_pagina"] = st.session_state["pagina"]


c_menu, c_filtro = st.columns([5, 1], vertical_alignment="center")
with c_menu:
    pagina = st.segmented_control("Telas", list(PAGINAS.keys()), default="Início",
                                  key="pagina", label_visibility="collapsed", on_change=_manter_pagina)
    pagina = pagina or "Início"

modulo = PAGINAS[pagina]

with c_filtro:
    with st.popover("Filtros", icon=":material/tune:", width="stretch"):
        componente = st.selectbox("Componente do IDH", ["Geral", "Longevidade", "Educação", "Renda"], key="f_comp")
        regioes = st.multiselect("Região", list(REGIOES_UF.keys()), default=list(REGIOES_UF.keys()), key="f_reg")
        if not regioes:
            regioes = list(REGIOES_UF.keys())
        opcoes_uf = sorted([uf for r in regioes for uf in REGIOES_UF[r]])
        ufs = st.multiselect("Unidade da Federação", opcoes_uf,
                             default=[u for u in UFS_PERSONAS if u in opcoes_uf], key="f_uf",
                             help="Vem marcado com os estados dos governadores do cenário. Vazio = todas as UFs das regiões escolhidas.")
        if not ufs:
            ufs = opcoes_uf
        anos = st.multiselect("Anos", ANOS, default=[a for a in ANOS if a >= 2000], key="f_anos")
        if not anos:
            anos = ANOS

        # upload da base da tela atual (opcional)
        arquivo = None
        if hasattr(modulo, "COLUNAS_UPLOAD"):
            st.divider()
            arquivo = st.file_uploader("Enviar base desta tela (CSV ou XLSX)", type=["csv", "xlsx"], key="up_" + pagina)
            st.caption("Colunas esperadas: " + ", ".join(modulo.COLUNAS_UPLOAD))
            st.caption("Sem upload, o app usa a base do Atlas Brasil que já está em dados/tratados.")

filtros = {"componente": componente, "regioes": regioes, "ufs": ufs, "anos": sorted(anos)}

anos_txt = f"{min(anos)} a {max(anos)}" if len(anos) > 1 else str(anos[0])
st.markdown(
    f'<div class="filtros-ativos">Mostrando <b>{componente}</b> · <b>{", ".join(ufs) if len(ufs) <= 8 else str(len(ufs)) + " UFs"}</b> · '
    f'<b>{anos_txt}</b>{" · base enviada" if arquivo is not None else ""}</div>',
    unsafe_allow_html=True,
)

modulo.mostrar(filtros, arquivo)

st.markdown("---")
st.caption("Fonte: Atlas do Desenvolvimento Humano no Brasil (PNUD, Ipea, FJP) · Convênios federais (SICONV)")
