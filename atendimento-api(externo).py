import requests

#Iniciando uma sessão

def open_session(app_token, user_token):
    # URL para a requisição
    url = "https://atendimento.trt1.jus.br/apirest.php/initSession"

    #Cabeçalhos da requisição
    headers = {
        "App-Token": "", #GLPI DEV
        "Authorization": "", #GLPI DEV
        "Accept": "application/json"
    }

    headers['App-Token'] = app_token
    headers['Authorization'] = user_token

    # Fazer a requisição GET
    response = requests.get(url, headers=headers)

    session_token = response.json()
    session_token = session_token['session_token']

    # Verificar o status da resposta
    if response.status_code == 200:  # HTTP 200 significa "Sucesso"
        print("Sessão criada!")
        return(session_token)
    else:
        print("Erro na criação da sessão!")
        print(f"Status Code: {response.status_code}")
        print("Mensagem de erro:", response.text)

###########################################################################

#Encerrando a sessão

def close_session(session_token, app_token):

    #Cabeçalhos da requisição  
    headers = {
        "Session-Token": "", #GLPI DEV
        "App-Token": "", #GLPI DEV
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token
    headers['App-Token'] = app_token

    url = "https://atendimento.trt1.jus.br/apirest.php/killSession"

    # Fazer a requisição GET
    response = requests.get(url, headers=headers)

    # Verificar o status da resposta
    if response.status_code == 200:  # HTTP 200 significa "Sucesso"
        print("Sessão encerrada!")
    else:
        print("Falha ao encerrar a sessão!")
        print(f"Status Code: {response.status_code}")
        print("Mensagem de erro:", response.text)

########################################################################

#Criando um Ticket

def create_ticket(user_token, app_token, assigned_user, requester_user, itilcategories_id, type, locations_id, titulo, descricao):
    
    session_token = open_session(app_token, user_token)

    ticket = {
        "input": { 
        "entities_id": 1,  # 0 - TRT1, 1 - Atendimento, 2 - Segurança da Informação, 3 - Pje Apoio
        "name": titulo, 
        "status": 2, #Em atendimento
        "requesttypes_id": 1,
        "content": descricao, 
        "urgency": 3,
        "impact": 3,
        "priority": 3, # 3-média / 4-urgênte (Indicação visual na tela do GLPI)
        "type": type, #Incidente / Requisição (2)
        "itilcategories_id": itilcategories_id,  # ID da categoria (veja no GLPI)
        "locations_id": locations_id,
        "_users_id_assign": assigned_user, #Técnico atribuido
        "_users_id_requester": requester_user #Usuário requerente
            }
    }

    #"_users_id_assign": assigned_user, #Atribui chamado ao técnico

    # URL para a requisição
    url = "https://atendimento.trt1.jus.br/apirest.php/Ticket"

    #Cabeçalhos da requisição
    headers = {
        "Session-Token": "", #GLPI DEV
        "App-Token": "", #GLPI DEV
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token
    headers['App-Token'] = app_token

    # Fazer a requisição GET
    response = requests.post(url, headers=headers, json=ticket)

    ticket_id = response.json()
    ticket_id = ticket_id['id']  

    # Verificar o status da resposta
    if response.status_code == 201 or response.status_code == 200 :  # HTTP 20X significa "Sucesso"
        print(f"Ticket ID: {ticket_id}")
        return ticket_id
    else:
        print("Erro na requisição!")
        print(f"Status Code: {response.status_code}")
        print("Mensagem de erro:", response.text)

    close_session(session_token, app_token)

####################################################################################################

#Adicionando uma nota no ticket

def add_followup(user_token, app_token, ticket_id, content):
   
    session_token = open_session(app_token, user_token)

    # Dados para atualização
    update_data = {
        "input":{
        "itemtype": "Ticket",
        "items_id": ticket_id,
        "content": content,
        "is_private": 0
        }
    }

    #Cabeçalhos da requisição  
    headers = {
        "Session-Token": "", #GLPI DEV
        "App-Token": "", #GLPI DEV
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token
    headers['App-Token'] = app_token


    # Endpoint para atualizar o ticket
    url = "https://atendimento.trt1.jus.br/apirest.php/ITILFollowup"

    # Realizando a requisição para atualizar o chamado
    response = requests.post(url, json=update_data, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Chamado atualizado com sucesso! ID: {ticket_id}")
    else:
        print(f"Falha ao atualizar chamado. Status: {response.status_code}, Erro: {response.text}")

    close_session(session_token, app_token)

###################################################################################################

#Solucionando o ticket

def solve_ticket(user_token, app_token, ticket_id):
    
    session_token = open_session(app_token, user_token)

    #Cabeçalhos da requisição  
    headers = {
        "Session-Token": "", #GLPI DEV
        "App-Token": "", #GLPI DEV
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token
    headers['App-Token'] = app_token

    # Dados para atualização
    solution_data = {
        "input": {
            "itemtype": "Ticket",
            "items_id": ticket_id,
            "solutiontypes_id": 10,
            },
        }
    
    # URL para a requisição
    url = f"https://atendimento.trt1.jus.br/apirest.php/Ticket/{ticket_id}"

    # Fazer a requisição GET
    response = requests.put(url, headers=headers, json=solution_data)

    # Verificar o status da resposta
    if response.status_code == 200:  # HTTP 200 significa "Sucesso"
        print("Chamado Solucionado!")
    else:
        print("Erro na solução do chamado!")
        print(f"Status Code: {response.status_code}")
        print("Mensagem de erro:", response.text)

    close_session(session_token, app_token)

#####################################################################################

