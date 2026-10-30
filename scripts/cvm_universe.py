"""Active CVM issuers, explicit comparison proposals and source-account provenance.

CAD defines inclusion. FCA and financial statements enrich a company but never
remove it. CVM activity categories are economic comparison proposals, not a
confirmation of a company's registered CNAE.
"""
import csv
from decimal import Decimal
import io
from pathlib import Path
import unicodedata
import zipfile

from config import COMPANIES


def _norm(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text or '')
                   if not unicodedata.combining(c)).upper().strip()


# This allow-list deliberately excludes categories spanning multiple CNAE
# sections: construction/materials, oil/gas, sugar/alcohol/cane, water/gas,
# toys/leisure, hospitality/tourism, and holdings without a principal sector.
# Holdings with a principal category inherit only a proposal for that group.
_CATEGORY_SECTIONS = {
    'Energia Elétrica': 'D',
    'Metalurgia e Siderurgia': 'C',
    'Máquinas, Equipamentos, Veículos e Peças': 'C',
    'Máqs., Equip., Veíc. e Peças': 'C',
    'Têxtil e Vestuário': 'C',
    'Farmacêutico e Higiene': 'C',
    'Bebidas e Fumo': 'C',
    'Alimentos': 'C',
    'Petroquímicos e Borracha': 'C',
    'Papel e Celulose': 'C',
    'Embalagens': 'C',
    'Comércio (Atacado e Varejo)': 'G',
    'Serviços Transporte e Logística': 'H',
    'Telecomunicações': 'J',
    'Comunicação e Informática': 'J',
    'Serviços Médicos': 'Q',
    'Educação': 'P',
    'Extração Mineral': 'B',
    'Reflorestamento': 'A',
    'Bancos': 'K',
    'Intermediação Financeira': 'K',
    'Bolsas de Valores/Mercadorias e Futuros': 'K',
    'Seguradoras e Corretoras': 'K',
    'Crédito Imobiliário': 'K',
    'Arrendamento Mercantil': 'K',
    'Securitização de Recebíveis': 'K',
}
CATEGORY_SECTIONS = {_norm(category): section for category, section in _CATEGORY_SECTIONS.items()}
HOLDING_PREFIX = _norm('Emp. Adm. Part. - ')
TARGET_CODES = {'1', '1.01', '1.01.01', '2.01', '2.01.04', '2.02.01', '2.03', '3.01', '3.11', '6.01'}
NORMAL_LABELS = {
    '3.01': {_norm('Receita de Venda de Bens e/ou Serviços')},
    '2.01.04': {_norm('Empréstimos e Financiamentos')},
}
SOURCE_ROOT = 'https://dados.cvm.gov.br/dataset/'
QUESTIONS = {
    'C': ['Como pedidos, utilização da capacidade e margens evoluíram?',
          'Qual a exposição a exportações, câmbio e operações fora da UF?',
          'O cronograma de vencimentos acompanha a geração de caixa?'],
    'G': ['A geração operacional de caixa acompanha estoques e recebíveis?',
          'Qual a concentração regional das vendas e a exposição a crédito ao consumidor?',
          'A renovação de linhas está incorporada nas projeções?'],
    'H': ['Contratos e volumes transportados sustentam a projeção?',
          'Quais corredores e clientes concentram receitas?',
          'Qual a necessidade de investimento e refinanciamento?'],
    'F': ['Qual a velocidade de vendas, distratos e recebimentos?',
          'Como se distribuem os projetos por UF e estágio de obra?',
          'Qual a necessidade de caixa até a conclusão dos projetos?'],
    'D': ['Quais concessões, áreas e atividades concentram o fluxo?',
          'O investimento contratado e os vencimentos cabem na geração de caixa?',
          'Quais premissas regulatórias ou contratuais precisam ser atualizadas?'],
}
GENERIC_QUESTIONS = [
    'Qual a atividade principal e qual grupo de comparação deve ser validado pelo analista?',
    'Quais documentos, períodos e informações individuais ainda precisam ser obtidos?',
    'Como geração de caixa, obrigações e concentração de receitas sustentam a análise?',
]


def _rows(archive, name):
    with archive.open(name) as raw:
        with io.TextIOWrapper(raw, encoding='latin-1', newline='') as stream:
            yield from csv.DictReader(stream, delimiter=';')


def load_active_cad(cache: Path) -> dict:
    """Return each distinct active CNPJ with a SEDE record, independently of FCA."""
    active = {}
    with (cache / 'cad_cia_aberta.csv').open(encoding='latin-1', newline='') as stream:
        for row in csv.DictReader(stream, delimiter=';'):
            if row['SIT'] == 'ATIVO' and row['TP_ENDER'] == 'SEDE':
                # CAD repeats company/address data for different responsible people.
                active.setdefault(row['CNPJ_CIA'], row)
    return active


