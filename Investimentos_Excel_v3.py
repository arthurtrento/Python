import pandas as pd
from openpyxl import Workbook
import re
import requests
import json

#Alterar incluindo 1 todo mês
#Mês atual Dezembro
CDB_PERC = "100"
CDB_PERC_2 = "99"
DEB_PERC = "98"
DEB_PERC_2 = "97"
FUN_PERC = "95"
FUN_PERC_2 = "94"

dataframe = pd.read_excel('C:/Users/arthur/Desktop/PosicaoDetalhada.xlsx', header=6) # O header é o número do inicio da leitura da linha
#dataframe = pd.read_excel('C:/Users/Arthur/Desktop/PosicaoDetalhada.xlsx', header=6) # O header é o número do inicio da leitura da linha
#dataframe = pd.read_excel('C:/Users/arthur.trento/Desktop/PosicaoDetalhada.xlsx', header=6) # O header é o número do inicio da leitura da linha

dataframe = dataframe.drop(dataframe.iloc[:, 2:41], axis=1) #Exclui as colunas de 2 a 41

dataframe.columns = ['Ativo', 'Posicao'] # Define o nome dos cabeçalhos das colunas

#print(dataframe.head)

titulos = {'NTNB PRINC mai/2045':'', 
'Franklin Valor e Liquidez FVL FIC FIA':'', 'Trend Investback FIC FIRF Simples':'',
'CDB BANCO PAN S/A - JAN/2027':'', 'CDB BMG - AGO/2025':'', 'CDB BANCO MASTER S/A - AGO/2026':'', 
'CDB BANCO MASTER S/A - NOV/2026':'', 'CDB BANCO MASTER S/A - NOV/2030':'', 'CDB BANCO MASTER S/A - MAR/2031':'', 
'CDB BANCO MASTER S/A - OUT/2030':'', 'CDB BANCO MASTER S/A - FEV/2031':'',
'CDB BANCO MASTER S/A - JUL/2029':'',
'DEB MOVIDA - JUN/2032':'', 'DEB PAMPA SUL - OUT/2036':'', 'DEB ROTA DAS BANDEIRAS - JUL/2034':'', 'DEB CSN MINERACAO - JUL/2037':'', 'DEB LITORAL SUL - OUT/2031':'', 
'DEB TAESA - ABR/2032':'', 'DEB ECHOENERGIA - JUN/2030':'',
'CRA BRF - JUL/2030':'', 'CRI SÃO CARLOS - SET/2029':'', 'CRA CARAMURU - JUL/2029':'', 'CRA JBS - ABR/2032':'' }


for x in titulos:

    #Esse bloco de código é usado caso a planilha da XP apresente os valores com string e não como float
    # titulos[x] = dataframe.query('Ativo == @x')[["Posicao"]] # Busca dentro do dataframe a "Posição", referente ao "Ativo" pesquisado 
    # titulos[x] = str(titulos[x])
    # pos = str(re.search("R\$", titulos[x]))   #Retorna uma string com informações do termo "R$" dentro da string
    # pos = (int(pos[28:30]))+1   # Extrai somente a posição do caractere "R$" dentro da string resultante do re.search acima, converte para integer e Adiciona 1 na posição atual (Server para extrair um espação em branco após o $)
    # titulos[x] = titulos[x][pos:] #Copia para dentro de cdb[x] apenas o valor 
    # titulos[x] = re.sub(r"\.", "", titulos[x])  #remove pontos da string
    # titulos[x] = re.sub(r"\,", ".", titulos[x])

    #Precisei alterar o código, pois pelo meu entendimento a planilha da XP passou a mostrar os valores em um formato diferente
    titulos[x] = dataframe.query('Ativo == @x')[["Posicao"]] # Busca dentro do dataframe a "Posição", referente ao "Ativo" pesquisado 
    titulos[x] = str(titulos[x])

    match = re.search(r'R\$\s?([\d.,]+)', titulos[x])
    if match:
        number = match.group(1)  # Pega o número após o R$
        number = number.replace('.', '').replace(',', '') #Extrai pontos e virgulas do número
    if len(number) > 1:
        number = number[:-2] + '.' + number[-2:] #Inclui um ponto antes do penúltimo número da string
    titulos[x] = number    
      
