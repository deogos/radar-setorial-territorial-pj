(function(root){
 'use strict';
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const number=(v,d=1)=>typeof v==='number'&&Number.isFinite(v)?v.toLocaleString('pt-BR',{minimumFractionDigits:d,maximumFractionDigits:d}):'—';
 const pct=v=>v==null?'—':number(v,2)+'%';
 const pp=v=>v==null?'—':(v>0?'+':'')+number(v,2)+' p.p.';
 const date=d=>d?new Date(d+'T12:00:00').toLocaleDateString('pt-BR'):'não disponível';
 const period=m=>m?new Date(m+'-01T12:00:00').toLocaleDateString('pt-BR',{month:'short',year:'2-digit'}).replace('.',''):'não disponível';
 function money(v){if(v==null)return '—';const a=Math.abs(v),k=a>=1e12?1e12:a>=1e9?1e9:a>=1e6?1e6:1;return 'R$ '+number(v/k)+(k===1e12?' tri':k===1e9?' bi':k===1e6?' mi':'');}
 function mini(label,value,note=''){return `<div class="mini-fact"><span class="caption">${esc(label)}</span><b>${value}</b><span class="caption">${esc(note)}</span></div>`;}
 function link(url,label){return typeof url==='string'&&/^https?:\/\//.test(url)?`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`:'';}
 function financial(c){
  const empty={cash:null,debtShort:null,debtLong:null,revenue:null,income:null,operating:null,liquidity:null};
  if(c.financial_status&&c.financial_status!=='available')return empty;
  const a=c.financial||{},v=code=>typeof a[code]?.value==='number'?a[code].value:null;
  const ca=v('1.01'),cl=v('2.01');
  return {cash:v('1.01.01'),debtShort:v('2.01.04'),debtLong:v('2.02.01'),revenue:v('3.01'),income:v('3.11'),operating:v('6.01'),liquidity:ca!=null&&cl>0?ca/cl:null};
 }
 function financialHTML(c){
  const accounts=c.financial||{},status=c.financial_status||(c.financial_date?'available':'missing');
  if(status==='missing')return '<div class="note">Sem demonstrativo utilizável nos arquivos do snapshot. O cadastro permanece disponível; valores ausentes não são tratados como zero.</div>';
  const scope=c.financial_scope==='individual'?'Individual':'Consolidado';
  const heading=`<p class="caption">${scope} · posição ${esc(date(c.financial_date))} · versão ${esc(c.financial_version)} · recebido na CVM em ${esc(date(c.financial_received))}.</p>`;
  if(status==='specialized'){
   const shown=Object.entries(accounts).filter(([,a])=>a&&typeof a.value==='number').slice(0,6);
   return heading+`<div class="note"><b>Demonstração especializada</b><br>As contas abaixo mantêm os nomes originais da CVM. A ficha não aplica indicadores padronizados de uma companhia não financeira.</div><div class="company-fins">${shown.map(([code,a])=>mini(a.label||code,money(a.value),`Conta ${code} · ${date(a.start||a.end)} a ${date(a.end)}`)).join('')}</div>`;
  }
  const f=financial(c),range=code=>{const a=accounts[code];return a?.start?`${date(a.start)} a ${date(a.end)}`:'Período não disponível';};
  return heading+`<div class="company-fins">${mini('Caixa e equivalentes',money(f.cash),'BPA · conta 1.01.01')}${mini('Empréstimos e financiamentos CP',money(f.debtShort),'BPP · conta 2.01.04')}${mini('Empréstimos e financiamentos LP',money(f.debtLong),'BPP · conta 2.02.01')}${mini(accounts['3.01']?.label||'Receita de vendas / serviços',money(f.revenue),range('3.01'))}${mini(accounts['6.01']?.label||'Caixa das atividades operacionais',money(f.operating),range('6.01'))}${mini('Liquidez corrente',f.liquidity==null?'—':number(f.liquidity,2)+'x','Ativo circulante / passivo circulante')}</div>`;
 }
 function render({company:c,metrics:m,status,sectorName,sizeLabel,month,aiPrompt='',exporting=false}){
  if(!c)return '<div class="panel empty">Nenhuma companhia corresponde aos filtros da consulta.</div>';
  const mapped=!!c.section,reviewed=!!c.mapping_reviewed;
  const mappingLabel=!mapped?'Sem enquadramento':reviewed?'Enquadramento editorial':'Comparador proposto · validar';
  const badge=status?`<span class="badge ${esc(status.code)}">${esc(status.label)}</span>`:'<span class="badge limited">Sem contexto de grupo</span>';
  const source=c.sources||{},activityTitle=c.fca_date?'Atividade declarada no FCA':'Setor cadastral CVM';
  const financialNote=c.financial_date?`o demonstrativo tem posição ${date(c.financial_date)} e data de recebimento própria`:'não há demonstrativo utilizável neste snapshot';
  const q=Array.isArray(c.questions)?c.questions:['Quais dados adicionais são necessários para avaliar o caso individual?'];
  return `<article class="panel" id="company-sheet">
   <div class="company-title"><div><span class="eyebrow">Companhia CVM · cadastro ativo</span><h2 style="margin-top:8px">${esc(c.name)}</h2><p class="caption">${esc(c.legal_name)}<br>CNPJ ${esc(c.cnpj)} · código CVM ${esc(c.cvm_code)}</p></div><button class="btn" data-export-company>Baixar ficha</button></div>
   <div class="company-profile"><span class="pill">Sede: ${esc(c.city)} / ${esc(c.uf)}</span><span class="pill">${esc(mappingLabel)}</span><span class="pill">${esc(sizeLabel)}</span></div>
   <div class="note${!reviewed?' warm':''}"><b>${esc(mappingLabel)}</b><br>${esc(c.mapping_note||'A atividade requer avaliação para definir um grupo de comparação.')}${mapped?` Grupo: ${esc(sectorName)}.`:''} O porte selecionado é o filtro do comparador, não uma classificação cadastral confirmada da companhia.</div>
   <div class="definition"><b>${activityTitle}</b><p>${esc(c.activity||c.cvm_sector||'Atividade não disponível.')}</p><p style="margin-top:5px">Setor CVM: ${esc(c.cvm_sector||'não informado')} · ${c.fca_date?`FCA ${date(c.fca_date)}, versão ${esc(c.fca_version)}.`:'FCA não encontrado no snapshot; referência do cadastro.'}</p></div>
   <h3 style="margin-top:20px">Contexto ${reviewed?'do grupo':'do comparador proposto'} em ${esc(period(month))}</h3>${badge}
   ${mapped?`<div class="company-fins">${mini('Inadimplência do grupo',pct(m?.npl),`${c.uf} · seção ${c.section}`)}${mini('Variação em três meses',pp(m?.delta),'Sinal descritivo do ambiente')}${mini('Diferença para Brasil',pp(m?.gap),'Mesmo setor e porte')}</div>`:'<div class="note">Sem enquadramento econômico definido. Os indicadores de um grupo não foram atribuídos a esta companhia.</div>'}
   <div class="note warm">${esc(status?.reasons?.join(' ')||'O contexto disponível não permite uma classificação desse recorte.')} Os sinais pertencem ao grupo de comparação. A inclusão da companhia não indica inadimplência, recuperação ou vínculo com o Itaú.${mapped&&!reviewed?' O enquadramento automático precisa de validação antes do uso em uma análise individual.':''}</div>
   <div class="financial-title"><h3>Demonstrativo público da companhia</h3>${financialHTML(c)}</div>
   <div class="note">Datas independentes: o radar usa ${esc(period(month))}; ${esc(financialNote)}. Esta consulta não reconstrói a informação individual conhecida em cada competência histórica. Dados financeiros não entram nos gatilhos do radar. As contas selecionadas não representam necessariamente todas as obrigações financeiras.</div>
   <h3 style="margin-top:23px">Perguntas para revisar as premissas</h3><ol class="question-list">${q.map(x=>`<li>${esc(x)}</li>`).join('')}</ol>
   <section class="ai-ready" aria-label="Integração futura com IA interna"><div class="panel-head"><div><h3>Análise assistida por IA</h3><p class="caption">A IA interna poderá ler esta ficha e elaborar uma opinião preliminar fundamentada, para revisão do analista.</p></div><span class="badge">Integração futura</span></div>${exporting?'':'<div class="ai-actions"><button class="btn" data-copy-ai>Copiar ficha para IA</button><button class="btn" data-export-ai>Baixar contexto JSON</button></div>'}<div class="ai-opinion"><b>Parecer da IA</b><p class="caption">Aguardando integração com o serviço interno. Nenhum parecer foi gerado nesta demonstração.</p></div>${exporting?'':`<details class="ai-prompt-details"><summary>Ver o texto preparado para a IA</summary><textarea class="ai-prompt" readonly aria-label="Texto da ficha preparado para a IA">${esc(aiPrompt)}</textarea></details><p class="caption">As ações acima preparam a ficha localmente. Nenhum dado é enviado a um modelo pela demo.</p>`}</section>
   <div class="source-links">${link(source.cad,'Cadastro CVM')}${link(source.fca,'Formulário Cadastral')}${link(c.financial_doc,'Documento financeiro')}${link(source.financial,'Dados estruturados')}</div>
   <p class="caption" style="margin-top:16px">Demonstrações consolidadas podem incluir operações em outras UFs e no exterior. A pertinência da sede e do enquadramento precisa ser examinada no caso individual.</p>
   ${mapped?`<button class="btn" data-cell="${esc(c.section)}|${esc(c.uf)}" style="margin-top:8px">Abrir contexto ${esc(c.uf)} · ${esc(sectorName)}</button>`:''}
  </article>`;
 }
 root.RadarCompanyView={render,financial};
 if(typeof module!=='undefined'&&module.exports)module.exports=root.RadarCompanyView;
})(globalThis);
