from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
from time import sleep

econodata_url = "https://www.econodata.com.br/empresas/"
print(f"voce deve digitar alguns dados,\n lembre-se:DIGITE CONFORME AS INSTRUÇÕES PARA EVITAR ERROS")
print("antes de começar certifique-se de que esta logado no site econodata,\n para que a consulta seja possivel.")
print("pressione \"enter\" para comecar")
estado = input('digite o estado da pesquisa(abreviado e minusculo)')
cidade = input('digite o nome da cidade(minusculo e sem acento, no lugar do espaço use: -)')
############################################## Definindo variáveis
#estado = "rs"
#cidade = "santo-angelo"
#estadoC = "rio-grande-do-sul"
EconodataSearch = f"{econodata_url}{estado}-{cidade}"
DCSCerealistas = f"https://www.diariocidade.com/{estado}/{cidade}/guia/distribuidoras-de-cereais/"
DCSPostos = f"https://www.diariocidade.com/{estado}/{cidade}/guia/postos-de-combustiveis/"
DCSFrigorificos = f"rs"
EspecificaConsultasPlus = f"https://consultas.plus/lista-de-empresas/"
SetoresAceitos = ['Atacadista de Soja','Atacadista de Defensivos AgrÃ­colas, Adubos, Fertilizantes e Corretivos do Solo','ComÃ©rcio Atacadista de Cereais e Leguminosas Beneficiados','Transporte RodoviÃ¡rio de Carga, Exceto Produtos Perigosos e MudanÃ§as, Intermunicipal, Interestadual e Internacional', 'ComÃ©rcio Varejista de CombustÃ­veis Para VeÃ­culos Automotores', 'Transporte RodoviÃ¡rio de Produtos Perigosos', 'Comércio Varejista de Combustíveis Para Veículos Automotores' ]
final = {}
ua = UserAgent()
############################################## Pegando links
resposta = requests.get(DCSCerealistas)
soup = BeautifulSoup(resposta.text, "html.parser")
elementos = soup.select("a.clearfix")
links1 = [elemento.get("href") for elemento in elementos]
links1.remove('https://www.diariocidade.com')

resposta = requests.get(DCSPostos)
soup = BeautifulSoup(resposta.text, "html.parser")
elementos = soup.select("a.clearfix")
links2 = [elemento.get("href") for elemento in elementos]
links2.remove('https://www.diariocidade.com')
print(links2)
############################################## Verificando os links

for link in links1:
    while(True):
        sleep(0.5)
        headers = {
            'User-Agent': ua.random
        }
        resposta = requests.get(link, headers=headers)
        soup = BeautifulSoup(resposta.text, "html.parser")
        soup.prettify()
        if "Request blocked" in soup.text:
            input("houve um bloqueio de tráfego, use uma VPN para continuar")
       
        else:
            break
    if resposta.url != link:
            print(f"o link:{link}, ignorando e indo para a proxima empresa")
            continue
    dts = soup.select("div.show-all-container dl.dados-empresa dt")
    dds = soup.select("div.show-all-container dl.dados-empresa dd")
    texto = soup.select("section.description.m-top strong")
    setor = texto[1].text
    if any(setorv in setor for setorv in SetoresAceitos) == True:
        for indice, valor in enumerate(dts):
            if dts[indice].text == "CNPJ:":
                CNPJ = dds[indice].text
                texto = soup.select("section.description.m-top strong")
                print(texto[0].text ,f'= CNPJ:{CNPJ}; setor:{texto[1].text} ')
                final[texto[0].text] = [CNPJ]

############################################### Alternando para evitar bloqueio de tráfego                
driver = webdriver.Firefox()
driver.get(EconodataSearch)
sleep(3)
wait = WebDriverWait(driver, 10)

BotaoFecharAnuncio = wait.until(EC.visibility_of_element_located(locator=(By.CSS_SELECTOR, "img.w-5.svg-gray-500.v-lazy-image.v-lazy-image-loaded")))
BotaoFecharAnuncio.click()
sleep(2)
BotaoIndustrias = driver.find_element(by=By.XPATH, value="//span[text()='Maiores indústrias']")
BotaoIndustrias.click()
BotaoIndustrias.click()
sleep(2)
código = driver.page_source
soup = BeautifulSoup(código, "html.parser")

nomes = soup.select('h4.font-normal.text-sm-base.text-ellipsis.overflow-hidden')
CNPJs = soup.select('h4.text-xs')
for indice, valor in enumerate(nomes):
    final[valor.text] = CNPJs[indice].text

driver.quit()
    

############################################ Pegando Postos de combustíveis
for link in links2:
    while(True):
        sleep(0.5)
        headers = {
            'User-Agent': ua.random
        }
        resposta = requests.get(link, headers=headers)
        soup = BeautifulSoup(resposta.text, "html.parser")
        soup.prettify()
        if "Request blocked" in soup.text:
            input("houve um bloqueio de tráfego, use uma VPN para continuar")
        else:
            break
    if resposta.url != link:
            print(f"o link:{link}, ignorando e indo para a proxima empresa")
            continue
    print(link)
    dts = soup.select("div.show-all-container dl.dados-empresa dt")
    dds = soup.select("div.show-all-container dl.dados-empresa dd")
    texto = soup.select("section.description.m-top strong")
    setor = texto[1].text
    if any(setorv in setor for setorv in SetoresAceitos) == True:
        for indice, valor in enumerate(dts):
            if dts[indice].text == "CNPJ:":
                CNPJ = dds[indice].text
                texto = soup.select("section.description.m-top strong")
                print(texto[0].text ,f'= CNPJ:{CNPJ}; setor:{texto[1].text} ')
                final[texto[0].text] = CNPJ
############################################ Unindo copiados ou de mesmo proprietário
with open(f'nomes_e_cnpjs.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write('Todas as maiores indústrias e cerealistas(sem filtros ainda)\n')
    for escrita in final:
        arquivo.write(f"\t\t\t\t {escrita}\n")
        arquivo.write(f"CNPJ: {final[escrita]}\n ")
print("arquivo com os nomes e cnpjs criados com sucesso!")
print(final)