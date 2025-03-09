import spacy
import nltk
from nltk.corpus import wordnet
from unidecode import unidecode
from deep_translator import GoogleTranslator

# Carregar o modelo do SpaCy em português
nlp = spacy.load("pt_core_news_sm")

def traduzir_frase(frase):
    # Usando deep-translator para tradução
    resultado = GoogleTranslator(source='en', target='pt').translate(frase)
    return resultado

def obter_definicao(palavra):
    syns = wordnet.synsets(palavra, lang="por")  
    if syns:
        definicao = syns[0].definition()  # Pega a definição da palavra
        return definicao
    return None

def lematizar_palavra(palavra):
    # Lematiza a palavra utilizando o modelo do SpaCy
    doc = nlp(palavra)
    return doc[0].lemma_

def processar_dicionario(entrada, saida):
    with open(entrada, "r", encoding="utf-8") as f:
        palavras = f.read().splitlines()  # Lê as palavras do arquivo

    palavras_lematizadas = set()  # Usamos um set para evitar palavras repetidas
    with open(saida, "w", encoding="utf-8") as f_saida:
        for palavra in palavras:
            definicao = obter_definicao(palavra)  # Obtém a definição da palavra
            if definicao:
                # Se a definição estiver em inglês, traduz para o português
                definicao_traduzida = traduzir_frase(definicao)
                # Lematiza a palavra apenas se for necessário
                palavra_lematizada = lematizar_palavra(palavra)
                f_saida.write(f'"{palavra_lematizada}", "{definicao_traduzida}"\n')

# Chamando a função para processar o dicionário
processar_dicionario("3.txt", "dicionario_definicoes3.txt")
