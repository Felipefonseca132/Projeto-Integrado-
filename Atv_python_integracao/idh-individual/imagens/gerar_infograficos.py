# Gera os infograficos da tela de noticias
# python imagens/gerar_infograficos.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

uf = pd.read_csv("dados/tratados/idhm_uf.csv")
br = pd.read_csv("dados/tratados/idhm_brasil.csv")
mun = pd.read_csv("dados/tratados/idhm_municipios_2010.csv")

PETROLEO, TERRACOTA, MOSTARDA, OLIVA, FUNDO, TEXTO = "#1D4E5F", "#B4462F", "#D49A1A", "#6B7F3A", "#FAF6EE", "#1F1A17"
plt.rcParams["font.family"] = "DejaVu Serif"
UFS = ["MA", "PA", "AC", "BA", "MG"]


def salvar(fig, nome):
    fig.savefig("imagens/" + nome, dpi=150, bbox_inches="tight", facecolor=FUNDO)
    plt.close(fig)
    print("salvo", nome)


# 1) dimensoes em 2024
d = uf[(uf["ano"] == 2024) & uf["uf"].isin(UFS) & (uf["componente"] != "Geral")]
p = d.pivot_table(index="uf", columns="componente", values="valor").reindex(UFS)
fig, ax = plt.subplots(figsize=(6, 4), facecolor=FUNDO)
ax.set_facecolor(FUNDO)
x = np.arange(len(UFS))
for i, (comp, cor) in enumerate([("Longevidade", OLIVA), ("Educação", PETROLEO), ("Renda", TERRACOTA)]):
    ax.bar(x + (i - 1) * 0.27, p[comp], width=0.27, color=cor, label=comp)
ax.set_xticks(x, UFS)
ax.set_ylim(0.6, 0.95)
ax.set_title("2024: a renda é a dimensão mais baixa", fontsize=13, color=TEXTO, weight="bold")
ax.legend(frameon=False, fontsize=9, ncol=3, loc="upper center")
ax.spines[["top", "right"]].set_visible(False)
salvar(fig, "infografico_dimensoes.png")

# 2) Brasil 1991 a 2024
fig, ax = plt.subplots(figsize=(6, 4), facecolor=FUNDO)
ax.set_facecolor(FUNDO)
ax.plot(br["ano"], br["valor"], color=PETROLEO, lw=3, marker="o")
for a in [1991, 2000, 2010, 2024]:
    v = br.loc[br["ano"] == a, "valor"].iloc[0]
    ax.annotate(f"{v:.3f}".replace(".", ","), (a, v), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=10, color=TEXTO)
ax.axhline(0.8, color=TERRACOTA, lw=1, ls="--")
ax.text(1991, 0.808, "muito alto", color=TERRACOTA, fontsize=9)
ax.set_ylim(0.45, 0.86)
ax.set_title("IDHM do Brasil: de 0,493 a 0,805", fontsize=13, color=TEXTO, weight="bold")
ax.spines[["top", "right"]].set_visible(False)
salvar(fig, "infografico_evolucao.png")

# 3) municipios por faixa em 2010
ordem = ["Muito baixo", "Baixo", "Médio", "Alto", "Muito alto"]
cont = mun["faixa"].value_counts().reindex(ordem).fillna(0)
fig, ax = plt.subplots(figsize=(6, 4), facecolor=FUNDO)
ax.set_facecolor(FUNDO)
barras = ax.bar(ordem, cont.values, color=[TERRACOTA, TERRACOTA, PETROLEO, PETROLEO, MOSTARDA])
for b, v in zip(barras, cont.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 30, f"{int(v):,}".replace(",", "."), ha="center", fontsize=10, color=TEXTO)
ax.set_title("Municípios por faixa de IDHM (2010)", fontsize=13, color=TEXTO, weight="bold")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.set_yticks([])
salvar(fig, "infografico_faixas.png")
