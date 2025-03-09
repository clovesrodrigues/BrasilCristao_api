import json
from rake_nltk import Rake
import re
import spacy

# Configuração dos caminhos de arquivos
#caminho_base = "/content/drive/My Drive/Colab Notebooks/" caminho_base + "biblia.json"
biblia_path = "biblia.json"
dicionario_path = "DICIONARIO_COMPLETO_definições.txt"
sinonimos_path = "DIC_SINONIMOS.txt"

# Carregar o arquivo JSON da Bíblia
with open(biblia_path, 'r', encoding='utf-8-sig') as f:
    biblia = json.load(f)

# Carregar o modelo de linguagem do spaCy
nlp = spacy.load("pt_core_news_sm")

# Função para carregar o dicionário de definições
def carregar_dicionario(arquivo):
    dicionario = {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            palavra, definicao = linha.strip().split('", "')
            palavra = palavra.replace('"', '').strip()
            definicao = definicao.replace('"', '').strip()
            dicionario[palavra.lower()] = definicao
    return dicionario

# Função para carregar o dicionário de sinônimos
def carregar_dicionario_sinonomos(arquivo):
    sinonomos = {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            palavra, lista_sinonomos = linha.strip().split('", "')
            palavra = palavra.replace('"', '').strip()
            sinonomos_lista = lista_sinonomos.replace('"', '').strip().split(', ')
            sinonomos[palavra.lower()] = sinonomos_lista
    return sinonomos

# Função para buscar definições no dicionário
def buscar_definicoes(palavras_chave, dicionario):
    definicoes = {}
    for palavra in palavras_chave:
        palavra_limpa = palavra.lower()
        if palavra_limpa in dicionario:
            definicoes[palavra] = dicionario[palavra_limpa]
    return definicoes

# Função para buscar sinônimos no dicionário de sinônimos
def buscar_sinonimos(palavras_chave, sinonomos):
    sinonimos = {}
    for palavra in palavras_chave:
        palavra_limpa = palavra.lower()
        if palavra_limpa in sinonomos:
            sinonimos[palavra] = ", ".join(sinonomos[palavra_limpa])
    return sinonimos

# Função para lematizar palavras-chave usando o spaCy
def lematizar_palavras(palavras):
    lemas = set()
    for palavra in palavras:
        doc = nlp(palavra)  # Análise da palavra com spaCy
        for token in doc:
            lemas.add(token.lemma_)  # Adiciona o lema (base) da palavra
    return lemas

# Inicializar o RAKE
rake = Rake(language="portuguese", min_length=3)

# Carregar os dicionários
dicionario = carregar_dicionario(dicionario_path)
sinonomos = carregar_dicionario_sinonomos(sinonimos_path)

while True:
    # Pedir o nome do livro
    livro_pesquisado = input("\n📖 Digite o nome do livro (abreviação, ex: gn para Gênesis) ou 'sair' para encerrar: ").strip().lower()
    
    if livro_pesquisado == "sair":
        print("👋 Saindo...")
        break

    # Buscar o livro no JSON
    livro_encontrado = next((livro for livro in biblia if livro["abbrev"].lower() == livro_pesquisado), None)

    if not livro_encontrado:
        print("❌ Livro não encontrado. Tente novamente.")
        continue

    print(f"\n📚 Livro encontrado: {livro_encontrado['abbrev'].upper()}")

    while True:
        # Pedir o número do capítulo
        capitulo_pesquisado = input("\n🔢 Digite o número do capítulo ou 'voltar' para escolher outro livro: ").strip().lower()
        
        if capitulo_pesquisado == "voltar" or capitulo_pesquisado == "sair":
            break

        if not capitulo_pesquisado.isdigit():
            print("⚠️ Digite um número válido.")
            continue
        
        capitulo_pesquisado = int(capitulo_pesquisado)

        # Verificar se o capítulo existe no livro
        if capitulo_pesquisado < 1 or capitulo_pesquisado > len(livro_encontrado["chapters"]):
            print("❌ Capítulo não encontrado. Digite um número válido.")
            continue

        # Pegar o texto do capítulo e gerar resumo com RAKE
        texto_capitulo = " ".join(livro_encontrado["chapters"][capitulo_pesquisado - 1])
        
        # Limitar o resumo a 512 caracteres
        if len(texto_capitulo) > 512:
            texto_capitulo_resumido = texto_capitulo[:512] + "..."
        else:
            texto_capitulo_resumido = texto_capitulo
        
        # Gerar o resumo com RAKE
        rake.extract_keywords_from_text(texto_capitulo)
        palavras_chave = rake.get_ranked_phrases()[:5]  # Top 5 palavras-chave

        # Tokenizar palavras-chave para garantir que estamos buscando palavras individuais
        palavras_individuais = set()  # Usamos um set para evitar repetições
        for chave in palavras_chave:
            palavras_individuais.update(re.findall(r'\b\w+\b', chave))  # Tokeniza as palavras

        # Lematizar as palavras-chave para melhorar a busca no dicionário
        palavras_lematizadas = lematizar_palavras(palavras_individuais)

        # Buscar as definições para as palavras-chave lematizadas
        definicoes = buscar_definicoes(palavras_lematizadas, dicionario)

        # Buscar os sinônimos para as palavras-chave lematizadas
        sinonimos = buscar_sinonimos(palavras_lematizadas, sinonomos)

        # Exibir saída
        print(f"\n📖 {livro_encontrado['abbrev'].upper()} - Capítulo {capitulo_pesquisado}")
        print(f"\n📝 Resumo: {texto_capitulo_resumido}")
        print(f"\n🏷️ Palavras-chave: {', '.join(palavras_chave)}\n")
        
        # Exibir definições
        print("🔍 Definições das palavras-chave:")
        for palavra, definicao in definicoes.items():
            print(f" - {palavra}: {definicao}")
        
        # Exibir sinônimos
        print("\n🔍 Sinônimos das palavras-chave:")
        for palavra, sinonimo in sinonimos.items():
            print(f" - {palavra}: {sinonimo}")
        
        # Permitir continuar pesquisando outros capítulos
