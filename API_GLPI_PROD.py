import requests

########################################################################################################################################
#Iniciando uma sessão

def open_session():
    # URL para a requisição
    url = "https://atendimento.trt1.jus.br/apirest.php/initSession"

    #Cabeçalhos da requisição (opcional)
    headers = {
        "App-Token": "xxxxxxxxxxxxxxxxxxxxxxxxx", #GLPI PROD
        "Authorization": "user_token xxxxxxxxxxxxxxxxxxxxxxxxx", #GLPI PROD
        "Accept": "application/json"
    }

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
###########################################################################################################################################

###########################################################################################################################################

#Criando um Ticket

def create_ticket(session_token, titulo, descricao):
    
    assigned_user = 4147

    ticket = {
        "input": { 
        "entities_id": 1,  # 0 - TRT1, 1 - Atendimento, 2 - Segurança da Informação, 3 - Pje Apoio
        "name": titulo, #"Suporte Ferramentas ITSM | Administração de Catálogo",
        "users_id_lastupdater": assigned_user,
        "status": 2, #Em atendimento
        "users_id_recipient": assigned_user,  # ID do usuário que abriu o ticket
        "requesttypes_id": 1,
        "content": descricao, #"&#60;div&#62;&#60;h1&#62;Dados do formulário&#60;/h1&#62;&#60;h2&#62;Solicitante&#60;/h2&#62;&#60;div&#62;&#60;b&#62;1) Nome ou login do solicitante : &#60;/b&#62;Arthur Williams Falcao Trento (4147)&#60;/div&#62;&#60;div&#62;&#60;b&#62;2) Selecione a sua localização : &#60;/b&#62;ANTONIO CARLOS - 12º andar&#60;/div&#62;&#60;div&#62;&#60;b&#62;3) Telefone de Contato : &#60;/b&#62;2199999999&#60;/div&#62;&#60;div&#62;&#60;b&#62;4) Adicionar Observador? : &#60;/b&#62;Não&#60;/div&#62;&#60;div&#62;&#60;b&#62;5) Chamado sendo aberto por : &#60;/b&#62;Outros Resolvedores&#60;/div&#62;&#60;div&#62;&#38;nbsp;&#60;/div&#62;&#60;h2&#62;Suporte Ferramentas ITSM&#60;/h2&#62;&#60;div&#62;&#60;b&#62;6) Selecione o serviço desejado : &#60;/b&#62;Administração de Catálogo&#60;/div&#62;&#60;div&#62;&#60;b&#62;7) Selecione : &#60;/b&#62;Avaliar e Aprovar Ajuste de Catálogo&#60;/div&#62;&#60;div&#62;&#38;nbsp;&#60;/div&#62;&#60;h2&#62;Descreva a sua solicitação&#60;/h2&#62;&#60;div&#62;&#60;b&#62;8) Descrição : &#60;/b&#62;&#60;p&#62;Teste&#60;/p&#62;&#60;/div&#62;&#60;div&#62;&#60;b&#62;9) Anexo : &#60;/b&#62;Nenhum documento anexado&#60;/div&#62;&#60;div&#62;&#60;b&#62;10) ##Atendimento## : &#60;/b&#62;&#60;/div&#62;&#60;/div&#62;",
        "urgency": 3,
        "impact": 3,
        "priority": 3,
        "itilcategories_id": 1655,  # ID da categoria (veja no GLPI)
        "type": 2, #Incidente / Requisição
        "takeintoaccount_delay_stat": 1,
        "locations_id": 7,
        "_users_id_assign": assigned_user, #Técnico atribuido
        "_users_id_requester": assigned_user #Usuário requerente
            }
    }

    #"_users_id_assign": assigned_user, #Atribui chamado ao técnico

    # URL para a requisição
    url = "https://atendimento.trt1.jus.br/apirest.php/Ticket"

    #Cabeçalhos da requisição
    headers = {
        "Session-Token": "", #GLPI PROD
        "App-Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxx", #GLPI PROD
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token

    # Fazer a requisição GET
    response = requests.post(url, headers=headers, json=ticket)

    ticket_id = response.json()
    ticket_id = ticket_id['id']  #Precisa alterar

    # Verificar o status da resposta
    if response.status_code == 201 or response.status_code == 200 :  # HTTP 20X significa "Sucesso"
        print(f"Ticket ID: {ticket_id}")
        return ticket_id
    else:
        print("Erro na requisição!")
        print(f"Status Code: {response.status_code}")
        print("Mensagem de erro:", response.text)

##############################################################################################################################

##############################################################################################################################

#Adicionando uma nota no ticket

def add_followup(session_token, ticket_id, content):
   
    # Dados para atualização
    update_data = {
        "input":{
        "itemtype": "Ticket",
        "items_id": ticket_id,
        "content": content,
        "is_private": 0
        }
    }

    #Cabeçalhos da requisição (opcional)
    headers = {
        "Session-Token": "", #GLPI PROD
        "App-Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", #GLPI PROD
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token

    # Endpoint para atualizar o ticket
    url = "https://atendimento.trt1.jus.br/apirest.php/ITILFollowup"

    # Realizando a requisição para atualizar o chamado
    response = requests.post(url, json=update_data, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Chamado atualizado com sucesso! ID: {ticket_id}")
    else:
        print(f"Falha ao atualizar chamado. Status: {response.status_code}, Erro: {response.text}")


##############################################################################################################################

##############################################################################################################################

#Solucionando o ticket

def solve_ticket(session_token, ticket_id):
    
    #Cabeçalhos da requisição (opcional)
    headers = {
        "Session-Token": "", #GLPI PROD
        "App-Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", #GLPI PROD
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token

    # Dados para atualização
    solution_data = {
        "input": {
            "itemtype": "Ticket",
            "items_id": ticket_id,
            "solutiontypes_id": 10,
            },
        }
    
    #"users_id_recipient": 4147,
    #"users_id":4147,
    #"status":2
    #"content": content,

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

##############################################################################################################################

##############################################################################################################################

def close_session(session_token):
    
    #Encerrando a sessão

    #Cabeçalhos da requisição (opcional)
    headers = {
        "Session-Token": "", #GLPI PROD
        "App-Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", #GLPI PROD
        "Content-Type": "application/json"
    }

    headers['Session-Token'] = session_token

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

##############################################################################################################################

##############################################################################################################################





