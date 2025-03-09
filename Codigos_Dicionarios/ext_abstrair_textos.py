import logging
from transformers import T5Tokenizer, T5ForConditionalGeneration
import fitz  # PyMuPDF
import requests
from lxml import html

logging.getLogger("transformers").setLevel(logging.ERROR)

# Carregar modelo T5 para resumo
tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Função para extrair texto de um PDF
def extrair_texto_pdf(caminho_pdf):
    """ Extrai texto de um arquivo PDF """
    doc = fitz.open(caminho_pdf)
    texto_completo = " ".join([pagina.get_text("text") for pagina in doc])
    return texto_completo

# Função para extrair texto de uma URL
def extrair_texto_url(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    # Filtra apenas elementos de texto relevantes
    text_elements = tree.xpath('//p | //h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //div[@style="text-align: center;"] | //div[@style="text-align: justify;"]')
    
    # Extrai e limpa o texto
    clean_text = "\n".join(
        [element.text_content().strip() for element in text_elements if element.text_content().strip()]
    )

    return clean_text

import random

def reduzir_texto(texto, limite=4096):
    """ Reduz o texto extrativamente, selecionando frases chave até o limite de caracteres """
    if len(texto) <= limite:
        return texto  # Se o texto já está dentro do limite, retorna o original

    # Divide o texto em frases (pode ser expandido com outro critério)
    frases = texto.split('. ')  # Divide em frases baseadas no ponto seguido de espaço

    # Se o texto é curto e já temos um número suficiente de frases, vamos apenas selecionar algumas
    if len(frases) <= 12:
        resultado = " ".join(frases[:12])
        return resultado[:limite]  # Retorna a primeira parte com limite de caracteres
    
    # Para textos maiores, seleciona aleatoriamente algumas frases para formar o resumo
    resultado = []
    total_chars = 0

    # Seleção aleatória de frases
    frases_selecionadas = random.sample(frases, k=len(frases) // 2)  # Pegando metade das frases aleatoriamente
    
    # Selecione frases até o limite de caracteres
    for frase in frases_selecionadas:
        if total_chars + len(frase) + 2 > limite:  # +2 porque o ". " foi removido antes
            break
        resultado.append(frase)
        total_chars += len(frase) + 2  # Conta o tamanho incluindo o ". "

    return ". ".join(resultado)  # Junta as frases selecionadas

# Função de resumo abstrativo
def resumo_abstrativo(texto, max_chars=512):
    """ Gera um resumo abstrativo limitado ao número de caracteres desejado """
    inputs = tokenizer("summarize: " + texto, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=512, min_length=128, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    resumo = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return resumo[:max_chars]  # Retorna o resumo cortado no limite de caracteres

# Escolher a origem do texto (PDF ou URL)
modo = "url"  # ou "pdf"
caminho_pdf = "teste.pdf"
url = "https://brasilcristao-contra-o-comunismo.blogspot.com/p/blocos-historicos-e-hegemonia.html"

if modo == "pdf":
    texto_original = extrair_texto_pdf(caminho_pdf)
elif modo == "url":
    texto_original = extrair_texto_url(url)
else:
    raise ValueError("Modo inválido. Use 'pdf' ou 'url'.")

# Passo 1: Redução para 2048 caracteres (extrativo)
texto_reduzido = reduzir_texto(texto_original, limite=2048)

# Passo 2: Geração de resumo abstrativo (280 caracteres)
resumo_final = resumo_abstrativo(texto_reduzido, max_chars=280)

print(f"\nResumo Final (280 caracteres):\n\n{resumo_final}...\n")
