import spacy
from spacy.matcher import Matcher

def identificar_predicacao(texto):
    nlp = spacy.load("pt_core_news_sm")
    matcher = Matcher(nlp.vocab)
    doc = nlp(texto)

    # Padrões para substratos (sujeitos)
    padrao_substrato = [{"POS": "DET", "OP": "?"}, {"POS": "NOUN"}]
    
    # Padrões para predicações universais (ex: "A virtude é necessária")
    padrao_universal = [
        {"POS": "NOUN", "DEP": "nsubj"},
        {"LEMMA": "ser"},
        {"POS": "ADJ"}
    ]
    
    # Padrões para predicações particulares (ex: "João é inteligente", "Ele é forte")
    padrao_particular = [
        {"POS": "PROPN"},
        {"LEMMA": "ser"},
        {"POS": "ADJ"}
    ]
    
    padrao_particular_pronome = [
        {"POS": "PRON"},
        {"LEMMA": "ser"},
        {"POS": "ADJ"}
    ]
    
    matcher.add("SUBSTRATO", [padrao_substrato])
    matcher.add("UNIVERSAL", [padrao_universal])
    matcher.add("PARTICULAR", [padrao_particular, padrao_particular_pronome])
    
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
    
    # Identificação de conclusões a partir de premissas particulares
    if particulares:
        conclusoes.append(f"Conclusão derivada: {particulares[-1]}")
    
    return {
        "substratos": substratos,
        "universais": universais,
        "particulares": particulares,
        "conclusoes": conclusoes
    }

# Exemplo de uso
versiculos = [
    ("Mateus", 5, 9, "Bem-aventurados os pacificadores, porque eles serão chamados filhos de Deus."),
    ("Provérbios", 15, 1, "A resposta branda desvia o furor, mas a palavra dura suscita a ira."),
    ("João", 8, 32, "E conhecereis a verdade, e a verdade vos libertará.")
]

# Concatenar os textos para análise
texto_versiculos = " ".join([versiculo[3] for versiculo in versiculos])
resultado_ = identificar_predicacao(texto_versiculos)

# Exibir resultados
categorias_ = {
    "Substratos": resultado_["substratos"],
    "Universais": resultado_["universais"],
    "Particulares": resultado_["particulares"],
    "Conclusões": resultado_["conclusoes"]
}

for categoria, elementos in categorias_.items():
    if elementos:  # Garante que só imprime se houver elementos na categoria
        print(f"\n{categoria}:")
        for item in elementos:
            print(f"- {item}")
