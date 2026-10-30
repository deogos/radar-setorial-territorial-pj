# Preparação da ficha para futura IA interna

Esta entrega prepara dados e instruções para uma futura IA autorizada do banco ler a ficha de uma companhia e redigir um parecer preliminar fundamentado. A aplicação atual funciona offline e não chama modelo, endpoint ou serviço externo, não recebe credenciais e não produz parecer fictício. O texto de preparação não constitui decisão de crédito.

## Contrato disponível

`web/ai-context.js` expõe `RadarAI` como global de navegador e módulo CommonJS. Não depende de DOM, rede, relógio ou bibliotecas externas. O build deve incluí-lo antes de `app.js`.

```javascript
const context = RadarAI.buildContext({
  data: DATA,
  company: selectedCompany,
  metrics: selectedCompany.section
    ? engine().metrics(state.month, selectedCompany.uf, selectedCompany.section)
    : null,
  status: selectedStatus, // resultado de RadarEngine.classify ou null
  sizeLabel: 'Médias e grandes',
  rules: {...state.rules},
  filters: {
    month: state.month,
    uf: selectedCompany.uf,
    section: selectedCompany.section || null,
    size: state.size
  }
});
const fichaTextual = RadarAI.toMarkdown(context);
const promptPreparado = RadarAI.toPrompt(context);
const jsonContexto = JSON.stringify(context, null, 2);
```

`filters` é opcional para compatibilidade, mas a interface deve fornecê-lo sempre. Sem agregado, não é possível deduzir a competência selecionada dos demais argumentos. O módulo conserva explicitamente `null`, não troca filtros pelo último mês do snapshot e não consulta outras empresas. Quando os filtros estão ausentes, aproveita as dimensões de `metrics`; sem elas, usa somente a UF e a seção da companhia e deixa o mês ausente. O código do porte precisa ser fornecido, porque os indicadores do motor não carregam essa dimensão. Quem chama deve obter `metrics` do motor criado para o mesmo `size` e fornecer o `status` calculado com os mesmos parâmetros.

O contexto contém uma cópia independente da companhia selecionada. Não inclui a lista de companhias, linhas brutas ou o cubo SCR. Preserva o manifesto do snapshot para rastreabilidade. As funções não alteram as entradas. Um CNPJ selecionado é obrigatório.

| Bloco | Conteúdo e uso |
|---|---|
| `contract_version` | `radar-ai-context/1.0.0`; versionar alterações incompatíveis |
| `purpose` | Preparação apenas, sem opinião gerada e com revisão humana obrigatória |
| `snapshot` | Versão dos dados, geração, meses disponíveis, último mês, cobertura CVM e manifesto com URLs, observação e hashes |
| `selection` | CNPJ, competência, UF, seção e porte exatamente fornecidos para a consulta selecionada |
| `parameters` | Gatilhos vigentes, piso e histórico; usa os parâmetros fornecidos ou, na ausência, os defaults do snapshot |
| `company` | Identificação, atividade, FCA, situação do mapeamento, datas, documentos, escopo e contas financeiras com códigos e rótulos da fonte |
| `mapping` | Origem e estado `reviewed`, `proposed`, `unknown` ou `unmapped`; não confirma CNAE |
| `group_context` | Indicadores agregados e classificação descritiva recebidos do motor, separados dos fatos da companhia |
| `sources` | Referências estáveis como `cvm.cad`, `cvm.fca`, `cvm.financial`, `bcb.scr`, `radar.mapping` e `radar.rules` |
| `evidence` | IDs estáveis, campo, valor, disponibilidade, período, unidade e `source_ref` para fundamentar afirmações futuras |
| `gaps` / `limitations` | Dados ausentes, validações necessárias e restrições de interpretação |

Exemplos de referência: a conta oficial `3.01` recebe `id = cvm.account.3.01` e `field_id = company.financial.3.01.value`; a taxa do grupo recebe `id = scr.npl` e `field_id = group_context.metrics.npl`; o parâmetro recebe `id = parameter.delta_pp`. IDs de conta identificam a conta da ficha selecionada. Para identificar uma evidência em auditoria entre fichas, combinar hash do contexto, CNPJ, ID, período, escopo e documento/versão. A enumeração de `financial` é um dicionário de códigos oficiais; não interpretar os pontos como navegação automática de propriedades.

`toMarkdown` produz uma ficha legível em PT-BR com dados da empresa, agregado, contas originais, parâmetros, lacunas, fontes e limites. Texto público é escapado para não virar HTML ou marcação ativa. `toPrompt` produz uma string JSON com tarefa, instruções, formato de resposta sugerido e todo o contexto dentro de `untrusted_input`. Não executa o prompt nem valida uma resposta de modelo, pois não há modelo integrado.

## Regras de interpretação preservadas

