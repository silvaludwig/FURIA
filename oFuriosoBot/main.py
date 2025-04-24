from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import aiohttp
from bs4 import BeautifulSoup

TOKEN = "7910113942:AAE09XPX5JHgaFFMGqhKTAYjYa68Wh9jfcE"


# COMANDOS FURIOSOS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "E aí, suave? Sou o FURIOSO, bot da Fúria. Fala comigo... \n"
        "/proximos_jogos - Próximas partidas\n"
        "/resultados - Últimos resultados\n"
        "/elenco - Elenco atual\n"
        "/noticias - Notícias da FURIA"
    )


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aqui vai o código que busca os dados dos próximos jogos..."
    )


async def resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aqui vai o código que busca os resultados dos últimos jogos..."
    )


async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aqui vai o código que busca o elenco do time...")


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aqui vai o código que busca as últmas notícias do time..."
    )


# Configuração do bot
if __name__ == "__main__":
    print("Bot rodando...")

    application = Application.builder().token(TOKEN).build()

    # Registra os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("proximos_jogos", proximos_jogos))
    application.add_handler(CommandHandler("resultados", resultados))
    application.add_handler(CommandHandler("elenco", elenco))
    application.add_handler(CommandHandler("noticias", noticias))

    print("Buscando mensagens...")
    application.run_polling(poll_interval=3)
