import json

# Definir categorias de pronomes com hierarquia detalhada
PRONOMES = {
    "Pronomes pessoais": {
        "caso_reto": {
            "singular": {
                "1a_pessoa": ["eu"],
                "2a_pessoa": ["tu"],
                "3a_pessoa": {"masculino": ["ele"], "feminino": ["ela"]}
            },
            "plural": {
                "1a_pessoa": ["nós"],
                "2a_pessoa": ["vós"],
                "3a_pessoa": {"masculino": ["eles"], "feminino": ["elas"]}
            }
        },
        "caso_obliquo": {
            "átonos": ["me", "te", "se", "nos", "vos", "o", "a", "lhe"],
            "tônicos": ["mim", "ti", "si", "conosco", "contigo"]
        }
    },
    "Pronomes possessivos": {
        "singular": {
            "1a_pessoa": {"objeto_singular": ["meu"], "objetos_plural": ["meus"]},
            "2a_pessoa": {"objeto_singular": ["teu"], "objetos_plural": ["teus"]},
            "3a_pessoa": {"objeto_singular": ["seu"], "objetos_plural": ["seus"]}
        },
        "plural": {
            "1a_pessoa": {"objeto_singular": ["nosso"], "objetos_plural": ["nossos"]},
            "2a_pessoa": {"objeto_singular": ["vosso"], "objetos_plural": ["vossos"]},
            "3a_pessoa": {"objeto_singular": ["seu"], "objetos_plural": ["seus"]}
        }
    },
    "Pronomes demonstrativos": {
        "presente": {"perto": ["este", "esta", "estes", "estas"], "distante": ["esse", "essa", "esses", "essas"]},
        "passado": ["aquele", "aquela", "aqueles", "aquelas"],
        "neutro": ["isto", "isso", "aquilo"]
    },
    "Pronomes indefinidos": {
        "variável": ["algum", "alguma", "alguns", "algumas", "nenhum", "nenhuma", "nenhuns", "nenhumas"],
        "invariável": ["cada", "quem", "alguém", "ninguém", "outrem"]
    },
    "Pronomes relativos": {
        "variável": ["cujo", "cuja", "cujos", "cujas"],
        "invariável": ["que", "quem", "onde"]
    },
    "Pronomes interrogativos": {
        "direto": ["quem", "que", "qual", "quais"],
        "indireto": {
            "quantidade": ["quanto", "quanta", "quantos", "quantas"],
            "modo": ["como"],
            "lugar": ["onde"],
            "gênero": ["qual", "quais"]
        }
    },
    "Pronomes de tratamento": {
        "singular": {
            "sem_abrev": {"Vossa Excelência": "V.Exa.", "Vossa Senhoria": "V.Sa.", "Vossa Majestade": "V.Maj."},
            "abreviaturas": {"V.Exa.": "Vossa Excelência", "V.Sa.": "Vossa Senhoria", "V.Maj.": "Vossa Majestade"}
        },
        "plural": {
            "sem_abrev": {"Vossas Excelências": "V.Exas.", "Vossas Senhorias": "V.Sas."},
            "abreviaturas": {"V.Exas.": "Vossas Excelências", "V.Sas.": "Vossas Senhorias"}
        }
    }
}

# Salvar em JSON
with open("pronomes.json", "w", encoding="utf-8") as json_file:
    json.dump(PRONOMES, json_file, ensure_ascii=False, indent=4)

print("Arquivo pronomes.json gerado com sucesso!")
