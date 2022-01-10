import pandas as pd 
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
import string
import re
import contractions
import streamlit as st 
import plotly.express as px

st.header('Busco empleo')
st.subheader('') 
st.subheader('') 
st.subheader('Ejemplo: Copia y pega el siguiente texto; luego, Ctrl+Enter') 
st.subheader('Busco empleo, Busco empleo, Busco empleo, comparte por favor') 

st.subheader('') 
st.subheader('') 

st.subheader('Puedes escribir el texto que desees y luego; Ctrl+Enter') 
st.subheader('') 
st.subheader('') 
st.title('Extractor de palabras clave')
st.markdown('Esta aplicación devuelve las palabras más comunes en el cuerpo de texto ingresado.')
st.write('Las características incluyen:')

"""
* Lematizar palabras (convertir palabras en raíces)
* Expandir las contracciones 
* Eliminar palabras vacías y puntuación"""

text = st.text_area('Pega el texto aquí: ').lower()
text_contract_fixed = contractions.fix(text)

wnl = WordNetLemmatizer()

#converting nltk tag to wordnet tag
def nltk_to_wn_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

stop = set(stopwords.words('english'))
punc = set(string.punctuation)

def lem_clean(doc):
    #tokenize the sentence and find the POS tag for each token
    nltk_tagged = pos_tag(word_tokenize(doc))  
    #tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_to_wn_tag(x[1])), nltk_tagged)
    lem_sent = []
    for word, tag in wordnet_tagged:
        word = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', word)
        if tag is None:
            #if there is no available tag, append the token as is
            lem_sent.append(word)
        else:        
            #else use the tag to lemmatize the token
            lem_sent.append(wnl.lemmatize(word, tag))
    stop_free = [word for word in lem_sent if word not in stop]
    punc_free = [word for word in stop_free if word not in punc]
    return punc_free

text_clean = lem_clean(text_contract_fixed)

#count word frequency
def word_freq(tokenized_text):
    word_list = []
    freq_list = []
    for word in tokenized_text:
        if word not in word_list:
            word_list.append(word)
            freq_list.append(tokenized_text.count(word))
    
    frequency_df = pd.DataFrame({'Keyword':word_list, 'Frequency': freq_list}).sort_values(by=['Frequency'], ascending=False).reset_index()
    return frequency_df.drop('index', axis =1)

df = word_freq(text_clean)

st.write(f'Total de palabras en el texto: {len(text.split())}')
st.write(f'Número de palabras únicas en el texto: {len(set(text.split()))}')

st.write(df)

top10 = df.iloc[:10].sort_values(by=['Frequency'], ascending=False)

fig = px.bar(top10, y='Frequency', x='Keyword', color = 'Keyword', color_discrete_sequence=px.colors.qualitative.Prism, title='10 palabras principales', template='ggplot2')
st.plotly_chart(fig, use_container_width=True)

#st.write('Created by [austyngo](https://github.com/austyngo).')
#st.write('Code available in my [GitHub repository](https://github.com/austyngo/keyword_tool).')

st.subheader('JAVIER HORACIO PÉREZ RICÁRDEZ')
st.subheader('email: jahoperi@gmail.com')