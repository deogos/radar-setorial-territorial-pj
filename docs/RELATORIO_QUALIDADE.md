# Relatório de qualidade e validação

Snapshot ampliado e revisão final em 30/10/2026, horário de São Paulo.

## Dados e reconciliação

- 18 verificações atuais de integridade e cobertura aprovadas, registradas em `data/validacao.json`.
- Os 53.100 registros e o controle de qualidade do SCR são idênticos aos do commit `02d20be`. A ampliação reutilizou o agregado, sem reprocessar os ZIPs SCR.
- As dez reconciliações Decimal da etapa original foram preservadas em `data/auditoria_scr_original.json`: sete saldos por recorte, diferença máxima de R$ 0,00. Essas auditorias não foram repetidas nesta ampliação.
- A revisão independente reconciliou os 660 CNPJs com os registros ativos de SEDE no CAD: zero faltantes, extras ou duplicados.
- Todas as 6.374 contas financeiras selecionadas foram conferidas contra os CSVs oficiais por CNPJ, referência, versão, escopo, conta e período. Nenhuma divergência de valor em BRL, rótulo ou escala; metadados e seleção do FCA também reconciliados.
- Cobertura: 652 com FCA; 592 com contas para ficha padronizada (a disponibilidade de cada conta pode variar), 48 com demonstração especializada e 20 sem contas utilizáveis. Há 12 enquadramentos editoriais, 491 propostas a validar e 157 sem associação setorial.

| Verificação atual | Resultado |
|---|---|
| Chave mês/UF/seção/porte sem duplicação | Passou |
| Esquema com sete saldos monetários | Passou |
| Saldos monetários não negativos | Passou |
| Inadimplência e AP não excedem carteira | Passou |
| Vencimentos de curto prazo não excedem carteira a vencer | Passou |
| Todas as competências têm as 27 UFs | Passou |
| CNPJs distintos no universo de companhias | Passou |
| Quantidade de companhias confere com cobertura declarada | Passou |
| Universo de CNPJs coincide com CAD ativo com SEDE | Passou |
| UF e seção válidas ou ausência explícita | Passou |
| Mapeamentos possuem procedência e revisão explícitas | Passou |
| Estados e escopos financeiros explícitos | Passou |
| Ausência financeira não é preenchida por zero | Passou |
| Datas de recebimento compatíveis com demonstrações disponíveis | Passou |
| Companhias possuem questões de análise inclusive sem enquadramento | Passou |
| Contas preservam valor finito, rótulo e escala original | Passou |
| Contas especializadas não recebem classificação financeira padronizada | Passou |
| Contagens de cobertura CVM reconciliadas com as companhias | Passou |

## Código e integração

- Python: 16 testes aprovados, cobrindo universo, seleção de documentos, escopos, períodos fiscais, ausência e semântica de contas.
- JavaScript: 13 subtestes TAP aprovados: 11 do contexto de IA e dois arquivos de teste, que executam respectivamente sete verificações do diretório e dez do perfil.
- Revisão de integração: 1.320 fichas renderizadas (660 de tela e 660 exportáveis) e 660 contextos estruturados, sem exceções, valores inválidos ou ação de abrir grupo sem setor.
- Dois achados de procedência no contexto de IA foram corrigidos: proposta de enquadramento referencia o cadastro que a originou; rótulo curto editorial não é apresentado como fato publicado pela CVM. Ambos possuem regressões automatizadas.

## Interface e navegador

Testes no Microsoft Edge headless, em página local, com 19 verificações por cenário: paginação, busca por CNPJ, filtros de cobertura, ficha especializada, ausência de demonstrativo ou de enquadramento, preservação da competência, exportação HTML/JSON, menu, quatro visões e transbordamento horizontal.

| Cenário | Largura interna | Verificações | Resultado |
|---|---:|---:|---|
| Consulta de empresas e quatro visões | 1576 px | 19 | Passou |
| Consulta de empresas e quatro visões | 496 px | 19 | Passou |

Relatórios atuais: `ui-companies-1576-qa.json` e `ui-companies-496-qa.json`. Os arquivos `ui-overview-*.json` são evidência histórica da revisão anterior e não entram na contagem acima. Capturas limpas do panorama e da consulta por empresa acompanham o pacote.

## Limites da validação

- A reconciliação não é auditoria externa das fontes oficiais e não comprova efeito econômico, capacidade preditiva ou qualidade de crédito individual.
- Cadastro disponível não significa análise de crédito ou enquadramento validados. Propostas automáticas precisam de revisão; UF da sede e seção ampla não representam toda a operação da companhia.
- Demonstrações especializadas não usam a liquidez genérica; contas ausentes permanecem ausentes. Escopos e períodos distintos exigem cuidado na comparação.
- Consultar uma competência histórica do SCR não reconstrói as informações individuais conhecidas naquela data.
- A IA interna não está conectada e nenhum parecer foi gerado; AWS permanece uma proposta documentada.
- Homologação no ambiente corporativo, componentes IDS e desempenho em escala dependem de um piloto.

## Repetir as verificações

```powershell
python scripts/validate.py --cache .cache/raw --skip-scr-audit --check-only
python -m unittest discover -s tests -q
node --test tests/test_ai_context.js tests/test_company_directory.js tests/test_company_profile.js
```

Para refazer também a auditoria Decimal SCR, remova `--skip-scr-audit` e disponha dos ZIPs oficiais no cache. `--check-only` evita substituir o relatório incluído. Sem cache, o validador confere o snapshot tratado. As verificações do navegador foram executadas por um harness local de QA, fora do produto.
