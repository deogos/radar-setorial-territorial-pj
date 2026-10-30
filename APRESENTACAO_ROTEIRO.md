# Estrutura flexível de apresentação — sessão de uma hora

Este material é um repertório para montar a apresentação com os assets do trabalho. Os blocos podem ocupar mais de um slide, ser combinados ou mudar de ordem conforme a banca. A duração da sessão é uma hora, com espaço para demonstração e discussão. Não há cronograma rígido por slide.

## 1. Mensagem que deve permanecer

> O radar transforma informações públicas de crédito em contexto organizado para revisar premissas de casos PJ, com indicadores verificáveis e perguntas para a análise individual.

Ao longo da conversa, conecte a fonte de dados a uma decisão de investigação. O interesse do case está na aplicação desse dado à rotina da área e na qualidade das escolhas analíticas.

## 2. Abertura possível

“Quando revisamos um caso, precisamos entender se as premissas apresentadas pela empresa continuam plausíveis. Estruturei um radar que usa dados públicos para acompanhar o ambiente de crédito do setor e da UF da sede. A partir daí, o analista consegue comparar referências, consultar uma empresa real e levar perguntas mais específicas para a revisão.”

Apresente então a pergunta central: **quais recortes merecem investigação e quais premissas do caso precisam ser verificadas?**

Um visual possível é um fluxo simples: contexto do grupo, enquadramento da empresa, evidência e pergunta de análise. Não é necessário começar com a arquitetura.

## 3. Bloco de problema e uso pela área

Conteúdo possível:

- A análise individual precisa dialogar com o ambiente externo.
- Fontes públicas agregadas exigem tratamento antes de serem comparadas.
- O objetivo do produto é reduzir o esforço de reunir contexto e organizar a revisão.
- O radar pode apoiar a preparação de uma discussão de caso ou o acompanhamento periódico de recortes.

Artefatos sugeridos: uma pergunta realista de análise, o fluxo do usuário e uma ficha de exemplo.

Se a banca perguntar sobre benefícios, apresente-os como hipóteses para o piloto: ganho de tempo na preparação, padronização das referências e relevância das perguntas. O case ainda não mediu impacto em recuperação financeira.

## 4. Bloco de dados e engenharia analítica

Mostre as fontes e seus papéis:

| Fonte | O que acrescenta |
|---|---|
| BCB / SCR.data | Contexto agregado do crédito PJ por período, UF, seção e porte |
| CVM / Cadastro e FCA | Identificação, sede e atividade declarada de empresas reais |
| CVM / ITR e DFP | Informações consolidadas da companhia com período e documento identificados |

Evidências do processamento: 20 competências, 6,28 milhões de linhas brutas, 2,56 milhões de linhas PJ e 53.100 agregados. O histórico vai de janeiro de 2025 a agosto de 2026. Há 12 companhias na amostra.

Explique uma escolha técnica com consequência analítica: converter saldos em centavos, agregar antes de calcular razões e preservar numeradores e denominadores. Outra escolha é separar a classificação CVM do mapeamento econômico para o comparador.

O apêndice pode conter campos, hashes, detalhes de codificação e comandos. Na fala principal, escolha os aspectos que ajudam a entender a confiabilidade dos resultados.

## 5. Bloco de construção dos sinais

Dois eixos bastam para explicar a classificação:

- Mudança recente: a taxa subiu quanto desde três meses antes?
- Nível relativo: o setor nessa UF está quanto acima da referência nacional?

Mostre os parâmetros iniciais de 0,5 p.p. e 1 p.p., o piso de R$ 100 milhões e a exigência de quatro competências contínuas. Informe que são hipóteses demonstrativas. A explicação ganha força ao mostrar a sensibilidade no próprio produto.

No recorte inicial de médias e grandes, em agosto de 2026, há 393 combinações elegíveis, 167 com algum gatilho e 61 com os dois. Uma tabela ou matriz ajuda a visualizar os critérios. Evite representar esses grupos como probabilidades de perda.

## 6. Bloco de investigação dos achados

Você pode usar três linhas de raciocínio, conforme o interesse da banca.

### Mudança recente e referência nacional

Comércio/SP: inadimplência de 4,47%, variação de +0,64 p.p. em três meses e diferença de +0,06 p.p. para o Brasil. O gatilho é deterioração recente. A diferença territorial não é o principal sinal naquele corte.

Pergunta para discussão: como o analista verificaria se as projeções do cliente incorporam essa mudança do ambiente?

### Diferença territorial sem forte mudança recente

Eletricidade e gás/PR: inadimplência de 1,26%, variação de +0,06 p.p. e diferença de +1,10 p.p. para o Brasil. O gatilho é o nível relativo.

Pergunta para discussão: que informação adicional ajuda a avaliar a pertinência da sede como referência para uma companhia com várias operações?

### Um contexto comum, informações individuais distintas

MRV e Direcional compartilham o comparador construção/MG. No recorte inicial, ele está sem gatilho. As informações individuais de junho de 2026 mostram liquidez corrente de aproximadamente 1,89x e 4,17x, respectivamente.

O ponto é explicar por que o contexto não individualiza a análise. Não use a comparação isolada para declarar uma companhia saudável ou problemática.

## 7. Demonstração principal

Prepare os percursos, mas preserve liberdade para navegar conforme surgirem perguntas.

### Percurso de decisão

1. Panorama em agosto de 2026, médias e grandes.
2. Explicação breve da matriz e das cores.
3. Abrir comércio/SP e mostrar série, referência e saldos.
4. Consultar Magazine Luiza e conferir perfil, período financeiro e perguntas.
5. Baixar a ficha, se for útil para mostrar como o resultado entra no trabalho.

