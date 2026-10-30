# Plano do case: Radar Setorial-Territorial PJ

Status: plano revisado após os ajustes do candidato. Demonstração funcional local, empresas reais e arquitetura de evolução na AWS.

## 1. Objetivo e tese

Criar uma demonstração funcional que use dados públicos para contextualizar a análise de clientes PJ pela diretoria de Recuperação e Reestruturação de Crédito.

Pergunta central: **quais recortes de setor e território apresentam deterioração do crédito, e quais premissas dos casos associados merecem revisão?**

O radar apoiará a priorização de análises e a discussão de premissas de recuperação. O analista continuará responsável por avaliar a empresa, sua geração de caixa, estrutura de dívida, garantias e alternativas de negociação.

Frase para apresentar a proposta:

> O radar organiza sinais públicos do ambiente de crédito dos clientes PJ e os transforma em prioridades de investigação para a análise de recuperação e reestruturação.

O diferencial proposto é o fluxo de trabalho: selecionar um recorte, compreender sua evolução, comparar referências e obter uma ficha com evidências e perguntas para a revisão de um caso. A existência de painéis públicos semelhantes deve ser reconhecida. Não é necessário alegar ineditismo ou desconhecimento das ferramentas internas do banco.

## 2. Premissas acordadas e limites de prazo

- O enunciado formal não está acessível. Usaremos o resumo fornecido pelo candidato.
- A solução e as tecnologias são livres.
- A prioridade é equilibrar análise de crédito e demonstração funcional.
- A entrega principal será um HTML portátil e um guia extenso em Markdown.
- A estrutura de apresentação será textual, para montagem com os assets disponíveis no trabalho.
- A sessão do case terá uma hora. O material deve sustentar aprofundamento, navegação e discussão, com blocos flexíveis e sem cronograma rígido por slide.
- A demonstração usará empresas reais e informações públicas verificadas. A amostra não será apresentada como carteira de clientes do banco.
- Além da arquitetura executável do MVP, será documentada uma arquitetura de evolução na AWS.
- O visual usará variáveis de tema e componentes fáceis de adaptar ao IDS com o Copilot.
- Nenhum dado do banco ou de seus clientes é necessário para a demonstração pública.

## 3. Fonte principal e recorte

### Banco Central: SCR.data, versão 2

