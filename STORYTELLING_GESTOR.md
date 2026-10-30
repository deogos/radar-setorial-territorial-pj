# Como apresentar o case ao gestor

Use este texto para ensaiar hoje. O [roteiro da sessão](APRESENTACAO_ROTEIRO.md) organiza slides e demo para uma hora com espaço para discussão. A proposta é apresentar seu raciocínio como candidato a Analytics Jr em Recuperação e Reestruturação de Crédito no Itaú BBA. Os critérios abaixo são uma preparação sugerida, sem presumir informações sobre a avaliação ou a rotina interna do banco.

## Abertura pronta — aproximadamente 60–90 segundos

> Imagine uma revisão de plano de uma empresa: a projeção depende de melhora da geração de caixa e de renovação de linhas. Antes de discutir se essas premissas se sustentam, eu preciso entender o que mudou no ambiente e o que ainda preciso verificar no caso.
>
> Foi dessa pergunta que parti. Construí um radar com dados públicos para organizar o contexto de crédito do setor e da UF da sede e conectá-lo a uma ficha de companhia, com fontes, datas e perguntas para análise.
>
> No comércio de São Paulo, por exemplo, a taxa do grupo subiu 0,64 ponto percentual em três meses. A diferença para o comércio no Brasil é pequena. Isso sustenta uma pergunta sobre mudança recente do ambiente; a taxa pertence ao grupo, não à empresa que vou consultar.
>
> Vou percorrer essa investigação: abrir o sinal, conferir a referência, olhar a companhia e chegar a uma pergunta verificável sobre caixa e vencimentos. Usarei companhias abertas como exemplos públicos, sem associá-las à carteira do banco.
>
> Ao final, proponho como testar a utilidade da ficha com analistas. Quero mostrar uma análise que possa ser conferida e usada para preparar melhor a revisão de um caso.

Depois da abertura, mostre a jornada do analista e entre em comércio/SP. O nome das ferramentas pode esperar até a explicação de como a evidência foi preparada.

## O arco da história

1. **A situação:** há uma premissa de recuperação de caixa a revisar. Apresente isso como cenário hipotético, sem inventar um cliente ou uma dificuldade observada no banco.
2. **A investigação:** o radar mostra mudança no grupo. Você confere período, porte, referência e saldos antes de interpretar.
3. **A descoberta:** comércio/SP tem alta recente, mas pequena diferença para o Brasil. A pergunta precisa refletir esse padrão; o agregado não prova uma causa paulista.
4. **A passagem ao caso:** a ficha permite verificar atividade, sede, documentos e números próprios. A próxima pergunta é como caixa, estoque, recebíveis e vencimentos sustentam as premissas daquela empresa.
5. **O julgamento:** MRV e Direcional compartilham um grupo sem gatilho e têm dados individuais diferentes. Essa comparação torna visível a necessidade de análise humana.
6. **O uso e a avaliação:** a investigação vira uma ficha rastreável. Um piloto verifica se ela ajuda o trabalho. A tecnologia sustenta esse fluxo; o resultado de negócio ainda precisa ser medido.

Copel/PR é um bom desvio de percurso se o gestor perguntar sobre território: o sinal vem da diferença para a referência nacional, com pouca mudança recente. Pergunte se a sede e o enquadramento representam as operações da companhia. Retome a pergunta do caso depois do exemplo.

Uma transição útil entre tela e interpretação é: **“O que esse dado permite afirmar, que pergunta ele abre e qual informação falta para responder?”** Use essa sequência ao longo da conversa.

## O que tornar visível para o gestor

| Capacidade | Evidência na sua apresentação |
|---|---|
| Entender a decisão | Relacionar o contexto às premissas de caixa, vencimentos e refinanciamento de uma revisão hipotética. |
| Raciocinar com dados | Explicar razão de saldos, comparação consistente, numerador e denominador; formular uma interpretação compatível com a evidência. |
| Reconhecer limites | Separar grupo de companhia, mapeamento de CNAE confirmado, porte do comparador de porte cadastral e consulta atual de reconstrução histórica. |
| Cuidar da qualidade | Mostrar fontes, períodos, versões e lacunas, inclusive os registros que não permitem uma ficha completa. |
| Entregar algo utilizável | Percorrer a demo e terminar em uma ficha com uma pergunta concreta para o analista. |
| Pensar em adoção | Propor avaliação com usuários e casos autorizados, com critérios para continuar ou ajustar. |
| Explicar sua contribuição | Sustentar as escolhas que fez e ser fiel sobre ferramentas utilizadas e validações efetivamente executadas. |

O caso fica mais convincente quando você consegue explicar uma escolha e sua consequência. Por exemplo: “Somei os saldos antes de calcular a taxa para preservar o peso das carteiras” ou “Deixei a atividade ambígua sem seção para não criar um comparador sem fundamento”.

