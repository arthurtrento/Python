import requests
from datetime import date, datetime
import ast 
from redmail import EmailSender
import logging
from logging.handlers import TimedRotatingFileHandler

#logging.basicConfig(level=logging.INFO, filename=r"C:/_PYTHON/vc_calls_queues/Log/Logs.log", format="%(asctime)s - %(levelname)s - %(message)s")

#Configuração do Log para criação de um arquivo por dia de monitoramento

# Configuração do logger
logger = logging.getLogger("DailyLogger")
logger.setLevel(logging.DEBUG)

# Configuração do handler para rotação diária
log_handler = TimedRotatingFileHandler(
    filename="C:/_PYTHON/vc_calls_queues/Log/Logs_",  # Nome base do arquivo de log
    when="midnight",           # Rotação diária
    interval=1,                # Intervalo de 1 dia
    backupCount=7,             # Mantém os últimos 7 arquivos de log
    encoding="utf-8"           # Codificação do arquivo de log
)
log_handler.suffix = "%d-%m-%y.log"  # Define o formato da data no nome do arquivo

# Formatação do log
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
log_handler.setFormatter(formatter)

# Adiciona o handler ao logger
logger.addHandler(log_handler)
##################################################################################


########################## Verificação da chamadas  ############################

def vc_calls():

    def enviar_email_calls():
        # Configure the sender
        email = EmailSender(
        host="mxg.trt1.jus.br", 
        port=587,
        #username='me@example.com',
        #password='<PASSWORD>'
        )
        # Send an email:
        email.send(
            subject=f"Alerta de Ligações perdidas no Voice Cloud",
            sender="datti@trt1.jus.br",
            receivers=['datti@trt1.jus.br'],
            text= "Percentual de ligações perdidas acima de 75%",
            html= """
            
            <h3> Total de ligações: {{trt_all_calls}} </h3>

            <h3> Ligações atendidas: {{trt_atendidas}}  </h3>

            <h3> Ligação(ões) abandonada(s): {{trt_abandonadas}}  </h3>

            <h3> Desistência(s): {{trt_desistentes}}  </h3>

            <h3> Tempo médio de atendimento: {{trt_tma}} minuto(s) </h3>

            <h3> Tempo médio de espera: {{trt_tme}} minuto(s) </h3>

            <a href="https://app.servicedesk.stefanini.io/login" target="_blank">Acesse o Dashboard Voice Cloud</a>

            """,
            
            body_params={
            "trt_all_calls": trt_all_calls,
            "trt_atendidas": trt_atendidas,
            "trt_abandonadas": trt_abandonadas,
            "trt_desistentes": trt_desistentes,
            "trt_tma": trt_tma,
            "trt_tme": trt_tme,
            
            }
                            
            )


    auth_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    headers = {'Authorization': f'Bearer {auth_token}'}

    data_ini = str(date.today()) + 'T00:00:00-03:00'
    data_fim = str(date.today()) + 'T23:59:59-03:00'

    data = str({ 
        "before_filter": {
        "$and": [
          {
            "$expr": {
              "$gte": [
                "$time",
                {
                  "$toDate": "xxxxx"
                }
              ]
            }
          },
          {
            "$expr": {
              "$lte": [
                "$time",
                {
                  "$toDate": "yyyyy"
                }
              ]
            }
          }
        ]
      },
      "custom_filter": [
        {
          "$match": {
            "queue_id": {
              "$in": [
                401,
                402
              ]
            }
          }
        }
      ]
    })

    data = data.replace("xxxxx", data_ini)
    data = data.replace("yyyyy", data_fim)
    data = ast.literal_eval(data) 

    url = 'https://api.servicedesk.stefanini.io/api/consolidado_trt/filter?$type=query'
    response = requests.post(url, headers=headers, json=data, verify=False) 

    response = response.json()
    #print(response.json())

    if response['data'] != None:

        ####'data'######
        # incall = response['data'][0]['consolidado']['recebidas']
        # atendidas = response['data'][0]['consolidado']['atendidas']
        # atendidas_sla = response['data'][0]['consolidado']['atendidas_sla']
        # atendidas_not_sla = response['data'][0]['consolidado']['atendidas_not_sla']
        # abandonadas = response['data'][0]['consolidado']['abandonadas']
        # desistentes = response['data'][0]['consolidado']['desistentes']
        # transferidas = response['data'][0]['consolidado']['transferidas']
        # all_calls = response['data'][0]['consolidado']['all_calls']
        # holdtime = response['data'][0]['consolidado']['holdtime']
        # calltime = response['data'][0]['consolidado']['calltime']
        # ns_calls = response['data'][0]['consolidado']['ns_calls']
        # abandonadas_porc = response['data'][0]['consolidado']['abandonadas_porc']
        # desistentes_porc = response['data'][0]['consolidado']['desistentes_porc']
        # atendidas_direta = response['data'][0]['consolidado']['atendidas_direta']
        # sla = response['data'][0]['consolidado']['sla']
        # service_level = response['data'][0]['consolidado']['service_level']
        # tma = response['data'][0]['consolidado']['tma']
        # tme = response['data'][0]['consolidado']['tme']
        

        #####by_queue######
        trt_id = response['data'][0]['by_queue'][0]['_id']
        trt_atendidas = response['data'][0]['by_queue'][0]['atendidas']
        trt_abandonadas = response['data'][0]['by_queue'][0]['abandonadas']
        trt_desistentes = response['data'][0]['by_queue'][0]['desistentes']
        trt_transferidas = response['data'][0]['by_queue'][0]['transferidas']
        trt_all_calls = response['data'][0]['by_queue'][0]['all_calls']
        trt_holdtime = response['data'][0]['by_queue'][0]['holdtime']
        trt_calltime = response['data'][0]['by_queue'][0]['calltime']
        trt_tma = response['data'][0]['by_queue'][0]['tma']
        trt_tma = round(trt_tma / 60, 2)
        trt_tme = response['data'][0]['by_queue'][0]['tme']
        trt_tme = round(trt_tme / 60, 2)
        trt_atendidas_direta = response['data'][0]['by_queue'][0]['atendidas_direta']
        perc_atendidas = round((100 * trt_atendidas) / trt_all_calls)

        if perc_atendidas < 75 and trt_all_calls > 15:  
          enviar_email_calls()
          logger.info(f'E-mail de ligações perdidas enviado! - {perc_atendidas}% de ligações atendidas'  )
        else: 
          logger.info(f'Nenhuma ação necessária - {perc_atendidas}% de ligações atendidas')
            

    else:
      
        logger.info("Sem atendimentos no momento")

