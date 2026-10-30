# Reconstruir ou adaptar rapidamente com Copilot

## Caminho mais rápido

Se o HTML abrir, a solução já está utilizável. Para aplicar o IDS, use os fontes em `web/`, preservando o motor e os dados. Após editar:

```powershell
python scripts/build.py
```

O build gera `index.html` com tudo incorporado. O ZIP inclui todos os arquivos necessários para reconstruir a interface sem baixar a base outra vez.

## Prompt para adaptação visual

Copie o texto abaixo e forneça o pacote ao Copilot no ambiente de trabalho:

```text
Adapte visualmente este Radar Setorial-Territorial PJ ao IDS disponível neste ambiente.

O produto já funciona e usa um snapshot público. Preserve:
- web/engine.js e as fórmulas existentes;
- o esquema de data/radar.json;
- filtros de competência e porte, parâmetros editáveis e piso de materialidade;
- classificação ausente para base limitada ou histórico insuficiente;
- soma de numeradores e denominadores antes de calcular razões;
- separação entre contexto do grupo e dados individuais da companhia;
- datas independentes do SCR.data e dos demonstrativos CVM;
- fontes, unidades monetárias, versão e notas de enquadramento;
- exportações e controle do menu lateral.

Edite os componentes visuais em web/index.template.html, web/style.css e web/app.js.
Use os assets e componentes IDS efetivamente disponíveis aqui. Não invente nomes de
componentes ou dependências internas. Mantenha uma versão portátil offline quando
isso for compatível com os assets fornecidos.

Depois gere o HTML usando python scripts/build.py. Confira as quatro visões,
filtros, navegação da matriz, ficha, CSV, estado sem dados e histórico inicial.
Não inclua dados internos de clientes no pacote público ou em repositório público.
```

## Prompt para reconstrução funcional, se necessário

```text
Reconstrua um dashboard de consulta com os arquivos públicos tratados deste pacote.

Objetivo: apoiar revisão de casos PJ com contexto externo de crédito, sem produzir
rating, PD ou decisão automática. A base é data/radar.json. O campo meta.fields
define a ordem dos arrays de records. Os valores monetários são reais.

Dimensões: mês, UF da sede, seção econômica e porte. Os presets são médias e
grandes, grandes, médias, micro e pequenas e todos os portes, incluindo porte
indisponível no último preset.

Fórmulas:
inadimplência_pct = 100 * SUM(carteira_inadimplencia) / SUM(carteira_ativa)
ap_pct = 100 * SUM(ativo_problematico) / SUM(carteira_ativa)
delta_3m_pp = taxa(t) - taxa(t-3 meses)
gap_pp = taxa(setor,UF,portes) - taxa(setor,Brasil,mesmos portes)
curto_pct = 100 * SUM(a_vencer_ate_90_dias + a_vencer_de_91_ate_360_dias)
                 / SUM(carteira_a_vencer)

Parâmetros iniciais: delta >= 0.5 p.p.; gap >= 1 p.p.; saldo >= R$100 milhões.
Exigir quatro competências contínuas com saldo positivo. Bases pequenas, sem
denominador ou sem histórico ficam sem classificação. Dois sinais significam
ambos os gatilhos acionados. Sem gatilho não significa baixo risco.

Criar quatro visões:
1) Panorama: KPIs nacionais, matriz setor x UF e ranking descritivo.
2) Detalhe: série do recorte contra Brasil e saldos do numerador e denominador.
3) Empresas reais: universo ativo de 660 companhias em companies, com busca e
   paginação de 25, CNPJ, fontes, cobertura financeira e situação de enquadramento.
   Preserve escopo individual/consolidado, ausência de dados e fichas especializadas.
   Inclua área futura de IA, cópia de ficha e exportação JSON, sem chamar modelos.
4) Metodologia: fórmulas, fontes, parâmetros e limitações.
A arquitetura AWS fica somente na documentação de apoio à apresentação, fora do HTML.

Empresas são exemplos públicos, sem atribuição de vínculo com o banco ou atraso.
A seção do comparador é um mapeamento econômico editorial; não é CNAE cadastral
confirmado da holding. O porte é do grupo selecionado pelo analista.

Os demonstrativos CVM possuem datas próprias. A consulta histórica do SCR não é
uma reconstrução do conjunto de informações individuais conhecido naquele mês.
Não usar os dados financeiros para os gatilhos do contexto.

Implementar exportação de CSV com filtros e parâmetros e ficha HTML por empresa.
Não exigir internet para abrir o resultado. Não usar CDN, fonte remota ou API no
carregamento. Pode consultar links de fonte quando o usuário decidir abri-los.
```

## Se só houver tempo para reconstruir parte

A sequência recomendada é preservar os dados tratados, o motor de indicadores e o detalhe do recorte. Depois monte a matriz e a consulta por empresa. Fontes e períodos precisam continuar visíveis mesmo em uma interface simplificada.

Não altere fórmulas para reproduzir uma cor ou um achado específico. Se a base, os filtros ou os parâmetros mudarem, os resultados também podem mudar e o roteiro deve ser conferido.

## Mapa para localizar alterações

| Mudança | Arquivo |
|---|---|
| Cores, tipografia e espaçamento | `web/style.css` |
| Estrutura de navegação e controles | `web/index.template.html` |
| Textos, cartões, gráficos e exportações | `web/app.js` |
| Fórmulas e classificação | `web/engine.js` |
| Parâmetros e exemplos editoriais | `scripts/config.py` |
| Universo ativo e cobertura CVM | `scripts/cvm_universe.py` |
| Busca e paginação | `web/company-directory.js` |
| Renderização dos estados da ficha | `web/company-profile.js` |
| Contrato e texto para IA interna | `web/ai-context.js` |
| Fonte de coleta e cache | `scripts/download.py` |
| Tratamento e vínculo de companhias | `scripts/pipeline.py` |
| Reconciliação com bruto | `scripts/validate.py` |
| Compilação do HTML único | `scripts/build.py` |

Alterar `config.py` requer executar novamente pipeline e build. Alterações em `web/` exigem apenas build. Os scripts usam biblioteca padrão do Python, sem instalação de pacotes.
