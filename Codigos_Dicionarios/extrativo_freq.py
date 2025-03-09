from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import spacy
import nltk
from nltk.corpus import stopwords
from lxml import html
import requests

# Baixar stopwords do NLTK (se necessário)
#nltk.download('stopwords')
stopwords_pt = stopwords.words('portuguese')

# Carregar modelo SpaCy para português
nlp = spacy.load("pt_core_news_md")

def get_clean_text_from_url(url):
    """ Extrai e limpa o texto relevante de uma página web """
    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    # Filtra elementos textuais importantes
    text_elements = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //p | //div[@style="text-align: justify;"]')
    
    # Extrai e limpa o texto
    clean_text = "\n".join(
        [element.text_content().strip() for element in text_elements if element.text_content().strip()]
    )

    return clean_text

def is_similar(nova_frase, frases_selecionadas, limiar=0.9):
    """ Verifica se uma nova frase é muito semelhante a alguma já escolhida """
    doc_novo = nlp(nova_frase)
    for frase in frases_selecionadas:
        doc_existente = nlp(frase)
        if doc_novo.similarity(doc_existente) > limiar:
            return True
    return False

def extrair_frases_mais_importantes(texto, num_frases=3):
    """ Usa TF-IDF para identificar as frases mais importantes e evitar repetições """

    # Processar o texto com spaCy para dividir corretamente em frases
    doc = nlp(texto)
    frases = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    if not frases:
        return "Nenhuma frase encontrada."

    # Criar o modelo TF-IDF com stopwords do português
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords_pt)

    # Ajustar e transformar o texto para obter as matrizes de TF-IDF
    tfidf_matrix = tfidf_vectorizer.fit_transform(frases)

    # Somar as pontuações TF-IDF por frase
    soma_tfidf = np.array(tfidf_matrix.sum(axis=1)).flatten()

    # Obter os índices das frases mais importantes
    indices_importantes = np.argsort(soma_tfidf)[::-1]

    # Selecionar frases mais importantes sem repetições
    resumo = []
    for i in indices_importantes:
        if len(resumo) >= num_frases:
            break
        if not is_similar(frases[i], resumo, limiar=0.9):
            resumo.append(frases[i])

    return ' '.join(resumo)  # Retorna as frases selecionadas como resumo

# URL do site a ser resumido
url = "https://brasilcristao-contra-o-comunismo.blogspot.com/p/a-escola-de-frankfurt-lumpem.html"
texto = get_clean_text_from_url(url)

# Obter o resumo com as 3 frases mais importantes sem repetições
resumo = extrair_frases_mais_importantes(texto, num_frases=2)
print("Resumo Extraído:", resumo)
