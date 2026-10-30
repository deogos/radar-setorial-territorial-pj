"""Small official-format fixtures exercise inclusion, provenance and account meaning."""
import csv
import importlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate
try:
    cvm = importlib.import_module('cvm_universe')
except ModuleNotFoundError:
    cvm = None

CAD_FIELDS = ['CNPJ_CIA', 'DENOM_SOCIAL', 'DENOM_COMERC', 'SIT', 'TP_ENDER',
              'CD_CVM', 'UF', 'MUN', 'SETOR_ATIV', 'DT_INI_SIT']
FCA_FIELDS = ['CNPJ_Companhia', 'Data_Referencia', 'Versao', 'ID_Documento',
              'Descricao_Atividade', 'Pagina_Web']
DOC_FIELDS = ['CNPJ_CIA', 'DT_REFER', 'VERSAO', 'DT_RECEB', 'LINK_DOC', 'ID_DOC']
ACCOUNT_FIELDS = ['CNPJ_CIA', 'DT_REFER', 'VERSAO', 'MOEDA', 'ESCALA_MOEDA',
                  'ORDEM_EXERC', 'DT_INI_EXERC', 'DT_FIM_EXERC', 'CD_CONTA',
                  'DS_CONTA', 'VL_CONTA']


def csv_text(fields, rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


class Fixture:
    def __init__(self, cache):
        self.cache = cache
        self.cad = []
        self.fca = []
        self.docs = {'itr': [], 'dfp': []}
        self.accounts = {}

    def company(self, cnpj, sector='Alimentos', **overrides):
        row = dict.fromkeys(CAD_FIELDS, '')
        row.update(CNPJ_CIA=cnpj, DENOM_SOCIAL='EMPRESA ' + cnpj,
                   SIT='ATIVO', TP_ENDER='SEDE', CD_CVM='123', UF='SP',
                   MUN='São Paulo', SETOR_ATIV=sector, DT_INI_SIT='2020-01-01')
        row.update(overrides)
        self.cad.append(row)

    def general(self, cnpj, version=1, date='2026-01-01'):
        self.fca.append(dict(CNPJ_Companhia=cnpj, Data_Referencia=date,
                             Versao=str(version), ID_Documento=str(100 + version),
                             Descricao_Atividade='Atividade publicada versão ' + str(version),
                             Pagina_Web='www.exemplo.com.br'))

    def document(self, cnpj, date='2026-06-30', version=1, kind='itr'):
        self.docs[kind].append(dict(CNPJ_CIA=cnpj, DT_REFER=date,
                                    VERSAO=str(version), DT_RECEB='2026-10-01',
                                    LINK_DOC='http://cvm.example/doc', ID_DOC=str(version)))

    def account(self, cnpj, code, label, value='2.5', date='2026-06-30',
                version=1, kind='itr', statement='BPA', scope='con',
                start='', order='ÚLTIMO', scale='MIL', currency='REAL'):
        row = dict(CNPJ_CIA=cnpj, DT_REFER=date, VERSAO=str(version),
                   MOEDA=currency, ESCALA_MOEDA=scale, ORDEM_EXERC=order,
                   DT_INI_EXERC=start, DT_FIM_EXERC=date, CD_CONTA=code,
                   DS_CONTA=label, VL_CONTA=value)
        self.accounts.setdefault((kind, statement, scope), []).append(row)

    def balance(self, cnpj, **kwargs):
        self.account(cnpj, '1', 'Ativo Total', **kwargs)
        self.account(cnpj, '2.01', 'Passivo Circulante', statement='BPP', **kwargs)

    def save(self):
        (self.cache / 'cad_cia_aberta.csv').write_text(csv_text(CAD_FIELDS, self.cad), encoding='latin-1')
        with zipfile.ZipFile(self.cache / 'fca_cia_aberta_2026.zip', 'w') as archive:
            archive.writestr('fca_cia_aberta_geral_2026.csv', csv_text(FCA_FIELDS, self.fca).encode('latin-1'))
        for kind, year in [('itr', 2026), ('dfp', 2025)]:
            with zipfile.ZipFile(self.cache / f'{kind}_cia_aberta_{year}.zip', 'w') as archive:
                archive.writestr(f'{kind}_cia_aberta_{year}.csv', csv_text(DOC_FIELDS, self.docs[kind]).encode('latin-1'))
                for (row_kind, statement, scope), rows in self.accounts.items():
                    if row_kind == kind:
                        archive.writestr(f'{kind}_cia_aberta_{statement}_{scope}_{year}.csv',
                                         csv_text(ACCOUNT_FIELDS, rows).encode('latin-1'))


class CompanyUniverseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cache = Path(self.tmp.name)
        self.fixture = Fixture(self.cache)

    def load(self):
        self.assertIsNotNone(cvm, 'The new CVM universe loader is not implemented')
        self.fixture.save()
        return cvm.load_company_universe(self.cache)

    def test_active_head_office_universe_is_deduplicated_without_requiring_fca(self):
        self.fixture.company('11', 'Comércio (Atacado e Varejo)')
        self.fixture.company('11', 'Comércio (Atacado e Varejo)')
        self.fixture.company('22')
        self.fixture.company('33', SIT='CANCELADA')
        self.fixture.company('44', TP_ENDER='FILIAL')
        companies, coverage = self.load()
        self.assertEqual({c['cnpj'] for c in companies}, {'11', '22'})
        self.assertEqual(coverage['total_active'], 2)
        self.assertEqual(coverage['with_fca'], 0)
        self.assertEqual(coverage['financial_missing'], 2)

    def test_missing_sources_stay_explicit_and_questions_have_a_fallback(self):
        self.fixture.company('11', 'Emp. Adm. Part. - Sem Setor Principal')
        companies, _ = self.load()
        company = companies[0]
        self.assertIsNone(company['section'])
        self.assertEqual(company['financial_status'], 'missing')
        self.assertEqual(company['financial'], {})
        for key in ['financial_date', 'financial_version', 'financial_received',
                    'financial_doc', 'financial_scope', 'fca_date', 'fca_version',
                    'fca_document', 'activity', 'website']:
            self.assertIsNone(company[key], key)
        self.assertGreaterEqual(len(company['questions']), 1)
        self.assertFalse(company['mapping_reviewed'])

    def test_editorial_mapping_and_short_name_override_automatic_sector_proposal(self):
        self.fixture.company('84.683.374/0001-49', 'Construção Civil, Mat. Constr. e Decoração')
        self.fixture.company('11', 'Comércio (Atacado e Varejo)')
        companies, coverage = self.load()
        companies = {c['cnpj']: c for c in companies}
        self.assertEqual(companies['84.683.374/0001-49']['name'], 'Tupy')
        self.assertEqual(companies['84.683.374/0001-49']['section'], 'C')
        self.assertTrue(companies['84.683.374/0001-49']['mapping_reviewed'])
        self.assertEqual(companies['11']['section'], 'G')
        self.assertFalse(companies['11']['mapping_reviewed'])
        self.assertIn('proposta', companies['11']['mapping_status'])
        self.assertIn('SETOR_ATIV', companies['11']['mapping_source'])
        self.assertEqual((coverage['mappings_reviewed'], coverage['mappings_proposed']), (1, 1))

    def test_mixed_sector_categories_and_unclassified_holdings_are_unmapped(self):
        categories = ['Construção Civil, Mat. Constr. e Decoração', 'Petróleo e Gás',
                      'Emp. Adm. Part. - Sem Setor Principal', 'Agricultura (Açúcar, Álcool e Cana)',
                      'Emp. Adm. Part. - Const. Civil, Mat. Const. e Decoração',
                      'Emp. Adm. Part. - Petróleo e Gás']
        for index, category in enumerate(categories):
            self.fixture.company(str(index), category)
        companies, coverage = self.load()
        self.assertTrue(all(c['section'] is None for c in companies))
        self.assertEqual(coverage['mappings_missing'], 6)

    def test_fca_latest_version_is_used_without_changing_the_active_cad_universe(self):
        self.fixture.company('11')
        self.fixture.general('11', 1)
        self.fixture.general('11', 3)
        self.fixture.general('22', 9)
        companies, coverage = self.load()
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0]['fca_version'], 3)
        self.assertIn('versão 3', companies[0]['activity'])
        self.assertEqual(coverage['with_fca'], 1)

    def test_latest_usable_document_wins_and_consolidated_is_preferred_within_it(self):
        self.fixture.company('11')
        self.fixture.document('11', version=1)
        self.fixture.balance('11', version=1, value='5')
        self.fixture.document('11', version=2)
        self.fixture.balance('11', version=2, value='7')
        self.fixture.balance('11', version=2, scope='ind', value='99')
        self.fixture.document('11', date='2026-09-30', version=1)
        companies, coverage = self.load()
        company = companies[0]
        self.assertEqual(company['financial_date'], '2026-06-30')
        self.assertEqual(company['financial_version'], 2)
        self.assertEqual(company['financial_scope'], 'consolidated')
        self.assertEqual(company['financial']['1']['value'], 7000)
        self.assertEqual(company['financial_received'], '2026-10-01')
        self.assertTrue(company['financial_doc'].startswith('https://'))
        self.assertEqual(coverage['financial_available'], 1)

    def test_latest_individual_fallback_is_explicit_instead_of_older_consolidated(self):
        self.fixture.company('11')
        self.fixture.document('11', kind='dfp', date='2025-12-31')
        self.fixture.balance('11', kind='dfp', date='2025-12-31', value='1')
        self.fixture.document('11')
        self.fixture.balance('11', scope='ind', value='4')
        companies, _ = self.load()
        self.assertEqual(companies[0]['financial_scope'], 'individual')
        self.assertEqual(companies[0]['financial_date'], '2026-06-30')
        self.assertEqual(companies[0]['financial']['1']['value'], 4000)

    def test_financial_account_values_preserve_labels_zero_scale_and_fiscal_ytd(self):
        self.fixture.company('11')
        self.fixture.document('11')
        self.fixture.balance('11')
        self.fixture.account('11', '3.01', 'Receita de Venda de Bens e/ou Serviços',
                             statement='DRE', start='2025-10-01', value='8.5')
        self.fixture.account('11', '3.01', 'Receita de Venda de Bens e/ou Serviços',
                             statement='DRE', start='2026-04-01', value='3')
        self.fixture.account('11', '3.01', 'Receita de Venda de Bens e/ou Serviços',
                             statement='DRE', start='2025-01-01', value='99', order='PENÚLTIMO')
        self.fixture.account('11', '2.01.04', 'Empréstimos e Financiamentos',
                             statement='BPP', value='0', scale='UNIDADE')
        companies, _ = self.load()
        financial = companies[0]['financial']
        self.assertEqual(financial['3.01']['value'], 8500)
        self.assertEqual(financial['3.01']['start'], '2025-10-01')
        self.assertEqual(financial['3.01']['end'], '2026-06-30')
        self.assertEqual(financial['3.01']['label'], 'Receita de Venda de Bens e/ou Serviços')
        self.assertEqual(financial['3.01']['scale_original'], 'MIL')
        self.assertEqual(financial['2.01.04']['value'], 0)
        self.assertNotIn('6.01', financial)

    def test_financial_sector_is_specialized_even_with_standard_looking_accounts(self):
        self.fixture.company('11', 'Bancos')
        self.fixture.document('11')
        self.fixture.balance('11')
        companies, coverage = self.load()
        self.assertEqual(companies[0]['financial_status'], 'specialized')
        self.assertEqual(companies[0]['financial']['1']['label'], 'Ativo Total')
        self.assertEqual(coverage['financial_specialized'], 1)
        self.assertEqual(coverage['financial_available'], 0)

    def test_financial_cad_sector_guard_does_not_depend_on_editorial_comparison(self):
        self.fixture.company('84.683.374/0001-49', 'Bancos')
        self.fixture.document('84.683.374/0001-49')
        self.fixture.balance('84.683.374/0001-49')
        companies, _ = self.load()
        self.assertEqual(companies[0]['section'], 'C')
        self.assertEqual(companies[0]['financial_status'], 'specialized')

    def test_nonstandard_revenue_or_debt_labels_prevent_standard_financial_classification(self):
        for cnpj in ['11', '22']:
            self.fixture.company(cnpj)
            self.fixture.document(cnpj)
            self.fixture.balance(cnpj)
        self.fixture.account('11', '3.01', 'Receitas de Intermediação Financeira', statement='DRE', start='2026-01-01')
        self.fixture.account('22', '2.01.04', 'Relações Interfinanceiras', statement='BPP')
        companies, coverage = self.load()
        self.assertEqual([c['financial_status'] for c in companies], ['specialized', 'specialized'])
        self.assertEqual(coverage['financial_specialized'], 2)

    def test_unknown_currency_is_rejected_instead_of_mislabeled_as_brl(self):
        self.fixture.company('11')
        self.fixture.document('11')
        self.fixture.balance('11', currency='DOLAR')
        self.assertIsNotNone(cvm, 'The new CVM universe loader is not implemented')
        self.fixture.save()
        with self.assertRaisesRegex(ValueError, 'MOEDA|Moeda|moeda'):
            cvm.load_company_universe(self.cache)

    def test_pipeline_reuses_existing_scr_records_and_publishes_coverage(self):
        self.fixture.company('11')
        self.fixture.save()
        (self.cache / 'manifesto_coleta.json').write_text('[]', encoding='utf-8')
        reuse = self.cache / 'existing.json'
        records = [['2026-08', 'SP', 'C', 'grande', 100, 1, 2, 97, 40, 10, 1]]
        quality = [{'raw_rows': 17, 'pj_rows': 9, 'archive': 'already-checked.zip'}]
        reuse.write_text(json.dumps({'records': records, 'quality': quality}), encoding='utf-8')
        destination = self.cache / 'output'
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/pipeline.py'),
                                 '--cache', str(self.cache), '--out', str(destination),
                                 '--reuse-scr', str(reuse)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads((destination / 'radar.json').read_text(encoding='utf-8'))
        self.assertEqual(payload['records'], records)
        self.assertEqual(payload['quality'], quality)
        self.assertEqual(payload['meta']['company_coverage']['total_active'], 1)

    def test_validator_accepts_missing_financials_and_unmapped_companies(self):
        self.fixture.company('11', 'Emp. Adm. Part. - Sem Setor Principal')
        companies, coverage = self.load()
        payload = {'companies': companies, 'meta': {'company_coverage': coverage}}
        self.assertTrue(callable(getattr(validate, 'company_checks', None)),
                        'Validator still assumes the twelve-company sample')
        checks = validate.company_checks(payload, self.cache)
        self.assertTrue(all(ok for ok, _ in checks), checks)

    def test_validator_compares_cnpj_identities_with_actual_active_cad(self):
        self.fixture.company('11')
        companies, coverage = self.load()
        companies[0]['cnpj'] = '22'
        payload = {'companies': companies, 'meta': {'company_coverage': coverage}}
        self.assertTrue(callable(getattr(validate, 'company_checks', None)),
                        'Validator does not compare the actual CAD universe')
        checks = validate.company_checks(payload, self.cache)
        self.assertTrue(any(not ok and 'CAD' in label for ok, label in checks), checks)

    def test_validator_rejects_a_standard_status_for_specialized_account_labels(self):
        self.fixture.company('11')
        self.fixture.document('11')
        self.fixture.balance('11')
        self.fixture.account('11', '3.01', 'Receitas de Intermediação Financeira', statement='DRE', start='2026-01-01')
        companies, coverage = self.load()
        companies[0]['financial_status'] = 'available'
        coverage.update(financial_available=1, financial_specialized=0)
        payload = {'companies': companies, 'meta': {'company_coverage': coverage}}
        self.assertTrue(callable(getattr(validate, 'company_checks', None)),
                        'Validator lacks financial semantic guards')
        checks = validate.company_checks(payload, self.cache)
        self.assertTrue(any(not ok and 'especializadas' in label for ok, label in checks), checks)


if __name__ == '__main__':
    unittest.main()
