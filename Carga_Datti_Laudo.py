from redmail import EmailSender
import pandas as pd
import oracledb
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import logging
from datetime import datetime
import API_GLPI_PROD

logging.basicConfig(level=logging.INFO, filename=r"C:/_PYTHON/carga_Datti_Laudo/Log/Logs.log", format="%(asctime)s - %(levelname)s - %(message)s") #Servidor DATTI

#Configuração do BD Oracle
un = 'xxxxxx'
pw = 'xxxxxxxxx'
cs = 'bdarchon.trt1.jus.br:1521/archon'
#d = r"C:\Program Files\instantclient_21_11" 
d = r"C:\Program Files\instantclient" #Padronizar o nome "instantclient" em todas as máquinas
oracledb.init_oracle_client(lib_dir=d)

#Função para enviar e-mail quando não houver bens na carga da DATTI-LAUDO
def send_email_empty():
        # Configure the sender
        email = EmailSender(
        host="mxg.trt1.jus.br", 
        port=587,
        #username='me@example.com',
        #password='<PASSWORD>'
        )
        # Send an email:
        email.send(
            subject=f"Relatório de Bens na carga - DATTI LAUDO",
            sender="datti@trt1.jus.br",
            receivers=['datti@trt1.jus.br'], #['arthur.trento@trt1.jus.br'],  
            text= "Relatório de Bens na carga - DATTI LAUDO",
            html= """
           <br>
           <h3> Não há bens na carga da DATTI-LAUDO. </h3>
           <br>
            """      
      )

#Funçao para envio de e-mail quando houves bens na carga da DATTI-LAUDO
def send_email_full(df):
        # Configure the sender
        email = EmailSender(
        host="mxg.trt1.jus.br", 
        port=587,
        #username='me@example.com',
        #password='<PASSWORD>'
        )
        # Send an email:
        email.send(
            subject=f"Relatório de Bens na carga - DATTI LAUDO",
            sender="datti@trt1.jus.br",
            receivers=['vlaraujo@stefanini.com, divat@trt1.jus.br, fcfernandes@stefanini.com, datti@trt1.jus.br'], #['arthur.trento@trt1.jus.br'],#   
            text= "Relatório de Bens na carga - DATTI LAUDO",
            html= """
           Prezados,
           <br>
           <br>
           Detectamos as seguintes bens na carga da DATTI LAUDO, sugerimos que esses bens sejam enviados para a DIVAT o mais rápido possível.
           <br>
           <br>
           Segue em anexo o arquivo com os bens na carga.
           <br>
           <br>
            """, 
            attachments={
                'Carga_Datti_Laudo.xlsx': df
                        }                
            )
                
# Query do BD para extrair bens na carga da DATTI-LAUDO
query = '''
SELECT                         --- Patrimonios distribuidos, com e sem transferencia pendente.
TO_CHAR(P.NUMERO) "Patrimônio",
NVL(ULTIMO_HISTPATR.SETOR, '(Não disponível)')"Setor", 
TO_CHAR(P.FLEX_CAMPO_08) "Localidade",
SUBSTR(P.DESCRICAO,1,80) "Descrição",
P.FLEX_CAMPO_03 "Modelo",
TO_CHAR(P.FLEX_CAMPO_02) "N. de Série",
P.FLEX_CAMPO_05 "Tipo Bem",
P.FLEX_CAMPO_04 "Status",
NVL(TRIM(TRANSF_PEND.NUM_ENVIO), 'Não') "Existe Transferência Pendente",
NVL(TO_CHAR(TRANSF_PEND.DATA_ENVIO,'DD/MM/YYYY')
    ,'(Não se aplica)')"Data Envio",
NVL(TRIM(TRANSF_PEND.SETOR_LOCAL_ORIGEM),'(Não se aplica)') "Setor | Localidade Origem",
NVL(TRIM(TRANSF_PEND.SETOR_LOCAL_DESTINO),'(Não se aplica)') "Setor | Localidade Destino",
TO_CHAR(P.DATA_ULT_ATUALIZ, 'dd/mm/yyyy') "Última atualização"
FROM AGORA.SM_PATRIMONIOS P
     LEFT JOIN ( SELECT SITP.NUMPATR,
                        SITP.NUMTRANSF NUM_ENVIO,
                        STP.DATA_ENVIO,
                        STP.SETOR_ORIGEM || ' | ' || STP.FLEX_CAMPO_02 SETOR_LOCAL_ORIGEM,
                        STP.SETOR_DESTINO || ' | ' || STP.FLEX_CAMPO_03 SETOR_LOCAL_DESTINO
                 FROM AGORA.SM_TRANSFPEND STP
                      INNER JOIN AGORA.SM_IT_TRANSFPEND SITP
                        ON SITP.NUMTRANSF = STP.NUMTRANSF
                      WHERE STP.FLG_CONSOL <> 'S'
                 ) TRANSF_PEND 
           ON ( TRANSF_PEND.NUMPATR = P.NUMERO)
     LEFT JOIN (SELECT H.SETOR,
                       H.NUMPATR,
                       H.DATA,
                       H.NUMTRANSF
			FROM AGORA.SM_HISTPATR H,
			(SELECT MAX(SEQ) MAX_SEQ,
			        NUMPATR,
			        GESTOR,
			        TIPO
			        FROM AGORA.SM_HISTPATR
			        GROUP BY NUMPATR,GESTOR,TIPO) ULT_H 
			WHERE H.SEQ = ULT_H.MAX_SEQ
			AND H.NUMPATR = ULT_H.NUMPATR
			AND H.GESTOR = ULT_H.GESTOR
			AND H.TIPO = ULT_H.TIPO
			AND ( H.FLG_ESTORNADO <> 'S' OR H.FLG_ESTORNADO IS NULL)) ULTIMO_HISTPATR
		ON (P.NUMERO = ULTIMO_HISTPATR.NUMPATR)
WHERE  P.FLEX_CAMPO_08 = 'Fórum Ministro Arnaldo Süssekind - 12º andar - Sala da DATTI - Terceirizados - Laudo - ala norte'
AND ULTIMO_HISTPATR.SETOR = 'DATTI'
'''

