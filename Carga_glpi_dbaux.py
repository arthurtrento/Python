#Criação tabela "DATTI"."ATEND_GLPI_ABERTURA_NOTAS" no Oracle BDAUX
'''
CREATE TABLE DATTI.ATEND_GLPI_ABERTURA_NOTAS (
    Ticket VARCHAR(15),                   --Número do ticket
    Data_modificacao TIMESTAMP,            -- Armazena data e hora
    ID_usuario VARCHAR(15),                     -- Identificador do usuário
    Login VARCHAR2(50),                   -- Nome de login do usuário
    Localizacao_Ergon VARCHAR2(255),       -- Localização no sistema Ergon
    Localizacao_AD VARCHAR2(255),           -- Localização no Active Directory (AD)
    Tipo VARCHAR(15)                     --tipo de alteração/modificação
  );
'''

#Criação VIEW VW_GLPI_INFO_ATENDIMENTOSidor
'''
CREATE OR REPLACE VIEW VW_GLPI_INFO_ATENDIMENTOS AS
	SELECT TIPO,
	TRIM(TICKET) AS TICKET,
	DATA_MODIFICACAO AS DATA_MODIFICAÇÃO,
	ID_USUARIO,
	LOGIN
	FROM DATTI.ATEND_GLPI_ABERTURA_NOTAS
	WITH READ ONLY;
'''

# Instrução para grant:
#GRANT SELECT ON DATTI.VW_GLPI_INFO_ATENDIMENTOS TO smd_consulta;


#Instalar a library mysql-connector-python
#Se o Python estiver travando na execução, pode ser a versão da library

import mysql.connector
from redmail import EmailSender
import oracledb
import logging

logging.basicConfig(level=logging.INFO, filename=r"C:/_PYTHON/carga_glpi_bdaux_info_atendimentos/Log/Logs.log", format="%(asctime)s - %(levelname)s - %(message)s") #Servidor DATTI

#Função para enviar e-mail quando houver falha na carga/acesso do DB
def send_email():
        # Configure the sender
        email = EmailSender(
        host="mxg.trt1.jus.br", 
        port=587,
        #username='me@example.com',
        #password='<PASSWORD>'
        )
        # Send an email:
        email.send(
            subject=f"Falha - Carga dados GLPI (Abertura e notas incluídas) -> Oracle BD AUX",
            sender="datti@trt1.jus.br",
            receivers=['datti@trt1.jus.br'], #['arthur.trento@trt1.jus.br'],  
            text= "Falha - Carga dados GLPI (Abertura e notas de chamados) -> Oracle BD AUX",
            html= """
           <br>
           <h3> Verificar a carga dos tickets do GLPI (Abertura e notas incluídas) na tabela "DATTI"."ATEND_GLPI_ABERTURA_NOTAS" do Oracle BDAUX . </h3>
           <br>
           <h3> Servidor da DATTI (C:/_PYTHON/carga_glpi_abertura_notas_dbaux) </h3>
           <br>
            """      
      )

