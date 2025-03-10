import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pesq_biblia import pesquisar_biblia  # Supondo que a função 'pesquisar_biblia' está no arquivo 'pesq_biblia.py'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Função que será chamada quando o comando /pesquisar for enviado
def pesquisar(update: Update, context: CallbackContext) -> None:
    # Receber parâmetros de pesquisa
    if len(context.args) < 2:
        update.message.reply_text(
            "📖 Para buscar um versículo da Bíblia, use o comando: /pesquisar <abreviação do livro> <capítulo> 📖\n\n"
            "Por exemplo: /pesquisar jo 3\n\n"
            "Certifique-se de usar a abreviação do livro em minúsculas (como 'gn' para Gênesis, 'ex' para Êxodo, etc.) e apenas o número do capítulo. "
            "O bot é sensível a maiúsculas e minúsculas, então use letras minúsculas para a abreviação. Boa leitura! 🙏"
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