#Cria um Dataframe vazio
df = pd.DataFrame()

#Cria uma planilha XLSX
planilha = Workbook()
sheet = planilha.active

#Execução da Query SQL do Agora
with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            for r in cursor.execute(query):
                df2 = pd.DataFrame({'Patrimonio':[r[0]],
                  'Setor':[r[1]],
                  'Localidade':[r[2]],
                  'Descrição':[r[3]],
                  'Modelo':[r[4]],
                  'N. de Série':[r[5]],
                  'Tipo Bem':[r[6]],
                  'Status':[r[7]],
                  'Existe Transferência Pendente':[r[8]],
                  'Data Envio':[r[9]],
                  'Setor - Localidade Origem Setor':[r[10]],
                  'Setor - Localidade Destino':[r[11]],
                  'Última atualização':[r[12]]        
                })
                df = pd.concat([df, df2], ignore_index=True)

 # Obter o dia da semana atual (0 = Segunda, 6 = Domingo)
hoje = datetime.now().weekday()

# Verificar se hoje é sexta-feira, os e-mails só são enviados na sexta
if hoje == 4:    
    #Verifica se o Dataframe está vazio ou não para tomar as decisões
    if df.empty == False:  #Se o Dataframe não estiver vazio 
        try:
            for x in dataframe_to_rows(df, index=True, header=True):
                sheet.append(x)
            planilha.save("C:/_PYTHON/carga_Datti_Laudo/Relatório/Carga_Datti_Laudo.xlsx")
            logging.info(f'Planilha criada com sucesso!')
        except:
            logging.info(f'Falha ao criar planilha')
        try:
            send_email_full(df)
            logging.info(f'E-mail enviado com sucesso!')
        except:
            logging.info(f'Falha ao enviar e-mail!')      
    else:   #Se o Dataframe estiver vazio
        logging.info(f'Nenhum bem na carga da DATTI-LAUDO')
        send_email_empty()
else:
     pass

#Criação de chamados no GLPI 

if hoje < 5:

    session_token = API_GLPI_PROD.open_session()

    if df.empty == False:  #Se o Dataframe não estiver vazio
        try: 
            #Criando o Ticket
            ticket_id = API_GLPI_PROD.create_ticket(session_token, "Bens carga DATTI_LAUDO", "Início da verificação de bens na carga da DATTI_LAUDO")
            #Adicionando uma nota
            API_GLPI_PROD.add_followup(session_token, ticket_id, "Detectamos bens na carga da DATTI LAUDO, planilha de bens gerada e enviada por e-mail para tratamento.")
            #Solucionado o Ticket
            API_GLPI_PROD.solve_ticket(session_token, ticket_id)
            logging.info(f'Bens localizados, chamado criado') 
        except:
            logging.info(f'Falha na criação do chamado - Bens localizados')
    else:
        try: 
            #Criando o Ticket
            ticket_id = API_GLPI_PROD.create_ticket(session_token, "Bens carga DATTI_LAUDO", "Início da verificação de bens na carga da DATTI_LAUDO")
            #Adicionando uma nota
            API_GLPI_PROD.add_followup(session_token, ticket_id, "Nenhum bem na carga da DATTI-LAUDO, não há ações a serem tomadas.")
            #Solucionado o Ticket
            API_GLPI_PROD.solve_ticket(session_token, ticket_id)
            logging.info(f'Nenhum bem localizado, chamado criado') 
        except:
            logging.info(f'Falha na criação do chamado - Nenhum bem localizado')

    API_GLPI_PROD.close_session(session_token)           
    
                
                


