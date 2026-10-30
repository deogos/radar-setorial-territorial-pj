"""Gera um único HTML offline a partir de fontes auditáveis."""
from pathlib import Path
import argparse,json

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();root=args.root
    data=json.loads((root/'data/radar.json').read_text(encoding='utf-8'))
    page=(root/'web/index.template.html').read_text(encoding='utf-8')
    replacements={'STYLE':(root/'web/style.css').read_text(encoding='utf-8'),'ENGINE':(root/'web/engine.js').read_text(encoding='utf-8'),'APP':(root/'web/app.js').read_text(encoding='utf-8'),'DATA':json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')}
    for key,name in [('DIRECTORY','company-directory.js'),('PROFILE','company-profile.js'),('AI','ai-context.js')]:replacements[key]=(root/'web'/name).read_text(encoding='utf-8')
    for key,value in replacements.items():page=page.replace('/*__'+key+'__*/',value)
    if '/*__' in page:raise ValueError('Marcador de build não preenchido')
    (root/'index.html').write_text(page,encoding='utf-8')
    print('HTML offline:',root/'index.html',len(page.encode('utf-8')),'bytes')
if __name__=='__main__':main()
