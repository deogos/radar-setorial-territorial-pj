"""Demonstra o tratamento real do SCR em um recorte: comércio/SP, médias e grandes.

Não altera o radar. Usa apenas a biblioteca padrão do Python.
Exemplo: python demonstrar_scr.py --zip CAMINHO/scrdata_2026.zip --snapshot CAMINHO/data/radar.json
"""
import argparse
import csv
import io
import json
import zipfile
from pathlib import Path

CAMPOS = [
    'carteira_ativa', 'carteira_inadimplencia', 'ativo_problematico',
    'carteira_a_vencer', 'a_vencer_ate_90_dias',
    'a_vencer_de_91_ate_360_dias', 'vencido_de_15_ate_90_dias',
]
SETOR = 'Comércio; reparação de veículos automotores e motocicletas'
PORTES = {'Médio': 'medio', 'Grande': 'grande'}

def centavos(texto):
    # Mesmo tratamento do pipeline: evita somar dinheiro com ponto flutuante.
    if ',' not in texto:
        raise ValueError('Decimal inesperado: ' + texto)
    valor = int(texto.replace('.', '').replace(',', ''))
    if valor < 0:
        raise ValueError('Saldo monetário negativo: ' + texto)
    return valor

def salvar_csv(path, cabecalho, linhas):
    with path.open('w', encoding='utf-8-sig', newline='') as arquivo:
        escritor = csv.writer(arquivo, delimiter=';')
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', type=Path, required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    saldos = {p: [0] * 7 for p in PORTES.values()}
    contagens = {'linhas_lidas_agosto': 0, 'linhas_pf_excluidas': 0,
                 'linhas_pj_agosto': 0, 'linhas_do_recorte': 0,
                 'contagens_de_operacoes_suprimidas_no_recorte': 0}
    brutas, tratadas, por_porte = [], [], {'medio': 0, 'grande': 0}
    with zipfile.ZipFile(args.zip) as pacote:
        with pacote.open('scrdata_202608.csv') as entrada:
            leitor = csv.DictReader(io.TextIOWrapper(entrada, encoding='utf-8-sig'), delimiter=';')
            cabecalho = leitor.fieldnames
            for linha in leitor:
                contagens['linhas_lidas_agosto'] += 1
                if linha['cliente'] != 'PJ':
                    contagens['linhas_pf_excluidas'] += 1
                    continue
                contagens['linhas_pj_agosto'] += 1
                if linha['uf'] != 'SP' or linha['cnae_ocupacao'] != SETOR or linha['porte'] not in PORTES:
                    continue
                contagens['linhas_do_recorte'] += 1
                if linha['numero_de_operacoes'] == '-1':
                    contagens['contagens_de_operacoes_suprimidas_no_recorte'] += 1
                porte = PORTES[linha['porte']]
                valores = [centavos(linha[campo]) for campo in CAMPOS]
                por_porte[porte] += 1
                for i, valor in enumerate(valores):
                    saldos[porte][i] += valor
                brutas.append([linha[campo] for campo in cabecalho])
                tratadas.append([linha['data_base'][:7], 'SP', 'G', porte] + valores)
    salvar_csv(args.out/'01_linhas_brutas_do_recorte.csv', cabecalho, brutas)
    salvar_csv(args.out/'02_linhas_padronizadas_centavos.csv',
               ['mes', 'uf', 'secao_cnae', 'porte'] + [c + '_centavos' for c in CAMPOS], tratadas)
    agregados = [[ '2026-08', 'SP', 'G', p ] + [v / 100 for v in saldos[p]] for p in ['medio', 'grande']]
    # Vírgula decimal para facilitar a leitura no Excel com configuração brasileira.
    salvar_csv(args.out/'03_agregado_reais.csv', ['mes', 'uf', 'secao_cnae', 'porte'] + CAMPOS,
               [r[:4] + [f'{v:.2f}'.replace('.', ',') for v in r[4:]] for r in agregados])
    snapshot = json.loads(args.snapshot.read_text(encoding='utf-8'))
    for registro in agregados:
        publicado = next(r for r in snapshot['records'] if r[:4] == registro[:4])
        assert all(abs(a-b) < .005 for a,b in zip(publicado[4:], registro[4:])), 'Agregado divergiu do radar'
    def somar(mes, uf):
        registros = [r for r in snapshot['records'] if r[0] == mes and (uf == 'BR' or r[1] == uf) and r[2] == 'G' and r[3] in PORTES.values()]
        return [sum(round(r[i] * 100) for r in registros) / 100 for i in range(4, 11)]
    atual = [sum(saldos[p][i] for p in saldos) / 100 for i in range(7)]
    anterior, brasil = somar('2026-05', 'SP'), somar('2026-08', 'BR')
    taxa = lambda v: 100 * v[1] / v[0]
    resultado = {
        'exemplo': 'Comércio / SP / médias e grandes / agosto de 2026',
        'arquivo_fonte': 'scrdata_2026.zip -> scrdata_202608.csv',
        'contagens': contagens, 'linhas_por_porte': por_porte,
        'agregados_conferidos_com_snapshot': True,
        'atual_recalculado_do_bruto': dict(zip(CAMPOS, atual)),
        'maio_sp_do_snapshot': dict(zip(CAMPOS, anterior)),
        'agosto_brasil_do_snapshot': dict(zip(CAMPOS, brasil)),
        'indicadores': {'inadimplencia_pct': taxa(atual), 'inadimplencia_maio_pct': taxa(anterior),
                        'referencia_brasil_pct': taxa(brasil), 'variacao_tres_meses_pp': taxa(atual)-taxa(anterior),
                        'diferenca_brasil_pp': taxa(atual)-taxa(brasil)},
        'nota': 'Agosto/SP foi recalculado do CSV bruto. Maio/SP e agosto/Brasil foram lidos do agregado já incluído no radar. A taxa pertence ao grupo, não a uma empresa.'
    }
    (args.out/'04_calculos_do_radar.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(resultado, ensure_ascii=True, indent=2))

if __name__ == '__main__':
    main()
