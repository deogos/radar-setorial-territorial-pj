# Relatório de qualidade e validação

Snapshot do case preparado em 29/10/2026, horário de São Paulo.

## Dados e reconciliação

- 19 verificações de integridade e auditoria concluídas com sucesso.
- 10 reconciliações independentes com o bruto, usando Decimal.
- Maior diferença entre saldos auditados: R$ 0.00.
- Verificações de limites dos saldos executadas sobre todas as linhas PJ processadas.
- Saldo de operações suprimidas não foi somado; a contagem não é usada pelo produto.

| Verificação | Resultado |
|---|---|
| Chave mês/UF/seção/porte sem duplicação | Passou |
| Esquema com sete saldos monetários | Passou |
| Saldos monetários não negativos | Passou |
| Inadimplência e AP não excedem carteira | Passou |
| Vencimentos de curto prazo não excedem carteira a vencer | Passou |
| Todas as competências têm as 27 UFs | Passou |
| Doze CNPJs distintos na amostra | Passou |
| Empresas com enquadramento rastreável | Passou |
| Datas de recebimento compatíveis com demonstrações | Passou |
| Auditoria Decimal do bruto: 2026-05 / BR / ALL, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-05 / MG / F, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-05 / SC / C, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-05 / RS / G, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-05 / SP / H, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-08 / BR / ALL, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-08 / MG / F, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-08 / SC / C, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-08 / RS / G, sete saldos | Passou |
| Auditoria Decimal do bruto: 2026-08 / SP / H, sete saldos | Passou |

## Interface e navegador

Testes executados no Microsoft Edge em modo headless, sobre a aplicação local. Cada cenário percorreu as interações e terminou na visão indicada. As dimensões abaixo são as larguras internas efetivamente informadas pelo navegador.

| Visão final | Largura interna | Verificações | Resultado |
|---|---:|---:|---|
| companies | 496 px | 24 | Passou |
| companies | 1576 px | 24 | Passou |
| detail | 1342 px | 24 | Passou |
| overview | 496 px | 24 | Passou |
| overview | 1576 px | 24 | Passou |

Os cenários exercitaram a matriz, o detalhe, troca de competência, filtros de porte, estado sem histórico, edição e restauração de parâmetros, busca de empresas, exportação de ficha e CSV, metodologia, arquitetura, modo apresentação, conteúdo válido e ausência de transbordamento horizontal.

As exportações foram interceptadas em memória no teste para verificar conteúdo sem gravar arquivos na pasta de downloads. Capturas representativas foram inspecionadas visualmente. A primeira abertura também foi verificada diretamente por arquivo local, sem servidor.

## Limites da validação

- A reconciliação Decimal examina dez recortes e sete saldos; não é auditoria externa das bases oficiais.
- As verificações de integridade não comprovam causa econômica, valor preditivo ou qualidade de crédito individual.
- A amostra de empresas exige análise de pertinência do mapeamento quando usada em outro contexto.
- A homologação no ambiente de trabalho e com componentes IDS ainda depende desse ambiente.
- Nenhum recurso AWS foi provisionado ou testado em conta de nuvem.
- O relatório não comprova desempenho em todos os navegadores ou escalas de uso.

## Como repetir as verificações de dados

```powershell
python scripts/validate.py --cache .cache/raw
```

Sem `--cache`, o validador confere apenas o snapshot tratado. Os resultados completos estão em `data/validacao.json`, `data/qualidade.json` e nos relatórios JSON de navegador desta pasta.
