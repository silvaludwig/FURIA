from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service
from selenium.webdriver import ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# servico = ChromeService(ChromeDriverManager().install())
# navegador = webdriver.Chrome(service=servico)

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
    servico = ChromeService(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    prox_jogo = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/div[3]/span'
    ).get_attribute("innerText")
    await update.message.reply_text(
        "Aqui vai o código que busca os dados dos próximos jogos..."
    )
    await update.message.reply_text(f"Próximo Jogo: {prox_jogo}")


async def resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servico = ChromeService(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)

    navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    data_jogo = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[1]/td[1]/span'
    ).get_attribute("innerText")
    time1 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[1]/td[2]/div[1]/a'
    ).get_attribute("innerText")
    placar_time1 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[1]/td[2]/div[2]/span[1]'
    ).get_attribute("innerText")
    time2 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[1]/td[2]/div[3]/a'
    ).get_attribute("innerText")
    placar_time2 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[1]/td[2]/div[2]/span[3]'
    ).get_attribute("innerText")

    await update.message.reply_text(
        "Aqui vai o código que busca os resultados dos últimos jogos..."
    )
    await update.message.reply_text(
        f"{data_jogo} | {time1}: {placar_time1} x {time2}: {placar_time2} "
    )
    navegador.quit()


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
