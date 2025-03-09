import spacy
import json
import random
from spacy.matcher import Matcher

# Função para transformar verbos em advérbios de modo com sufixos adequados
def verbo_para_adv_modo(verb):
    # Tratamento para verbos terminados em "-ar"
    if verb.endswith("ar"):
        # Remove o "ar" e adiciona sufixos típicos de advérbios de modo
        return f"de maneira: {verb[:-2]}ado"  # Exemplo: "falar" -> "de maneira falado"
    
    # Tratamento para verbos terminados em "-er"
    elif verb.endswith("er"):
        # Remove o "er" e adiciona sufixos típicos de advérbios de modo
        return f"de forma: {verb[:-2]}ente"  # Exemplo: "fazer" -> "de forma fazente"
    
    # Tratamento para verbos terminados em "-ir"
    elif verb.endswith("ir"):
        # Remove o "ir" e adiciona sufixos típicos de advérbios de modo
        return f"de modo: {verb[:-2]}ido"  # Exemplo: "partir" -> "de modo partido"
    
    # Se o verbo não termina com "-ar", "-er" ou "-ir", retornamos um caso genérico
    else:
        return f"de maneira: {verb}"  # Exemplo: "nadar" -> "de maneira nadar"

def processar_universais(universais):
    novas_conclusoes = []
    
    if universais:
        for u in universais[-12:]:  # Pegando as últimas 3 premissas universais
            doc_u = nlp(u)  # Reprocessar a sentença para acessar os tokens
            # Encontrar o verbo e aplicar a transformação
            for token in doc_u:
                if token.pos_ == "VERB" and token.dep_ in ["ROOT", "xcomp"]:
                    adv_modo = verbo_para_adv_modo(token.lemma_)  # Transformar verbo em advérbio de modo
                    novas_conclusoes.append(f"\nTemo derivado {u.replace(token.text, adv_modo)}.")
    
    return novas_conclusoes

def identificar_predicacao(texto):
    nlp = spacy.load("pt_core_news_sm")
    matcher = Matcher(nlp.vocab)
    doc = nlp(texto)

    padrao_substrato = [{"POS": "DET", "OP": "?"}, {"POS": "NOUN"}]

    # Premissa Universal ajustada para pegar a premissa inteira (substrato + predicação)
    padrao_universal = [
        {"POS": "VERB", "DEP": {"in": ["ROOT", "xcomp"]}},  # Verbo raiz ou complemento de verbo
        #{"LEMMA": {"in": ["ser", "estar", "falar", "andar", "lutar", "fazer", "afastar", "desistir"]}},  # Ações principais
        {"POS": "NOUN", "OP": "?"},  # Objeto ou complemento (substantivo)
        {"POS": "DET", "OP": "?"}   # Determinante opcional para capturar o sujeito ou o objeto
    ]

    # Premissa Particular ajustada para pegar a premissa inteira (substrato + predicação)
    padrao_particular = [
        #{"POS": "VERB", "DEP": {"in": ["xcomp", "dobj"]}},  # Verbo com complemento direto ou expresso
        {"POS": "DET", "OP": "?"},  # Determinante opcional (pronome ou artigo)
        {"POS": "NOUN", "OP": "?"}  # Substantivo (objeto)
    ]

    # Premissa Particular Pronome ajustada para pegar pronomes com predicação
    padrao_particular_pronome = [
        {"POS": "PRON"},  # Pronome
        {"LEMMA": {"in": ["ser", "estar", "falar", "andar", "lutar", "fazer"]}},  # Ações centrais
        {"POS": "ADJ", "OP": "?"}  # Adjetivo opcional após o verbo
    ]

    padrao_efeito = [
        {"POS": "PRON"},  # Pronome pessoal
        {"POS": "VERB"}  # Qualquer verbo
    ]

    matcher.add("SUBSTRATO", [padrao_substrato])
    matcher.add("UNIVERSAL", [padrao_universal])
    matcher.add("PARTICULAR", [padrao_particular])
    matcher.add("ParticularPronome", [padrao_particular_pronome])
    matcher.add("PremissaEfeito", [padrao_efeito])
    
    matches = matcher(doc)
    
    substratos = []
    universais = []
    particulares = []
    conclusoes = []
    
    for match_id, start, end in matches:
        regra = nlp.vocab.strings[match_id]
        span = doc[start:end]
        if regra == "SUBSTRATO":
            substratos.append(span.text)
        elif regra == "UNIVERSAL":
            universais.append(span.text)
        elif regra == "PARTICULAR":
            particulares.append(span.text)
        elif regra == "PremissaEfeito":
            conclusoes.append(span.text)

    # Criar novas conclusões transformadas em advérbios de modo
    novas_conclusoes = []

    if substratos:
        novas_conclusoes = processar_universais(substratos)  
        # Adicionar as novas conclusões à lista de conclusões
        conclusoes.extend(novas_conclusoes)

    if universais:
        novas_conclusoes = processar_universais(universais)  
        # Adicionar as novas conclusões à lista de conclusões
        conclusoes.extend(novas_conclusoes)

    if particulares:
        novas_conclusoes = processar_universais(particulares)  
        # Adicionar as novas conclusões à lista de conclusões
        conclusoes.extend(novas_conclusoes)


    return {
        "substratos": substratos,
        "universais": universais,
        "particulares": particulares,
        "conclusoes": conclusoes
    }

