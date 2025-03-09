from gtts import gTTS
import spacy
from io import BytesIO
import pygame
import speech_recognition as sr #pip install SpeechRecognition --user

# Inicializa o pygame para áudio
pygame.mixer.init()

# Carrega o modelo do SpaCy em português
nlp = spacy.load("pt_core_news_md")

# Inicializa o reconhecedor de voz
recognizer = sr.Recognizer()

# Base de dados simples (dicionário de intenções e respostas)
base_respostas = {
    "saudacao": {
        "palavras": ["olá", "oi", "e aí", "bom dia"],
        "respostas": ["Oi! Tudo bem com você?", "Olá! Como posso te ajudar hoje?", "E aí! Como está seu dia?"]
    },
    "identidade": {
        "palavras": ["quem", "você", "qual seu nome"],
        "respostas": ["Eu sou HEGEMONIA, prazer em te conhecer!", "Meu nome é HEGEMONIA, criado por Cloves Rodrigues, intergalátco!", "Sou HEGEMONIA, sua assistente virtual!"]
    },
    "tempo": {
        "palavras": ["tempo", "clima", "chover"],
        "respostas": ["Não sei o clima exato, mas espero que esteja ensolarado aí!", "O tempo está bom na sua cidade?", "Aqui na nuvem, está sempre claro!"]
    },
    "funcionamento": {
        "palavras": ["como", "funciona", "o que você faz"],
        "respostas": ["Eu escuto você, penso um pouco e respondo como um amigo!", "Funcionando com voz e inteligência, quer testar?", "Falo com você e tento entender o que precisa!"]
    },
    "agradecimento": {
        "palavras": ["obrigado", "valeu", "grato"],
        "respostas": ["De nada! Sempre aqui pra ajudar!", "Por nada, foi um prazer!", "Valeu você por me chamar!"]
    }
}

# Função para reconhecer a fala do microfone
def reconhecer_voz():
    with sr.Microphone() as source:
        print("Fale algo (ou diga 'sair')...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {texto}")
            return texto
        except sr.UnknownValueError:
            print("Não entendi.")
            return None
        except sr.RequestError:
            print("Erro de conexão.")
            return None

# Função para filtrar e processar a fala
def processar_pergunta(texto):
    if not texto:
        return "Fale algo claro pra eu te entender!"
    
    # Filtra o texto com SpaCy
    doc = nlp(texto.lower())
    # Remove stopwords e pega palavras relevantes
    palavras_filtradas = [token.text for token in doc if not token.is_stop and not token.is_punct]
    if not palavras_filtradas:
        return " veja, não peguei o que você quis dizer. Pode repetir?"
    
    # Detecta intenção com base na base de dados
    for intencao, dados in base_respostas.items():
        if any(palavra in palavras_filtradas for palavra in dados["palavras"]):
            # Escolhe uma resposta aleatória da lista
            from random import choice
            return choice(dados["respostas"])
    
    # Raciocínio simples: verifica similaridade com perguntas conhecidas
    texto_processado = " ".join(palavras_filtradas)
    if "porque" in texto.lower():
        return "você disse : {texto_processado}! Boa pergunta! Talvez porque o universo gosta de nos surpreender, né?"
    elif "seria ?" in texto.lower():
        return "você disse : {texto_processado}! Qualquer um serve, mas vou te dar minha opinião: o melhor é o que você gosta!"
    
    # Resposta padrão
    return f"você disse : {texto_processado}! Não sei bem como responder isso, você disse algo sobre {texto_processado}. Quer explicar mais?"

# Função para falar a resposta
def falar_resposta(texto, volume=1.0):
    tts = gTTS(text=texto, lang='pt')  # Voz padrão do Google
    mp3_buffer = BytesIO()
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)
    pygame.mixer.music.load(mp3_buffer)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Loop principal
def main():
    print("Chat inteligente com gTTS e STT! Fale algo ou 'sair'. Use 'volume X' para ajustar.")
    volume = 1.0
    while True:
        pergunta = reconhecer_voz()
        if pergunta and "sair" in pergunta.lower():
            falar_resposta("Tchau! Foi bom conversar com você!", volume)
            break
        elif pergunta and pergunta.lower().startswith("volume "):
            try:
                volume = float(pergunta.split()[1])
                if 0.0 <= volume <= 1.0:
                    print(f"Volume ajustado para {volume}")
                    falar_resposta(f"Volume ajustado para {volume}", volume)
                else:
                    print("Volume entre 0.0 e 1.0")
            except:
                print("Erro. Fale: 'volume 0.5'")
        else:
            resposta = processar_pergunta(pergunta)
            print(f"Resposta: {resposta}")
            falar_resposta(resposta, volume)

if __name__ == "__main__":
    main()