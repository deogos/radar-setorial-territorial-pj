# Ampliação CVM e preparação para IA interna

## Escopo solicitado

Incluir todas as 660 companhias com registro ativo no snapshot cadastral da CVM de 29/10/2026, preservando o radar setorial e permitindo consulta individual. Preparar um espaço de evolução em que a IA interna leia a ficha e produza um parecer preliminar fundamentado nos dados.

## Decisões de implementação

- Preservar HTML offline, quatro visões, menu recolhível, rodapé “Case de Analytics”, ausência de arquitetura AWS no HTML e repositório privado com Pages despublicado.
- Usar todas as companhias ativas por CNPJ distinto, sem exigir demonstrativo ou FCA para incluir o cadastro.
- Ampliar o tratamento da CVM sobre os arquivos já baixados. Não repetir o processamento SCR quando não houver mudança nessa base.
- Manter os 12 enquadramentos editoriais originais; classificar novos enquadramentos como propostas automáticas a validar. Atividades ambíguas ficam sem associação automática.
- Exibir ausência de dados e demonstrativos especializados sem preenchimento por zero. As contas de bancos e outras atividades financeiras não serão apresentadas automaticamente como indicadores de uma empresa não financeira.
- Adotar busca, filtros de cobertura e paginação para navegar pelas 660 companhias.
- Preparar contexto estruturado e texto de ficha para uso pela IA interna. A demo não chamará nenhum modelo, não solicitará credenciais e não inventará um parecer.
- Incluir fontes, períodos, regras, situação do mapeamento e dados faltantes no contexto entregue à IA. O parecer futuro será preliminar e revisado pelo analista.

## Alternativas consideradas

O cadastro ativo completo foi escolhido em lugar de manter uma amostra ou incluir registros cancelados, pois responde ao universo corrente discutido com o usuário. Para dados financeiros, aproveitar os arquivos estruturados existentes é mais reproduzível do que consultar individualmente cada site de RI. Na IA, preparar um contrato independente de fornecedor atende ao pedido de evolução sem presumir a API privada do banco.

## Critérios de conclusão

Todas as 660 companhias aparecem na consulta, sem CNPJ duplicado. Empresas sem mapeamento, sem demonstrativo ou com demonstração especializada abrem sem erros e exibem sua situação. Busca e paginação funcionam. Ficha e contexto exportados preservam a empresa selecionada, fontes e filtros. A opção de IA se identifica como futura e não realiza chamadas de rede. A documentação e o pacote reproduzem a ampliação. GitHub permanece privado e Pages despublicado.
