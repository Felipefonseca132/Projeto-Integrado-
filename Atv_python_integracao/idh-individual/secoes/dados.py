# Carregamento das bases (padrao ou enviada pelo usuario)

import pandas as pd
import streamlit as st

from estatisticas import ler_arquivo

COLUNA = {"Geral": "geral", "Longevidade": "longevidade", "Educação": "educacao", "Renda": "renda"}
COLUNAS_UF = ["uf", "ano", "componente", "valor"]
COLUNAS_MUN = ["municipio", "uf", "geral", "longevidade", "educacao", "renda"]


@st.cache_data
def _ler(caminho):
    return pd.read_csv(caminho)


def carregar(caminho, arquivo, colunas):
    if arquivo is not None:
        try:
            df = ler_arquivo(arquivo)
            faltam = [c for c in colunas if c not in df.columns]
            if faltam:
                st.error("O arquivo enviado não tem as colunas: " + ", ".join(faltam) + ". Usando a base padrão.")
            else:
                st.success(f"Base enviada carregada: {len(df)} linhas.")
                return df
        except Exception as erro:
            st.error(f"Não consegui ler o arquivo ({erro}). Usando a base padrão.")
    return _ler(caminho)


def base_uf(arquivo=None):
    return carregar("dados/tratados/idhm_uf.csv", arquivo, COLUNAS_UF)


def base_municipios(arquivo=None):
    return carregar("dados/tratados/idhm_municipios_2010.csv", arquivo, COLUNAS_MUN)


def base_brasil():
    return _ler("dados/tratados/idhm_brasil.csv")
