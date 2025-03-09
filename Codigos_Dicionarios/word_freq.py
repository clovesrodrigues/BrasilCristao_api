import spacy
from collections import Counter
import requests
from lxml import html
import nltk
from nltk.corpus import stopwords

# Baixar stopwords do NLTK (se necessário)
#nltk.download('stopwords')
stopwords_pt = set(stopwords.words('portuguese'))

# Carregar o modelo spaCy
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

def is_similar(nova_frase, frases_selecionadas, limiar=0.8):
    """ Verifica se uma nova frase é muito semelhante a alguma já escolhida """
    doc_novo = nlp(nova_frase)
    for frase in frases_selecionadas:
        doc_existente = nlp(frase)
        if doc_novo.similarity(doc_existente) > limiar:
            return True
    return False

def extrair_frases_por_frequencia(texto, num_frases=3):
    """ Usa a Frequência de Palavras para selecionar frases mais importantes """

    # Processar o texto com spaCy para dividir corretamente em frases
    doc = nlp(texto)
    frases = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    if not frases:
        return "Nenhuma frase encontrada."

    # Extrair palavras relevantes (removendo stopwords e pontuação)
    palavras = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stopwords_pt]

    # Contar a frequência das palavras
    word_freq = Counter(palavras)

    # Classificar frases pela soma das frequências das palavras que elas contêm
    frase_scores = {}
    for frase in frases:
        score = sum(word_freq[token.text.lower()] for token in nlp(frase) if token.is_alpha)
        frase_scores[frase] = score

    # Ordenar frases por pontuação de relevância
    frases_ordenadas = sorted(frase_scores, key=frase_scores.get, reverse=True)

    # Selecionar frases mais relevantes sem repetições
    resumo = []
    for frase in frases_ordenadas:
        if len(resumo) >= num_frases:
            break
        if not is_similar(frase, resumo, limiar=0.8):
            resumo.append(frase)

    return ' '.join(resumo)  # Retorna o resumo final

# URL do site a ser resumido
url = "https://brasilcristao-contra-o-comunismo.blogspot.com/p/conceitos-valor-e-o-trabalho-e.html"
texto = get_clean_text_from_url(url)

# Obter o resumo com as 3 frases mais importantes pelo método Word Frequency
resumo = extrair_frases_por_frequencia(texto, num_frases=2)
print("\nResumo Extraído:\n\n", resumo+"\n")
