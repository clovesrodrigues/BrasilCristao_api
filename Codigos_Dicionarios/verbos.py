import spacy
import json
import os

# Carrega o modelo
nlp = spacy.load("pt_core_news_md")

# Arquivos
ARQUIVO_JSON = "verbos_conjugados.json"
ARQUIVO_ENTRADA = "verbos.txt"
ARQUIVO_SAIDA = "verbos_conjugados.txt"

def carregar_conjugacoes_existentes():
    """Carrega conjugações existentes do arquivo JSON, se existir."""
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8-sig") as f:
            conteudo = f.read().strip()  # Remove espaços extras e caracteres indesejados
            if conteudo:  # Apenas tenta carregar se o arquivo não estiver vazio
                return json.loads(conteudo)
            else:
                print("Aviso: O arquivo JSON está vazio.")
                return {}
    return {}

def salvar_conjugacoes(conjugacoes):
    """Salva todas as conjugações no arquivo JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(conjugacoes, f, ensure_ascii=False, indent=4)

def conjugar_verbo(verbo_lematizado):
    """Conjuga um verbo em todos os tempos verbais e retorna uma lista de formas conjugadas."""
    if verbo_lematizado.endswith("ar"):
        terminação = "ar"
        radical = verbo_lematizado[:-2]
    elif verbo_lematizado.endswith("er"):
        terminação = "er"
        radical = verbo_lematizado[:-2]
    elif verbo_lematizado.endswith("ir"):
        terminação = "ir"
        radical = verbo_lematizado[:-2]
    else:
        print(f"Verbo não segue padrão regular: {verbo_lematizado}")
        return []

    # Conjugações para todos os tempos verbais
    conjugacoes = {
        "Presente": [
            f"{radical}{'o' if terminação == 'ar' else 'o' if terminação == 'er' else 'o'}",
            f"{radical}{'as' if terminação == 'ar' else 'es' if terminação == 'er' else 'es'}",
            f"{radical}{'a' if terminação == 'ar' else 'e' if terminação == 'er' else 'e'}",
            f"{radical}{'amos' if terminação == 'ar' else 'emos' if terminação == 'er' else 'imos'}",
            f"{radical}{'ais' if terminação == 'ar' else 'eis' if terminação == 'er' else 'is'}",
            f"{radical}{'am' if terminação == 'ar' else 'em' if terminação == 'er' else 'em'}"
        ],
        "Pretérito Imperfeito": [
            f"{radical}{'ava' if terminação == 'ar' else 'ia' if terminação == 'er' else 'ia'}",
            f"{radical}{'avas' if terminação == 'ar' else 'ias' if terminação == 'er' else 'ias'}",
            f"{radical}{'ava' if terminação == 'ar' else 'ia' if terminação == 'er' else 'ia'}",
            f"{radical}{'ávamos' if terminação == 'ar' else 'íamos' if terminação == 'er' else 'íamos'}",
            f"{radical}{'áveis' if terminação == 'ar' else 'íeis' if terminação == 'er' else 'íeis'}",
            f"{radical}{'avam' if terminação == 'ar' else 'iam' if terminação == 'er' else 'iam'}"
        ],
        "Pretérito Perfeito": [
            f"{radical}{'ei' if terminação == 'ar' else 'i' if terminação == 'er' else 'i'}",
            f"{radical}{'aste' if terminação == 'ar' else 'este' if terminação == 'er' else 'iste'}",
            f"{radical}{'ou' if terminação == 'ar' else 'eu' if terminação == 'er' else 'iu'}",
            f"{radical}{'amos' if terminação == 'ar' else 'emos' if terminação == 'er' else 'imos'}",
            f"{radical}{'astes' if terminação == 'ar' else 'estes' if terminação == 'er' else 'istes'}",
            f"{radical}{'aram' if terminação == 'ar' else 'eram' if terminação == 'er' else 'iram'}"
        ],
        "Futuro do Presente": [
            f"{verbo_lematizado}ei",
            f"{verbo_lematizado}ás",
            f"{verbo_lematizado}á",
            f"{verbo_lematizado}emos",
            f"{verbo_lematizado}eis",
            f"{verbo_lematizado}ão"
        ],
        "Futuro do Pretérito": [
            f"{verbo_lematizado}ia",
            f"{verbo_lematizado}ias",
            f"{verbo_lematizado}ia",
            f"{verbo_lematizado}íamos",
            f"{verbo_lematizado}íeis",
            f"{verbo_lematizado}iam"
        ],
        "Subjuntivo Presente": [
            f"{radical}{'e' if terminação == 'ar' else 'a' if terminação == 'er' else 'a'}",
            f"{radical}{'es' if terminação == 'ar' else 'as' if terminação == 'er' else 'as'}",
            f"{radical}{'e' if terminação == 'ar' else 'a' if terminação == 'er' else 'a'}",
            f"{radical}{'emos' if terminação == 'ar' else 'amos' if terminação == 'er' else 'amos'}",
            f"{radical}{'eis' if terminação == 'ar' else 'ais' if terminação == 'er' else 'ais'}",
            f"{radical}{'em' if terminação == 'ar' else 'am' if terminação == 'er' else 'am'}"
        ],
        "Subjuntivo Pretérito Imperfeito": [
            f"{radical}{'asse' if terminação == 'ar' else 'esse' if terminação == 'er' else 'isse'}",
            f"{radical}{'asses' if terminação == 'ar' else 'esses' if terminação == 'er' else 'isses'}",
            f"{radical}{'asse' if terminação == 'ar' else 'esse' if terminação == 'er' else 'isse'}",
            f"{radical}{'ássemos' if terminação == 'ar' else 'êssemos' if terminação == 'er' else 'íssemos'}",
            f"{radical}{'ásseis' if terminação == 'ar' else 'êsseis' if terminação == 'er' else 'ísseis'}",
            f"{radical}{'assem' if terminação == 'ar' else 'essem' if terminação == 'er' else 'issem'}"
        ],
        "Imperativo Afirmativo": [
            "",  # Não há forma para "eu" no imperativo
            f"{radical}{'a' if terminação == 'ar' else 'e' if terminação == 'er' else 'e'}",
            f"{radical}{'e' if terminação == 'ar' else 'a' if terminação == 'er' else 'a'}",
            f"{radical}{'emos' if terminação == 'ar' else 'amos' if terminação == 'er' else 'amos'}",
            f"{radical}{'ai' if terminação == 'ar' else 'ei' if terminação == 'er' else 'i'}",
            f"{radical}{'em' if terminação == 'ar' else 'am' if terminação == 'er' else 'am'}"
        ]
    }

    # Junta todas as formas conjugadas em uma lista única
    formas_conjugadas = []
    for tempo in conjugacoes.values():
        formas_conjugadas.extend([forma for forma in tempo if forma])  # Ignora formas vazias
    return formas_conjugadas

def conjugar_todos_os_tempos():
    """Lê verbos de um arquivo txt, conjuga e salva em outro arquivo txt e JSON."""
    # Carrega as conjugações existentes do JSON
    verbos_conjugados = carregar_conjugacoes_existentes()
    formas_conjugadas_totais = []

    # Lê os verbos do arquivo verbos.txt
    try:
        with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
            verbos = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo '{ARQUIVO_ENTRADA}' não encontrado.")
        return

    houve_alteracao = False

    # Processa cada verbo
    for verbo in verbos:
        doc = nlp(verbo)
        verbo_lematizado = doc[0].lemma_ if doc else verbo
        print(f"Verbo lido: {verbo}, Lemma: {verbo_lematizado}")

        # Verifica se o verbo já está no JSON
        if verbo_lematizado in verbos_conjugados:
            print(f"Verbo '{verbo_lematizado}' já existe no JSON. Usando conjugações existentes.")
            formas_conjugadas = []
            for tempo in verbos_conjugados[verbo_lematizado].values():
                formas_conjugadas.extend(tempo.values())
        else:
            # Conjuga o verbo novo
            formas_conjugadas = conjugar_verbo(verbo_lematizado)
            if formas_conjugadas:
                verbos_conjugados[verbo_lematizado] = {
                    "Presente": {
                        "eu": formas_conjugadas[0], "tu": formas_conjugadas[1], "ele/ela": formas_conjugadas[2],
                        "nós": formas_conjugadas[3], "vós": formas_conjugadas[4], "eles/elas": formas_conjugadas[5]
                    },
                    "Pretérito Imperfeito": {
                        "eu": formas_conjugadas[6], "tu": formas_conjugadas[7], "ele/ela": formas_conjugadas[8],
                        "nós": formas_conjugadas[9], "vós": formas_conjugadas[10], "eles/elas": formas_conjugadas[11]
                    },
                    "Pretérito Perfeito": {
                        "eu": formas_conjugadas[12], "tu": formas_conjugadas[13], "ele/ela": formas_conjugadas[14],
                        "nós": formas_conjugadas[15], "vós": formas_conjugadas[16], "eles/elas": formas_conjugadas[17]
                    },
                    "Futuro do Presente": {
                        "eu": formas_conjugadas[18], "tu": formas_conjugadas[19], "ele/ela": formas_conjugadas[20],
                        "nós": formas_conjugadas[21], "vós": formas_conjugadas[22], "eles/elas": formas_conjugadas[23]
                    },
                    "Futuro do Pretérito": {
                        "eu": formas_conjugadas[24], "tu": formas_conjugadas[25], "ele/ela": formas_conjugadas[26],
                        "nós": formas_conjugadas[27], "vós": formas_conjugadas[28], "eles/elas": formas_conjugadas[29]
                    },
                    "Subjuntivo Presente": {
                        "eu": formas_conjugadas[30], "tu": formas_conjugadas[31], "ele/ela": formas_conjugadas[32],
                        "nós": formas_conjugadas[33], "vós": formas_conjugadas[34], "eles/elas": formas_conjugadas[35]
                    },
                    "Subjuntivo Pretérito Imperfeito": {
                        "eu": formas_conjugadas[36], "tu": formas_conjugadas[37], "ele/ela": formas_conjugadas[38],
                        "nós": formas_conjugadas[39], "vós": formas_conjugadas[40], "eles/elas": formas_conjugadas[41]
                    },
                    "Imperativo Afirmativo": {
                        "eu": "", "tu": formas_conjugadas[42], "ele/ela": formas_conjugadas[43],
                        "nós": formas_conjugadas[44], "vós": formas_conjugadas[45], "eles/elas": formas_conjugadas[46]
                    }
                }
                houve_alteracao = True
                print(f"Verbo '{verbo_lematizado}' conjugado e adicionado ao JSON.")

        # Adiciona as formas conjugadas à lista total
        formas_conjugadas_totais.extend(formas_conjugadas)

    # Salva no arquivo de saída (verbos_conjugados.txt)
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        for forma in formas_conjugadas_totais:
            f.write(f"{forma}\n")

    # Salva o JSON atualizado apenas se houve alterações
    if houve_alteracao:
        salvar_conjugacoes(verbos_conjugados)
        print(f"Conjugações atualizadas salvas em '{ARQUIVO_JSON}'.")
    else:
        print("Nenhum verbo novo foi conjugado.")

    print(f"Verbos conjugados salvos em '{ARQUIVO_SAIDA}'.")

# Teste
conjugar_todos_os_tempos()