# #####################################################################################################

# #Buscando valor do carro na tabela FIPE

try:
    
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas/25/modelos/9678/anos/2022-1"

    r = requests.request("GET", url, verify = False)

    text = json.loads(r.text)
    valor = text['Valor']
    valor = re.sub(r'R\$', "", valor)
    valor = re.sub(r' ', "", valor)
    valor = re.sub(r'\.', "", valor)

except:
    print("Erro ao baixar dados da API FIPE")
    
# ########################################################################################################

# #Colocando os valores em uma planilha do Excel 

planilha = Workbook()

sheet = planilha.active 

#Títulos de INFLAÇÃO
sheet['A1'] = "CDB BANCO PAN S/A - JAN/2027"
sheet['A2'] = float(titulos['CDB BANCO PAN S/A - JAN/2027'])
sheet['B2'] = f"##((B{CDB_PERC}*100)/B{CDB_PERC_2})-100"
sheet['C1'] = "CDB BMG - AGO/2025"
sheet['C2'] = float(titulos['CDB BMG - AGO/2025'])
sheet['D2'] = f"##((D{CDB_PERC}*100)/D{CDB_PERC_2})-100"
sheet['E1'] = "CDB BMG - AGO/2025"
sheet['E2'] = float(titulos['CDB BANCO MASTER S/A - AGO/2026'])
sheet['F2'] = f"##((F{CDB_PERC}*100)/F{CDB_PERC_2})-100"
sheet['G1'] = "Waiting CDB"
#sheet['G2'] = float(titulos['CDB BMG - NOV/2024'])
#sheet['H2'] = f"##((H{CDB_PERC}*100)/H{CDB_PERC_2})-100"
sheet['I1'] = "Waiting CDB"
#sheet['I2'] = float(titulos['CDB BMG - AGO/2024'])
#sheet['J2'] = f"##((J{CDB_PERC}*100)/J{CDB_PERC_2})-100"

# #Títulos de PRÉ-FIXADOS
sheet['K1'] = "CDB BANCO MASTER S/A - NOV/2026"
sheet['K2'] = float(titulos['CDB BANCO MASTER S/A - NOV/2026'])
sheet['L2'] = f"##((L{CDB_PERC}*100)/L{CDB_PERC_2})-100"
sheet['M1'] = "CDB BANCO MASTER S/A - NOV/2030"
sheet['M2'] = float(titulos['CDB BANCO MASTER S/A - NOV/2030'])
sheet['N2'] = f"##((N{CDB_PERC}*100)/N{CDB_PERC_2})-100"
sheet['O1'] = "CDB BANCO MASTER S/A - MAR/2031"
sheet['O2'] = float(titulos['CDB BANCO MASTER S/A - MAR/2031'])
sheet['P2'] = f"##((P{CDB_PERC}*100)/P{CDB_PERC_2})-100"
sheet['Q1'] = "CDB BANCO MASTER S/A - OUT/2030"
sheet['Q2'] = float(titulos['CDB BANCO MASTER S/A - OUT/2030'])
sheet['R2'] = f"##((R{CDB_PERC}*100)/R{CDB_PERC_2})-100"
sheet['S1'] = "CDB BANCO MASTER S/A - FEV/2031"
sheet['S2'] = float(titulos['CDB BANCO MASTER S/A - FEV/2031'])
sheet['T2'] = f"##((T{CDB_PERC}*100)/T{CDB_PERC_2})-100"

# #Títulos PÒS-FIXADOS
sheet['U1'] = "CDB BANCO MASTER S/A - JUL/2029"
sheet['U2'] = float(titulos['CDB BANCO MASTER S/A - JUL/2029'])
sheet['V2'] = f"##((V{CDB_PERC}*100)/V{CDB_PERC_2})-100"
sheet['W1'] = "Waiting CDB"
#sheet['W2'] = float(titulos['LC WILL FINANCEIRA (MASTER) - DEZ/2024'])
#sheet['X2'] = f"##((X{CDB_PERC}*100)/X{CDB_PERC_2})-100"

