# Achados para investigação e discussão do case

Base: BCB/SCR.data v2, agosto de 2026, médias e grandes. Os cálculos usam saldos agregados. Os indicadores das companhias vêm dos demonstrativos CVM, com datas próprias. Valores arredondados para apresentação.

## Referência nacional

| Indicador | Resultado |
|---|---:|
| Carteira ativa | R$ 2,26 trilhões |
| Carteira das operações inadimplentes | R$ 44,36 bilhões |
| Taxa de inadimplência | 1,97% |
| Variação desde maio de 2026 | +0,12 p.p. |
| Proporção de ativos problemáticos | 5,60% |
| Participação a vencer até 360 dias | 46,03% |

No piso inicial de R$ 100 milhões, 393 combinações têm materialidade e histórico suficientes. Dessas, 61 acionam ambos os gatilhos, 35 acionam apenas deterioração recente, 71 acionam apenas diferença territorial e 226 ficam sem gatilho. Outras 149 combinações com saldo ficam sem classificação por materialidade ou histórico. A matriz também mostra combinações sem saldo publicado.

## Contextos associados à amostra de companhias

| Atividade / UF | Carteira | Inadimplência | Δ 3m | Diferença Brasil | Leitura padrão |
|---|---:|---:|---:|---:|---|
| Indústria / SC | R$ 41,94 bi | 1,44% | +0,03 p.p. | −0,33 p.p. | Sem gatilho |
| Indústria / RS | R$ 49,16 bi | 2,15% | +0,00 p.p. | +0,37 p.p. | Sem gatilho |
| Indústria / SP | R$ 194,34 bi | 1,40% | +0,14 p.p. | −0,38 p.p. | Sem gatilho |
| Comércio / RS | R$ 34,51 bi | 4,06% | +0,48 p.p. | −0,35 p.p. | Sem gatilho |
| Comércio / SP | R$ 111,90 bi | 4,47% | +0,64 p.p. | +0,06 p.p. | Deterioração recente |
| Transporte / SP | R$ 69,81 bi | 1,84% | −0,29 p.p. | −0,44 p.p. | Sem gatilho |
| Construção / MG | R$ 12,22 bi | 2,95% | +0,27 p.p. | −0,73 p.p. | Sem gatilho |
| Eletricidade e gás / MG | R$ 8,57 bi | 0,55% | +0,53 p.p. | +0,39 p.p. | Deterioração recente |
| Eletricidade e gás / PR | R$ 2,74 bi | 1,26% | +0,06 p.p. | +1,10 p.p. | Acima da referência |

A pequena variação da indústria/RS é positiva antes do arredondamento. A tabela não é um ranking de risco das companhias associadas aos recortes.

## Exemplo de análise: comércio em São Paulo

O recorte sobe 0,64 p.p., mas fica apenas 0,06 p.p. acima do comércio no Brasil. A evidência sustenta a existência de deterioração recente no corte. Ela não sustenta, isoladamente, que o fenômeno é específico de São Paulo.

Na consulta a Magazine Luiza, o analista pode formular perguntas sobre geração de caixa, estoque, recebíveis e dependência de renovação de linhas. As respostas exigem análise da companhia e de suas operações. A taxa de 4,47% é do grupo de comparação.

## Exemplo de análise: eletricidade e gás no Paraná

O recorte está acima da referência nacional pelo parâmetro escolhido, com variação recente pequena. Isso gera uma leitura diferente do comércio/SP: o nível relativo merece investigação, enquanto a mudança de três meses não aciona o gatilho.

Copel é uma companhia pública disponível para demonstrar o vínculo com o comparador. Como o grupo tem diferentes atividades e operações, o mapeamento econômico e a pertinência da sede precisam ser examinados no caso individual.

## Exemplo de análise: contexto comum de MRV e Direcional

As duas empresas compartilham a referência construção/MG, que não aciona os gatilhos iniciais. Os demonstrativos consolidados de junho de 2026 mostram dados distintos:

| Informação pública | MRV | Direcional |
|---|---:|---:|
| Caixa e equivalentes | R$ 438,3 mi | R$ 1.529,6 mi |
| Empréstimos e financiamentos CP | R$ 1.652,3 mi | R$ 309,0 mi |
| Empréstimos e financiamentos LP | R$ 6.994,1 mi | R$ 2.732,5 mi |
| Liquidez corrente | 1,89x | 4,17x |

Esses números não isolam caixa disponível para todo tipo de obrigação nem descrevem todas as condições contratuais. Eles ajudam a demonstrar por que o contexto comum não resolve a análise individual. Composição de ativos, projetos, recursos vinculados e cronograma de dívida são pontos de investigação.

## Exemplo de análise: numerador e denominador em agropecuária/RO

| Informação | Maio/2026 | Agosto/2026 |
|---|---:|---:|
| Carteira ativa | R$ 155,1 mi | R$ 132,6 mi |
| Carteira das operações inadimplentes | R$ 47,4 mi | R$ 49,8 mi |
| Taxa de inadimplência | 30,55% | 37,55% |

A alta de aproximadamente 7 p.p. combina aumento do numerador e redução do denominador. Não é possível identificar os tomadores, medir a concentração por empresa ou atribuir a causa a partir desse agregado. O recorte também deixa de ser elegível com piso de R$ 1 bilhão.

## Sensibilidade e implicação de uso

| Alta 3m | Diferença Brasil | Piso | Elegíveis | Algum gatilho | Dois gatilhos |
|---|---|---|---:|---:|---:|
| 0,5 p.p. | 1,0 p.p. | R$ 100 mi | 393 | 167 | 61 |
| 1,0 p.p. | 2,0 p.p. | R$ 100 mi | 393 | 100 | 37 |
| 0,5 p.p. | 1,0 p.p. | R$ 1 bi | 197 | 69 | 17 |
| 1,0 p.p. | 2,0 p.p. | R$ 1 bi | 197 | 34 | 10 |

Parâmetros mais exigentes selecionam menos grupos. Isso não demonstra maior precisão. A escolha operacional deve ser examinada com os usuários e, se houver objetivo preditivo futuro, com uma base apropriada de desfechos.

## Procedência e reprodução

Os saldos estão em `data/scr_agregado.csv`. Os dados individuais e links de documentos estão em `data/empresas.json`. As regras são implementadas em `web/engine.js` e os parâmetros iniciais ficam em `scripts/config.py`.

Fontes: [BCB/SCR.data](https://dadosabertos.bcb.gov.br/dataset/scr_data), [CVM/ITR](https://dados.cvm.gov.br/dataset/cia_aberta-doc-itr) e [CVM/FCA](https://dados.cvm.gov.br/dataset/cia_aberta-doc-fca). Os números acima são cálculos derivados do snapshot do case, não uma reprodução de conclusões publicadas pelas fontes.
