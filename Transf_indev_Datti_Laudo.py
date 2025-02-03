from redmail import EmailSender
from datetime import date
import logging
import oracledb
import pandas as pd
from datetime import datetime
import API_GLPI_PROD

un = 'xxxxxxxxxx'
pw = 'xxxxxxxxxx'
cs = 'bdarchon.trt1.jus.br:1521/archon'

#d = r"C:\Program Files\instantclient_21_11"
d = r"C:\Program Files\instantclient"

oracledb.init_oracle_client(lib_dir=d)


logging.basicConfig(level=logging.INFO, filename=r"C:/_PYTHON/transf_indev_datti_laudo/Log/Logs_transf_indev.log", format="%(asctime)s - %(levelname)s - %(message)s")
#logging.basicConfig(level=logging.INFO, filename=r"C:/Users/arthu/Desktop/Logs_transf_indev.log", format="%(asctime)s - %(levelname)s - %(message)s")
#logging.basicConfig(level=logging.INFO, filename=r"C:/Users/arthur.trento/Desktop/Logs_transf_indev.log", format="%(asctime)s - %(levelname)s - %(message)s")


query_sel = '''
            SELECT
                TO_CHAR(P.NUMERO) "Patrimônio",
                NVL(ULTIMO_HISTPATR.SETOR, '(Não disponível)')"Setor", 
                TO_CHAR(P.FLEX_CAMPO_08) "Localidade",
                P.FLEX_CAMPO_03 "Modelo",
                P.DESCRICAO "Descrição",
                NVL(TRIM(TRANSF_PEND.SETOR_LOCAL_DESTINO),'(Não se aplica)') "Setor | Localidade Destino",
                TRANSF_PEND.DATA_CRIACAO "Data Criação Transf."
                FROM AGORA.SM_PATRIMONIOS P
                    LEFT JOIN ( SELECT SITP.NUMPATR,
                                        SITP.NUMTRANSF NUM_ENVIO,
                                        STP.DATA_ENVIO,
                                        STP.SETOR_ORIGEM || ' | ' || STP.FLEX_CAMPO_02 SETOR_LOCAL_ORIGEM,
                                        STP.SETOR_DESTINO || ' | ' || STP.FLEX_CAMPO_03 SETOR_LOCAL_DESTINO,
                                        TO_CHAR(STP.DATA_CRIACAO,'dd/mm/yyyy') DATA_CRIACAO
                                FROM AGORA.SM_TRANSFPEND STP
                                    INNER JOIN AGORA.SM_IT_TRANSFPEND SITP
                                        ON SITP.NUMTRANSF = STP.NUMTRANSF
                                     WHERE STP.DATA_CRIACAO > (SELECT SYSDATE -1 FROM DUAL)
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
                WHERE TRANSF_PEND.SETOR_LOCAL_DESTINO NOT LIKE '%DIVAT%'
                AND ULTIMO_HISTPATR.SETOR = 'DATTI'
            
'''

count = 0
fails = []

try:
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            for r in cursor.execute(query_sel):
                #print(r)
                r = list(r)
                fails.append(r)
                if r != None:
                    count = count + 1

    print(count)
    
    df = pd.DataFrame.from_dict(fails)
    
    print(df)
    
except:
    logging.info("Falha na conexão DB Oracle")


if count > 0:
    # Configure the sender#
    email = EmailSender(
    host="mxg.trt1.jus.br", 
    port=587,
    #username='me@example.com',
    #password='<PASSWORD>'
    )

    try:
        # Send an email:
        email.send(
        subject="Movimentações no setor DATTI",
        sender="datti@trt1.jus.br",
        receivers=['datti@trt1.jus.br'],                     #['datti@trt1.jus.br'],
        # attachments={
        # 'transf.xlsx': pd.DataFrame(data=fails, index=[0])
        # },
        text= " ",
        html= """

        <h1> Transferências setor DATTI: </h1>
        <h4> Foram localizadas transferências do setor DATTI para localidade diversa da DIVAT </h4> 
        <h4> Patrimônio - Setor - Localidade - Modelo - Descrição - Setor(Localidade Destino) - Data Criação Transf. </h4>
        
        """,
        attachments={ 'Transf_Datti_Laudo.xlsx': df }             
    )
        print('Enviando e-mail')
    except:
        logging.info("Falha no envio do e-mail")
else:
    pass

#Criação de chamados no GLPI 

# Obter o dia da semana atual (0 = Segunda, 6 = Domingo)
hoje = datetime.now().weekday()

if hoje < 5:

    session_token = API_GLPI_PROD.open_session()

    if count > 0:
        try: 
            #Criando o Ticket
            ticket_id = API_GLPI_PROD.create_ticket(session_token, "Movimentações no setor DATTI", "Início da verificação das transferências do setor DATTI")
            #Adicionando uma nota
            API_GLPI_PROD.add_followup(session_token, ticket_id, "Foram localizadas transferências do setor DATTI para localidade diversa da DIVAT, e-mail enviado para tratamento.")
            #Solucionado o Ticket
            API_GLPI_PROD.solve_ticket(session_token, ticket_id)
            logging.info(f'Tranferências inconsistentes localizadas, chamado criado') 
        except:
            logging.info(f'Falha na criação do chamado - Tranferências inconsistentes localizadas')
    else:
        try: 
            #Criando o Ticket
            ticket_id = API_GLPI_PROD.create_ticket(session_token, "Movimentações no setor DATTI", "Início da verificação das transferências do setor DATTI")
            #Adicionando uma nota
            API_GLPI_PROD.add_followup(session_token, ticket_id, "Nenhuma transferência do setor DATTI para localidade diversa da DIVAT, não há ações a serem tomadas.")
            #Solucionado o Ticket
            API_GLPI_PROD.solve_ticket(session_token, ticket_id)
            logging.info(f'Nenhuma transferência inconsitente localizada, chamado criado') 
        except:
            logging.info(f'Falha na criação do chamado - Nenhuma transferência inconsistente')

logging.info("Concluído")