# #Debêntures
sheet['A4'] = "DEB ECHOENERGIA - JUN/2030"
sheet['A5'] = float(titulos['DEB ECHOENERGIA - JUN/2030'])
sheet['B5'] = f"##((B{DEB_PERC}*100)/B{DEB_PERC_2})-100"
sheet['C4'] = "CRI SÃO CARLOS - SET/2029"
sheet['C5'] = float(titulos['CRI SÃO CARLOS - SET/2029'])
sheet['D5'] = f"##((D{DEB_PERC}*100)/D{DEB_PERC_2})-100"
sheet['E4'] = "DEB PAMPA SUL - OUT/2036"
sheet['E5'] = float(titulos['DEB PAMPA SUL - OUT/2036'])
sheet['F5'] = f"##((F{DEB_PERC}*100)/F{DEB_PERC_2})-100"
sheet['G4'] = "DEB LITORAL SUL - OUT/2031"
sheet['G5'] = float(titulos['DEB LITORAL SUL - OUT/2031'])
sheet['H5'] = f"##((H{DEB_PERC}*100)/H{DEB_PERC_2})-100"
sheet['I4'] = "CRA JBS - ABR/2032"
sheet['I5'] = float(titulos['CRA JBS - ABR/2032'])
sheet['J5'] = f"##((J{DEB_PERC}*100)/J{DEB_PERC_2})-100"
sheet['K4'] = "DEB TAESA - ABR/2032"
sheet['K5'] = float(titulos['DEB TAESA - ABR/2032'])
sheet['L5'] = f"##((L{DEB_PERC}*100)/L{DEB_PERC_2})-100"
sheet['M4'] = "Waiting DEB"
#sheet['M5'] = float(titulos['DEB RAPOSO TAVARES - CART - DEZ/2024'])
#sheet['N5'] = f"##((N{DEB_PERC}*100)/N{DEB_PERC_2})-100"
sheet['O4'] = "DEB MOVIDA - JUN/2032"
sheet['O5'] = float(titulos['DEB MOVIDA - JUN/2032'])
sheet['P5'] = f"##((P{DEB_PERC}*100)/P{DEB_PERC_2})-100"
sheet['Q4'] = "DEB CSN MINERACAO - JUL/2037"
sheet['Q5'] = float(titulos['DEB CSN MINERACAO - JUL/2037'])
sheet['R5'] = f"##((R{DEB_PERC}*100)/R{DEB_PERC_2})-100"
sheet['S4'] = "DEB ROTA DAS BANDEIRAS - JUL/2034"
sheet['S5'] = float(titulos['DEB ROTA DAS BANDEIRAS - JUL/2034'])
sheet['T5'] = f"##((T{DEB_PERC}*100)/T{DEB_PERC_2})-100"
sheet['U4'] = "CRA CARAMURU - JUL/2029"
sheet['U5'] = float(titulos['CRA CARAMURU - JUL/2029'])
sheet['V5'] = f"##((V{DEB_PERC}*100)/V{DEB_PERC_2})-100"
sheet['W4'] = "CRA BRF - JUL/2030"
sheet['W5'] = float(titulos['CRA BRF - JUL/2030'])
sheet['X5'] = f"##((X{DEB_PERC}*100)/X{DEB_PERC_2})-100"

#Fundos de investimento
sheet['A7'] = "Franklin Valor e Liquidez FVL FIC FIA"
sheet['A8'] = float(titulos['Franklin Valor e Liquidez FVL FIC FIA'])
sheet['B8'] = f"##((B{FUN_PERC}*100)/B{FUN_PERC_2})-100"
sheet['C7'] = "Trend Investback FIC FIRF Simples"
sheet['C8'] = float(titulos['Trend Investback FIC FIRF Simples'])
sheet['D8'] = f"##((H{FUN_PERC}*100)/H{FUN_PERC_2})-100"

#Tesouro direto
sheet['A10'] = "NTNB PRINC mai/2045"
sheet['A11'] = float(titulos['NTNB PRINC mai/2045'])
#sheet['C10'] = "NTNB PRINC ago/2024"
#sheet['C11'] = float(titulos['NTNB PRINC ago/2024'])


#FIPE do carro
sheet['A13'] = "Honda City"
sheet['A14'] = valor

planilha.save("C:/Users/arthur/Desktop/output.xlsx")

            
            