### Percurso de comparação

1. Abrir eletricidade e gás/PR.
2. Diferenciar o gatilho de nível do gatilho de variação.
3. Consultar Copel e discutir o enquadramento econômico de grupos consolidados.
4. Mostrar os limites da UF da sede.

### Percurso analítico

1. Abrir agropecuária/RO.
2. Conferir maio e agosto nos saldos.
3. Explicar como numerador e denominador contribuem para a taxa.
4. Aumentar o piso para R$ 1 bilhão e mostrar a mudança de elegibilidade.
5. Restaurar os parâmetros.

Se não houver conexão no local, a demonstração continua disponível pelo HTML. Mantenha uma cópia extraída do pacote e capturas das telas como apoio.

## 8. Bloco de sensibilidade e escolhas

Esta tabela pode funcionar como slide ou como discussão no produto:

| Parâmetros | Elegíveis | Algum gatilho | Dois gatilhos |
|---|---:|---:|---:|
| 0,5 p.p.; 1 p.p.; R$ 100 mi | 393 | 167 | 61 |
| 1 p.p.; 2 p.p.; R$ 100 mi | 393 | 100 | 37 |
| 0,5 p.p.; 1 p.p.; R$ 1 bi | 197 | 69 | 17 |
| 1 p.p.; 2 p.p.; R$ 1 bi | 197 | 34 | 10 |

Agosto de 2026, médias e grandes. Os resultados mudam quando a base e os parâmetros mudam. A escolha inicial deve considerar o uso e a capacidade de revisão, além de avaliação dos analistas. Não há uma medida de acurácia preditiva neste exercício.

## 9. Bloco de arquitetura e operação

Comece pela solução que efetivamente funciona: download oficial, tratamento Python, dados tratados e HTML portátil.

Depois apresente a evolução AWS e o problema que cada componente resolve:

- EventBridge Scheduler e Step Functions: execução agendada e coordenação.
- ECS/Fargate e Glue conforme a carga: coleta e preparação.
- S3: dados brutos, tratados e analíticos com versões.
- Glue Data Catalog e Athena: catálogo e investigação SQL.
- Aplicação autenticada sobre resultados pré-calculados: consulta.
- Logs, verificações e preservação da última publicação válida: operação.

O diagrama completo está em `ARQUITETURA_AWS.md`. Explique que a escolha final depende da medição do volume e dos padrões existentes. Nenhum recurso AWS foi provisionado para o case.

Uma boa pergunta para se preparar: “se a fonte mudar o esquema ou ficar indisponível, o que o usuário vê?”. A resposta proposta é manter a última publicação válida com sua competência, registrar a falha e permitir reprocessamento controlado.

## 10. Bloco de implantação e avaliação

Proponha um piloto com uma amostra autorizada de revisões e um grupo pequeno de analistas. O desenho deve registrar quais sinais foram úteis, quais perguntas geraram investigação adicional e quanto tempo foi necessário para preparar o contexto.

Uma integração futura pode vincular CNPJ, exposição e estágio do caso em ambiente restrito. A ordenação por impacto na carteira dependeria desses dados. O MVP público não inventa exposição bancária.

Como evolução, podem entrar indicadores de atividade do IBGE, ponderação territorial por receitas ou operações e avaliação temporal com dados internos. A inclusão de fontes deve responder a uma pergunta e preservar compatibilidade econômica e temporal.

## 11. Apêndices disponíveis

Escolha os materiais conforme a pergunta, sem assumir que todos precisam virar slides:

- Dicionário das variáveis e fórmulas.
- Exemplo de média simples versus razão de somas.
- Relatório de qualidade e auditoria Decimal.
- Amostra de empresas e fontes do mapeamento.
- Datas de crédito e de demonstrativos.
- Efeito do denominador em agropecuária/RO.
- Sensibilidade dos parâmetros.
- Componentes e alternativas da arquitetura AWS.
- Métricas do piloto e limites de inferência.

## 12. Perguntas de aprofundamento

| Pergunta provável | Linha de resposta |
|---|---|
| Isso já não existe no BCB? | O BCB fornece a fonte e um painel. O case propõe aplicação no fluxo de revisão, com empresa real e ficha de investigação. |
| Por que olhar território? | Pode revelar diferenças do grupo e orientar perguntas. A sede é parcial para operações distribuídas. |
| Como você sabe o porte da companhia? | O produto informa que o porte é do comparador, selecionado pelo analista. |
| Por que o mesmo contexto aparece para duas empresas? | O indicador pertence ao grupo. Os dados individuais permitem diferenciá-las. |
| Por que esses cortes? | São parâmetros iniciais transparentes; a sensibilidade foi examinada, mas não há calibração contra default. |
| Como comprovar valor? | Piloto com tempo de preparação e relevância avaliada pelos usuários. Impacto financeiro exige estudo adicional. |
| Como tratar revisões de dados? | Preservar snapshots, versões e histórico de publicações; reprocessar competências afetadas. |
| O que está implementado na AWS? | A arquitetura é proposta. O MVP executável é local e reproduzível. |

## 13. Preparação final

Antes da apresentação, abra o HTML no computador que será usado. Confirme os filtros iniciais, teste um clique na matriz e uma consulta por empresa. Escolha os exemplos que você consegue explicar e confira os números no mesmo snapshot. Mantenha os períodos nas telas ou nos slides.

Durante a fala, diferencie dado, interpretação e ação de investigação. Quando uma pergunta exigir informação que o case não contém, indique qual fonte ou validação seria necessária para responder. Isso preserva a precisão da análise e abre uma discussão útil sobre a implantação.
