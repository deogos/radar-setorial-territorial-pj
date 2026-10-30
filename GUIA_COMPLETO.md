# Guia completo do case — Radar Setorial-Territorial PJ

## 1. O que você está apresentando

Uma solução de Analytics que transforma dados públicos de crédito em contexto organizado para revisar casos de clientes PJ. O produto permite selecionar setor, UF e porte, acompanhar a deterioração do grupo, comparar referências e gerar uma ficha com perguntas para a análise individual.

A tese para defender é:

> A área já analisa o cliente individualmente. O radar acrescenta uma leitura externa padronizada, com origem e cálculos verificáveis, para investigar premissas e organizar revisões.

O projeto não depende de alegar que a ideia é inédita. O Banco Central possui um painel próprio do SCR.data. O espaço do case é uma aplicação no fluxo de trabalho da área: enquadramento de uma empresa real, comparação consistente, evidências e perguntas para o caso.

O usuário principal é o analista que prepara ou revisa uma análise de recuperação e reestruturação. Um gestor também pode usar a visão agregada para discutir onde concentrar investigação. A interface pública não conhece exposição do banco, rating interno, garantias, atraso individual ou condições de uma negociação.

## 2. Relação com recuperação e reestruturação

Na revisão de um caso, é útil confrontar a história apresentada pela empresa com o comportamento observável do seu ambiente de crédito. A deterioração do setor pode levar o analista a verificar se a recuperação projetada da geração de caixa continua plausível. Uma diferença territorial relevante pode motivar perguntas sobre concentração de receitas e operações. A estrutura de vencimentos do grupo pode abrir a discussão sobre dependência de renovação de linhas.

Esses usos exigem um passo adicional: olhar os dados do cliente. Um aumento da inadimplência agregada não explica sozinho a causa da dificuldade, a viabilidade do plano ou o melhor caminho de recuperação. O radar organiza o ponto de partida dessa investigação.

Exemplos de ligação entre evidência e ação:

| Evidência pública | Hipótese de investigação | Verificação no caso individual |
|---|---|---|
| Inadimplência do grupo cresce em três meses | O cenário de crédito pode ter mudado | Atualizar premissas de caixa e evidências de renovação de linhas |
| Setor na UF supera a referência nacional | Pode existir exposição territorial relevante | Conferir distribuição das operações e receitas da companhia |
| Ativos problemáticos elevados | A inadimplência isolada não resume a deterioração do grupo | Investigar reestruturações e fragilidades individuais com fontes adequadas |
| Parcela importante da carteira vence em até 360 dias | O perfil do grupo justifica discutir refinanciamento | Abrir o cronograma real da dívida e verificar condições de rolagem |
| Taxa sobe enquanto a carteira cai | O denominador pode explicar parte da mudança | Comparar numerador, denominador e composição antes de interpretar |

Uma recomendação de carência, desconto, prazo ou execução de garantia depende de análise adicional. Essa fronteira de uso deve aparecer naturalmente na sua defesa.

## 3. O que foi entregue

O arquivo `index.html` é a aplicação pronta. Ele contém estilos, JavaScript e o snapshot tratado. Não precisa de servidor, instalação, internet ou API disponível durante a demonstração.

O código-fonte editável fica em `web/`. O motor de cálculo está separado da interface em `web/engine.js`. Os scripts em `scripts/` reproduzem a coleta, o tratamento, a validação e a geração do HTML. Os dados e manifestos ficam em `data/`.

Os outros materiais explicam os achados, a apresentação, a evolução AWS e a reconstrução com Copilot. Para uma transferência rápida ao trabalho, leve o ZIP completo. Se só conseguir levar um arquivo executável, leve o HTML. Para entender ou reconstruir o projeto, leve este guia e os scripts.

## 4. Fontes públicas e por que foram escolhidas

### Banco Central — contexto de crédito

