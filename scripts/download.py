"""Coleta oficial, com cache e hashes. Apenas biblioteca padrão do Python."""
import argparse, hashlib, json, urllib.request, zipfile
from pathlib import Path
from datetime import datetime, timezone

def sources(years):
    result = {f'scrdata_{y}.zip':f'https://www.bcb.gov.br/pda/desig/scrdata_{y}.zip' for y in years}
    result.update({
      'cad_cia_aberta.csv':'https://dados.cvm.gov.br/dados/cia_aberta/CAD/DADOS/cad_cia_aberta.csv',
      'fca_cia_aberta_2026.zip':'https://dados.cvm.gov.br/dados/cia_aberta/DOC/FCA/DADOS/fca_cia_aberta_2026.zip',
      'itr_cia_aberta_2026.zip':'https://dados.cvm.gov.br/dados/cia_aberta/DOC/ITR/DADOS/itr_cia_aberta_2026.zip',
      'dfp_cia_aberta_2025.zip':'https://dados.cvm.gov.br/dados/cia_aberta/DOC/DFP/DADOS/dfp_cia_aberta_2025.zip',
    })
    return result

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache',type=Path,default=Path('.cache/raw'))
    p.add_argument('--years',type=int,nargs='+',default=[2025,2026])
    p.add_argument('--refresh',action='store_true')
    a=p.parse_args();a.cache.mkdir(parents=True,exist_ok=True)
    old_path=a.cache/'manifesto_coleta.json'
    old=json.loads(old_path.read_text(encoding='utf-8')) if old_path.exists() else {}
    manifest={}
    for name,url in sources(a.years).items():
        path=a.cache/name;previous=old.get(name,{})
        if a.refresh or not path.exists():
            print('Baixando',name,flush=True)
            req=urllib.request.Request(url,headers={'User-Agent':'RadarSetorialCase/1.0 contato: projeto demonstrativo'})
            temp=path.with_suffix(path.suffix+'.part')
            with urllib.request.urlopen(req,timeout=120) as response,temp.open('wb') as f:
                while block:=response.read(1024*1024): f.write(block)
                last_modified=response.headers.get('Last-Modified')
            temp.replace(path)
            collected=datetime.now(timezone.utc).isoformat()
        else:
            # Na importação de cache preexistente, a data é de observação local.
            collected=previous.get('observed_at_utc',datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat())
            last_modified=previous.get('source_last_modified')
        if name.endswith('.zip'):
            with zipfile.ZipFile(path) as z: entries=[{'name':i.filename,'bytes':i.file_size,'crc32':format(i.CRC,'08x')} for i in z.infolist()]
        else: entries=[]
        manifest[name]={'url':url,'observed_at_utc':collected,'source_last_modified':last_modified,'bytes':path.stat().st_size,'sha256':sha256(path),'entries':entries}
        print(name,manifest[name]['bytes'],'bytes',flush=True)
    old_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Manifesto:',old_path)

if __name__=='__main__':main()
