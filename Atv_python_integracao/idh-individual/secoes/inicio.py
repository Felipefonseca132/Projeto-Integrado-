import streamlit as st
from layout import cabecalho


def mostrar(filtros, arquivo=None):
    cabecalho("Onde investir para reduzir a desigualdade?",
              "As três dimensões do IDH (longevidade, educação e renda) nos estados do consórcio",
              "Projeto Integrador • Números que Falam • Indicador 4")
    st.markdown(
        "Somos a **Lupa Social**, uma startup de análise de dados. Um consórcio de governadores quer criar um "
        "**fundo regional para reduzir desigualdades** e precisa saber em que dimensão do IDH investir primeiro."
    )
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("Perguntas que o painel responde")
        st.markdown(
            "1. Qual dimensão do IDH (saúde, educação ou renda) **mais puxa a nota para baixo** em cada estado?\n"
            "2. Qual a **evolução do IDHM** desde os anos 2000 até o dado mais recente (2024)?\n"
            "3. Quais municípios têm os **menores e maiores índices** e qual é a **dispersão** (IQR e desvio padrão) entre os estados?"
        )
        st.subheader("Como ler o IDHM")
        st.markdown(
            "O IDHM vai de **0 a 1**. Ele é a média geométrica de três dimensões:\n"
            "- **Longevidade:** esperança de vida ao nascer\n"
            "- **Educação:** escolaridade dos adultos e frequência escolar dos jovens\n"
            "- **Renda:** renda por pessoa\n\n"
            "Faixas: muito baixo (até 0,499), baixo (0,500 a 0,599), médio (0,600 a 0,699), alto (0,700 a 0,799) e muito alto (0,800 ou mais)."
        )
    with c2:
        st.subheader("Nossos clientes")
        st.markdown(
            """
| Persona | Cargo |
|---|---|
| João | Governador do Maranhão |
| Helder | Governador do Pará |
| Gladson | Governador do Acre |
| Susu | Governador da Bahia |
| Verinha | Governadora de Minas Gerais |
"""
        )
        st.info("Use o menu no topo para trocar de tela. O botão Filtros (componente, UF e anos) vale para todas as telas.")
    st.subheader("De onde vêm os dados")
    st.markdown(
        "- **IDHM por UF, 1991 a 2024**, geral e por dimensão: Atlas do Desenvolvimento Humano no Brasil (PNUD, Ipea e FJP). "
        "1991, 2000 e 2010 vêm dos Censos; de 2012 em diante, da PNAD Contínua (Radar IDHM).\n"
        "- **IDHM dos 5.565 municípios em 2010**: Atlas Brasil, com base no Censo 2010 (último dado municipal completo).\n"
        "- **Convênios federais pagos aos municípios**: valores pagos por convênios do governo federal (SICONV), "
        "para 3.232 municípios, usados como medida de investimento público."
    )
