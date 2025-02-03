import pyautogui as pag
import time
from datetime import date
from cv2 import imread
import os
import pandas as pd
import logging
import oracledb
import os
import re

#logging.basicConfig(level=logging.INFO, filename=r"C:/Users/arthur.trento/Desktop/Log/REAVALIAÇÃO_BENS.log", format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M')
logging.basicConfig(level=logging.INFO, filename=r"C:/Reavaliacao_bens/REAVALIAÇÃO_BENS.log", format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M')

###DB PRODUÇÃO
#un = 'xxxxxxxxxxxx'
#pw = 'xxxxxxxxxxxx'
#cs = 'bdarchon.trt1.jus.br:1521/archon'

###DB HOMOLOGAÇÃO
un = 'xxxxxxxxxxxxx'
pw = 'xxxxxxxxxxxxxx'
cs = '10.1.72.88:1521/agorad.trt1.jus.br'

path = r"C:\Program Files\instantclient_21_11"

oracledb.init_oracle_client(lib_dir=path)

df = pd.read_excel('C:/Reavaliacao_bens/REAVALIAÇÃO_BENS.xlsx')

for i in range(len(df)):
    pat = df['Patrimônio'].iloc[i]
    #data = df['Data'].iloc[i]
    anos = df['VIDA ÚTIL REMANESCENTE'].iloc[i]
    valor = df['VALOR'].iloc[i]
    descricao = df['DESCRIÇÃO'].iloc[i]
    pat = str(pat)
    #data = str(data)
    anos = int(anos)
    anos = str(anos)
    descricao = str(descricao)
    valor = str(valor)
    valor = valor.replace(".", ",")   
    
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
                with connection.cursor() as cursor:
                    sql = f"""select count(numero) from "AGORA"."SM_PATR_REAVALIACAO" where numero = '{pat}'"""
                    for r in cursor.execute(sql):
                        count = re.sub('\D', '', str(r))  
                        print(count)   
                        
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            sql = f"""select max(TO_CHAR(data_reaval, 'yyyy/mm/dd')) from "AGORA"."SM_PATR_REAVALIACAO" where numero = '{pat}'"""
            for r in cursor.execute(sql):
                last_reav = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', str(r))     

    time.sleep(3)

    pag.write("1")
    pag.press("Enter")

    pat = int(pat)
    if pat >= 2000000:
        pag.write("n")
    else:
        pag.write("p")
    pat = str(pat)
        
    pag.press("Tab")
    pag.write(pat)
    pag.press("F8")
    pag.hotkey('ctrl', 'PageDown')

    if count == 0:
        pass
    elif count == '1':
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
    elif count == '2':
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
    elif count == '3':
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
    elif count == '4':
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])
        pag.press(["Tab","Tab","Tab"])


    #pag.write(data)
    pag.press("Tab")
    time.sleep(0.2)
    pag.press("F9")
    time.sleep(0.2)
    pag.press("Enter")
    time.sleep(0.2)
    pag.write(anos)
    time.sleep(0.2)
    pag.press("Tab")
    time.sleep(0.2)
    pag.write(valor)
    time.sleep(0.2)
    pag.press("Tab")
    time.sleep(0.2)
    pag.write(descricao)
    time.sleep(0.5)
    pag.click(x=24, y=65) #button='right'
    
    #break

    time.sleep(5)

    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            sql = f"""select max(TO_CHAR(data_reaval, 'yyyy/mm/dd')) from "AGORA"."SM_PATR_REAVALIACAO" where numero = '{pat}' and data_reaval = trunc(sysdate)"""
            for r in cursor.execute(sql):
                salvar_ok = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', str(r))  
                if salvar_ok == 'None':
                    time.sleep(15)
                    for x in cursor.execute(sql):
                        salvar_ok = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', str(x))
                        if salvar_ok == 'None':
                            logging.info(f"Erro ao salvar o patrimônio:{pat}")
                            print(f"Erro ao salvar o patrimônio:{pat}") 
                            exit()
                        else:
                            data_atual = f"{date.today():%Y%m%d}"
                            if last_reav == data_atual:
                                logging.info(f"Já foi reavaliado no périodo: {pat}")
                                print(f"Já foi reavaliado no périodo: {pat}")
                                pag.press("Enter")
                                time.sleep(0.2)
                                pag.hotkey('Alt', 'F4')
                                time.sleep(0.2)
                                pag.press("right")
                                time.sleep(0.2)
                                pag.press("Enter")
                                pag.click(x=378, y=32)
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press("right")
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press("Enter")        
                            else: 
                                pag.press("Enter")
                                time.sleep(0.2)
                                pag.hotkey('Alt', 'F4')
                                time.sleep(0.2)
                                #pag.click(x=388, y=43) #, button='right'
                                pag.click(x=378, y=32)
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press("right")
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press(["down","down","down","down","down"])
                                time.sleep(0.2)
                                pag.press("Enter")
                                print(f"Reavaliado com sucesso: {pat}")
                                logging.info(f"Reavaliado com sucesso: {pat}")
                else:
                    data_atual = f"{date.today():%Y%m%d}"
                    if last_reav == data_atual:
                        logging.info(f"Já foi reavaliado no périodo: {pat}")
                        print(f"Já foi reavaliado no périodo: {pat}")
                        pag.press("Enter")
                        time.sleep(0.2)
                        pag.hotkey('Alt', 'F4')
                        time.sleep(0.2)
                        pag.press("right")
                        time.sleep(0.2)
                        pag.press("Enter")
                        pag.click(x=378, y=32)
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press("right")
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press("Enter")        
                    else: 
                        pag.press("Enter")
                        time.sleep(0.2)
                        pag.hotkey('Alt', 'F4')
                        time.sleep(0.2)
                        #pag.click(x=388, y=43) #, button='right'
                        pag.click(x=378, y=32)
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press("right")
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press(["down","down","down","down","down"])
                        time.sleep(0.2)
                        pag.press("Enter")
                        print(f"Reavaliado com sucesso: {pat}")
                        logging.info(f"Reavaliado com sucesso: {pat}") 
    
    
    
                            
        

    

    
    

    
    
    
    
    
    
    
    
    
    
    

    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    

                        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
						
				
    # break
                      

      

    













