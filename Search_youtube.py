#https://developers.google.com/docs/api/quickstart/python?hl=pt-br

#Acesso ao console do Google 
#https://console.cloud.google.com/apis

import pandas as pd
from openpyxl import Workbook
#import requests
#import json
from googleapiclient.discovery import build
import googleapiclient

#dataframe = pd.read_excel('G:/Outros computadores/Meu computador/Python/Em_desenvolvimento/spotify.xlsx', header=1) # O header é o número do inicio da leitura da linha
dataframe = pd.read_excel('C:/Users/arthu/Desktop/Python/Em_desenvolvimento/spotify.xlsx', header=1) # O header é o número do inicio da leitura da linha

dataframe = dataframe.iloc[0:] #Lê todas as linhas

#Caso as colunas mudem de posição na planilha da XPI, alterar abaixo
dataframe = dataframe.iloc[0:, [0,1,2]] #Lê todas as linhas e as colunas 1, 2 e 5

dataframe.columns = ['Musica', 'Artista','Album'] # Define o nome dos cabeçalhos das colunas

#print(dataframe)

planilha = Workbook()

sheet = planilha.active

sheet.append(["Pesquisa", "Option1", "Option2", "Option3", "Option4", "Option5"])

check = 0

api_key = 'AIzaSyDbg6s4DzV64gzPkN6gd06sgves2YdlU90'

youtube = build('youtube', 'v3', developerKey=api_key)

for i in range(len(dataframe)):

    check = check + 1

    print(check)

    search = dataframe['Musica'].iloc[i] + " " + dataframe['Artista'].iloc[i]

    request = youtube.search().list(
            part="snippet",
            order="viewCount",
            q= search,  #sample: boating|sailing -fishing  | (or) , - (menos)
            type="video",
            videoDefinition="high",
            videoDuration="medium",
            safeSearch="strict",
            maxResults="5"
        )
    response = request.execute()

    option1, option2, option3, option4, option5 = "N/A", "N/A", "N/A", "N/A", "N/A" 
    
    try:
        option1 = response['items'][-1]['id']['videoId']
    except:
        pass
    try:
        option2 = response['items'][-2]['id']['videoId']
    except:
        pass
    try:
        option3 = response['items'][-3]['id']['videoId']
    except:
        pass
    try:
        option4 = response['items'][-4]['id']['videoId']
    except:
        pass
    try:
        option5 = response['items'][-5]['id']['videoId']
    except:
        pass

    sheet.append([search, option1, option2, option3, option4, option5])

planilha.save("Youtube_results.xlsx")
           
