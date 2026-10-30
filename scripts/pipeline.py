"""Trata SCR.data e CVM; preserva saldos e procedência. Sem dependências externas."""
import argparse,csv,io,json,zipfile,unicodedata
from collections import defaultdict,Counter
from datetime import datetime,timezone
from pathlib import Path
from config import SECTORS,STATES,SIZES,RULES,COMPANIES

FIELDS=['carteira_ativa','carteira_inadimplencia','ativo_problematico','carteira_a_vencer','a_vencer_ate_90_dias','a_vencer_de_91_ate_360_dias','vencido_de_15_ate_90_dias']
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c)).upper()
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

def companies(cache):
    wanted={c[0]:c for c in COMPANIES};cad={};generals={};docs={};accounts={};fca_meta={}
    with (cache/'cad_cia_aberta.csv').open(encoding='latin-1',newline='') as f:
      for r in csv.DictReader(f,delimiter=';'):
        if r['CNPJ_CIA'] in wanted and r['SIT']=='ATIVO' and r['TP_ENDER']=='SEDE':cad[r['CNPJ_CIA']]=r
    with zipfile.ZipFile(cache/'fca_cia_aberta_2026.zip') as z:
      for r in reader(z,'fca_cia_aberta_geral_2026.csv'):
        c=r['CNPJ_Companhia']
        if c not in wanted:continue
        key=(r['Data_Referencia'],int(r['Versao']),int(r['ID_Documento']))
        if c not in generals or key>generals[c][0]:generals[c]=(key,r)
    target_codes={'1','1.01','1.01.01','2.01','2.01.04','2.02.01','2.03','3.01','3.11','6.01'}
    for filename,year,kind in [('dfp_cia_aberta_2025.zip',2025,'dfp'),('itr_cia_aberta_2026.zip',2026,'itr')]:
      with zipfile.ZipFile(cache/filename) as z:
        for r in reader(z,f'{kind}_cia_aberta_{year}.csv'):
          c=r['CNPJ_CIA']
          if c in wanted:docs[(c,r['DT_REFER'],int(r['VERSAO']))]=r
        for statement in ['BPA','BPP','DRE','DFC_MI','DFC_MD']:
          name=f'{kind}_cia_aberta_{statement}_con_{year}.csv'
          if name not in z.namelist():continue
          for r in reader(z,name):
            c=r['CNPJ_CIA'];code=r['CD_CONTA']
            if c not in wanted or code not in target_codes or norm(r['ORDEM_EXERC'])!='ULTIMO':continue
            if r['DT_FIM_EXERC']!=r['DT_REFER']:continue
            if statement in ['DRE','DFC_MI','DFC_MD'] and not r['DT_INI_EXERC'].endswith('-01-01'):continue
            key=(c,r['DT_REFER'],int(r['VERSAO']));accounts.setdefault(key,{})[code]=r
    result=[]
    for c,name,sector,profile in COMPANIES:
      if c not in cad or c not in generals:raise ValueError('Cadastro não encontrado: '+name)
      ca=cad[c];g=generals[c][1]
      available=[k for k in accounts if k[0]==c and k in docs]
      if not available:raise ValueError('Demonstrativo não encontrado: '+name)
      latest=max(available,key=lambda k:(k[1],k[2]));acc=accounts[latest];doc=docs[latest]
      financial={}
      for code,r in acc.items():
        if r['MOEDA']!='REAL' or r['ESCALA_MOEDA'] not in ['MIL','UNIDADE']:raise ValueError('Escala não suportada')
        val=float(r['VL_CONTA'])*(1000 if r['ESCALA_MOEDA']=='MIL' else 1)
        financial[code]={'value':val,'label':r['DS_CONTA'],'start':r.get('DT_INI_EXERC'),'end':r['DT_FIM_EXERC'],'scale_original':r['ESCALA_MOEDA']}
      note='Referência econômica do grupo consolidado; a seção selecionada é um mapeamento analítico documentado, não o CNAE cadastral confirmado da holding.' if profile=='holding' else 'Mapeamento analítico da atividade descrita no FCA para a seção do grupo de comparação. Não representa consulta ao CNAE cadastral da Receita.'
      questions={
       'C':['Como pedidos, utilização da capacidade e margens evoluíram?','Qual a exposição a exportações, câmbio e operações fora da UF?','O cronograma de vencimentos acompanha a geração de caixa?'],
       'G':['A geração operacional de caixa acompanha estoques e recebíveis?','Qual a concentração regional das vendas e a exposição a crédito ao consumidor?','A renovação de linhas está incorporada nas projeções?'],
       'H':['Contratos e volumes transportados sustentam a projeção?','Quais corredores e clientes concentram receitas?','Qual a necessidade de investimento e refinanciamento?'],
       'F':['Qual a velocidade de vendas, distratos e recebimentos?','Como se distribuem os projetos por UF e estágio de obra?','Qual a necessidade de caixa até a conclusão dos projetos?'],
       'D':['Quais concessões, áreas e atividades concentram o fluxo?','O investimento contratado e os vencimentos cabem na geração de caixa?','Quais premissas regulatórias ou contratuais precisam ser atualizadas?'],
      }[sector]
      result.append({'cnpj':c,'name':name,'legal_name':ca['DENOM_SOCIAL'],'cvm_code':int(ca['CD_CVM']),'uf':ca['UF'],'city':ca['MUN'],'cvm_sector':ca['SETOR_ATIV'],'section':sector,'activity':g['Descricao_Atividade'],'fca_date':g['Data_Referencia'],'fca_version':int(g['Versao']),'fca_document':g['ID_Documento'],'website':g['Pagina_Web'],'mapping_note':note,'mapping_status':'mapeamento econômico editorial','profile':profile,'questions':questions,'financial_date':latest[1],'financial_version':latest[2],'financial_received':doc['DT_RECEB'],'financial_doc':doc['LINK_DOC'].replace('http:','https:'),'financial':financial,'sources':{'cad':'https://dados.cvm.gov.br/dataset/cia_aberta-cad','fca':'https://dados.cvm.gov.br/dataset/cia_aberta-doc-fca','financial':'https://dados.cvm.gov.br/dataset/cia_aberta-doc-itr' if latest[1].startswith('2026') else 'https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp'}})
      print(name,ca['UF'],latest[1],len(financial),'contas',flush=True)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,default=Path('.cache/raw'));p.add_argument('--out',type=Path,default=Path('data'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    records,qc=scr(a.cache,a.out);cos=companies(a.cache)
    months=sorted({r[0] for r in records});manifest=json.loads((a.cache/'manifesto_coleta.json').read_text(encoding='utf-8'))
    payload={'meta':{'title':'Radar Setorial-Territorial PJ','version':'1.0.0','built_at_utc':datetime.now(timezone.utc).isoformat(),'first_month':months[0],'last_month':months[-1],'months':months,'currency':'BRL','unit':'reais','fields':['month','uf','section','size']+FIELDS,'rules':RULES,'source':'Banco Central / SCR.data v2','coverage':'PJ, todas as modalidades, segmentos, origens e indexadores; território da sede','company_comparison':'mapeamento econômico editorial; porte do comparador selecionado pelo analista'},'states':STATES,'sectors':{k:{'name':v[0],'official':v[1]} for k,v in SECTORS.items()},'records':records,'companies':cos,'quality':qc,'manifest':manifest}
    dump(a.out/'radar.json',payload);dump(a.out/'empresas.json',cos);dump(a.out/'manifesto.json',manifest)
    dump(a.out/'qualidade.json',{'months':months,'source_rows':sum(q['raw_rows'] for q in qc),'pj_rows':sum(q['pj_rows'] for q in qc),'aggregated_rows':len(records),'checks':qc,'companies':len(cos)})
    print('Gerado',a.out/'radar.json',len(records),'registros;',len(cos),'empresas',flush=True)

if __name__=='__main__':main()