def _general_records(cache, active):
    records = {}
    with zipfile.ZipFile(cache / 'fca_cia_aberta_2026.zip') as archive:
        for row in _rows(archive, 'fca_cia_aberta_geral_2026.csv'):
            cnpj = row['CNPJ_Companhia']
            if cnpj not in active:
                continue
            key = (row['Data_Referencia'], int(row['Versao']), int(row['ID_Documento']))
            if cnpj not in records or key > records[cnpj][0]:
                records[cnpj] = (key, row)
    return {cnpj: pair[1] for cnpj, pair in records.items()}


def _financial_records(cache, active):
    documents, accounts = {}, {}
    for kind, year in [('dfp', 2025), ('itr', 2026)]:
        with zipfile.ZipFile(cache / f'{kind}_cia_aberta_{year}.zip') as archive:
            for row in _rows(archive, f'{kind}_cia_aberta_{year}.csv'):
                cnpj = row['CNPJ_CIA']
                if cnpj in active:
                    key = (cnpj, row['DT_REFER'], int(row['VERSAO']), kind)
                    # Repeated document rows have the same identity; keep the last
                    # receipt if an upstream archive contains duplicate metadata.
                    if key not in documents or row['DT_RECEB'] > documents[key]['DT_RECEB']:
                        documents[key] = row
            names = set(archive.namelist())
            for scope in ['con', 'ind']:
                for statement in ['BPA', 'BPP', 'DRE', 'DFC_MI', 'DFC_MD']:
                    name = f'{kind}_cia_aberta_{statement}_{scope}_{year}.csv'
                    if name not in names:
                        continue
                    for row in _rows(archive, name):
                        cnpj, code = row['CNPJ_CIA'], row['CD_CONTA']
                        if (cnpj not in active or code not in TARGET_CODES
                                or _norm(row['ORDEM_EXERC']) != 'ULTIMO'
                                or row['DT_FIM_EXERC'] != row['DT_REFER']):
                            continue
                        start = row.get('DT_INI_EXERC') or None
                        if statement in ['DRE', 'DFC_MI', 'DFC_MD'] and not start:
                            continue
                        key = (cnpj, row['DT_REFER'], int(row['VERSAO']), kind, scope)
                        selected = accounts.setdefault(key, {})
                        previous = selected.get(code)
                        # DRE can publish both quarter and year-to-date rows marked
                        # ULTIMO. The earliest current-exercise start is the YTD
                        # period; it also supports fiscal years starting after Jan 1.
                        if previous is None or (start and start < (previous.get('DT_INI_EXERC') or '9999')):
                            selected[code] = row
    return documents, accounts


def _usable(accounts):
    # A document index entry alone is not evidence of usable financial accounts.
    # A partial balance remains usable; absent indicators are never filled by zero.
    return '1' in accounts and bool({'2.01', '2.03', '3.01', '6.01'} & accounts.keys())


def financial_requires_specialized(company):
    """Economic comparison choice cannot override source financial semantics."""
    category = _norm(company.get('cvm_sector'))
    if category.startswith(HOLDING_PREFIX):
        category = category[len(HOLDING_PREFIX):].strip()
    financial = company.get('financial', {})
    return (company.get('section') == 'K' or CATEGORY_SECTIONS.get(category) == 'K'
            or any(code in financial and _norm(financial[code]['label']) not in labels
                   for code, labels in NORMAL_LABELS.items()))


def _mapping(cnpj, category, editorials):
    if cnpj in editorials:
        _, name, section, profile = editorials[cnpj]
        note = ('Referência econômica do grupo consolidado; a seção selecionada é um mapeamento analítico documentado, '
                'não o CNAE cadastral confirmado da holding.' if profile == 'holding' else
                'Mapeamento analítico da atividade descrita no FCA para a seção do grupo de comparação. '
                'Não representa consulta ao CNAE cadastral da Receita.')
        return name, section, profile, True, 'config.COMPANIES: revisão editorial', 'mapeamento econômico editorial', note
    normalized = _norm(category)
    is_holding = normalized.startswith(HOLDING_PREFIX)
    principal = normalized[len(HOLDING_PREFIX):].strip() if is_holding else normalized
    section = CATEGORY_SECTIONS.get(principal)
    source = 'CAD CVM SETOR_ATIV: ' + category
    if section:
        note = ('Proposta automática de comparação econômica pela categoria setorial da CVM'
                + (' do grupo investido' if is_holding else '')
                + '; depende de validação do analista e não confirma CNAE cadastral.')
        status = 'proposta automática a validar'
    else:
        note = ('Categoria CVM ampla, mista ou sem setor principal; a seção de comparação depende '
                'de análise da atividade. CNAE cadastral não consultado.')
        status = 'sem mapeamento'
    return None, section, 'holding' if is_holding else 'companhia', False, source, status, note


