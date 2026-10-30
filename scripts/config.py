"""Parâmetros explícitos do protótipo. Não representam política de crédito."""
SECTORS = {
 'A': ('Agropecuária', 'Agricultura, pecuária, produção florestal, pesca e aquicultura'),
 'B': ('Indústrias extrativas', 'Indústrias extrativas'),
 'C': ('Indústria de transformação', 'Indústrias de transformação'),
 'D': ('Eletricidade e gás', 'Eletricidade e gás'),
 'E': ('Água e resíduos', 'Água, esgoto, atividades de gestão de resíduos e descontaminação'),
 'F': ('Construção', 'Construção'),
 'G': ('Comércio', 'Comércio; reparação de veículos automotores e motocicletas'),
 'H': ('Transporte e logística', 'Transporte, armazenagem e correio'),
 'I': ('Alojamento e alimentação', 'Alojamento e alimentação'),
 'J': ('Informação e comunicação', 'Informação e comunicação'),
 'K': ('Atividades financeiras', 'Atividades financeiras, de seguros e serviços relacionados'),
 'L': ('Atividades imobiliárias', 'Atividades imobiliárias'),
 'M': ('Serviços profissionais', 'Atividades profissionais, científicas e técnicas'),
 'N': ('Serviços administrativos', 'Atividades administrativas e serviços complementares'),
 'O': ('Administração pública', 'Administração pública, defesa e seguridade social'),
 'P': ('Educação', 'Educação'),
 'Q': ('Saúde e serviços sociais', 'Saúde humana e serviços sociais'),
 'R': ('Cultura e recreação', 'Artes, cultura, esporte e recreação'),
 'S': ('Outros serviços', 'Outras atividades de serviços'),
 'T': ('Serviços domésticos', 'Serviços domésticos'),
 'U': ('Organismos internacionais', 'Organismos internacionais e outras instituições extraterritoriais'),
 'NI': ('Atividade não informada', 'Não informados'),
}
STATES = dict(AC='Acre', AL='Alagoas', AP='Amapá', AM='Amazonas', BA='Bahia', CE='Ceará', DF='Distrito Federal', ES='Espírito Santo', GO='Goiás', MA='Maranhão', MT='Mato Grosso', MS='Mato Grosso do Sul', MG='Minas Gerais', PA='Pará', PB='Paraíba', PR='Paraná', PE='Pernambuco', PI='Piauí', RJ='Rio de Janeiro', RN='Rio Grande do Norte', RS='Rio Grande do Sul', RO='Rondônia', RR='Roraima', SC='Santa Catarina', SP='São Paulo', SE='Sergipe', TO='Tocantins')
SIZES = {'Micro':'micro', 'Pequeno':'pequeno', 'Médio':'medio', 'Grande':'grande', 'Indisponível':'ni'}
RULES = {'delta_pp':0.5, 'gap_pp':1.0, 'materiality_brl':100_000_000, 'min_history':4}
# Mapeamento econômico editorial para comparação: não é CNAE cadastral da holding.
# A descrição da atividade, os dados cadastrais e a origem ficam no produto final.
COMPANIES = [
 ('84.683.374/0001-49','Tupy','C','industrial'),
 ('88.611.835/0001-29','Marcopolo','C','industrial'),
 ('84.429.695/0001-11','WEG','C','holding'),
 ('56.720.428/0001-63','Romi','C','industrial'),
 ('92.754.738/0001-62','Lojas Renner','G','varejo'),
 ('47.960.950/0001-21','Magazine Luiza','G','varejo'),
 ('02.387.241/0001-60','Rumo','H','holding'),
 ('02.351.144/0001-18','Tegma','H','logistica'),
 ('08.343.492/0001-20','MRV','F','construcao'),
 ('16.614.075/0001-00','Direcional','F','construcao'),
 ('00.864.214/0001-06','Energisa','D','holding'),
 ('76.483.817/0001-20','Copel','D','holding'),
]
