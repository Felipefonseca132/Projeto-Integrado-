# ETL do IDHM
# Bases do Atlas do Desenvolvimento Humano no Brasil (PNUD, Ipea e FJP)
#
# 1) IDHM por UF de 1991 a 2024, geral e por dimensao (4 arquivos exportados do Atlas)
# 2) IDHM dos 5.565 municipios em 2010 (Censo), geral e por dimensao
# 3) Convenios federais pagos aos municipios, para cruzar IDHM x investimento publico
#
# Rodar da pasta do projeto:  python etl/tratar_idhm.py

import pandas as pd

BRUTOS = "dados/brutos/"
TRATADOS = "dados/tratados/"

REGIAO_POR_COD = {"1": "Norte", "2": "Nordeste", "3": "Sudeste", "4": "Sul", "5": "Centro-Oeste"}
SIGLA_POR_COD = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL", 28: "SE", 29: "BA",
    31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR", 42: "SC", 43: "RS",
    50: "MS", 51: "MT", 52: "GO", 53: "DF",
}
ARQUIVOS_UF = {
    "Geral": "idhm_geral_uf.csv",
    "Longevidade": "idhm_longevidade_uf.csv",
    "Educação": "idhm_educacao_uf.csv",
    "Renda": "idhm_renda_uf.csv",
}

# IDHM do Brasil (Atlas): 1991, 2000 e 2010 pelos Censos; 2012 em diante pela PNAD Continua
BRASIL = {1991: 0.493, 2000: 0.612, 2010: 0.727, 2012: 0.744, 2013: 0.752, 2014: 0.760, 2015: 0.762,
          2016: 0.767, 2017: 0.770, 2018: 0.777, 2019: 0.782, 2020: 0.776, 2021: 0.757, 2022: 0.788,
          2023: 0.798, 2024: 0.805}


def tratar_uf():
    partes = []
    for componente, arquivo in ARQUIVOS_UF.items():
        # o Atlas exporta com uma linha de titulo, ; como separador e virgula no decimal
        df = pd.read_csv(BRUTOS + arquivo, sep=";", skiprows=1, decimal=",", encoding="utf-8-sig")
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]  # coluna vazia do ; no fim da linha
        df = df.rename(columns={"Sigla": "uf", "Código": "cod_uf", "Estado": "estado"})
        longo = df.melt(id_vars=["uf", "cod_uf", "estado"], var_name="ano", value_name="valor")
        longo["componente"] = componente
        partes.append(longo)

    uf = pd.concat(partes, ignore_index=True)
    uf["ano"] = uf["ano"].astype(int)
    uf["regiao"] = uf["cod_uf"].astype(str).str[0].map(REGIAO_POR_COD)
    uf["fonte"] = uf["ano"].apply(lambda a: "Censo" if a <= 2010 else "PNAD Contínua")

    print("UF: linhas", len(uf), "| UFs", uf["uf"].nunique(), "| anos", sorted(uf["ano"].unique()))
    print("valores vazios:", uf["valor"].isna().sum())
    uf.to_csv(TRATADOS + "idhm_uf.csv", index=False)

    br = pd.DataFrame({"ano": list(BRASIL.keys()), "valor": list(BRASIL.values())})
    br.to_csv(TRATADOS + "idhm_brasil.csv", index=False)
    return uf


def faixa_idhm(v):
    # faixas oficiais do Atlas
    if v < 0.5:
        return "Muito baixo"
    if v < 0.6:
        return "Baixo"
    if v < 0.7:
        return "Médio"
    if v < 0.8:
        return "Alto"
    return "Muito alto"


def tratar_municipios():
    mun = pd.read_csv(BRUTOS + "atlas2013_idhm_municipios_2010.csv", sep=";", decimal=",", encoding="utf-8-sig")
    mun = mun.rename(columns={"ANO": "ano", "UF": "cod_uf", "Codmun7": "cod_mun", "Município": "municipio",
                              "IDHM": "geral", "IDHM_E": "educacao", "IDHM_L": "longevidade", "IDHM_R": "renda"})
    mun["uf"] = mun["cod_uf"].map(SIGLA_POR_COD)
    mun["regiao"] = mun["cod_uf"].astype(str).str[0].map(REGIAO_POR_COD)
    mun["municipio"] = mun["municipio"].str.title()
    mun["faixa"] = mun["geral"].apply(faixa_idhm)
    # dimensao que mais puxa o IDHM para baixo em cada municipio
    mun["pior_dimensao"] = mun[["longevidade", "educacao", "renda"]].idxmin(axis=1).map(
        {"longevidade": "Longevidade", "educacao": "Educação", "renda": "Renda"})

    mun = mun[["cod_mun", "municipio", "uf", "regiao", "ano", "geral", "longevidade", "educacao", "renda", "faixa", "pior_dimensao"]]
    print("municípios:", len(mun), "| sem UF:", mun["uf"].isna().sum())
    mun.to_csv(TRATADOS + "idhm_municipios_2010.csv", index=False)
    return mun


def tratar_convenios(mun):
    conv = pd.read_csv(BRUTOS + "convenios_federais_municipios.csv")
    conv = conv.dropna(subset=["cod7", "pop"])
    conv["cod_mun"] = conv["cod7"].astype(int)
    conv = conv[["cod_mun", "n_convenio", "total_pago", "pop"]]
    df = mun.merge(conv, on="cod_mun", how="inner")
    df["pago_por_habitante"] = (df["total_pago"] / df["pop"]).round(2)
    print("municípios com convênios:", len(df))
    df.to_csv(TRATADOS + "idhm_x_convenios.csv", index=False)
    return df


if __name__ == "__main__":
    tratar_uf()
    m = tratar_municipios()
    tratar_convenios(m)
    print("pronto")
