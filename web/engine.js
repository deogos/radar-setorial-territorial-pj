/* Regras descritivas do protótipo. Nenhum resultado representa PD individual. */
(function(root){
 'use strict';
 const presets={all:['micro','pequeno','medio','grande','ni'],mg:['medio','grande'],grande:['grande'],medio:['medio'],mp:['micro','pequeno']};
 function shift(month,n){let [y,m]=month.split('-').map(Number);let d=new Date(Date.UTC(y,m-1+n,1));return d.toISOString().slice(0,7);}
 function create(data,size='mg'){
  if(!presets[size])throw Error('Filtro de porte inválido');
  const cube=new Map(),allowed=new Set(presets[size]);
  function add(k,v){let a=cube.get(k);if(!a){a=Array(7).fill(0);cube.set(k,a);}for(let i=0;i<7;i++)a[i]+=v[i];}
  for(const r of data.records){if(!allowed.has(r[3]))continue;const v=r.slice(4);for(const uf of [r[1],'BR'])for(const s of [r[2],'ALL'])add(`${r[0]}|${uf}|${s}`,v);}
  const get=(m,u,s)=>cube.get(`${m}|${u}|${s}`)||null;
  const ratio=(a,i,j)=>a&&a[j]>0?100*a[i]/a[j]:null;
  function metrics(m,u,s){
   const a=get(m,u,s);if(!a||a[0]<=0)return null;
   const p=get(shift(m,-3),u,s),n=get(m,'BR',s),rate=ratio(a,1,0),old=ratio(p,1,0),national=ratio(n,1,0);
   return {month:m,uf:u,section:s,active:a[0],impaired:a[1],problem:a[2],due:a[3],short:a[4]+a[5],early:a[6],npl:rate,ap:ratio(a,2,0),shortShare:a[3]>0?100*(a[4]+a[5])/a[3]:null,delta:old==null?null:rate-old,national,gap:u==='BR'||national==null?null:rate-national,previousActive:p?.[0]??null,previousImpaired:p?.[1]??null,history:[0,-1,-2,-3].every(t=>{let x=get(shift(m,t),u,s);return x&&x[0]>0;})};
  }
  function series(m,u,s){return data.meta.months.filter(t=>t<=m).map(t=>metrics(t,u,s)).filter(Boolean);}
  return {metrics,series,get,size};
 }
 function classify(m,rules){
  if(!m)return {code:'missing',label:'Sem dados',flags:0,eligible:false,reasons:['Sem saldo publicado para a combinação selecionada.']};
  if(m.active<rules.materiality_brl)return {code:'limited',label:'Baixa materialidade',flags:0,eligible:false,reasons:['Saldo do grupo abaixo do piso demonstrativo.']};
  if(!m.history||m.delta==null)return {code:'limited',label:'Histórico insuficiente',flags:0,eligible:false,reasons:['É necessário histórico contínuo de quatro competências.']};
  const recent=m.delta>=rules.delta_pp,above=m.gap!=null&&m.gap>=rules.gap_pp;
  const reasons=[];if(recent)reasons.push('Aumento da inadimplência em três meses atingiu o parâmetro.');if(above)reasons.push('Diferença para o mesmo setor no Brasil atingiu o parâmetro.');
  return {code:recent&&above?'both':recent?'recent':above?'above':'none',label:recent&&above?'Dois sinais':recent?'Deterioração recente':above?'Acima da referência':'Sem gatilho',flags:Number(recent)+Number(above),eligible:true,reasons:reasons.length?reasons:['Os parâmetros atuais não acionam os gatilhos do protótipo. Isso não comprova baixo risco.']};
 }
 root.RadarEngine={create,classify,presets,shift};
 if(typeof module!=='undefined'&&module.exports)module.exports=root.RadarEngine;
})(globalThis);
