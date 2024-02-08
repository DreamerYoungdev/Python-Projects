
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
from time import sleep
import csv
ua = UserAgent()
proxies = {'http': 'http://201.91.82.155:3128', 'https': 'https://186.215.87.194:6006'}
cnpjinfo = "http://cnpj.info/"

count = 1
chavepesquisa = {}
grandes = {}
pequenas = {}
medias = {}
micro = {}
grandes = {}
demais = {}
SEnq = {}
no1= {}
no2= {}
no3= {}

with open("nomes_e_cnpjs.txt", 'r') as arquivo:
    for linha in arquivo:
        if count > 1:
            if count % 2 == 0:
                nome = linha.strip()
            else:
                cnpj = linha.strip().replace("[", "").replace('CNPJ: ', '').replace('.', "").replace("/", "").replace("-", "").replace("]", "").replace("'", "")
                chavepesquisa[nome] = cnpj
        count+= 1
print (chavepesquisa)
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\Root\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
driver = uc.Chrome(options=options)
for nome in chavepesquisa:
    setor = "setor nao encontrado"
    endereco = "endereco nao encontrado"
    socios = "socios nao encontrados"
    telefone = "telefone nao encontrado"
    url = "https://cnpj.biz/"+chavepesquisa[nome]
    print(nome,': ')
    sleep(1)
    driver.get(url=url)
    sleep(1)
    if driver.current_url != url:
        print("ocorreu um erro")
        print(url)
        print(driver.current_url)
        no1[nome] = chavepesquisa[nome]
        continue
    resposta = driver.page_source
    soup = BeautifulSoup(resposta, "html.parser")
    ps = soup.select("div.column-1.box p")
    for p in ps:
        if "Porte" in p.text:
            porte = p.select_one('b').text
            print(porte)
        elif "Telefone" in p.text:
            telefones = p.select('b')
            telefone = []
            for i in telefones:
                telefone.append(i.text)
            if telefone == []:
                telefone ="telefone nao encontrado"
        elif "cio-Administrador" in p.text and "Qualifi" not in p.text:
            socios = p.text
            print(socios)
        elif "correspond" in p.text:
            endereco = ""
            tudo = p.select_one('b')
            for i in tudo.text.split("  "):
                endereco += i + ", "
        elif "Tipo" in p.text:
            if  "Matr" in p.select_one("b").text:
                tipo = 'matriz'  
            elif "Fili" in p.select_one("b").text:
                print("nao e matriz entao vou descartando:", nome)
                tipo = "filial"
                break
            else:
                print("alguma coisa deu errado, refazer essa parte")
    if tipo == "filial":
        continue
    setor = soup.select_one('div.col.c12 span b u').text
    if setor == None:
        setor = "setor não encontrado"
    complemento = [chavepesquisa[nome], socios, telefone, endereco, setor]
    print(porte)
    if "Micro" in porte:
        micro[nome] = complemento
    elif "Pequen" in porte:
        pequenas[nome] = complemento
    elif "Medi" in porte:
        medias[nome] = complemento
    elif "Gran" in porte:
        grandes[nome]= complemento
    elif "Dema" in porte:
        demais[nome] = complemento
    elif "Sem En" in porte:
        SEnq[nome] = complemento
    else:
        print("houve um erro ao reconhecer categorias")
driver.quit()
print("micro", micro)
print("pequenas", pequenas)
print("grande", grandes)
print("med", medias)
print("dema", demais)
print("Sem Enq", SEnq)
EconoEmpresas = {} 
for i in SEnq:
    if str(i).isupper():
        EconoEmpresas[i] = SEnq[i]
for i in EconoEmpresas:
    SEnq.pop(i)
with open("nomes_e_cnpjsPlanilha.txt", 'w') as arquivo:
    arquivo.write("-separador-o registro de empresas sera feito com preferencia nas demais, e com dados retirados do Econodata\n, pois ali se relatam as maiores industrias em ordem\n")
    arquivo.write("-separador-Ordem:Empresa:,\t\tCNPJ|\tSocios|\tTelefone|\tEndereço|\tSetor\n")
    arquivo.write("-separadorDM-Demais(Maiores Indústrias)\n")
    for i in EconoEmpresas:
        arquivo.write(f"{i}: \t{EconoEmpresas[i][0]}|{EconoEmpresas[i][1]}|{EconoEmpresas[i][2]}|{EconoEmpresas[i][3]}|{EconoEmpresas[i][4]}\n") 
    arquivo.write("-separadorD-Demais(gerais)\n")
    for i in SEnq:
        arquivo.write(f"{i}: \t{SEnq[i][0]}|{SEnq[i][1]}|{SEnq[i][2]}|{SEnq[i][3]}|{SEnq[i][4]}\n") 
    arquivo.write("-separadorM-Médias\n")
    for i in medias:
        arquivo.write(f"{i}: \t{medias[i][0]}|{medias[i][1]}|{medias[i][2]}|{medias[i][3]}|{medias[i][4]}\n") 
    arquivo.write("-separadorP-Pequenas\n")
    for i in pequenas:
        arquivo.write(f"{i}: \t{pequenas[i][0]}|{pequenas[i][1]}|{pequenas[i][2]}|{pequenas[i][3]}|{pequenas[i][4]}\n") 
    arquivo.write("-separadorMi-Micro\n")
    for i in micro:
        arquivo.write(f"{i}: \t{micro[i][0]}|{micro[i][1]}|{micro[i][2]}|{micro[i][3]}|{micro[i][4]}\n") 