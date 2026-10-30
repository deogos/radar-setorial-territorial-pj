# Como o SCR vira o radar — explicação prática

Este documento descreve o código que está implementado. O exemplo foi executado sobre o CSV oficial já baixado e conferido com o snapshot do radar. Não foi necessário baixar os arquivos novamente.

## 1. O que baixamos

O Banco Central publica arquivos como `scrdata_2026.zip`. Dentro dele há CSVs mensais, como `scrdata_202608.csv`, referente a agosto de 2026. O download atual é uma requisição HTTP para um arquivo público, não uma consulta de API que retorna JSON por empresa.

Fonte efetivamente utilizada: [ZIP SCR de 2026](https://www.bcb.gov.br/pda/desig/scrdata_2026.zip).

O script `radar-setorial-territorial/scripts/download.py` salva os arquivos em cache e registra URL, data observada, tamanho e hash SHA-256 no manifesto. O hash permite verificar se duas cópias do arquivo são iguais; não garante a correção econômica do conteúdo.

```text
BCB → ZIP anual → CSVs mensais
                       ↓
             Python: filtrar e agregar
                       ↓
         scr_agregado.csv + radar.json
                       ↓
             build.py → index.html
                       ↓
       JavaScript: filtros, taxas e gatilhos
```

## 2. O que uma linha do CSV significa

O CSV usa separador `;`, codificação UTF-8 e vírgula decimal. Uma linha representa uma combinação de grupos públicos: data, UF, segmento, PF/PJ, atividade, porte, modalidade, submodalidade, origem e indexador.

**Não é uma linha por empresa, nem por contrato. Não há CNPJ.** O Banco Central já publica os dados agrupados; nosso tratamento faz uma nova agregação para o uso do radar.

Estas são duas linhas reais de agosto, com apenas algumas colunas exibidas:

| Data | UF | Cliente | Atividade | Porte | Modalidade | Indexador | Carteira ativa | Carteira inadimplente |
|---|---|---|---|---|---|---|---:|---:|
| 31/08/2026 | SP | PJ | Comércio | Grande | Arrendamento | Flutuantes | R$ 3.819.589,22 | R$ 254.048,03 |
| 31/08/2026 | SP | PJ | Comércio | Grande | Arrendamento | Prefixado | R$ 4.085.405,34 | R$ 0,00 |

As descrições de atividade e modalidade foram abreviadas apenas nesta tabela. As colunas e os textos originais estão preservados em [01_linhas_brutas_do_recorte.csv](exemplo_scr/01_linhas_brutas_do_recorte.csv).

## 3. Como tratamos em Python

O tratamento de produção está em `radar-setorial-territorial/scripts/pipeline.py`, função `scr`.

1. Abre o ZIP e lê cada CSV linha por linha, sem descompactar tudo no disco.
2. Mantém `cliente == 'PJ'`; exclui as linhas PF.
3. Reduz a data à competência: `2026-08-31` vira `2026-08`.
4. Mapeia a descrição da atividade para a seção: comércio vira `G`.
5. Padroniza o porte: `Médio` vira `medio`; `Grande` vira `grande`.
6. Converte os sete saldos monetários para centavos inteiros antes de somar: `3819589,22` vira `381958922` centavos.
7. Soma os saldos pela chave **mês × UF × seção × porte**.
8. Volta de centavos para reais e salva o resultado.

O trecho central do código de produção é:

```python
if r[ix['cliente']] != 'PJ':
    counts['pf_rows'] += 1
    continue

dt = r[ix['data_base']][:7]
uf = r[ix['uf']]
sector = by_name.get(r[ix['cnae_ocupacao']])
size = SIZES.get(r[ix['porte']])
key = (dt, uf, sector, size)
vals = [cents(r[i]) for i in money]

target = aggr[key]
for i, v in enumerate(vals):
    target[i] += v
```

Segmento, modalidade, submodalidade, origem e indexador deixam de ser filtros no radar: seus saldos são somados dentro da chave final. Por isso, as duas linhas da tabela anterior contribuem para o mesmo agregado `2026-08 / SP / G / grande`.

Os sete saldos mantidos são carteira ativa, carteira de operações inadimplentes, ativos problemáticos, carteira a vencer, a vencer até 90 dias, a vencer de 91 a 360 dias e vencido de 15 a 90 dias.

O código também confere dimensões conhecidas, valores não negativos e consistência entre saldos. A coluna `numero_de_operacoes` não é somada: ela pode conter `-1`, que indica contagem suprimida. Isso não transforma os saldos publicados naquela linha em zero. No recorte deste exemplo, 74 linhas têm contagem suprimida e mantêm seus saldos publicados.

## 4. Execução real: comércio em São Paulo

O demonstrador leu o CSV inteiro de agosto e separou comércio/SP, portes médio e grande:

| Etapa | Linhas |
|---|---:|
| CSV de agosto inteiro | 313.138 |
| PF excluídas | 182.271 |
| PJ no arquivo | 130.867 |
| PJ de comércio/SP, médio e grande | 428 |
| Dessas, porte médio | 239 |
| Dessas, porte grande | 189 |
| Resultado agregado do recorte | 2 |

As 428 linhas viraram duas linhas tratadas:

| Competência | UF | Seção | Porte | Carteira ativa | Carteira inadimplente |
|---|---|---|---|---:|---:|
| 2026-08 | SP | G | medio | R$ 52.688.759.793,28 | R$ 3.361.045.959,87 |
| 2026-08 | SP | G | grande | R$ 59.210.867.162,45 | R$ 1.638.438.637,11 |

Abra os arquivos nesta ordem no Excel:

- [01 — Linhas brutas](exemplo_scr/01_linhas_brutas_do_recorte.csv): 428 linhas, com as colunas originais.
- [02 — Linhas padronizadas](exemplo_scr/02_linhas_padronizadas_centavos.csv): as mesmas 428 linhas, com a chave final e os sete saldos em centavos.
- [03 — Agregado](exemplo_scr/03_agregado_reais.csv): duas linhas, uma por porte, com saldos em reais.
- [04 — Cálculos](exemplo_scr/04_calculos_do_radar.json): totais, referências e taxas usadas na explicação.

Os dois agregados recalculados do bruto coincidiram com os registros já incluídos no radar. A produção faz esse processo para todos os recortes, e não somente comércio/SP. No snapshot completo, foram lidas 6.276.330 linhas, mantidas 2.557.914 linhas PJ e publicados 53.100 agregados em 20 competências.

## 5. Como o agregado vira a taxa da tela

O tratamento guarda os saldos separados por porte. Quando você seleciona **Médias e grandes**, o motor `radar-setorial-territorial/web/engine.js` soma os saldos dos dois portes e calcula:

```text
Carteira ativa = 52.688.759.793,28 + 59.210.867.162,45
               = R$ 111.899.626.955,73

Carteira inadimplente = 3.361.045.959,87 + 1.638.438.637,11
                     = R$ 4.999.484.596,98

Taxa = 4.999.484.596,98 / 111.899.626.955,73 × 100
     = 4,4678295...% → 4,47% na tela
```

**Não fazemos média simples das taxas dos portes nem das linhas.** Somamos numeradores e denominadores antes da divisão.

Os demais cálculos são:

| Indicador | Cálculo | Resultado na tela |
|---|---|---:|
| Inadimplência atual | Saldo inadimplente / carteira ativa × 100 | 4,47% |
| Taxa de maio/SP | Mesmo cálculo, três meses antes | 3,83% |
| Variação em três meses | 4,4678295... − 3,8302683... | +0,64 p.p. |
| Referência do comércio no Brasil | Soma das UFs, mesmos portes e mês | 4,41% |
| Diferença para o Brasil | 4,4678295... − 4,4113523... | +0,06 p.p. |

O Brasil inclui São Paulo. Os cálculos usam a precisão disponível e arredondam para exibição no final.

Neste exemplo, a alta supera o gatilho demonstrativo de 0,5 p.p.; a diferença para o Brasil fica abaixo de 1 p.p. O piso de carteira e o histórico contínuo também são atendidos. O motor real confirmou a classificação **Deterioração recente**, com um sinal.

Agosto/SP foi recalculado diretamente do bruto neste exercício. Maio/SP e agosto/Brasil foram lidos do snapshot já tratado; não foi repetido todo o processamento nacional. O resultado foi conferido também com o motor JavaScript de produção.

## 6. Como o HTML recebe esses dados

O pipeline gera `data/scr_agregado.csv` e `data/radar.json`. O CSV é uma saída legível para análise e conferência; a aplicação usa o JSON.

O script `scripts/build.py` incorpora o JSON, o JavaScript e os estilos em `index.html`. Ao abrir o HTML, o navegador lê os dados já incluídos e calcula as taxas e os gatilhos conforme seus filtros. **Abrir ou filtrar a demo não consulta o Banco Central e não atualiza a base.** Para atualizar, é necessário executar novamente coleta, tratamento, validação e build.

## 7. Como repetir o exemplo

Já deixei as saídas prontas. O script didático está em [demonstrar_scr.py](exemplo_scr/demonstrar_scr.py). A partir da raiz do projeto, depois de baixar o ZIP oficial para o cache:

```powershell
python docs/exemplo_scr/demonstrar_scr.py --zip .cache/raw/scrdata_2026.zip --snapshot data/radar.json
```

Se levar o script para outro computador, baixe o ZIP oficial e ajuste `--zip` para o local onde o salvou. Ajuste `--snapshot` para o `data/radar.json` do pacote. O exemplo é fixo em agosto de 2026 e requer Python 3.10 ou superior. Ele não altera o radar.

O fluxo de produção completo, executado na pasta do projeto, é:

```powershell
python scripts/download.py --cache .cache/raw
python scripts/pipeline.py --cache .cache/raw --out data
python scripts/validate.py --cache .cache/raw
python scripts/build.py
```

## 8. Como explicar na entrevista

> “Usei arquivos públicos do Banco Central. Um script Python lê os CSVs mensais, filtra PJ, padroniza as dimensões e soma sete saldos por mês, UF da sede, atividade e porte. Depois, o HTML calcula as taxas a partir desses saldos. Em comércio/SP, por exemplo, 428 linhas de agosto viram dois agregados, um médio e um grande. A combinação dos portes resulta em inadimplência de 4,47%, com alta de 0,64 ponto percentual em três meses. Essa é uma informação do grupo para orientar perguntas sobre o caso individual.”

Os dados de uma companhia específica vêm da outra trilha, a CVM. Não extraímos do SCR público a dívida, o atraso ou o rating de uma empresa por CNPJ.