## Como falar das lacunas sem enfraquecer a entrega

> A consulta cobre os 660 CNPJs ativos do snapshot. Isso não significa 660 fichas completas. Há 592 com ficha financeira padronizada, 48 com demonstração especializada e 20 sem demonstrativo disponível. Nos comparadores, preservei 12 enquadramentos editoriais com revisão, identifiquei 491 propostas a validar e deixei 157 sem enquadramento. Preferi mostrar o que precisa de validação a completar uma informação sem evidência.

Esses números vêm de `data/radar.json`, `meta.company_coverage`, no snapshot cadastral de 29/10/2026. Mostre um estado de ausência na demo, explique sua consequência e retorne ao fluxo. Cadastro consultável, comparador válido e dado financeiro disponível são coberturas diferentes.

## Como posicionar a IA e a arquitetura

Diga: “Já preparei uma ficha estruturada com fontes, períodos, filtros e lacunas. Uma IA interna autorizada poderia ler esse contexto e devolver uma síntese, evidências citadas, interpretações condicionais e perguntas. O parecer seria preliminar e revisado pelo analista.”

Mostre a seção “Integração futura” e a exportação do contexto. Hoje a demo não chama modelo nem gera parecer. A integração futura exige autorização no servidor, tratamento do texto público como dado não confiável, auditoria e conferência das referências. Não use um parecer inventado para ilustrar funcionamento.

Para tecnologia, explique a entrega local reproduzível e uma decisão de qualidade. Se houver pergunta sobre escala, use o documento AWS para discutir agendamento, versões e última publicação válida. A arquitetura é proposta; não houve implantação. Evite recitar serviços sem relacioná-los a uma necessidade de operação.

## Perguntas difíceis e respostas curtas

| Pergunta | Resposta que você consegue sustentar |
|---|---|
| O que isso muda em uma recuperação? | Pode ajudar a confrontar premissas do plano e preparar perguntas. Condições de negociação dependem de capacidade de pagamento, viabilidade, garantias e informações do caso que o radar não contém. |
| O sinal indica que a empresa vai atrasar? | Não. É uma observação sobre um grupo. Não estimei probabilidade de default por companhia. |
| Por que 0,5 e 1 ponto percentual? | São parâmetros demonstrativos, transparentes e ajustáveis. Examinei a sensibilidade; ainda seria preciso avaliar a utilidade com a área. |
| Mais grupos sinalizados significa maior acerto? | Não. Significa mais grupos atingindo os critérios. Sem desfechos apropriados, não há medida de acurácia ou recall. |
| Como priorizar o que importa para o banco? | O case ordena sinais descritivos. Prioridade por exposição e estágio do caso dependeria de dados internos autorizados e de uma regra discutida com a área. |
| Por que olhar a sede de uma empresa nacional? | A sede é a dimensão publicada. Eu verificaria distribuição de receitas, ativos e operações antes de tratá-la como representativa. Copel ajuda a discutir esse limite. |
| Posso usar a ficha para um mês antigo? | Posso consultar o agregado daquele mês. A ficha CVM contém os documentos do snapshot e pode incluir informação publicada depois; não é uma reconstrução histórica. |
| Por que manter empresas sem dados ou sem seção? | Elas pertencem ao universo cadastral ativo. Excluí-las esconderia a cobertura. A interface informa a lacuna e evita fabricar números ou associação econômica. |
| Como sabe que uma pergunta é útil? | Ainda não medi. No piloto, registraria se o analista a considerou relevante, se gerou uma verificação e que correção foi necessária. |
| Qual foi o retorno financeiro? | Não há retorno financeiro medido. Eu começaria por utilidade e esforço de preparação. Relacionar o uso a recuperação financeira exigiria estudo adicional de desfechos e outros fatores. |
| Por que não ficar no painel do BCB? | O BCB fornece a fonte e um painel. O case propõe a passagem desse contexto para uma ficha de companhia e uma pergunta de revisão. O piloto precisa demonstrar se essa aplicação acrescenta valor. |
| A IA e a AWS já estão funcionando? | O HTML local e as exportações estão implementados. IA e AWS são evoluções documentadas; nenhum modelo é chamado e nenhum serviço AWS foi provisionado. |

## Fechamento pronto

> Eu começaria com um piloto pequeno de revisões autorizadas, validando os enquadramentos e comparando a preparação da ficha com uma referência consistente. Mediria tempo, relevância das perguntas e correções dos analistas, incluindo casos com e sem gatilho. A partir disso, decidiria o que ajustar e se vale integrar à rotina. O que entrego hoje é um ponto de partida verificável para essa avaliação.

Hoje, ensaie a abertura, comércio/SP e a distinção entre MRV e Direcional. No trabalho, aplique os assets e adapte o número de slides à conversa. Mantenha o piloto como próximo passo proposto e preserve os números e períodos do snapshot.
