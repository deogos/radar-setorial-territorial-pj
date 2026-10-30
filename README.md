# Radar Setorial-Territorial PJ

<!-- PUBLICATION -->
Repositório temporariamente privado. O GitHub Pages está despublicado. Abra `index.html` localmente para usar a demo.

Consulta demonstrativa de contexto de crédito para apoiar a revisão de casos PJ em recuperação e reestruturação. Usa dados públicos do Banco Central e cadastro das 660 companhias ativas no snapshot da CVM, com cobertura financeira e enquadramento identificados.

O radar identifica mudanças em grupos econômicos e territoriais, compara referências e gera perguntas para a análise individual. As companhias consultáveis não constituem uma carteira do banco. O projeto é independente e não é um produto oficial do Itaú.

## Abrir agora

Baixe o repositório e abra **index.html** em Edge, Chrome ou Firefox. O arquivo incorpora dados, estilos e lógica e funciona offline. A visualização do código HTML dentro do GitHub não executa a aplicação.

No GitHub, use **Code → Download ZIP**, extraia o pacote e abra o HTML. Se o GitHub Pages estiver habilitado, o endereço publicado também executa a aplicação.

## O que está implementado

- Matriz de 27 UFs e 22 categorias de atividade publicadas: 21 seções CNAE e “Não informados”.
- 20 competências, de janeiro de 2025 a agosto de 2026.
- Filtros por porte do grupo de comparação.
- Gatilhos demonstrativos por variação em três meses e diferença para o Brasil.
- Piso de materialidade ajustável, histórico contínuo e classificação explicada.
- Detalhe com série histórica, numerador e denominador.
- Consulta às 660 companhias ativas, com busca, paginação, filtros de cobertura, demonstrativos consolidados ou individuais identificados e estados explícitos de ausência.
- Exportação de CSV e ficha HTML, além de controle para abrir e fechar o menu lateral.
- Espaço de integração futura com IA interna, com cópia de ficha e exportação JSON; nenhum modelo é chamado.
- Metodologia dentro da aplicação e arquitetura AWS em documento separado para a apresentação.

O processamento examinou 6.276.330 linhas brutas, filtrou 2.557.914 linhas PJ e publicou 53.100 agregados. Os detalhes da execução e das verificações estão no relatório de qualidade.

## Cobertura das companhias

| Situação no snapshot | Quantidade |
|---|---:|
| Cadastros ativos distintos | 660 |
| Com FCA | 652 |
| Contas utilizáveis para ficha padronizada | 592 |
| Demonstração especializada | 48 |
| Sem contas utilizáveis nos períodos baixados | 20 |
| Enquadramentos editoriais do case | 12 |
| Propostas automáticas a validar | 491 |
| Sem associação setorial definida | 157 |

Ter cadastro disponível não significa ter uma análise individual de crédito validada. Propostas e ausências ficam identificadas. Os 12 exemplos originais continuam disponíveis pela busca.

## Conteúdo do pacote

| Caminho | Uso |
|---|---|
| `index.html` | Aplicação pronta, sem instalação |
| `GUIA_COMPLETO.md` | Lógica de negócio, fórmulas, resultados, reprodução e defesa |
| `APRESENTACAO_ROTEIRO.md` | Blocos flexíveis para a sessão de uma hora |
| `STORYTELLING_GESTOR.md` | Abertura, narrativa e percurso de demonstração para o gestor |
| `AVALIACAO_COMO_GESTOR.md` | Crítica independente, riscos e prioridades para preparar a defesa |
| `INTEGRACAO_IA.md` | Contrato da ficha, integração futura e revisão do parecer |
| `ARQUITETURA_AWS.md` | Proposta de evolução, diagrama e justificativas |
| `RECONSTRUIR_COM_COPILOT.md` | Instruções para reconstrução e adaptação ao IDS |
| `docs/ACHADOS.md` | Resultados numéricos e leituras para a apresentação |
| `docs/RELATORIO_QUALIDADE.md` | Verificações e limites da validação |
| `scripts/` | Coleta, tratamento, validação e build |
| `web/` | HTML, CSS, motor de cálculo e interface |
| `data/` | Snapshot tratado, empresas, manifesto e verificações |

## Reconstruir o HTML com os dados incluídos

Requer Python 3.10 ou superior, sem bibliotecas externas. Execute na pasta do projeto:

```powershell
python scripts/build.py
```

## Reproduzir coleta e tratamento

Os arquivos originais somam aproximadamente 336 MB compactados e são lidos em streaming. Garanta espaço para o cache e acesso aos domínios oficiais.

```powershell
python scripts/download.py --cache .cache/raw
python scripts/pipeline.py --cache .cache/raw --out data
python scripts/validate.py --cache .cache/raw
python scripts/build.py
```

Para obter uma versão nova das fontes durante 2026:

```powershell
python scripts/download.py --cache .cache/raw --refresh
```

Depois, repita pipeline, validação e build. O case está fixado nos arquivos de 2025/2026. A virada de ano exige atualizar os nomes de arquivos CVM e a escolha de exercícios nos scripts. Arquivos oficiais podem sofrer revisão, portanto uma nova coleta não garante os mesmos resultados do snapshot incluído.

Para atualizar apenas a CVM, preservando o agregado SCR existente:

```powershell
python scripts/pipeline.py --cache .cache/raw --out data --reuse-scr data/radar.json
python scripts/validate.py --cache .cache/raw --skip-scr-audit
python scripts/build.py
```

Para verificar o snapshot sem baixar os brutos:

```powershell
python scripts/validate.py
```

A auditoria Decimal diretamente contra o bruto só ocorre quando `--cache` é informado.

## Fontes e condições de uso

- [BCB / SCR.data](https://dadosabertos.bcb.gov.br/dataset/scr_data) e [metodologia v2](https://www.bcb.gov.br/pda/desig/metodologia_versao2.pdf).
- [CVM / Cadastro](https://dados.cvm.gov.br/dataset/cia_aberta-cad), [FCA](https://dados.cvm.gov.br/dataset/cia_aberta-doc-fca), [ITR](https://dados.cvm.gov.br/dataset/cia_aberta-doc-itr) e [DFP](https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp).

Código sob licença MIT. Dados e bases derivadas mantêm atribuição às fontes e são disponibilizados conforme ODbL, como descrito em `LICENSE-DADOS.md`. O manifesto contém URLs e hashes dos arquivos oficiais utilizados.

## Limites essenciais

O SCR.data público descreve grupos. A UF representa a sede da PJ. O enquadramento é editorial, proposto automaticamente a partir do setor CVM, ou ausente. Ele pode diferir do CNAE cadastral da holding e propostas precisam de revisão. O porte é o filtro do comparador, sem atribuição automática à empresa.

Os demonstrativos CVM têm datas próprias e não entram nos gatilhos. A consulta de competências antigas não reconstrói as informações individuais conhecidas naquele momento. Não há PD estimada, rating, decisão automática ou ganho de recuperação validado. A arquitetura AWS é uma proposta documentada, sem implantação em nuvem nesta entrega.