try:
    #Acesso ao BD GLPI 
    def acess_bd_glpi():
        try:
            mydb_glpi = mysql.connector.connect(
                host="10.1.64.198",
                user="xxxxxxxxx",
                password="xxxxxxxxxxx",
                database="glpi",
                #auth_plugin='mysql_native_password'
            )
            #logging.info("Sucess - Conexão MySQL GLPI - 10.1.64.198")
        except:
            logging.info("Fail - Conexão MySQL GLPI - 10.1.64.198")

        #Query para verificação de tickets abertos            
        try:
            if mydb_glpi.is_connected():
                #print("Conexão bem-sucedida com o banco de dados.")
                cursor_glpi = mydb_glpi.cursor()
                cursor_glpi.execute(""" select items_id as Ticket, DATE_FORMAT(iss.date_creation, '%d-%m-%Y %H:%i:%s') as 'Data_modificacao', 
                        users_id_recipient as 'ID_usuario', u.name as Login, 
                        u.comment as 'Localizacao_Ergon', user_dn as 'Localizacao_AD' from 
                        glpi.glpi_plugin_formcreator_issues iss
                        inner join glpi.glpi_users u
                        on iss.users_id_recipient = u.id
                        where user_dn not like '%Terceiros%' and u.user_dn  not like '%zabbix%'
                        order by iss.date_mod desc
                        """)
               
                tickets_abertos = cursor_glpi.fetchall()
                tickets_abertos = [tupla + ('Criação',) for tupla in tickets_abertos] #Incluir o tipo na lista de tuplas
                
                cursor_glpi.close()
        except:
            logging.info('Falha na query de Tickets abertos')
        
        #Query para verificação de nota incluídas nos tickets    
        try:
            if mydb_glpi.is_connected():
                #print("Conexão bem-sucedida com o banco de dados.")
                cursor_glpi = mydb_glpi.cursor()
                cursor_glpi.execute(""" select items_id as Ticket, DATE_FORMAT(flu.date_creation, '%d-%m-%Y %H:%i:%s') as 'Data_modificacao', 
                        users_id as 'ID_usuario', name as Login, 
                        u.comment as 'Localizacao_Ergon', user_dn as 'Localicao_AD'   from 
                        glpi.glpi_itilfollowups flu
                        inner join glpi.glpi_users u
                        on flu.users_id = u.id
                        where u.user_dn  not like '%Terceiros%' and u.user_dn  not like '%zabbix%'  
                        order by flu.date_mod desc
                        """)

                
                notas_incluidas = cursor_glpi.fetchall()
                notas_incluidas = [tupla + ('Nota',) for tupla in notas_incluidas] #Incluir o tipo na lista de tuplas

                cursor_glpi.close()       
        except:
            logging.info('Falha na query de notas incluídas')

        #Query para verificação de tarefas incluídas nos tickets    
        try:
            if mydb_glpi.is_connected():
                #print("Conexão bem-sucedida com o banco de dados.")
                cursor_glpi = mydb_glpi.cursor()
                cursor_glpi.execute(""" select tks.tickets_id as Ticket, DATE_FORMAT(tks.date_creation, '%d-%m-%Y %H:%i:%s') as 'Data_modificacao', 
                                        tks.users_id as 'ID_usuario', name as Login, 
                                        u.comment as 'Localizacao_Ergon', user_dn as 'Localicao_AD'   
                                        from glpi.glpi_tickettasks tks
                                        inner join glpi.glpi_users u
                                        on tks.users_id = u.id
                                        where u.user_dn  not like '%Terceiros%' and u.user_dn  not like '%zabbix%'  
                                        order by tks.date_mod desc
                        """)

                
                tarefas_incluidas = cursor_glpi.fetchall()
                tarefas_incluidas = [tupla + ('Tarefa',) for tupla in tarefas_incluidas] #Incluir o tipo na lista de tuplas

                cursor_glpi.close()       
        except:
            logging.info('Falha na query de tarefas incluídas')

        
        #Query para verificação de tickets fechados
        try:
            if mydb_glpi.is_connected():
                #print("Conexão bem-sucedida com o banco de dados.")
                cursor_glpi = mydb_glpi.cursor()
                cursor_glpi.execute(""" select tk.items_id as Ticket, DATE_FORMAT(tk.date_mod, '%d-%m-%Y %H:%i:%s') as 'Data_modificacao', users_id as 'ID_usuario', 
                                        u.name as Login, u.comment as 'Localizacao_Ergon', user_dn as 'Localizacao_AD' 
                                        from glpi.glpi_itilsolutions tk
                                        inner join glpi.glpi_users u
                                        on tk.users_id = u.id
                                        where u.user_dn not like '%Terceiros%' and u.user_dn  not like '%zabbix%'  
                                        order by tk.date_mod desc
                        """)
                
                
                tickets_fechados = cursor_glpi.fetchall()
                tickets_fechados = [tupla + ('Fechamento',) for tupla in tickets_fechados] #Incluir o tipo na lista de tuplas

                cursor_glpi.close()    
                mydb_glpi.close()   
        except:
            logging.info('Falha na query de tickets fechados')


        #Concatenas as lista de tickets abertos, fechados e notas incluídas
        concat_list = tickets_abertos + notas_incluidas + tarefas_incluidas + tickets_fechados

        return concat_list

    
    #Configuração do BD Oracle
    un = 'xxxxxxx'
    pw = 'xxxxxxxxxxxx'
    cs = 'ora12cprod.trt1.jus.br:1521/bdaux'
    #d = r"C:\Program Files\instantclient_21_11" 
    d = r"C:\Program Files\instantclient" #Padronizar o nome "instantclient" em todas as máquinas
    oracledb.init_oracle_client(lib_dir=d)

    try:
        #Truncar a tabela ATEND_GLPI_ABERTURA_NOTAS antes de realizar a carga
        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
            with connection.cursor() as cursor:
                sql = """TRUNCATE TABLE DATTI.ATEND_GLPI_ABERTURA_NOTAS"""
                cursor.execute(sql)
    except:
        logging.info('Falha no processo de TRUNCATE na tabela no BDAUX DATTI.ATEND_GLPI_ABERTURA_NOTAS ')
    

    try:
        #Inserir concat_list na tabela ATEND_GLPI_ABERTURA_NOTAS 
        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO "DATTI"."ATEND_GLPI_ABERTURA_NOTAS"
                        (Ticket, Data_modificacao, ID_usuario, Login, Localizacao_Ergon, Localizacao_AD, Tipo) 
                        VALUES (:1, TO_DATE(:2, 'DD-MM-YYYY HH24:MI:SS'), :3, :4, :5, :6, :7)"""
                cursor.executemany(sql, acess_bd_glpi())
            
            connection.commit()
            connection.close()
    except:
        logging.info('Falha no processo de INSERT na tabela no BDAUX DATTI.ATEND_GLPI_ABERTURA_NOTAS ')
    
    logging.info('Sucess - Extração e carga')
except:
     #Enviar e-mail para a DATTI em caso de falha no processo
     send_email()
     logging.info('FAIL - Extração e carga')












