from gtts import gTTS
import pygame
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from io import BytesIO
import speech_recognition as sr

# Inicializa o pygame para áudio
pygame.mixer.init()

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

# Função para reconhecer a fala do microfone
'''def reconhecer_voz():
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
            return None'''

# Definindo o CustomLogicAdapter
class CustomLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):  # Corrigido para __init__
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return "Olá" in statement.text

    def process(self, input_statement, additional_response_selection_parameters=None):
        return Statement("Olá! Como posso ajudar você?")

# Criação do ChatBot
chatbot = ChatBot(
    'MeuChatBot',
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.MathematicalEvaluation'
    ],
    database_uri='sqlite:///database.sqlite3'
)

# Supõe-se que você tenha um arquivo texto com perguntas e respostas
data = []
try:
    with open('perguntas_respostas.txt', 'r', encoding='utf-8') as file:  # Adicionando encoding
        for line in file:
            stripped_line = line.strip()
            if stripped_line:  # Adiciona à lista apenas se não estiver vazia
                data.append(stripped_line)
except FileNotFoundError:
    print("O arquivo perguntas_respostas.txt não foi encontrado.")
except UnicodeDecodeError:
    print("Erro de codificação ao ler o arquivo. Verifique a codificação do arquivo.")

# Treinamento do ChatBot
trainer = ListTrainer(chatbot)
trainer.train(data)

# Loop de interação com o usuário
def main():
    print("Chat inteligente com o ChatBot! Fale algo ou 'sair'.")
    volume = 1.0
    while True:
        try:
            user_input = input("Você: ")
            #pergunta = reconhecer_voz()
            if user_input.lower() == 'sair':
                falar_resposta("Até logo!", volume)
                break
            response = chatbot.get_response(user_input)
            print(f"ChatBot: {response}")
            falar_resposta(str(response), volume)  # Resposta em voz alta
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

if __name__ == "__main__":  # Corrigido
    main()  # Este ponto de entrada deve estar sempre no final
