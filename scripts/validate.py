"""Verificação de integridade e auditoria Decimal independente de grupos do bruto."""
import argparse,csv,io,json,math,zipfile
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
from config import SECTORS,STATES
from cvm_universe import load_active_cad,financial_requires_specialized


def company_checks(data,cache=None):
 """Check coverage and explicit missing states; optionally compare actual CAD IDs."""
 companies=data['companies'];coverage=data['meta'].get('company_coverage',{})
 cnpjs=[company['cnpj'] for company in companies]
 checks=[(len(cnpjs)==len(set(cnpjs)),'CNPJs distintos no universo de companhias'),
         (len(companies)==coverage.get('total_active'),'Quantidade de companhias confere com cobertura declarada')]
 if cache is not None:
  checks.append((set(cnpjs)==set(load_active_cad(Path(cache))),'Universo de CNPJs coincide com CAD ativo com SEDE'))
 checks.extend([
  (all((company.get('uf') is None or company['uf'] in STATES) and
       (company.get('section') is None or company['section'] in SECTORS) for company in companies),
   'UF e seção válidas ou ausência explícita'),
  (all(type(company.get('mapping_reviewed')) is bool and isinstance(company.get('mapping_source'),str)
       and bool(company['mapping_source']) and (not company['mapping_reviewed'] or company.get('section') is not None)
       for company in companies),'Mapeamentos possuem procedência e revisão explícitas'),
  (all(company.get('financial_status') in ['available','specialized','missing'] and
       company.get('financial_scope') in ['consolidated','individual',None] and
       isinstance(company.get('financial'),dict) for company in companies),'Estados e escopos financeiros explícitos'),
  (all((company.get('financial_status')!='missing' or
        (company.get('financial')=={} and company.get('financial_scope') is None)) and
       (company.get('financial_status')=='missing' or
        (bool(company.get('financial')) and company.get('financial_scope') in ['consolidated','individual']))
       for company in companies),'Ausência financeira não é preenchida por zero'),
  (all(not company.get('financial_received') or not company.get('financial_date') or
       company['financial_received']>=company['financial_date'] for company in companies),
   'Datas de recebimento compatíveis com demonstrações disponíveis'),
  (all(isinstance(company.get('questions'),list) and bool(company['questions']) for company in companies),
   'Companhias possuem questões de análise inclusive sem enquadramento'),
  (all(isinstance(account.get('value'),(int,float)) and not isinstance(account['value'],bool) and
       math.isfinite(account['value']) and bool(account.get('label')) and
       account.get('scale_original') in ['MIL','UNIDADE']
       for company in companies for account in company.get('financial',{}).values()),
   'Contas preservam valor finito, rótulo e escala original'),
  (all(company.get('financial_status')!='available' or not financial_requires_specialized(company)
       for company in companies),'Contas especializadas não recebem classificação financeira padronizada'),
 ])
 expected={
  'with_fca':sum(company.get('fca_date') is not None for company in companies),
  'financial_available':sum(company.get('financial_status')=='available' for company in companies),
  'financial_specialized':sum(company.get('financial_status')=='specialized' for company in companies),
  'financial_missing':sum(company.get('financial_status')=='missing' for company in companies),
  'mappings_reviewed':sum(bool(company.get('mapping_reviewed')) for company in companies),
  'mappings_proposed':sum(company.get('section') is not None and not company.get('mapping_reviewed') for company in companies),
  'mappings_missing':sum(company.get('section') is None for company in companies),
 }
 checks.append((all(coverage.get(key)==value for key,value in expected.items()),'Contagens de cobertura CVM reconciliadas com as companhias'))
 return checks

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--cache',type=Path);p.add_argument('--skip-scr-audit',action='store_true',help='Valida universo CAD sem repetir auditoria do bruto SCR');p.add_argument('--check-only',action='store_true',help='Não grava data/validacao.json');a=p.parse_args()
 d=json.loads((a.root/'data/radar.json').read_text(encoding='utf-8'));checks=[]
 def check(ok,label):
  checks.append({'check':label,'passed':bool(ok)})
  if not ok:raise AssertionError(label)
 rows=d['records'];keys=[tuple(r[:4]) for r in rows]
 check(len(keys)==len(set(keys)),'Chave mês/UF/seção/porte sem duplicação')
 check(all(len(r)==11 for r in rows),'Esquema com sete saldos monetários')
 check(all(all(v>=0 for v in r[4:]) for r in rows),'Saldos monetários não negativos')
 check(all(r[5]<=r[4]+.02 and r[6]<=r[4]+.02 for r in rows),'Inadimplência e AP não excedem carteira')
 check(all(r[8]+r[9]<=r[7]+.03 for r in rows),'Vencimentos de curto prazo não excedem carteira a vencer')
 check(all(len({r[1] for r in rows if r[0]==m})==27 for m in d['meta']['months']),'Todas as competências têm as 27 UFs')
 for ok,label in company_checks(d,a.cache):check(ok,label)
 audit=[]
 if a.cache and not a.skip_scr_audit:
  fields=['carteira_ativa','carteira_inadimplencia','ativo_problematico','carteira_a_vencer','a_vencer_ate_90_dias','a_vencer_de_91_ate_360_dias','vencido_de_15_ate_90_dias']
  targets=[('BR','ALL'),('MG','F'),('SC','C'),('RS','G'),('SP','H')]
  for month in ['2026-05','2026-08']:
   raw={k:[Decimal(0)]*7 for k in targets};prepared={k:[Decimal(0)]*7 for k in targets}
   with zipfile.ZipFile(a.cache/'scrdata_2026.zip') as z:
    with z.open('scrdata_'+month.replace('-','')+'.csv') as f:
     for r in csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig'),delimiter=';'):
      if r['cliente']!='PJ' or r['porte'] not in ['Médio','Grande']:continue
      for u,s in targets:
       if (u=='BR' or r['uf']==u) and (s=='ALL' or r['cnae_ocupacao']==SECTORS[s][1]):
        for i,field in enumerate(fields):raw[u,s][i]+=Decimal(r[field].replace(',','.'))
   for r in rows:
    if r[0]!=month or r[3] not in ['medio','grande']:continue
    for u,s in targets:
     if (u=='BR' or r[1]==u) and (s=='ALL' or r[2]==s):
      for i,v in enumerate(r[4:]):prepared[u,s][i]+=Decimal(str(v))
   for u,s in targets:
    diffs=[abs(x-y) for x,y in zip(raw[u,s],prepared[u,s])]
    check(all(x<=Decimal('.02') for x in diffs),f'Auditoria Decimal do bruto: {month} / {u} / {s}, sete saldos')
    audit.append({'month':month,'uf':u,'section':s,'raw_brl':[str(v) for v in raw[u,s]],'max_difference_brl':str(max(diffs))})
 report={'passed':all(c['passed'] for c in checks),'checks':checks,'independent_raw_audits':audit}
 if not a.check_only:(a.root/'data/validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'passed':report['passed'],'checks':len(checks),'raw_audits':len(audit)},ensure_ascii=True))
if __name__=='__main__':main()
