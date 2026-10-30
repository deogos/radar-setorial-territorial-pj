(function(root){
 'use strict';
 function normalized(value){return String(value??'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();}
 function filterCompanies(companies,filters={}){
  const q=normalized(filters.query),digits=q.replace(/\D/g,'');
  return companies.filter(c=>{
   if(filters.financial&&filters.financial!=='all'&&(c.financial_status||'available')!==filters.financial)return false;
   if(filters.mapping==='reviewed'&&!c.mapping_reviewed)return false;
   if(filters.mapping==='proposed'&&(!c.section||c.mapping_reviewed))return false;
   if(filters.mapping==='unmapped'&&c.section)return false;
   if(filters.section&&filters.section!=='all'&&c.section!==filters.section)return false;
   if(filters.uf&&filters.uf!=='all'&&c.uf!==filters.uf)return false;
   if(!q)return true;
   const text=normalized([c.name,c.legal_name,c.cnpj,c.uf,c.city,c.cvm_sector,c.activity].join(' '));
   return text.includes(q)||(digits.length>=3&&/^[\d./\-\s]+$/.test(q)&&String(c.cnpj).replace(/\D/g,'').includes(digits));
  }).sort((a,b)=>String(a.name).localeCompare(String(b.name),'pt-BR',{sensitivity:'base'})||String(a.cnpj).localeCompare(String(b.cnpj)));
 }
 function paginate(companies,page=1,pageSize=25){
  pageSize=Number.isInteger(pageSize)&&pageSize>0?pageSize:25;
  const total=companies.length,totalPages=Math.max(1,Math.ceil(total/pageSize));
  page=Math.min(totalPages,Math.max(1,Math.trunc(Number(page))||1));
  const start=(page-1)*pageSize,items=companies.slice(start,start+pageSize);
  return {items,page,pageSize,total,totalPages,start:items.length?start+1:0,end:start+items.length};
 }
 root.RadarCompanies={filterCompanies,paginate};
 if(typeof module!=='undefined'&&module.exports)module.exports=root.RadarCompanies;
})(globalThis);
