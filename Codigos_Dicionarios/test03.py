from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

class CustomLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        # Implementar lógica para processar a entrada
        return "Olá" in statement.text

    def process(self, input_statement, additional_response_selection_parameters=None):
        # Implementar lógica de resposta
        return Statement("Olá! Como posso ajudar você?")

# Criação do chatbot
chatbot = ChatBot(
    'MeuChatBot',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ]
)

# Criando a instância do CustomLogicAdapter após definir o chatbot
custom_adapter = CustomLogicAdapter(chatbot)
chatbot.logic_adapters.append(custom_adapter)  # Add custom logic adapter to the chatbot

# Supõe-se que você tenha um arquivo texto com perguntas e respostas
data = []
with open('perguntas_respostas.txt', 'r', encoding='utf-8') as file:
    # Lê todas as linhas e filtra linhas vazias
    for line in file:
        stripped_line = line.strip()
        if stripped_line:  # Adiciona à lista apenas se não estiver vazia
            data.append(stripped_line)

# Treinamento do chatbot
trainer = ListTrainer(chatbot)
trainer.train(data)

# Loop de interação com o usuário
while True:
    try:
        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            print("ChatBot: Até logo!")
            break
        response = chatbot.get_response(user_input)
        print(f"ChatBot: {response}")
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
