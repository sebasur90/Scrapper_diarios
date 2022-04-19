import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from diarios_rss import diarios
import agrega_sentimientos
import datetime
fecha_str=str(datetime.date.today())
import os


noticias={}

def recorre_diarios():    
    contador=0
    for diario in diarios:
        print(f"Obteniendo noticias de {diarios[diario]['diario']} ,seccion {diarios[diario]['seccion']} ")
        time.sleep(2)
        url=requests.get(diarios[diario]['rss'])    
        soup=BeautifulSoup(url.content, "xml")      
        items_pagina=soup.find_all('item')   
        for item in range(len(items_pagina)):
            noticia={}
            noticia['diario']=diarios[diario]['diario']
            noticia['seccion']=diarios[diario]['seccion']
            noticia['titulo']= items_pagina[item].title.text            
            if items_pagina[item].description == None or items_pagina[item].description == " " or items_pagina[item].description == "<NA>":
                if diarios[diario]['diario']=='Perfil':
                    noticia['descripcion']=items_pagina[item].description.text.split("</p>")[1].split('<a href')[0]  
                if diarios[diario]['diario']=='La_izquierda_diario':
                    noticia['descripcion']=items_pagina[item].description.text.split("<p>")[1].split('</p>')[0] 
                else:                                                     
                    noticia['descripcion']=items_pagina[item].title.text
            else:
                if diarios[diario]['diario']=='Perfil':
                    noticia['descripcion']=items_pagina[item].description.text.split("</p>")[1].split('<a href')[0] 
                if diarios[diario]['diario']=='La_izquierda_diario':
                    noticia['descripcion']=items_pagina[item].description.text.split("<p>")[1].split('</p>')[0]       
                else:        
                    noticia['descripcion'] =(items_pagina[item].description.text)
            
            noticias[contador]=noticia    
            contador=contador +1


def formateo_noticias(noticias):   
    dataframe_noticias = pd.DataFrame(noticias).transpose()
    dataframe_noticias.drop_duplicates(subset=['titulo'])
    """ dataframe_noticias.to_excel(
        f"noticias_rss.xlsx") """
    return dataframe_noticias

def sentimientos(dataframe_noticias):
    noticias=agrega_sentimientos.genera_excel_sentimientos(dataframe_noticias)
    noticias.to_excel(f"diarios/noticias_con_sentimientos_{fecha_str}.xlsx")
    pass

def apila_diarios_historicos():
    lista_diarios=os.listdir('diarios')
    lista_diarios.remove('diarios_historicos.xlsx')
    dataframes=[]
    for diarios in lista_diarios:
        dataframes.append(pd.read_excel("diarios/"+diarios))
    apilados = pd.concat(dataframes, axis=0) 
    apilados.to_excel(f"diarios/diarios_historicos.xlsx")   


def transforma_letras_para_wordcloud(dataframe_noticias):
    columna_analizada = list(dataframe_noticias.titulo)
    acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
               'Á': 'A', 'E': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    lista_palabras_para_wordcloud = []
    for palabras in columna_analizada:
        palabras_div = palabras.split(' ')
        for letras in palabras_div:
            for acen in acentos:
                if acen in letras:
                    letras = letras.replace(acen, acentos[acen])
            lista_palabras_para_wordcloud.append(letras.lower())
    return ' '.join(lista_palabras_para_wordcloud)



def genera_wordcloud(palabras_para_wordcloud):
    palabras_ignoradas = set(['a', 'ante', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'para', 'por', 'segun', 'sin', 'sobre', 'el', 'la', 'los', 'las',
                               '...', 'y', 'hoy', 'este', 'cuanto',  'un', 'del', 'las',  'que', 'con', 'todos',  'es', '¿qué',  'como', 'cada',
                              'jueves', '¿cuanto', 'hoy', 'al', 'cual', 'se', 'su', 'sus', 'lo', 'una', 'un', 'tiene',
                              'le', 'habia'])

    wordcloud = WordCloud(width=1920, height=1080, stopwords=palabras_ignoradas).generate(
        palabras_para_wordcloud)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f"wordclouds/wordcloud_noticias_rss_{fecha_str}.png")




def run():
    recorre_diarios()    
    dataframe_noticias=formateo_noticias(noticias)
    sentimientos(dataframe_noticias)
    apila_diarios_historicos()
    palabras_para_wordcloud = transforma_letras_para_wordcloud(
        dataframe_noticias)
    genera_wordcloud(palabras_para_wordcloud)


if __name__ == '__main__':
    run()