num_resultados = 3

nlp = spacy.load("pt_core_news_md")  

with open('biblia.json', 'r', encoding='utf-8-sig') as f:
    biblia = json.load(f)

def carregar_dicionario_sinonimos(arquivo):
    dicionario = {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            partes = linha.strip().split('", "')
            if len(partes) >= 2:  # Garante que a linha tenha pelo menos uma palavra e sinônimos
                palavra = partes[0].replace('"', '')  # Remove aspas iniciais
                sinonimos = [s.replace('"', '') for s in partes[1:]]  # Remove aspas extras nos sinônimos
                dicionario[palavra] = sinonimos
    return dicionario

dicionario_sinonimos = carregar_dicionario_sinonimos('DIC_SINONIMOS.txt')

espaço = "____________________________________________________________"

def lematizar_palavra(palavra):
    doc = nlp(palavra)
    return doc[0].lemma_

while True:    
    consulta = input(espaço + "\n\nDIGITE ALGUM TERMO A SER PESQUISADO (ou 'sair' para encerrar) \n>>>   ").strip().lower()
    if consulta in ["sair", "exit"]:
        print("Saindo do programa.")
        break

    doc = nlp(consulta)

    termos = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ"]]

    resultados = []
    for livro in biblia:
        for capitulo_num, versiculos in enumerate(livro['chapters'], start=1):
            for versiculo_num, texto in enumerate(versiculos, start=1):
                if consulta in texto.lower():
                    resultados.append((livro['abbrev'], capitulo_num, versiculo_num, texto))

    sinonimos_encontrados = {}
    for termo in termos:
        if termo in dicionario_sinonimos:
            sinonimos_encontrados[termo] = dicionario_sinonimos[termo]
        else:
            sinonimos_encontrados[termo] = ["Nenhum sinônimo encontrado."]

    print("\nVERSÍCULOS (CONTEXTUALIZADOS COM AS PERGUNTAS):   \n")
    random.shuffle(resultados)
    resultados_aleatorios = resultados[:num_resultados]

    texto_versiculos = " ".join([texto for _, _, _, texto in resultados_aleatorios])
    resultado_ = identificar_predicacao(texto_versiculos)

    for livro, capitulo, versiculo, texto in resultados_aleatorios:
        print(f"{livro} {capitulo}:{versiculo} - {texto}\n")
 
    categorias_ = {
    "Substratos": resultado_["substratos"],
    "Universais": [lematizar_palavra(item) for item in resultado_["universais"]],
    "Particulares": resultado_["particulares"],
    "Conclusões": resultado_["conclusoes"]}
    
    for categoria, elementos in categorias_.items():
        if elementos:  
            print(f"Processando {categoria}: {', '.join(elementos)}\n")
            #for item in elementos:
             #   print("-", item)

    print("\nSINÔNIMOS TERMO PRICIPAL:")
    for termo, sin in sinonimos_encontrados.items():
        print(f"- {termo}: {', '.join(sin)}")

    for substrato in resultado_["substratos"]:
        # Para cada substrato encontrado, vamos procurar sinônimos
        if substrato in dicionario_sinonimos:
            sinonimos_encontrados[substrato] = dicionario_sinonimos[substrato]
        #else:
            #sinonimos_encontrados[substrato] = ["Não encontrei."]

    # Agora, você pode imprimir os sinônimos de todos os termos e substratos encontrados
    print("\nSINÔNIMOS TERMOS SUBSTRATOS:")
    for termo, sin in sinonimos_encontrados.items():
        print(f"- {termo}: {', '.join(sin)}")


       