O [SCR.data](https://dadosabertos.bcb.gov.br/dataset/scr_data) divulga agregados mensais de crédito e oferece dimensões compatíveis com a proposta. O case usa apenas PJ, agrega as linhas por mês, UF, seção econômica e porte e mantém os saldos necessários para recalcular indicadores.

A [metodologia v2](https://www.bcb.gov.br/pda/desig/metodologia_versao2.pdf) define a UF da PJ pela sede, a atividade no nível de seção CNAE e os conceitos de inadimplência e ativos problemáticos. Os arquivos mensais estão em ZIP anual. O recorte começa em 2025 para evitar atravessar a mudança de identificação dos ativos problemáticos.

O SCR.data público não fornece o histórico individual de uma empresa por CNPJ. Portanto, não fazemos um cruzamento de operações individuais do SCR com as companhias. Associamos cada empresa a um grupo de comparação.

### CVM — empresas reais

O [cadastro de companhias abertas](https://dados.cvm.gov.br/dataset/cia_aberta-cad) fornece a identificação corporativa e o cadastro da sede. O [FCA](https://dados.cvm.gov.br/dataset/cia_aberta-doc-fca) oferece descrição da atividade. Os conjuntos [ITR](https://dados.cvm.gov.br/dataset/cia_aberta-doc-itr) e [DFP](https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp) fornecem demonstrações estruturadas.

O cadastro consultável contém as 660 companhias ativas distintas do arquivo CVM. As 12 companhias originais permanecem como exemplos com enquadramento editorial: Tupy, Marcopolo, WEG, Romi, Lojas Renner, Magazine Luiza, Rumo, Tegma, MRV, Direcional, Energisa e Copel. Nas demais, 491 associações são propostas automáticas a validar e 157 permanecem sem seção definida. A lista não representa carteira do banco nem análise individual validada.

O setor da CVM e a seção CNAE não são intercambiáveis automaticamente. Usamos a atividade declarada para documentar um enquadramento econômico editorial. Holdings recebem uma ressalva específica. Uma implantação interna deve usar o cadastro autorizado e o enquadramento validado pela organização.

## 5. Snapshot efetivamente utilizado

| Item | Resultado |
|---|---|
| Período SCR | Janeiro de 2025 a agosto de 2026 |
| Competências | 20 |
| Linhas brutas lidas | 6.276.330 |
| Linhas PJ após filtro | 2.557.914 |
| Registros agregados | 53.100 |
| UFs | 27 |
| Categorias econômicas | 21 seções CNAE e “Não informados” |
| Portes publicados | Micro, pequeno, médio, grande e indisponível |
| Companhias ativas consultáveis | 660 |
| Enquadramentos editoriais / propostos / ausentes | 12 / 491 / 157 |
| Financeiros padronizados / especializados / ausentes | 592 / 48 / 20 |

A coleta e o preparo ocorreram em 29/10/2026, no horário de São Paulo. As datas precisas de observação dos arquivos e de construção estão nos manifestos. Agosto de 2026 é a última competência encontrada no arquivo de crédito utilizado. Não se presumiu uma competência mais recente.

Os demonstrativos têm datas próprias e podem ser consolidados ou individuais. No universo ampliado há 423 seleções consolidadas, 217 individuais e 20 companhias sem contas utilizáveis nos períodos baixados. WEG e Romi, por exemplo, têm posição de setembro de 2026. A interface identifica competência, escopo, versão, recebimento e contas ausentes.

## 6. Tratamento e modelo de dados

### Sequência do processamento

1. Obter os arquivos oficiais e registrar URL, tamanho, data de observação e hash SHA-256.
2. Ler o CSV do SCR com codificação UTF-8 e separador ponto e vírgula.
3. Filtrar `cliente = PJ` antes de interpretar a coluna de atividade econômica.
4. Validar UF, atividade e porte contra as dimensões esperadas.
5. Converter os valores monetários com vírgula decimal em centavos inteiros.
6. Agregar os saldos por mês, UF, seção e porte, somando as demais dimensões detalhadas.
7. Publicar CSV e JSON com valores monetários em reais.
8. Ler a CVM em latin-1, selecionar sede e registro ativo e obter a atividade no FCA.
9. Selecionar a referência e versão mais recente com contas utilizáveis, no exercício “ÚLTIMO”; preferir consolidado no mesmo documento e identificar explicitamente o escopo individual quando selecionado.
10. Gerar a aplicação com os dados incorporados e validar os resultados.

As linhas publicadas no arquivo do SCR são o ponto de agregação. A implementação não mistura um total já consolidado com seus detalhes. Dimensões desconhecidas ou saldos monetários negativos interrompem o tratamento para inspeção, em vez de serem silenciosamente convertidos.

A contagem de operações pode conter o sentinela `-1`. Esse campo não entra nos indicadores. Por isso, o piso de carteira é um critério de materialidade financeira, sem afirmar confiança estatística ou número mínimo de empresas.

### Esquema do agregado

```text
mes
uf
secao_cnae
porte
carteira_ativa
carteira_inadimplencia
ativo_problematico
carteira_a_vencer
a_vencer_ate_90_dias
a_vencer_de_91_ate_360_dias
vencido_de_15_ate_90_dias
```

No JSON, os registros são arrays compactos. A ordem das colunas está em `meta.fields`. Os valores monetários estão em reais, sem divisão implícita por mil ou milhão. A interface faz apenas a formatação visual para mi, bi ou tri.

### Agregação no navegador

O motor monta uma estrutura em memória para o porte selecionado. Cada registro contribui para seu setor e UF, para o mesmo setor no Brasil e para os totais correspondentes. Ao mudar o filtro, os numeradores e denominadores são recalculados com o mesmo universo.

A consulta de companhias usa busca e paginação de 25 registros, com filtros por cobertura financeira e situação do enquadramento. O radar mantém os presets de médias e grandes, grandes, médias, micro e pequenas e todos os portes. “Todos” inclui o porte indisponível. O porte do comparador não é atribuído automaticamente à companhia da CVM.

## 7. Fórmulas que você precisa explicar

```text
Inadimplência (%) = 100 × Σ carteira_inadimplencia / Σ carteira_ativa

Ativos problemáticos (%) = 100 × Σ ativo_problematico / Σ carteira_ativa

Variação 3 meses (p.p.) = taxa(t) − taxa(t − 3 meses)

Diferença territorial (p.p.) = taxa(setor, UF, porte) − taxa(setor, Brasil, porte)

A vencer até 360 dias (%) =
100 × [Σ a_vencer_ate_90_dias + Σ a_vencer_de_91_ate_360_dias]
    / Σ carteira_a_vencer
```

O numerador da inadimplência representa o saldo das operações enquadradas nesse conceito. Usar apenas o valor das parcelas vencidas acima de 90 dias produziria uma medida diferente. Ativos problemáticos e inadimplência se sobrepõem e não são somados.

A razão é calculada depois de agregar os saldos. Uma média simples das taxas de linhas com carteiras de tamanhos diferentes daria peso indevido às carteiras pequenas. Se o denominador for zero ou a combinação não existir, o resultado é ausente.

O Brasil inclui a UF selecionada. Esse benchmark permite leitura contextual, mas não deve ser descrito como um teste independente ou como Brasil excluindo a UF.

## 8. Gatilhos do protótipo

O padrão inicial é:

- Deterioração recente: alta de pelo menos **0,5 p.p.** em três meses.
- Acima da referência: diferença de pelo menos **1,0 p.p.** para o mesmo setor no Brasil.
- Dois sinais: ambos ocorrem.
- Elegibilidade: carteira de pelo menos **R$ 100 milhões** e quatro competências contínuas com saldo positivo.

Esses parâmetros são hipóteses demonstrativas, não cortes calibrados de uma política de crédito. O analista pode alterá-los e observar a seleção mudar.

“Sem gatilho” informa que os critérios não foram atingidos. Essa classificação não comprova segurança. Uma base abaixo do piso ou sem histórico suficiente permanece sem classificação. Os gatilhos também não produzem probabilidade de default nem recomendação automática de negociação.

## 9. Resultados centrais para a apresentação

No recorte de médias e grandes, em agosto de 2026:

- A carteira nacional agrega aproximadamente **R$ 2,26 trilhões**.
- A taxa de inadimplência é **1,97%**.
- A variação desde maio é **+0,12 p.p.**.
- Há **393 recortes elegíveis**, dos quais **167** têm pelo menos um gatilho e **61** têm os dois.

Os números descrevem o universo e os parâmetros deste projeto. Não representam dados da carteira do Itaú.

### Exemplo A: comércio em São Paulo

Inadimplência de **4,47%**, variação de **+0,64 p.p.** e diferença de **+0,06 p.p.** para a referência nacional. O grupo aciona deterioração recente, enquanto a diferença territorial não atinge o parâmetro.

A leitura é uma piora recente que não aparece como grande desvio da referência nacional do comércio. A pergunta é como essa mudança conversa com as premissas do caso. Magazine Luiza é uma empresa real disponível para abrir essa discussão, sem atribuir a ela a taxa do grupo.

### Exemplo B: eletricidade e gás no Paraná

Inadimplência de **1,26%**, variação de **+0,06 p.p.** e diferença de **+1,10 p.p.** para a referência nacional. O gatilho é estar acima da referência, sem deterioração recente suficiente para acionar o outro critério.

Esse exemplo mostra por que separar nível relativo e direção recente. Copel pode ilustrar a consulta por companhia, observando que o grupo consolidado e a seção econômica são mais amplos que uma operação específica.

### Exemplo C: duas empresas, um mesmo contexto

MRV e Direcional estão associadas ao comparador de construção em Minas Gerais. O grupo registra **2,95%** de inadimplência, **+0,27 p.p.** em três meses e **−0,73 p.p.** para o Brasil, sem gatilho padrão.

Nos demonstrativos consolidados de junho de 2026, a liquidez corrente calculada é aproximadamente **1,89x** na MRV e **4,17x** na Direcional. A diferença não é uma classificação de qualidade de crédito. Ela demonstra que o mesmo grupo de comparação convive com situações financeiras individuais distintas.

Para discutir as empresas, seria necessário entender composição dos ativos, recursos vinculados, cronograma de projetos, fluxo de caixa e estrutura de dívida. O contexto sozinho não determina essa resposta.

### Exemplo D: efeito do denominador

Na agropecuária de Rondônia, o grupo de médias e grandes registra cerca de **37,55%** de inadimplência em agosto, com alta de **7,00 p.p.** desde maio. No mesmo intervalo, a carteira ativa passa de aproximadamente **R$ 155,1 milhões para R$ 132,6 milhões**, enquanto a carteira inadimplente passa de **R$ 47,4 milhões para R$ 49,8 milhões**.

A taxa sobe com contribuição do aumento do numerador e da queda do denominador. O dado não permite identificar os tomadores ou atribuir uma causa. A carteira também fica perto do piso inicial e sai da classificação quando o piso passa para R$ 1 bilhão.

Esse exemplo é útil para demonstrar investigação analítica e sensibilidade. Evite apresentá-lo como prova de um choque econômico regional sem evidência adicional.

## 10. Sensibilidade dos parâmetros

| Alta 3m | Diferença Brasil | Piso | Elegíveis | Algum gatilho | Dois gatilhos |
|---|---|---|---:|---:|---:|
| 0,5 p.p. | 1,0 p.p. | R$ 100 mi | 393 | 167 | 61 |
| 1,0 p.p. | 2,0 p.p. | R$ 100 mi | 393 | 100 | 37 |
| 0,5 p.p. | 1,0 p.p. | R$ 1 bi | 197 | 69 | 17 |
| 1,0 p.p. | 2,0 p.p. | R$ 1 bi | 197 | 34 | 10 |

Todos os resultados se referem a agosto de 2026, médias e grandes. O exercício mostra a relação entre sensibilidade e volume de revisões sugeridas. Não mede precisão, recall ou qualidade preditiva, pois não existe uma base de desfechos individuais no projeto.

Uma evolução pode usar a capacidade de revisão da equipe e a relevância avaliada pelos analistas para orientar a escolha dos parâmetros. O piso não equivale à exposição do banco no grupo.

## 11. Leitura dos demonstrativos das empresas

As informações da CVM preservam o escopo consolidado ou individual e os valores da escala MIL são multiplicados por mil para obter reais. A seleção usa referência/versão com contas utilizáveis, exercício “ÚLTIMO” e encerramento na data de referência. Receita e fluxo de caixa mantêm o período acumulado do exercício publicado, inclusive exercícios que não começam em janeiro. As 48 demonstrações especializadas exibem rótulos originais e não recebem automaticamente os indicadores padronizados abaixo.

| Informação | Conta utilizada |
|---|---|
| Caixa e equivalentes | BPA 1.01.01 |
| Ativo circulante | BPA 1.01 |
| Passivo circulante | BPP 2.01 |
| Empréstimos e financiamentos CP | BPP 2.01.04 |
| Empréstimos e financiamentos LP | BPP 2.02.01 |
| Receita de vendas ou serviços | DRE 3.01 |
| Caixa das atividades operacionais | DFC 6.01 |
| Liquidez corrente | Ativo circulante / passivo circulante |

O nome da conta original é preservado no JSON. As contas de empréstimos e financiamentos não são apresentadas como uma definição universal de dívida financeira total. Outros passivos, arrendamentos, garantias, restrições de caixa e condições contratuais podem exigir notas explicativas.

Os demonstrativos não alimentam os gatilhos do radar. A ficha reúne duas camadas: contexto público do grupo e fatos públicos da companhia. Como elas têm datas diferentes, não se deve chamar essa consulta de backtest ou visão histórica das informações disponíveis na época.

## 12. Como demonstrar o produto

Abra o HTML e confira que a competência inicial é agosto de 2026, com médias e grandes. Apresente a pergunta de negócio antes dos números.

No panorama, explique as duas dimensões da cor. Clique em comércio/SP para abrir o detalhe. Mostre a comparação nacional e a variação em três meses. Abaixo do gráfico, confira os saldos que ajudam a interpretar a taxa.

Depois entre em empresas reais, selecione Magazine Luiza e diferencie os indicadores do grupo dos números do demonstrativo. Mostre uma pergunta que o analista levaria para a revisão.

Use Copel para ilustrar um gatilho de diferença territorial. Use MRV e Direcional para demonstrar que o radar não substitui a análise individual. Se houver espaço, abra agropecuária/RO e explique o denominador.

Em “Ajustar gatilhos”, aumente o piso de 100 para 1.000 milhões e observe a seleção. Restaure o padrão antes de concluir ou mudar de exemplo.

O botão de CSV exporta a visão com filtros e parâmetros. A consulta por empresa permite baixar uma ficha HTML que também pode ser impressa. O botão “Fechar menu” recolhe a navegação lateral e passa a mostrar “Abrir menu” para restaurá-la.

## 13. Reproduzir no trabalho

### Apenas abrir

Extraia o ZIP e abra `index.html`. Nenhum comando é necessário.

### Alterar o visual e reconstruir

Edite `web/style.css`, principalmente as variáveis `--brand`, `--nav`, `--ink`, `--bg`, `--surface`, `--line` e `--radius`. Adapte componentes e tipografia aos assets disponíveis do IDS. Depois:

```powershell
python scripts/build.py
```

O HTML gerado incorpora os arquivos novamente. Editar apenas um CSS externo não altera o HTML já compilado.

### Refazer o tratamento

Na pasta do projeto, com Python 3.10 ou superior:

```powershell
python scripts/download.py --cache .cache/raw
python scripts/pipeline.py --cache .cache/raw --out data
python scripts/validate.py --cache .cache/raw
python scripts/build.py
```

São utilizadas apenas bibliotecas padrão do Python. O cache evita baixar novamente quando os arquivos já existem. O argumento `--refresh` solicita nova coleta; uma fonte revisada pode alterar os achados e requer atualizar a apresentação.

### Download manual alternativo

Se o acesso programático estiver indisponível, baixe as URLs de `data/manifesto.json` no navegador e salve os arquivos em `.cache/raw`, mantendo os nomes. Execute `download.py` sem `--refresh` para registrar os hashes do cache e siga o tratamento.

O leitor processa o conteúdo dos ZIPs em streaming. Não é necessário descompactar vários gigabytes de CSV no disco. A execução local original usou Python 3.11.

## 14. Qualidade e evidências de validação

O tratamento verificou dimensões e saldos em todas as competências. O validador confirmou integridade do esquema, unicidade da chave, valores não negativos, consistência de denominadores, presença das 27 UFs e integridade do universo ativo e dos estados de cobertura.

Uma auditoria adicional leu diretamente o bruto de maio e agosto de 2026 e recalculou sete saldos com Decimal, de forma independente da agregação por centavos inteiros. Foram conferidos o total nacional de médias e grandes e quatro recortes: construção/MG, indústria/SC, comércio/RS e transporte/SP. Os dez conjuntos reconciliaram sem diferença.

No navegador Edge headless, foram exercitados filtros, navegação, regras, busca, exportações, conteúdo das quatro visões e controle do menu. Na ampliação, 19 verificações por cenário confirmaram paginação, consulta por CNPJ, ausência de demonstração/mapeamento, ficha especializada e contexto de IA em desktop e tela estreita. As capturas foram inspecionadas. O relatório registra o escopo e não equivale à homologação em todos os navegadores ou no ambiente corporativo.

## 15. Arquitetura AWS e modernização

A aplicação local é o que está implementado. A arquitetura AWS é uma proposta de evolução, detalhada em `ARQUITETURA_AWS.md`.

O desenho começa com EventBridge Scheduler e Step Functions, executa coleta Python em ECS/Fargate, preserva arquivos brutos no S3, prepara camadas tratadas e analíticas, usa Glue Data Catalog e Athena para acesso SQL e disponibiliza indicadores pré-calculados por uma aplicação autenticada.

A modernização agrega agendamento, reprocessamento, rastreabilidade, controle da publicação e operação. A qualidade deve impedir que uma execução com problemas substitua o último resultado válido. O custo e o dimensionamento exigem volume e frequência medidos.

O mesmo código Python pode compor uma primeira implantação em contêiner. A adoção de Glue para etapas de transformação depende da carga e dos padrões da plataforma. A integração com dados internos deve acontecer em ambiente restrito, mantendo o pacote público com dados públicos.

## 16. Piloto e avaliação de utilidade

Proponha um piloto com um grupo pequeno de analistas e revisões reais autorizadas. Registre o uso da ficha e peça uma avaliação da relevância dos sinais. Compare o tempo de preparação de análises com uma referência construída de maneira consistente.

As medidas iniciais podem ser tempo de preparação, cobertura dos recortes relevantes, disponibilidade das atualizações, sinais considerados úteis e premissas que exigiram investigação adicional. A coleta desses resultados ajudará a ajustar o produto e os parâmetros.

Não há retorno financeiro medido no case. Para relacionar o radar a recuperação, seria necessário acompanhar desfechos, diferenças entre casos, momento da intervenção e outros fatores que afetam o resultado. Uma comparação simples antes/depois não provaria causalidade.

## 17. Perguntas da banca e respostas sugeridas

**Por que uma fonte de crédito agregada para analisar uma empresa?** Ela contextualiza o ambiente do grupo. A conclusão individual depende dos dados da empresa, e a ficha deixa essa separação explícita.

**Por que isso é útil para recuperação, além de concessão?** O contexto pode confrontar premissas de melhora, refinanciamento e geração de caixa usadas na revisão de um plano.

**Por que criar algo se o BCB já tem painel?** O projeto aplica o dado a um fluxo de revisão, com enquadramento, referências consistentes e ficha de investigação. A utilidade precisa ser demonstrada no piloto.

**Como escolheu os parâmetros?** São hipóteses iniciais transparentes para a demonstração. A análise de sensibilidade mostra seu impacto. Uma implantação exigiria avaliação com analistas e resultados apropriados.

**Por que não usar machine learning?** A base pública disponível não fornece o desfecho individual necessário para desenvolver e validar uma probabilidade de default por companhia. As regras atuais permitem explicar a seleção.

**Uma empresa com grupo vermelho deve receber uma condição diferente?** O sinal exige investigação. Condições de negociação dependem da capacidade de pagamento, garantias, viabilidade e estratégia do caso.

**A sede representa onde a companhia opera?** Pode representar apenas parte da exposição. Para empresas nacionais ou internacionais, seria necessário considerar a distribuição de receitas, ativos ou operações.

**O porte da companhia está confirmado?** O filtro define o grupo de comparação. Não atribuímos automaticamente a ela o porte do SCR.

**Duas empresas do mesmo setor e UF recebem o mesmo contexto?** Sim. Isso é esperado em uma ferramenta contextual. As informações próprias e a análise individual permitem diferenciá-las.

**Como validar algo preditivo no futuro?** Com base interna autorizada, desfechos bem definidos, separação temporal e controle das informações disponíveis em cada data. Esse trabalho ainda não foi feito.

**Por que o histórico começa em 2025?** O recorte evita atravessar a mudança do indicador de ativos problemáticos. É adequado ao protótipo descritivo, mas curto para estudar ciclos longos.

**Os sinais explicam a causa da deterioração?** Não. Saldos e taxas podem refletir alterações de composição. A interpretação exige investigação complementar.

**A AWS está funcionando?** O MVP está funcionando localmente. A evolução AWS está documentada com responsabilidades e caminho de migração, sem provisionamento nesta entrega.

## 18. Como posicionar sua contribuição

Explique as decisões que você consegue sustentar: escolha das fontes, granularidade, soma de saldos, referências, parâmetros, limites, transformação em perguntas e desenho de operação. Use a demo para tornar essas decisões visíveis.

Uma formulação possível é:

> Estruturei uma solução descritiva com dados públicos e empresas reais. A preocupação foi ligar cada sinal a uma investigação útil, manter os cálculos verificáveis e mostrar como o protótipo poderia evoluir para uma rotina operada pela área.

Se perguntarem sobre ferramentas usadas no desenvolvimento, responda de forma fiel ao processo. Dominar e explicar as escolhas vale mais do que atribuir ao case resultados ou validações que ele ainda não possui.

## 19. Ampliação e integração futura com IA

A ampliação inclui todas as 660 companhias ativas do snapshot, sem excluir um cadastro por falta de FCA ou demonstração. O financeiro pode ser utilizável, especializado ou ausente; as contas efetivamente publicadas conservam rótulo, escala e período. Uma ausência é exibida como indisponível e não como zero.

No enquadramento, os 12 casos editoriais originais são distinguidos das 491 propostas por categoria CVM e dos 157 sem associação. Uma proposta não confirma CNAE nem valida a pertinência do comparador para aquele grupo econômico.

A área “Análise assistida por IA” prepara a ficha para um futuro serviço interno. “Copiar ficha para IA” gera um texto de entrada e “Baixar contexto JSON” preserva dados, fontes, períodos, filtros, parâmetros e lacunas. A demo não chama modelo e não produz parecer fictício. O espaço de parecer permanece identificado como aguardando integração.

Uma integração real poderá solicitar síntese de fatos, interpretações condicionais, pontos de atenção, lacunas e perguntas, com referências às evidências. A opinião será preliminar e revisada pelo analista. O modelo não deve transformar taxa do grupo em inadimplência individual, inventar dado ausente ou tratar texto público como instrução. O contrato completo está em `INTEGRACAO_IA.md`.

Para se preparar para a banca, use `STORYTELLING_GESTOR.md` e `AVALIACAO_COMO_GESTOR.md`. A ampliação do cadastro deve ser apresentada junto com a cobertura e a qualidade, sem confundir 660 registros com 660 pareceres validados.
