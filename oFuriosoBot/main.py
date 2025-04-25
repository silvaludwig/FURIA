from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


# servico = ChromeService(ChromeDriverManager().install())
# navegador = webdriver.Chrome(service=servico)

TOKEN = "7910113942:AAE09XPX5JHgaFFMGqhKTAYjYa68Wh9jfcE"


# COMANDOS FURIOSOS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "E aí, suave? Sou o FURIOSO, bot da Fúria. \n"
        "Se liga nos comandos que vc pode mandar aqui pra mim: \n"
        "/proximos_jogos - Pra saber quando será a próxima partida Furiosa\n"
        "/ultimos_jogos - Resultados dos últimos jogos da Fúria\n"
        "/elenco - Conheça nosso time MVP\n"
        "/noticias - Notícias Furiosas!"
    )


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servico = ChromeService(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    prox_jogo = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/div[3]/span'
    ).get_attribute("innerText")
    await update.message.reply_text("Acessando base de dados...")
    await update.message.reply_text(prox_jogo)
    navegador.quit()


async def ultimos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servico = ChromeService(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    await update.message.reply_text("Acessando base de dados...")
    navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    sleep(1)
    await update.message.reply_text("Listando os três últimos jogos da Fúria...")

    # primeiro jogo
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

    # segundo jogo
    data_jogo2 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[2]/td[1]/span'
    ).get_attribute("innerText")
    time12 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[2]/td[2]/div[1]/a'
    ).get_attribute("innerText")
    placar_time12 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[2]/td[2]/div[2]/span[1]'
    ).get_attribute("innerText")
    time22 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[2]/td[2]/div[3]/a'
    ).get_attribute("innerText")
    placar_time22 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[2]/td[2]/div[2]/span[3]'
    ).get_attribute("innerText")

    # terceiro jogo
    data_jogo3 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[3]/td[1]/span'
    ).get_attribute("innerText")
    time13 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[3]/td[2]/div[1]/a'
    ).get_attribute("innerText")
    placar_time13 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[3]/td[2]/div[2]/span[1]'
    ).get_attribute("innerText")
    time23 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[3]/td[2]/div[3]/a'
    ).get_attribute("innerText")
    placar_time23 = navegador.find_element(
        By.XPATH, '//*[@id="matchesBox"]/table/tbody[1]/tr[3]/td[2]/div[2]/span[3]'
    ).get_attribute("innerText")

    sleep(1)
    await update.message.reply_text(
        f"{data_jogo} | {time1}: {placar_time1} x {time2}: {placar_time2}\n "
    )
    await update.message.reply_text(
        f"{data_jogo2} | {time12}: {placar_time12} x {time22}: {placar_time22}\n "
    )
    await update.message.reply_text(
        f"{data_jogo3} | {time13}: {placar_time13} x {time23}: {placar_time23}\n "
    )
    navegador.quit()


async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servico = ChromeService(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    await update.message.reply_text("Acessando base de dados...")
    sleep(1)
    navegador.get("https://www.hltv.org/team/8297/furia#tab-rosterBox")
    await update.message.reply_text("Listando players ativos...")
    coach = navegador.find_element(
        By.XPATH, '//*[@id="rosterBox"]/div[2]/table/tbody/tr/td[1]/a/div[2]/div'
    ).get_attribute("innerText")
    player1 = navegador.find_element(
        By.XPATH, '//*[@id="rosterBox"]/div[4]/table/tbody/tr[1]/td[1]/a/div[2]/div'
    ).get_attribute("innerText")
    player2 = navegador.find_element(
        By.XPATH, '//*[@id="rosterBox"]/div[4]/table/tbody/tr[2]/td[1]/a/div[2]/div'
    ).get_attribute("innerText")
    player3 = navegador.find_element(
        By.XPATH, '//*[@id="rosterBox"]/div[4]/table/tbody/tr[3]/td[1]/a/div[2]/div'
    ).get_attribute("innerText")
    player4 = navegador.find_element(
        By.XPATH, '//*[@id="rosterBox"]/div[4]/table/tbody/tr[4]/td[1]/a/div[2]/div'
    ).get_attribute("innerText")
    player5 = navegador.find_element(
        By.XPATH, '//*[@id="rosterBox"]/div[4]/table/tbody/tr[5]/td[1]/a/div[2]/div'
    ).get_attribute("innerText")
    await update.message.reply_text(
        f"Coach:  {coach}\n"
        f"Elenco:  {player1}  |  {player2}  |  {player3}  |  {player4}  |  {player5}"
    )
    navegador.quit()


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
    application.add_handler(CommandHandler("ultimos_jogos", ultimos_jogos))
    application.add_handler(CommandHandler("elenco", elenco))
    application.add_handler(CommandHandler("noticias", noticias))

    print("Buscando mensagens...")
    application.run_polling(poll_interval=3)
