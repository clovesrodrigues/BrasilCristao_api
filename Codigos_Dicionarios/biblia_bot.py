import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from pesq_biblia import pesquisar_biblia  # Supondo que a função 'pesquisar_biblia' está no arquivo 'pesq_biblia.py'

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Função que será chamada quando o comando /pesquisar for enviado
async def pesquisar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Receber parâmetros de pesquisa
    if len(context.args) < 2:
        await update.message.reply_text(
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
    await update.message.reply_text(resultado)

# Função principal que inicia o bot
async def main() -> None:
    # Substitua pelo seu token do bot
    token = '7935309073:AAExRc1FgYYwLoxVi_nJ3mneObs9anI5GM4'

    # Criar a Application
    application = Application.builder().token(token).build()

    # Registrar os comandos
    application.add_handler(CommandHandler("pesquisar", pesquisar))

    # Iniciar o bot de forma assíncrona
    try:
        await application.run_polling()
    finally:
        await application.shutdown()

if __name__ == '__main__':
    import asyncio
    # Executar o bot com asyncio, sem tentar manipular o loop manualmente
    asyncio.run(main())  # Usar asyncio.run() diretamente
