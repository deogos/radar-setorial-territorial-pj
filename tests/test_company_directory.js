const assert=require('node:assert/strict');
let directory;
try{directory=require('../web/company-directory.js');}catch{}
assert.ok(directory,'A consulta precisa de um módulo para filtrar e paginar todas as companhias.');
const companies=[
 {cnpj:'01.234.567/0001-89',name:'São Bento',legal_name:'São Bento S.A.',uf:'SP',section:'C',cvm_sector:'Metalurgia',mapping_reviewed:true,financial_status:'available'},
 {cnpj:'12.345.678/0001-90',name:'Alfa',legal_name:'Alfa Participações',uf:'MG',section:null,mapping_reviewed:false,financial_status:'missing'},
 {cnpj:'23.456.789/0001-01',name:'Banco Beta',uf:'SP',section:'K',mapping_reviewed:false,financial_status:'specialized'},
 {cnpj:'34.567.890/0001-12',name:'Delta',uf:'PR',section:'D',mapping_reviewed:false,financial_status:'available'}
];
assert.equal(directory.filterCompanies(companies,{query:'sao bento'})[0].cnpj,companies[0].cnpj,'Busca deve ignorar acentos.');
assert.equal(directory.filterCompanies(companies,{query:'01234567000189'})[0].cnpj,companies[0].cnpj,'Busca deve aceitar CNPJ sem pontuação.');
assert.deepEqual(directory.filterCompanies(companies,{mapping:'unmapped'}).map(x=>x.name),['Alfa']);
assert.deepEqual(directory.filterCompanies(companies,{financial:'specialized'}).map(x=>x.name),['Banco Beta']);
assert.deepEqual(directory.filterCompanies(companies,{mapping:'proposed',financial:'available'}).map(x=>x.name),['Delta']);
let p=directory.paginate(directory.filterCompanies(companies,{}),999,3);
assert.equal(p.page,2);assert.equal(p.totalPages,2);assert.equal(p.items.length,1);assert.equal(p.total,4);
p=directory.paginate([],10,25);assert.equal(p.items.length,0);assert.equal(p.total,0);assert.equal(p.page,1);
console.log('Company directory: 7 behavior checks passed.');