def load_company_universe(cache: Path) -> tuple[list[dict], dict]:
    """Enrich all active headquarters, keeping missing and specialized data explicit."""
    cache = Path(cache)
    active = load_active_cad(cache)
    general = _general_records(cache, active)
    documents, accounts = _financial_records(cache, active)
    candidates = {}
    for key, rows in accounts.items():
        if key[:4] in documents and _usable(rows):
            candidates.setdefault(key[0], []).append(key)
    editorials = {company[0]: company for company in COMPANIES}
    result = []
    for cnpj, cad in active.items():
        fca = general.get(cnpj, {})
        name, section, profile, reviewed, mapping_source, mapping_status, note = _mapping(
            cnpj, cad.get('SETOR_ATIV', ''), editorials)
        company = {
            'cnpj': cnpj, 'name': name or cad.get('DENOM_COMERC') or cad['DENOM_SOCIAL'],
            'legal_name': cad['DENOM_SOCIAL'], 'cvm_code': int(cad['CD_CVM']),
            'uf': cad.get('UF') or None, 'city': cad.get('MUN') or None,
            'cvm_sector': cad.get('SETOR_ATIV') or None, 'section': section,
            'activity': fca.get('Descricao_Atividade') or None,
            'fca_date': fca.get('Data_Referencia') or None,
            'fca_version': int(fca['Versao']) if fca else None,
            'fca_document': fca.get('ID_Documento') or None,
            'website': fca.get('Pagina_Web') or None,
            'mapping_note': note, 'mapping_status': mapping_status,
            'mapping_reviewed': reviewed, 'mapping_source': mapping_source,
            'profile': profile, 'questions': list(QUESTIONS.get(section, GENERIC_QUESTIONS)),
            'financial_status': 'missing', 'financial_scope': None,
            'financial_date': None, 'financial_version': None,
            'financial_received': None, 'financial_doc': None, 'financial': {},
            'sources': {'cad': SOURCE_ROOT + 'cia_aberta-cad',
                        'fca': SOURCE_ROOT + 'cia_aberta-doc-fca', 'financial': None},
        }
        if cnpj in candidates:
            # Newest usable reference/version first; consolidated wins ties only.
            latest = max(candidates[cnpj], key=lambda key: (key[1], key[2], key[4] == 'con'))
            document = documents[latest[:4]]
            raw_accounts = accounts[latest]
            financial = {}
            for code, row in raw_accounts.items():
                if row['MOEDA'] != 'REAL':
                    raise ValueError(f'Moeda CVM não suportada: {cnpj} / {row["MOEDA"]}')
                if row['ESCALA_MOEDA'] not in ['MIL', 'UNIDADE']:
                    raise ValueError(f'Escala CVM não suportada: {cnpj} / {row["ESCALA_MOEDA"]}')
                multiplier = 1000 if row['ESCALA_MOEDA'] == 'MIL' else 1
                financial[code] = {
                    'value': float(Decimal(row['VL_CONTA']) * multiplier),
                    'label': row['DS_CONTA'], 'start': row.get('DT_INI_EXERC') or None,
                    'end': row['DT_FIM_EXERC'], 'scale_original': row['ESCALA_MOEDA'],
                }
            company['financial'] = financial
            specialized = financial_requires_specialized(company)
            company.update(
                financial_status='specialized' if specialized else 'available',
                financial_scope='consolidated' if latest[4] == 'con' else 'individual',
                financial_date=latest[1], financial_version=latest[2],
                financial_received=document.get('DT_RECEB') or None,
                financial_doc=(document.get('LINK_DOC') or '').replace('http:', 'https:') or None,
                financial=financial,
            )
            company['sources']['financial'] = SOURCE_ROOT + 'cia_aberta-doc-' + latest[3]
        result.append(company)
    editorial_order = {company[0]: index for index, company in enumerate(COMPANIES)}
    result.sort(key=lambda company: (editorial_order.get(company['cnpj'], len(COMPANIES)),
                                     _norm(company['name']), company['cnpj']))
    coverage = {
        'total_active': len(result),
        'with_fca': sum(company['fca_date'] is not None for company in result),
        'financial_available': sum(company['financial_status'] == 'available' for company in result),
        'financial_specialized': sum(company['financial_status'] == 'specialized' for company in result),
        'financial_missing': sum(company['financial_status'] == 'missing' for company in result),
        'mappings_reviewed': sum(company['mapping_reviewed'] for company in result),
        'mappings_proposed': sum(company['section'] is not None and not company['mapping_reviewed'] for company in result),
        'mappings_missing': sum(company['section'] is None for company in result),
    }
    return result, coverage
