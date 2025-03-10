import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import nltk
import json
from rake_nltk import Rake
import re
import spacy
import os

nltk.download('punkt_tab')

# Configuração dos caminhos de arquivos
biblia_path = "biblia.json"
dicionario_path = "DICIONARIO_COMPLETO_definições.txt"
sinonimos_path = "DIC_SINONIMOS.txt"

# Carregar o modelo de linguagem do spaCy
nlp = spacy.load("pt_core_news_sm")

# Função para carregar o JSON da Bíblia
def carregar_biblia():
    with open(biblia_path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

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
def carregar_dicionario_sinonimos(arquivo):
    sinonimos = {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            palavra, lista_sinonimos = linha.strip().split('", "')
            palavra = palavra.replace('"', '').strip()
            sinonimos_lista = lista_sinonimos.replace('"', '').strip().split(', ')
            sinonimos[palavra.lower()] = sinonimos_lista
    return sinonimos

# Função para buscar definições no dicionário
def buscar_definicoes(palavras_chave, dicionario):
    return {palavra: dicionario[palavra.lower()] for palavra in palavras_chave if palavra.lower() in dicionario}

# Função para buscar sinônimos no dicionário de sinônimos
def buscar_sinonimos(palavras_chave, sinonimos):
    return {palavra: sinonimos[palavra.lower()] for palavra in palavras_chave if palavra.lower() in sinonimos}

# Função para lematizar palavras-chave usando o spaCy
def lematizar_palavras(palavras):
    return {token.lemma_ for palavra in palavras for token in nlp(palavra)}

# Inicializar o RAKE
rake = Rake(language="portuguese", min_length=3)

# Carregar os dados
biblia = carregar_biblia()
dicionario = carregar_dicionario(dicionario_path)
sinonimos = carregar_dicionario_sinonimos(sinonimos_path)

# Função para pesquisar na Bíblia
def pesquisar_biblia(livro_pesquisado, capitulo_pesquisado):
    logging.info(f"Pesquisando Bíblia: {livro_pesquisado}, capítulo: {capitulo_pesquisado}")  # Agora 'logging' está importado
    # Buscar o livro no JSON
    livro_encontrado = next((livro for livro in biblia if livro["abbrev"].lower() == livro_pesquisado), None)

    if not livro_encontrado:
        return "❌ Livro não encontrado. Tente novamente."

    if not capitulo_pesquisado.isdigit():
        return "⚠️ Digite um número válido para o capítulo."

    capitulo_pesquisado = int(capitulo_pesquisado)

    if capitulo_pesquisado < 1 or capitulo_pesquisado > len(livro_encontrado["chapters"]):
        return "❌ Capítulo não encontrado. Digite um número válido."

    texto_capitulo = " ".join(livro_encontrado["chapters"][capitulo_pesquisado - 1])

    rake.extract_keywords_from_text(texto_capitulo)
    palavras_chave = rake.get_ranked_phrases()[:3]

    palavras_individuais = set(re.findall(r'\b\w+\b', " ".join(palavras_chave)))
    palavras_lematizadas = lematizar_palavras(palavras_individuais)

    definicoes = buscar_definicoes(palavras_lematizadas, dicionario)
    sinonimos_encontrados = buscar_sinonimos(palavras_lematizadas, sinonimos)  # Renomeado a variável

    resultado = f"\n📖 {livro_encontrado['abbrev'].upper()} - Capítulo {capitulo_pesquisado}"
    resultado += f"\n\n📝 TEXTO BÍBLICO : \n\n{texto_capitulo[:1024]}..." #{texto_capitulo[:512]}... se der problema
    resultado += f"\n\n👉🏻Siga t.me/CRIADOR_DE_CONTEUDO_DIREITA 📖✨ \n🇧🇷🇧🇷🇧🇷 E add @biblialize_bot no seu Grupo tb ! 🇧🇷🇧🇷🇧🇷\n JESUS É TOP !\n"

    if definicoes:
        resultado += "\n🔍 Definições das palavras-chave:\n"
        resultado += "\n".join(f" - {palavra}: {definicao}" for palavra, definicao in definicoes.items())

    if sinonimos_encontrados:  # Alterado para a nova variável
        resultado += "\n\n🔍 Sinônimos das palavras-chave:\n"
        resultado += "\n".join(f" - {palavra}: {', '.join(sinonimos)}" for palavra, sinonimos in sinonimos_encontrados.items())

    return resultado

# Função que será chamada quando o comando /pesquisar for enviado
def pesquisar(update: Update, context: CallbackContext) -> None:
    # Receber parâmetros de pesquisa
    if len(context.args) < 2:
        update.message.reply_text(
    "📖 Para buscar um versículo da Bíblia, use o comando: /biblia <abreviação do livro> <capítulo> 📖\n\n"
    "Por exemplo: /biblia jo 3\n\n"
    "Certifique-se de usar a abreviação do livro em minúsculas (como 'gn' para Gênesis, 'ex' para Êxodo, etc.) e apenas o número do capítulo. "
    "O bot é sensível a maiúsculas e minúsculas, então use letras minúsculas para a abreviação. Boa leitura! 🙏"
    "👉🏻Siga t.me/CRIADOR_DE_CONTEUDO_DIREITA 📖✨ 🇧🇷🇧🇷🇧🇷 E add @biblialize_bot no seu Grupo tb ! 🇧🇷🇧🇷🇧🇷"
    )
        return

    livro = context.args[0]  # O primeiro parâmetro é o livro
    capitulo = context.args[1]  # O segundo parâmetro é o capítulo

    # Chamar a função pesquisar_biblia e obter o resultado
    resultado = pesquisar_biblia(livro, capitulo)

    # Enviar o resultado de volta para o Telegram
    update.message.reply_text(resultado)

# Função principal que inicia o bot
def main() -> None:
    # Substitua pelo seu token do bot TELEGRAM_TOKEN, agora pegando do ambiente
    token = os.getenv('TELEGRAM_TOKEN')

    if not token:
        print("Erro: O token do Telegram não foi encontrado.")
        return

    # Criar o updater e o dispatcher
    updater = Updater(token)

    # Obter o dispatcher para registrar os handlers
    dispatcher = updater.dispatcher

    # Registrar os comandos TELEGRAM_TOKEN
    dispatcher.add_handler(CommandHandler("biblia", pesquisar))

    # Iniciar o bot
    updater.start_polling()

    # Manter o bot rodando
    updater.idle()

if __name__ == '__main__':
    main()