Fonte principal: [catálogo oficial do SCR.data](https://dadosabertos.bcb.gov.br/dataset/scr_data).

O catálogo informa divulgação mensal de agregados de crédito, com dimensões de cliente, UF, atividade econômica e porte. O núcleo usará exclusivamente PJ. O público de comparação poderá ser filtrado por porte, com destaque inicial para médios e grandes. Esse recorte é uma escolha da demo, sem representar uma definição da carteira do BBA.

A [metodologia da versão 2](https://www.bcb.gov.br/pda/desig/metodologia_versao2.pdf) estabelece que a atividade PJ aparece em seção CNAE, a UF corresponde à sede e os arquivos mensais CSV são distribuídos em ZIP anual. Também registra mudança na identificação de ativos problemáticos a partir de janeiro de 2025.

Decisões para o MVP:

- Trabalhar de janeiro de 2025 até a última competência efetivamente disponível e validada.
- Construir a base na granularidade mês × UF × seção CNAE × porte, agregando as demais dimensões sem duplicar totais e detalhes.
- Incluir os recortes existentes nas 27 UFs, distinguindo combinações sem dados de valores iguais a zero.
- Permitir a comparação com o mesmo setor e porte no Brasil, mantendo os outros filtros compatíveis.
- Escolher os exemplos da apresentação depois da extração, com critérios de relevância e disponibilidade de histórico.

Essa escolha limita o histórico inicial, mas evita atravessar a mudança de 2025 no indicador de ativos problemáticos. A última competência não será presumida a partir da data do computador.

### CVM: empresas reais e aplicação do radar

O núcleo passa a usar duas fontes obrigatórias: BCB para o contexto de crédito e CVM para identificar empresas reais. O [cadastro de companhias abertas](https://dados.cvm.gov.br/dataset/cia_aberta-cad) disponibiliza dados cadastrais, incluindo CNPJ e situação do registro. O [Formulário Cadastral](https://dados.cvm.gov.br/dataset/cia_aberta-doc-fca) oferece conteúdo estruturado, incluindo arquivos de informações gerais e endereços.

A proposta é selecionar aproximadamente 8 a 12 companhias não financeiras, conforme a qualidade dos dados, e aprofundar 2 ou 3 na apresentação. Para os exemplos aprofundados, examinar demonstrações públicas e registrar indicadores financeiros efetivamente disponíveis e comparáveis. O [ITR da CVM](https://dados.cvm.gov.br/dataset/cia_aberta-doc-itr) é uma fonte estruturada possível, complementada pelos documentos oficiais de RI quando necessário.

Regras para a associação das empresas ao radar:

- Guardar CNPJ, denominação social, data da informação e fonte de cada atributo.
- Verificar sede e atividade econômica em documentos públicos. A classificação setorial da CVM não será automaticamente tratada como seção CNAE.
- Documentar o mapeamento para o grupo de comparação, principalmente se a companhia tiver atividades diversificadas ou funcionar como holding.
- Evitar atribuir todo o grupo consolidado ao CNPJ de uma subsidiária ou confundir razão social com marca comercial.
- Tratar o porte do comparador como filtro analítico quando o porte da companhia segundo o critério do SCR não estiver confirmado.
- Não preencher dívida com o banco, atraso individual, rating interno ou exposição bancária sem uma fonte pública que efetivamente forneça a informação. Esses campos não são necessários no MVP.

As empresas serão exemplos de consulta pública. A inclusão na amostra não significa que sejam clientes do Itaú, estejam inadimplentes ou estejam em recuperação.

### IBGE: complemento após o núcleo

O IBGE será a primeira opção de ampliação, usando sua [API oficial de agregados](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3). A prova inicial será um indicador de atividade industrial para contextualizar o recorte de indústria.

Esse complemento só entrará depois que coleta, cálculos e HTML do núcleo estiverem funcionando. Antes de exibi-lo, será necessário validar tabela, variável, cobertura territorial, período e correspondência econômica. Uma série geral de atividade da UF deverá aparecer como contexto territorial quando sua cobertura não coincidir com o setor selecionado.

O núcleo será concluído com BCB e CVM. O IBGE é uma ampliação de contexto econômico, condicionada à conclusão das entregas principais.

## 4. Como o analista usará a solução

1. Selecionar período, setor, UF e porte.
2. Identificar recortes com deterioração recente e diferenças em relação à referência nacional do mesmo setor.
3. Abrir o detalhe para verificar indicadores, tendência, saldos e cobertura dos dados.
4. Selecionar uma empresa real da amostra pública e conferir seu enquadramento no grupo de comparação.
5. Gerar uma ficha de contexto com evidências, ressalvas e perguntas para a análise do caso.
6. Exportar a ficha para apoiar uma discussão ou registro de análise.

Exemplos de perguntas produzidas pela ficha:

- A projeção de caixa do cliente considera a piora observada no seu ambiente de crédito?
- Os vencimentos do cliente dependem de renovação de linhas? Qual evidência interna confirma essa dependência?
- A deterioração aparece também na referência nacional do setor ou está mais concentrada na UF?
- A situação do cliente diverge de seu grupo de comparação? Quais dados internos ajudam a explicar a diferença?

O radar pode sugerir verificação de fluxo de caixa, vencimentos, concentração de receitas e premissas de refinanciamento. Uma definição de carência, desconto, garantia ou prazo de renegociação exige análise individual adicional.

## 5. Indicadores e regras de interpretação

| Indicador | Construção prevista | Utilidade |
|---|---|---|
| Taxa de inadimplência | Soma de `carteira_inadimplencia` dividida pela soma de `carteira_ativa` | Medir o nível de deterioração do recorte |
| Variação em três meses | Taxa atual menos a taxa de três meses antes, em pontos percentuais | Mostrar direção e intensidade recente |
| Diferença para a referência | Taxa do setor na UF menos a taxa do mesmo setor no Brasil, com porte e filtros compatíveis | Contextualizar o componente territorial |
| Proporção de ativos problemáticos | Soma de `ativo_problematico` dividida pela soma de `carteira_ativa` | Complementar a leitura de deterioração |
| Vencimentos em até 360 dias | Soma dos valores a vencer até 90 dias e de 91 a 360 dias, dividida pela carteira a vencer | Abrir a discussão sobre perfil de vencimentos do grupo |
| Saldo de crédito e sua evolução | Saldo agregado por competência e variações em janelas disponíveis | Dar escala e ajudar a interpretar movimentos das taxas |

As razões serão calculadas após agregar numeradores e denominadores. Não usaremos média simples das taxas de cada linha.

O campo de carteira inadimplente abrange o saldo das operações enquadradas no conceito de inadimplência. O campo de parcelas vencidas acima de 90 dias tem outro significado. A implementação deverá preservar essa distinção.

Ativos problemáticos e inadimplência têm sobreposição. Não somaremos as duas medidas para criar um volume de deterioração.

O primeiro MVP usará regras legíveis para sinalizar atenção, acompanhadas de seus motivos. Os parâmetros ficarão em configuração, com identificação explícita de que são hipóteses demonstrativas. Sua definição final ocorrerá após examinar a distribuição dos dados. Faremos uma comparação simples entre parâmetros mais e menos sensíveis para mostrar como a seleção muda.

Não construiremos uma probabilidade de default ou uma escala de 0 a 100 sem base de resultados individuais para desenvolvimento e validação.

## 6. Empresas reais e aplicação na análise

A demonstração usará uma amostra de companhias reais, com identificação e enquadramento documentados. Cada empresa será associada ao grupo público de comparação compatível com a informação verificada.

A tela permitirá localizar empresas da amostra associadas aos recortes sinalizados. A ordenação considerará os sinais do contexto, acompanhados dos motivos. A exposição do banco não será estimada. A interface identificará dados próprios da companhia, dados do grupo de comparação e interpretações analíticas.

O indicador do grupo não será apresentado como indicador financeiro da empresa. Nos exemplos aprofundados, os demonstrativos públicos poderão ajudar a discutir como o contexto dialoga com a situação observável da companhia. Qualquer leitura financeira identificará período, unidade monetária, base individual ou consolidada e documento utilizado. Uma futura integração com carteira interna exigiria os dados autorizados dessa carteira.

O porte do tomador, a modalidade e a abrangência econômica do cliente afetam a comparação. Para empresas com operação em várias UFs, a sede é uma referência parcial. Como evolução, poderíamos ponderar indicadores pelas receitas ou operações em cada localidade, caso esses dados internos estivessem disponíveis.

## 7. Escopo da interface

O HTML terá três visões principais:

1. **Panorama:** filtros, matriz setor × UF e lista ordenável de recortes, com nível de deterioração e mudança recente.
2. **Detalhe do recorte:** série histórica, comparação nacional, indicadores explicados, escala da carteira e informações de cobertura.
3. **Consulta por empresa:** amostra de empresas reais e ficha exportável com perfil público, contexto do grupo, evidências e perguntas de revisão.

Haverá acesso visível à metodologia e à procedência: fonte, competência, data de coleta, abrangência e definição dos cálculos.

A interface deverá permitir impressão ou exportação de uma ficha e abrir corretamente em navegador sem conexão. Os gráficos, estilos e dados necessários ficarão no próprio pacote, sem depender de CDN.

## 8. Arquitetura e reprodução

```text
Fonte pública oficial
    |
    v
Coleta em Python com registro de origem e data
    |
    v
Arquivos brutos e metadados em cache local
    |
    v
Validação de esquema, tipos, períodos e dimensões
    |
    v
Filtro PJ, agregação e cálculo dos indicadores
    |
    v
CSV/JSON tratados + relatório de qualidade
    |
    v
Construção de HTML portátil com dados incorporados
    |
    v
Uso local e publicação do pacote público no GitHub
```

Tecnologias previstas: Python para coleta e tratamento, CSV/JSON para intercâmbio, HTML/CSS/JavaScript para consulta. As dependências exatas serão fixadas após conferir o ambiente.

O acesso ao SCR.data será descrito corretamente como download de arquivos públicos. A API será usada onde a fonte oferecer esse mecanismo. O navegador consultará o snapshot tratado, preservando a demonstração quando a fonte estiver indisponível.

A atualização do case será reproduzível por comandos documentados. O agendamento automático ficará como evolução, salvo se houver tempo após a validação das entregas obrigatórias.

### Arquitetura de evolução na AWS

A proposta será documentada em [ARQUITETURA_AWS.md](ARQUITETURA_AWS.md), com diagrama, componentes, justificativas e caminho de migração do código local.

Fluxo proposto: EventBridge Scheduler agenda uma execução no Step Functions; tarefas Python em ECS/Fargate coletam os arquivos; S3 preserva os dados brutos; Glue prepara as camadas tratada e analítica em Parquet; Glue Data Catalog e Athena oferecem acesso SQL; a aplicação consome resultados pré-calculados por uma API autenticada. O armazenamento da interface e dos artefatos públicos poderá usar S3 e CloudFront.

O desenho incluirá verificação de qualidade antes da publicação, histórico de versões, reprocessamento, tratamento de falhas, IAM, criptografia, logs e controles de consulta. A integração futura com dados internos ficará em ambiente restrito, sem publicação no GitHub.

Trata-se de uma proposta de evolução tecnológica, sem afirmar que descreve a arquitetura interna do Itaú. A implantação de recursos AWS não faz parte desta etapa de planejamento.

## 9. Entregas

| Arquivo ou conjunto | Conteúdo |
|---|---|
| `radar.html` | Demo portátil com dados públicos reais e consulta a empresas reais verificadas |
| `GUIA_COMPLETO.md` | Problema, uso, fontes, dicionário, fórmulas, decisões, arquitetura, comandos, limitações e instruções para reconstrução com Copilot |
| `APRESENTACAO_ROTEIRO.md` | Blocos flexíveis para a sessão de uma hora, argumentos, evidências, percursos de demonstração e aprofundamentos |
| `ARQUITETURA_AWS.md` | Proposta de evolução na AWS, diagrama, justificativas, operação e migração do MVP |
| Scripts e configuração | Coleta, tratamento e geração do HTML de maneira reproduzível |
| Dados tratados | Snapshot compacto utilizado pela demo e sua procedência |
| Relatório de qualidade | Competências, cobertura, verificações e limitações encontradas |
| README do repositório | Como abrir, atualizar e entender o projeto |

Arquivos brutos volumosos ficarão no cache local, fora do versionamento. O repositório terá instruções e referências suficientes para sua obtenção. A atribuição da fonte e as condições de uso dos dados serão verificadas no preparo da publicação.

O guia extenso precisará explicar a lógica com clareza suficiente para reconstruir o case no trabalho, incluindo um comando ou prompt de reconstrução e os pontos onde adaptar o tema ao IDS.

## 10. Estrutura aberta da apresentação

Preparar material modular para uma sessão de uma hora. A sequência será ajustada aos achados e ao formato da conversa. Os itens abaixo são blocos de conteúdo, que podem ocupar quantos slides ou momentos de navegação forem úteis. Não há limite fixo de oito slides nem duração obrigatória por bloco.

| Bloco | Objetivo | Material possível |
|---|---|---|
| Problema e rotina da área | Explicar o espaço de decisão que o radar apoia | Perguntas de análise e fluxo de trabalho proposto |
| Fontes e construção | Mostrar domínio da procedência e do tratamento | BCB, CVM, granularidade, indicadores e verificações |
| Investigação dos dados | Sustentar conclusões com evidências | Achados, comparações, exceções e sensibilidade das regras |
| Demonstração e empresas reais | Explorar o produto e sua aplicação | Panorama, detalhe, consulta por empresa e ficha |
| Discussão de crédito | Conectar sinais a premissas e verificações | Dois ou três exemplos reais aprofundados, com dados públicos |
| Engenharia e AWS | Explicar como a solução pode operar e evoluir | Arquitetura do MVP, arquitetura AWS e decisões de implementação |
| Implantação e avaliação | Propor um piloto com critérios de sucesso | Usuários, atualização, métricas de utilidade e próximos passos |
| Debate e aprofundamento | Responder às perguntas conforme surgirem | Apêndice técnico, fórmulas, limitações e alternativas |

Os títulos dos slides de achados serão reescritos com base nas conclusões efetivamente sustentadas pelos dados. Não anteciparemos uma conclusão empírica.

O roteiro fornecerá percursos de demonstração e explicações de apoio, preservando liberdade para adaptar a ordem e dedicar mais tempo aos pontos levantados pela banca.

## 11. Perguntas que o candidato precisa conseguir defender

**Por que criar isso se o Banco Central já tem um painel?**

O case aproveita a fonte pública e propõe uma aplicação no fluxo da área: vínculo com o enquadramento do cliente, comparação consistente e ficha de investigação. O ganho precisa ser demonstrado pelo uso.

**Como a ferramenta ajuda um caso já em recuperação?**

Ela permite confrontar premissas de melhora, disponibilidade de refinanciamento e comportamento esperado do grupo com evidências externas. Isso orienta perguntas e revisões, sem dispensar a análise individual.

**Uma UF em deterioração prova que a empresa está pior?**

Não. O radar descreve o grupo. A resposta sobre a empresa depende de seus dados e de sua exposição econômica efetiva.

**Qual retorno financeiro a solução gera?**

Ainda não há retorno medido. O piloto poderá medir tempo de preparação da análise, utilidade das fichas e proporção de sinalizações consideradas relevantes pelos analistas. A relação com recuperação financeira exigiria acompanhamento e avaliação próprios.

**Como validar os alertas?**

Primeiro validar os cálculos e a sensibilidade dos parâmetros. Depois, revisar amostras com especialistas. Se houver acesso futuro a resultados internos, testar a associação com deterioração posterior usando somente informações disponíveis em cada data e uma separação temporal adequada.

**Crédito em queda significa aumento de risco?**

Não necessariamente. Pode refletir amortização, menor demanda, migração de financiamento ou mudança da composição do grupo. Saldo, numerador e denominador precisam ser examinados juntos.

## 12. Sequência de execução e critérios de corte

1. **Validar a fonte:** obter os arquivos, conferir esquema, volume e competências. Inspecionar algumas linhas e a lógica das dimensões antes de desenhar o painel.
2. **Construir a base:** filtrar PJ, tratar tipos, agregar, calcular indicadores e conferir alguns totais manualmente.
3. **Analisar:** selecionar achados com materialidade e histórico suficiente. Estabelecer as regras demonstrativas e testar sua sensibilidade.
4. **Montar a demo:** criar as visões, verificar o cadastro das empresas reais, associar os grupos de comparação e gerar as fichas.
5. **Documentar:** registrar comandos, dados, fórmulas, premissas, arquitetura AWS e blocos de apresentação. Aprofundar os exemplos reais selecionados com documentos públicos.
6. **Validar o pacote:** abrir offline, testar filtros e exportação, conferir números e apresentação visual.
7. **Publicar no GitHub:** preparar o repositório e disponibilizar os arquivos. A URL de apresentação só será informada depois de verificar o acesso. GitHub Pages será uma conveniência adicional caso a conta e as políticas permitam.
8. **Ampliar:** incluir o complemento IBGE após a conclusão do núcleo validado.

Se a fonte estiver temporariamente indisponível, tentar outro acesso oficial ou uma competência oficial anterior, registrando a defasagem. Dados públicos fictícios não substituirão a extração. Se não for possível obter um snapshot oficial, essa dependência será informada antes de afirmar que a demo usa dados reais.

## 13. Critérios de conclusão

- HTML abre offline e todos os filtros principais funcionam.
- Fontes e competências ficam visíveis.
- Indicadores exibidos correspondem ao snapshot tratado.
- Cálculos respeitam denominadores e filtros de comparação.
- Ausência de dados não vira zero ou classificação favorável.
- Recortes com baixa materialidade ou histórico insuficiente são identificados.
- Empresas reais têm identificação, enquadramento e fontes verificadas.
- Dados da companhia e indicadores do grupo de comparação têm identificação distinta.
- A amostra não é apresentada como carteira do banco e não contém exposição bancária inventada.
- A ficha liga evidências a verificações concretas do caso.
- O guia permite reproduzir a coleta, o tratamento e o HTML.
- A apresentação tem uma narrativa apoiada nos achados reais.
- O material permite aprofundamento e discussão ao longo da sessão de uma hora.
- A arquitetura AWS explica responsabilidades, operação e migração a partir do MVP.
- Não há promessa de previsão, ganho financeiro ou decisão automática sem evidência.
- Acesso ao pacote no GitHub é verificado, ou a pendência de publicação é explicitada.

## 14. Estado das verificações no planejamento

A documentação oficial do SCR.data, da API de agregados do IBGE, do cadastro e de formulários da CVM foi consultada. As funções principais dos componentes AWS propostos foram conferidas em documentação oficial. A extração dos arquivos brutos, a conferência do esquema e a disponibilidade dos recortes ainda serão validadas na execução.

O terminal local apresentou falha de resolução dos domínios na tentativa inicial de acesso direto. A documentação estava acessível pela ferramenta de pesquisa. O primeiro passo de implementação deve resolver o acesso ao download oficial, sem presumir que a coleta já está concluída.
