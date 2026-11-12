# Números que Falam: IDH / IDHM

Projeto Integrador Python e Matemática, **Indicador 4: Índice de Desenvolvimento Humano (IDH / IDHM)**.
Trabalho individual. Dashboard em Streamlit da startup **Lupa Social** para o consórcio de governadores do Maranhão, Pará, Acre, Bahia e Minas Gerais.

## Perguntas de negócio

1. Qual dimensão do IDH (saúde, educação ou renda) mais puxa a nota para baixo em cada estado?
2. Qual a evolução do IDHM desde os anos 2000 até o dado mais recente?
3. Quais municípios têm os menores e maiores índices e qual é a dispersão (IQR e desvio padrão) entre os estados?

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

Para refazer as bases tratadas a partir dos arquivos brutos:

```bash
python etl/tratar_idhm.py
python imagens/gerar_infograficos.py
```

## Telas

| Tela | O que mostra |
|---|---|
| Dimensões por estado | Gráfico de radar com longevidade, educação e renda, barras agrupadas e a pior dimensão de cada UF |
| Evolução do IDHM | Linhas de 1991 a 2024 por UF e Brasil, ganho de cada estado |
| Municípios e dispersão | KPIs, todas as estatísticas, histograma, boxplot por UF, ranking dos 10 menores e maiores, outliers |
| IDH x investimento | Dispersão (scatter) entre IDHM e convênios federais pagos por habitante, com correlação |
| Na imprensa | Notícias sobre superação da pobreza e infográficos |

Menu de telas no topo e botão Filtros ao lado: componente do IDH (Geral, Longevidade, Educação, Renda), Região, UF e anos. Cada tela aceita upload de CSV ou XLSX.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `app.py` | Menu lateral, filtros e upload |
| `etl/tratar_idhm.py` | ETL: lê os arquivos do Atlas, troca vírgula por ponto, passa para formato longo, junta municípios e convênios |
| `estatisticas.py` | Média, mediana, moda, quartis, IQR, amplitude, variância, desvio padrão, limites de outlier |
| `secoes/` | Uma tela por arquivo |
| `dados/brutos/` | Arquivos como vieram do Atlas Brasil |
| `dados/tratados/` | Bases limpas que o app usa |
| `ANALISE.md` | Análise descritiva |

## Fontes

- **Atlas do Desenvolvimento Humano no Brasil** (PNUD, Ipea e FJP): IDHM por UF de 1991 a 2024 (geral, longevidade, educação e renda). 1991, 2000 e 2010 vêm dos Censos; de 2012 em diante, da PNAD Contínua (Radar IDHM). Por isso há uma mudança de metodologia entre 2010 e 2012.
- **Atlas Brasil 2013**: IDHM dos 5.565 municípios em 2010 (Censo).
- **Convênios federais (SICONV)**: valor pago a 3.232 municípios, usado como medida de investimento público.
