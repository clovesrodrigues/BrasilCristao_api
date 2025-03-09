import json
from rake_nltk import Rake
import spacy
import nltk
from nltk.corpus import stopwords

# Baixar stopwords do NLTK (se necessário)
# nltk.download('punkt')
stopwords_pt = set(stopwords.words('portuguese'))

# Carregar o modelo spaCy
nlp = spacy.load("pt_core_news_md")

# Carregar o dicionário de definições
def carregar_dicionario(arquivo):
    dicionario = {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            palavra, definicao = linha.strip().split('", "')
            palavra = palavra.replace('"', '').strip()
            definicao = definicao.replace('"', '').strip()
            dicionario[palavra.lower()] = definicao
    return dicionario

# Função para gerar resumo usando RAKE
def extrair_frases_por_rake(texto, num_frases=3):
    """ Usa RAKE para identificar palavras-chave e extrair frases relevantes """
    doc = nlp(texto)
    frases = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    
    if not frases:
        return "Nenhuma frase encontrada."
    
    rake = Rake(language="portuguese", stopwords=stopwords_pt)
    rake.extract_keywords_from_text(texto)
    keywords = set(rake.get_ranked_phrases()[:12])  # Pega as 12 palavras-chave mais importantes
    
    # Dividir as palavras-chave em palavras isoladas
    palavras_isoladas = set()
    for keyword in keywords:
        palavras_isoladas.update(keyword.split())

    return ' '.join(frases[:num_frases]), palavras_isoladas  # Retorna o resumo e as palavras isoladas

# Função para buscar as definições no dicionário
def buscar_definicoes(palavras_chave, dicionario):
    definicoes = {}
    for palavra in palavras_chave:
        palavra_limpa = palavra.lower()
        if palavra_limpa in dicionario:
            definicoes[palavra] = dicionario[palavra_limpa]
        else:
            definicoes[palavra] = "Definição não encontrada."
    return definicoes

# Carregar o dicionário
dicionario = carregar_dicionario('DICIONARIO_COMPLETO_definições.txt')

# Carregar o arquivo JSON da Bíblia
with open('biblia.json', 'r', encoding='utf-8-sig') as f:
    biblia = json.load(f)

# Exemplo de uso: Digitar o nome do livro e capítulo para gerar resumo e definições
livro_pesquisado = "sl"  # Salmos como exemplo
capitulo_pesquisado = 2  # Capítulo 2 como exemplo

livro_encontrado = next((livro for livro in biblia if livro["abbrev"].lower() == livro_pesquisado), None)

if livro_encontrado:
    texto_capitulo = " ".join(livro_encontrado["chapters"][capitulo_pesquisado - 1])
    resumo, palavras_chave = extrair_frases_por_rake(texto_capitulo)
    
    # Buscar definições
    definicoes = buscar_definicoes(palavras_chave, dicionario)

    # Exibir resumo e definições
    print(f"\n📖 {livro_pesquisado.upper()} - Capítulo {capitulo_pesquisado}")
    print(f"\n📝 Resumo: {resumo}")
    
    print("\n🏷️ Palavras-chave:")
    print(", ".join(palavras_chave))

    print("\nDefinições:")
    for palavra, definicao in definicoes.items():
        print(f" - {palavra}: {definicao}")
else:
    print(f"Livro {livro_pesquisado} não encontrado.")