################## Verificação da FILA  ############################

def vc_queues():
    
      def enviar_email_queue():
        # Configure the sender
        email = EmailSender(
        host="xxxxxx.trt1.jus.br", 
        port=587,
        #username='me@example.com',
        #password='<PASSWORD>'
        )
        # Send an email:
        email.send(
            subject=f"Alerta de fila no Voice Cloud - Fila atual: {waiting}",
            sender="datti@trt1.jus.br",
            receivers=['datti@trt1.jus.br'],
            text= "O Service-Desk está operando com uma fila de espera superior a 5 posições.",
            html= """
             
            <h3> {{waiting}} ligação(ões) na fila </h3>
            <h3> {{incall}} ligação(ões) em curso </h3>
            <h3> {{agents_available}} atendente(s) está(ão) disponível(is) </h3>
            <h3> {{agents_paused}} atendente(s) pausado(s) </h3>
            <h3> {{agents_ringing}} atendente(s) chamando </h3>

            """,
            
            body_params={
            "waiting": waiting,
            "incall": incall,
            "agents_available": agents_available,
            "agents_paused": agents_paused,
            "agents_ringing": agents_ringing
            }
                        
        )

      auth_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
      headers = {'Authorization': f'Bearer {auth_token}'}
      data = {  }


      url = 'https://api.servicedesk.stefanini.io/api/func/queue_status_trt'
      response = requests.post(url, headers=headers, json=data, verify=False) 
      response = response.json()

      incall = response['data']['incall']
      waiting = response['data']['waiting']
      agents_available = response['data']['agents_available']
      agents_paused = response['data']['agents_paused']
      agents_ringing = response['data']['agents_ringing']

      if waiting >= 5:
          enviar_email_queue()
          logger.info(f"E-mail de fila enviado! - Fila:{waiting}")
      else:
          logger.info(f'Nenhuma ação necessária  - Fila: {waiting}')

#Só verifica se for dia da semana e o horário estiver entre 08h e 17h.

# Obter o horário atual
now = datetime.now()

# Verificar se é dia útil (segunda a sexta) e horário entre 08:00 e 17:00
if now.weekday() < 5 and now.weekday() > 0 and 8 <= now.hour < 17:
    vc_calls()
    vc_queues()






