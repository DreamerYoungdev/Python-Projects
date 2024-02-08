import openpyxl
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
EconoEmpresas = {}
SEnq = {}
medias = {}
pequenas = {}
micro = {}
count =""
print("iniciando processo de leitura...")
with open('nomes_e_cnpjsPlanilha.txt', 'r') as arquivo:
    for linha in arquivo:
        if "-separador-" in linha:
            continue
        elif "-separadorDM" in linha:
            count = "DM"
            continue
        elif "-separadorD-" in linha:
            count = "D"
            continue
        elif "-separadorM-" in linha:
            count = "M"
            continue
        elif "-separadorP" in linha:
            count = "P"
            continue
        elif "-separadorMi" in linha:
            count = "Mi"
            continue
        if count == "DM":
            partes = linha.split(":")
            nome = partes[0]
            complemento = partes[1].strip().split("|")
            for i in range(len(complemento)):
                complemento[i] = complemento[i].strip()
            EconoEmpresas[nome] = complemento
        elif count == "D":
            partes = linha.split(":")
            nome = partes[0]
            complemento = partes[1].strip().split("|")
            for i in range(len(complemento)):
                complemento[i] = complemento[i].strip()
            SEnq[nome] = complemento
        elif count == "M":
            partes = linha.split(":")
            nome = partes[0]
            complemento = partes[1].strip().split("|")
            for i in range(len(complemento)):
                complemento[i] = complemento[i].strip()
            medias[nome] = complemento
        elif count == "P":
            partes = linha.split(":")
            nome = partes[0]
            complemento = partes[1].strip().split("|")
            for i in range(len(complemento)):
                complemento[i] = complemento[i].strip()
            pequenas[nome] = complemento
        elif count == "Mi":
            partes = linha.split(":")
            nome = partes[0]
            complemento = partes[1].strip().split("|")
            for i in range(len(complemento)):
                complemento[i] = complemento[i].strip()
            micro[nome] = complemento
#print(EconoEmpresas)
print("organizando para escrever na planilha")
doc = Workbook()
planilha = doc.active
dados = [['Empresa','CNPJ','Socios','Telefone','Endereço','Setor', "Porte"]]

for i in EconoEmpresas:
    arrayfinal = []
    nome = i
    arrayfinal.append(nome)
    complemento = EconoEmpresas[i]
    for o in complemento:
        arrayfinal.append(o)
    arrayfinal.append('demais')
    dados += [arrayfinal]
for i in SEnq:
    arrayfinal = []
    nome = i
    arrayfinal.append(nome)
    complemento = SEnq[i]
    for o in complemento:
        arrayfinal.append(o)
    arrayfinal.append('demais')
    dados += [arrayfinal]
for i in medias:
    arrayfinal = []
    nome = i
    arrayfinal.append(nome)
    complemento = medias[i]
    for o in complemento:
        arrayfinal.append(o)
    arrayfinal.append('medias')
    dados += [arrayfinal]

for i in pequenas:
    if len(dados) < 15:
        arrayfinal = []
        nome = i
        arrayfinal.append(nome)
        complemento = pequenas[i]
        for o in complemento:
            arrayfinal.append(o)
        arrayfinal.append('pequenas')
        dados += [arrayfinal]
for i in micro:
    if len(dados) < 15:
        arrayfinal = []
        nome = i
        arrayfinal.append(nome)
        complemento = micro[i]
        for o in complemento:
            arrayfinal.append(o)
        arrayfinal.append('micro')
        dados += [arrayfinal]
print(dados)
for row_data in dados:
    planilha.append(row_data)
table = Table(displayName="MeusDados", ref=f"A1:G{len(dados) + 1}")
style = TableStyleInfo(
    name="TableStyleMedium9", showFirstColumn=False,
    showLastColumn=False, showRowStripes=True, showColumnStripes=True
)
table.tableStyleInfo = style     

# Adicionar a tabela à planilha
planilha.add_table(table)
nome = input("digite um nome para a planilha:")
# Salvar a planilha em um arquivo
doc.save(filename=f"{nome}.xlsx")