"""Verificação de integridade e auditoria Decimal independente de grupos do bruto."""
import argparse,csv,io,json,zipfile
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
from config import SECTORS

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--cache',type=Path);a=p.parse_args()
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
 check(len(d['companies'])==12 and len({c['cnpj'] for c in d['companies']})==12,'Doze CNPJs distintos na amostra')
 check(all(c['uf'] in d['states'] and c['section'] in d['sectors'] for c in d['companies']),'Empresas com enquadramento rastreável')
 check(all(c['financial_received']>=c['financial_date'] for c in d['companies']),'Datas de recebimento compatíveis com demonstrações')
 audit=[]
 if a.cache:
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
 (a.root/'data/validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'passed':report['passed'],'checks':len(checks),'raw_audits':len(audit)},ensure_ascii=True))
if __name__=='__main__':main()
