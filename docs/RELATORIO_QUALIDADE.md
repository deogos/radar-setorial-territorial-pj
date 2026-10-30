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

Revisão de interface em 30/10/2026. Testes executados no Microsoft Edge headless, em página local. Cada cenário percorreu as quatro visões e verificou o botão de abrir/fechar o menu, seus estados de acessibilidade, a ausência da seção AWS e o rodapé lateral simplificado.

| Visão final | Largura interna | Verificações | Resultado |
|---|---:|---:|---|
| overview | 1576 px | 13 | Passou |
| overview | 496 px | 13 | Passou |
| companies | 1576 px | 13 | Passou |

Capturas limpas do panorama e da consulta por empresa foram inspecionadas. Os testes da versão inicial também exercitaram filtros, regras, busca e exportações; esses cálculos e funções não foram alterados nesta revisão. O HTML e as fontes foram conferidos para confirmar a remoção da arquitetura AWS da interface. A documentação AWS foi preservada para apoio à apresentação.

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