- A taxa SCR pertence ao grupo, nunca à empresa individual. Não revela atraso, exposição, rating, recuperação, PD ou vínculo com o banco.
- Porte é filtro do comparador. UF é sede. O enquadramento pode representar a atividade do grupo econômico, não o CNAE cadastral da holding.
- Mapeamento não revisado fica proposto ou desconhecido. Sem seção, o módulo elimina agregado e classificação, mesmo que sejam fornecidos por engano. Um agregado com mês, UF ou seção diferentes dos filtros também é excluído e a lacuna fica registrada.
- Contas preservam os rótulos, códigos, período e escala original. Valores financeiros já estão em BRL; não reaplicar `MIL`. Não são calculados automaticamente liquidez, dívida total ou outros indicadores.
- Demonstração `specialized` requer interpretação própria. Contas de instituições financeiras não recebem nomes padronizados de empresas não financeiras. `financial_scope` individual, consolidado ou ausente é explícito.
- `null`, conta ausente e demonstrativo `missing` são indisponibilidade. Zero numérico fornecido permanece zero publicado. Não há preenchimento por zero ou aproximação.
- Competência do SCR, posição do demonstrativo, período da conta, recebimento, versão e data FCA têm significados diferentes. O snapshot não reconstrói a informação individual conhecida em uma competência passada; uma consulta histórica pode conter documento publicado depois dela.
- Gatilhos e contagem de sinais são descritivos e não calibrados para default. “Sem gatilho” não demonstra baixo risco. Alterações de composição do grupo podem alterar taxas.

## Rota de integração futura, independente de fornecedor

Uma implementação interna pode seguir o fluxo: analista autenticado seleciona a ficha → serviço interno autorizado valida e versiona o contexto → adaptador de modelo aprovado recebe instruções e dados → serviço valida a resposta e suas referências → analista revisa o parecer. O projeto não pressupõe nome, URL, autenticação ou contrato da API privada do banco. Nenhuma dessas chamadas está implementada.

A autorização deve ocorrer no servidor, vinculada ao usuário, finalidade e caso permitido. Um HTML baixado ou um CNPJ enviado pelo navegador não comprova acesso. O servidor deve validar esquema e versão, reconstruir ou conferir o snapshot e os filtros, limitar tamanho e campos, e obter dados internos somente de fontes autorizadas para aquele usuário. Não colocar segredos no HTML nem aceitar instruções de sistema vindas do contexto ou do cliente. Transporte e retenção devem seguir as políticas internas aplicáveis.

O adaptador pode atender ao provedor homologado pelo banco sem mudar os IDs da ficha. Instruções de sistema e regras de negócio devem ser controladas no servidor, separadas dos dados. Descrições de atividade, rótulos, URLs e perguntas públicas são dados não confiáveis e podem conter tentativa de injeção de prompt. O envelope JSON preserva a separação e o texto original para inspeção; isso não garante que um modelo será imune. Para este caso de síntese, o modelo deve operar sem ferramenta de rede, execução de comandos ou acesso autônomo a sistemas internos. Links de fonte não devem acionar navegação automática.

## Auditoria e revisão de saída

Na integração futura, registrar a identidade autorizada, finalidade/caso, instante da solicitação, hash canônico e cópia protegida do contexto, versão do contrato, snapshot e hashes das fontes, filtros e parâmetros, versão do template de instruções, provedor/modelo aprovado e versão disponível, configurações da execução, identificador da requisição e saída original. Esses registros são uma proposta de integração, não logs gerados pela demo. Reexecuções com modelos podem variar; guardar a saída efetivamente revisada.

Validar a estrutura da resposta no servidor e conferir se cada referência citada existe no `evidence`/`sources` daquele contexto, com valor, período, escopo e fonte compatíveis. Rejeitar referências inexistentes e sinalizar afirmações factuais sem suporte. O formato sugerido no prompt inclui síntese executiva concisa, evidências, interpretações condicionais, lacunas e perguntas. Não aceitar score inventado, causa não sustentada, inferência de atraso individual pelo setor ou decisão automática. Dados ausentes devem permanecer explícitos.

O analista deve conferir as evidências, o enquadramento, a atualidade dos documentos e o alcance do agregado antes de usar a saída. Registrar versão revisada, responsável, data e alterações. Até essa revisão, a saída permanece identificada como preliminar. O uso em decisões seguirá o processo interno de crédito e as informações autorizadas do caso.

A proposta AWS continua apenas no documento `ARQUITETURA_AWS.md`; esta preparação não implanta serviços ou cria dependência de nuvem. A interface de produto não precisa exibir detalhes dessa arquitetura.

## Verificação local

```powershell
node --test tests/test_ai_context.js
```

Os testes cobrem ficha completa, cópia independente, fontes e períodos, filtros, demonstrativo ausente, demonstração especializada, mapeamento proposto/ausente, zero publicado, conteúdo com instruções maliciosas, agregado desalinhado e uso global/CommonJS sem DOM ou rede. Eles não validam a qualidade de um parecer de IA, pois nenhum parecer é gerado nesta etapa.
