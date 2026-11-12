# Funcoes de estatistica usadas no painel

import numpy as np
import pandas as pd


def classe_modal(valores, largura=0.05):
    # o IDHM tem 3 casas decimais e quase nenhum valor se repete,
    # entao a moda e a classe (faixa) com mais municipios
    valores = pd.Series(valores).dropna()
    inicio = np.floor(valores.min() / largura) * largura
    fim = np.ceil(valores.max() / largura) * largura + largura
    bordas = np.round(np.arange(inicio, fim + largura / 2, largura), 4)
    contagem = pd.cut(valores, bins=bordas, right=False).value_counts()
    classe = contagem.idxmax()
    return classe.left, classe.right, int(contagem.max())


def moda_simples(valores):
    # valor exato que mais se repete (pode ter empate, pega o menor)
    return pd.Series(valores).dropna().mode().iloc[0]


def calcular_estatisticas(valores, largura_moda=0.05):
    s = pd.Series(valores).dropna()
    q1, q2, q3 = s.quantile(0.25), s.quantile(0.50), s.quantile(0.75)
    iqr = q3 - q1
    moda_ini, moda_fim, moda_qtd = classe_modal(s, largura_moda)
    est = {
        "n": len(s),
        "media": s.mean(),
        "mediana": s.median(),
        "moda": moda_simples(s),
        "moda_ini": moda_ini,
        "moda_fim": moda_fim,
        "moda_qtd": moda_qtd,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": iqr,
        "minimo": s.min(),
        "maximo": s.max(),
        "amplitude": s.max() - s.min(),
        "variancia": s.var(ddof=1),
        "desvio_padrao": s.std(ddof=1),
        "lim_inferior": q1 - 1.5 * iqr,
        "lim_superior": q3 + 1.5 * iqr,
    }
    est["cv"] = est["desvio_padrao"] / est["media"] * 100
    return est


def tabela_estatisticas(est):
    linhas = [
        ["Média", fmt(est["media"], 3)],
        ["Mediana (Q2)", fmt(est["mediana"], 3)],
        ["Moda (valor mais repetido)", fmt(est["moda"], 3)],
        ["Classe modal", f'{fmt(est["moda_ini"], 2)} a {fmt(est["moda_fim"], 2)} ({est["moda_qtd"]} municípios)'],
        ["Q1 (25%)", fmt(est["q1"], 3)],
        ["Q3 (75%)", fmt(est["q3"], 3)],
        ["IQR (Q3 - Q1)", fmt(est["iqr"], 3)],
        ["Mínimo", fmt(est["minimo"], 3)],
        ["Máximo", fmt(est["maximo"], 3)],
        ["Amplitude", fmt(est["amplitude"], 3)],
        ["Variância", fmt(est["variancia"], 5)],
        ["Desvio padrão", fmt(est["desvio_padrao"], 3)],
        ["Coef. de variação", f'{fmt(est["cv"], 1)}%'],
        ["Limite inferior (Q1 - 1,5·IQR)", fmt(est["lim_inferior"], 3)],
        ["Limite superior (Q3 + 1,5·IQR)", fmt(est["lim_superior"], 3)],
    ]
    return pd.DataFrame(linhas, columns=["Medida", "Valor"])


def ler_arquivo(arquivo):
    # aceita csv (com , ou ;) e xlsx vindo do st.file_uploader
    nome = arquivo.name.lower()
    if nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(arquivo)
    return pd.read_csv(arquivo, sep=None, engine="python", encoding="utf-8-sig")


def fmt(numero, casas=0):
    # formato brasileiro: 1.234,567
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")
