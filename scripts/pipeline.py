"""Trata SCR.data e CVM; preserva saldos e procedência. Sem dependências externas."""
import argparse,csv,io,json,zipfile
from collections import defaultdict,Counter
from datetime import datetime,timezone
from pathlib import Path
from config import SECTORS,STATES,SIZES,RULES
from cvm_universe import load_company_universe

FIELDS=['carteira_ativa','carteira_inadimplencia','ativo_problematico','carteira_a_vencer','a_vencer_ate_90_dias','a_vencer_de_91_ate_360_dias','vencido_de_15_ate_90_dias']
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
def reader(z,name,encoding='latin-1'):
    return csv.DictReader(io.TextIOWrapper(z.open(name),encoding=encoding),delimiter=';')
def cents(v):
    if ',' not in v: raise ValueError('Decimal SCR inesperado: '+v)
    return int(v.replace('.','').replace(',',''))

def scr(cache,out):
    by_name={v[1]:k for k,v in SECTORS.items()};aggr=defaultdict(lambda:[0]*7);qc=[]
    for archive in sorted(cache.glob('scrdata_*.zip')):
      with zipfile.ZipFile(archive) as z:
       for name in sorted(z.namelist()):
        if not name.endswith('.csv'):continue
        counts=Counter();total=[0]*7;dimset=set();err=Counter();period=None
        # A versão 2 do SCR está em UTF-8; os CSV CVM usam latin-1.
        with z.open(name) as f:
         rows=csv.reader(io.TextIOWrapper(f,encoding='utf-8-sig'),delimiter=';')
         h=next(rows);ix={k:h.index(k) for k in ['data_base','uf','cliente','cnae_ocupacao','porte']+FIELDS};money=[ix[k] for k in FIELDS]
         for r in rows:
          counts['raw_rows']+=1
          if r[ix['cliente']]!='PJ':counts['pf_rows']+=1;continue
          counts['pj_rows']+=1
          dt=r[ix['data_base']][:7];uf=r[ix['uf']];sector=by_name.get(r[ix['cnae_ocupacao']]);size=SIZES.get(r[ix['porte']]);period=dt
          if sector is None or size is None or uf not in STATES:raise ValueError('Dimensão desconhecida: '+repr(r[:6]))
          key=(dt,uf,sector,size);vals=[cents(r[i]) for i in money]
          if any(v<0 for v in vals):raise ValueError('Saldo monetário negativo ou suprimido: '+repr(r[:6]))
          # Valores de operações suprimidos (-1) não são usados ou somados.
          if vals[1]>vals[0]+1:err['inad_maior_carteira']+=1
          if vals[2]>vals[0]+1:err['ap_maior_carteira']+=1
          if vals[4]+vals[5]>vals[3]+2:err['curto_maior_a_vencer']+=1
          target=aggr[key]
          for i,v in enumerate(vals):target[i]+=v;total[i]+=v
          dimset.add((uf,sector,size))
        item={'archive':archive.name,'entry':name,'month':period,**counts,'aggregated_cells':len(dimset),'checks':dict(err),'total_brl':[round(v/100,2) for v in total]}
        qc.append(item);print(name,counts['pj_rows'],'linhas PJ;',len(dimset),'células',flush=True)
    records=[[dt,uf,s,p]+[round(v/100,2) for v in vals] for (dt,uf,s,p),vals in sorted(aggr.items())]
    with (out/'scr_agregado.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['mes','uf','secao_cnae','porte']+FIELDS);w.writerows(records)
    return records,qc

def reuse_scr(path,out):
    """Reuse already aggregated balances and their original quality records."""
    payload=json.loads(path.read_text(encoding='utf-8'))
    records,qc=payload['records'],payload['quality']
    if not records or any(len(row)!=11 for row in records):
        raise ValueError('SCR reutilizado sem registros ou com esquema incompatível')
    with (out/'scr_agregado.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream,delimiter=';')
        writer.writerow(['mes','uf','secao_cnae','porte']+FIELDS)
        writer.writerows(records)
    return records,qc


def main():
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,default=Path('.cache/raw'));p.add_argument('--out',type=Path,default=Path('data'));p.add_argument('--reuse-scr',type=Path,metavar='RADAR_JSON',help='Reutiliza saldos e auditoria SCR de radar.json existente');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    records,qc=reuse_scr(a.reuse_scr,a.out) if a.reuse_scr else scr(a.cache,a.out)
    cos,company_coverage=load_company_universe(a.cache)
    months=sorted({r[0] for r in records});manifest=json.loads((a.cache/'manifesto_coleta.json').read_text(encoding='utf-8'))
    payload={'meta':{'title':'Radar Setorial-Territorial PJ','version':'1.1.0','built_at_utc':datetime.now(timezone.utc).isoformat(),'first_month':months[0],'last_month':months[-1],'months':months,'currency':'BRL','unit':'reais','fields':['month','uf','section','size']+FIELDS,'rules':RULES,'source':'Banco Central / SCR.data v2','coverage':'PJ, todas as modalidades, segmentos, origens e indexadores; território da sede','company_comparison':'mapeamento econômico editorial ou proposta automática a validar; não confirma CNAE; porte do comparador selecionado pelo analista','company_coverage':company_coverage},'states':STATES,'sectors':{k:{'name':v[0],'official':v[1]} for k,v in SECTORS.items()},'records':records,'companies':cos,'quality':qc,'manifest':manifest}
    dump(a.out/'radar.json',payload);dump(a.out/'empresas.json',cos);dump(a.out/'manifesto.json',manifest)
    dump(a.out/'qualidade.json',{'months':months,'source_rows':sum(q['raw_rows'] for q in qc),'pj_rows':sum(q['pj_rows'] for q in qc),'aggregated_rows':len(records),'checks':qc,'companies':len(cos),'company_coverage':company_coverage})
    print('Gerado',a.out/'radar.json',len(records),'registros;',len(cos),'empresas',flush=True)

if __name__=='__main__':main()
