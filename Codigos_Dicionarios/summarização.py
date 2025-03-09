import spacy

from lxml import html
import requests

from summarizer import Summarizer

def get_clean_text_from_url(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    # Filtra apenas elementos de texto relevantes
    text_elements = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //div[@style="text-align: center;"] | //div[@style="text-align: justify;"]')
    
    # Extrai e limpa o texto
    clean_text = "\n".join(
        [element.text_content().strip() for element in text_elements if element.text_content().strip()]
    )

    return clean_text

def extrative_summary_bert(text, max_length=1):  # Aqui você pode ajustar a quantidade de frases
    model = Summarizer()
    summary = model(text)
    
    # Controlar o número de frases no resumo
    sentences = summary.split('. ')  # Divida as frases pelo ponto seguido de espaço
    if len(sentences) > max_length:
        summary = '. '.join(sentences[:max_length]) + '.'
    
    return summary

url = "https://brasilcristao-contra-o-comunismo.blogspot.com"

text = get_clean_text_from_url(url)
texto_tratado_01 = extrative_summary_bert(text)
#texto_final = extrative_summary_bert(texto_tratado_01)
print(texto_tratado_01)