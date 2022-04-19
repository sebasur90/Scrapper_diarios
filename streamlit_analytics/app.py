import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
noticias=pd.read_excel('../diarios/diarios_historicos.xlsx')

noticias=noticias.iloc[:,3:]

diarios=list(noticias.diario.unique())
secciones=list(noticias.seccion.unique())
columna_para_nube=['titulo','descripcion']

st.title("Noticias")


with st.sidebar:
            
            diarios_select = st.multiselect('Selecciona los  diarios',
     diarios ,default=diarios)
            secciones_select = st.multiselect('Selecciona las secciones',
            secciones,default=secciones)
           
            palabra_buscada = st.text_input('Buscar palabra', 'Ninguna')
            


if palabra_buscada=="Ninguna":
    pass
else:
    noticias=noticias[noticias['titulo'].str.contains(palabra_buscada)]
           
st.session_state['dataframe_filtrado']=noticias[(noticias.diario.isin (diarios_select)) & (noticias.seccion.isin (secciones_select))  ]
st.dataframe(st.session_state['dataframe_filtrado'].sample(frac=1))
st.session_state['dataframe_agrupado']=st.session_state['dataframe_filtrado'].groupby('diario')[['pond_negativos','pond_neutro','pond_positivo']].mean().reset_index()

fig = px.bar(st.session_state['dataframe_agrupado'], x="diario", y=['pond_neutro',"pond_negativos",'pond_positivo'],text_auto=True,
title="Analisis de sentimientos")
fig.update_layout(legend_title_text='Pond de los sentimientos')

st.plotly_chart(fig)



def transforma_letras_para_wordcloud(dataframe_noticias):
    columna_analizada = list(dataframe_noticias['titulo'])
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



def genera_wordcloud(dataframe_noticias):
    palabras_para_wordcloud=transforma_letras_para_wordcloud(dataframe_noticias)
    palabras_ignoradas = set(['a', 'ante', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'para', 'por', 'segun', 'sin', 'sobre', 'el', 'la', 'los', 'las',
                               '...', 'y', 'hoy', 'este', 'cuanto',  'un', 'del', 'las',  'que', 'con', 'todos',  'es', '¿qué',  'como', 'cada',
                              'jueves', '¿cuanto', 'hoy', 'al', 'cual', 'se', 'su', 'sus', 'lo', 'una', 'un', 'tiene',
                              'le', 'habia'])

    wordcloud = WordCloud(width=1920, height=1080, stopwords=palabras_ignoradas).generate(
        palabras_para_wordcloud)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")    
    st.pyplot()








if st.button('Generar Nube'):
       genera_wordcloud(st.session_state['dataframe_filtrado'])
else:
       pass



