
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys


data = pd.read_csv("ml-25m/links.csv", dtype='str')
new_data = {'movieId':[], 'stars':[], 'directors':[], 'writers':[]}
for i in range(len(data)):
    try:
        movie = data.imdbId[i] #pegando o id do filme na imdb da tabela
        page = requests.get('https://www.imdb.com/title/tt' + movie + '/fullcredits') #acessando o link
        soup = BeautifulSoup(page.text, 'html.parser') #lendo texto
        tela = soup.find_all(class_='simpleTable simpleCreditsTable') #filtrando texto, pegando a classe com as tabelas de directos e writers
        page2 = requests.get('https://www.imdb.com/title/tt' + movie) #acessando o link
        soup2 = BeautifulSoup(page2.text, 'html.parser') #lendo texto
        tela2 = soup2.find_all(class_='credit_summary_item') #filtrando o texto, pegando a classe com os dados de stars


        #Pegando valores das stars
        text = tela2[2].find_all('a') #filtrando texto, pegando todos os 'a'
        stars = []
        for name in text: #para cada 'a' no texto
            new_name = name.contents[0].replace('\n', '') #tirando /n
            new_name = new_name.replace(' ', '', 1) #tirando espaço
            if(new_name != 'Seefull cast & crew'):
                stars.append(new_name) #adionando os diretores na coluna diretor
        stars = '|'.join(map(str, stars)) #alterando o separador da lista de diretores para '|' em vez de ','



        #Pegando valores dos diretores
        text = tela[0].find_all('a') #filtrando texto, pegando todos os 'a'
        directors = []
        for name in text: #para cada 'a' no texto
            new_name = name.contents[0].replace('\n', '') #tirando /n
            new_name = new_name.replace(' ', '', 1) #tirando espaço
            directors.append(new_name) #adionando os diretores na coluna diretor
        directors = '|'.join(map(str, directors)) #alterando o separador da lista de diretores para '|' em vez de ','


        #Pegando valores dos writers
        text = tela[1].find_all('a') #filtrando texto, pegando todos os 'a'
        writers = []
        for name in text: #para cada 'a' no texto
            new_name = name.contents[0].replace('\n', '') #tirando /n
            new_name = new_name.replace(' ', '', 1) #tirando espaço
            writers.append(new_name) #adionando os writers na coluna diretor
        writers = '|'.join(map(str, writers)) #alterando o separador da lista de writers para '|' em vez de ','

        


        new_data['movieId'].append(data.imdbId[i]) #adicionando movieId no dicionario com dados
        new_data['stars'].append(stars) #adicionando stars no dicionario com dados
        new_data['directors'].append(directors) #adicionando directos no dicionario com dados
        new_data['writers'].append(writers) #adicionando writers no dicionario com dados

        print(i)

    except:
        continue

new_data = pd.DataFrame(new_data, columns=['movieId','stars','directors','writers']) #transformando dicionario num dataframe do pandas
new_data.to_csv("ml-25m/cast_crew.csv", index=False) #transformando em csv