from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os

TOKEN = os.getenv("TOKEN_BOT") or "SEU_TOKEN_AQUI"


# ---- MENU PRINCIPAL ----
def menu_principal():
    teclado = [
        [InlineKeyboardButton("Próximos Jogos", callback_data="proximos_jogos")],
        [InlineKeyboardButton("Últimos Jogos", callback_data="ultimos_jogos")],
        [InlineKeyboardButton("Elenco", callback_data="elenco")],
        [InlineKeyboardButton("Notícias", callback_data="noticias")],
    ]
    return InlineKeyboardMarkup(teclado)


# ---- HANDLERS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🟡⚫ E aí, Furioso! Escolha uma opção:", reply_markup=menu_principal()
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Remove o "loading" do botão

    if query.data == "proximos_jogos":
        await proximos_jogos(update, context)
    elif query.data == "ultimos_jogos":
        await ultimos_jogos(update, context)
    elif query.data == "elenco":
        await elenco(update, context)
    elif query.data == "noticias":
        await noticias(update, context)


# ---- FUNÇÕES DOS MENUS ----
async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")

        prox_jogo = navegador.find_element(
            By.XPATH, '//*[@id="matchesBox"]/div[3]/span'
        ).text
        await query.edit_message_text(
            f"🔥 Próximo Jogo:\n{prox_jogo}", reply_markup=menu_principal()
        )
    except Exception as e:
        await query.edit_message_text(
            f"❌ Erro: {str(e)}", reply_markup=menu_principal()
        )
    finally:
        if "navegador" in locals():
            navegador.quit()


async def ultimos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
        sleep(1)

        # Extrai os últimos 3 jogos
        resultados = []
        for i in range(1, 4):
            data = navegador.find_element(
                By.XPATH, f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[1]/span'
            ).text
            time1 = navegador.find_element(
                By.XPATH, f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[1]/a'
            ).text
            placar1 = navegador.find_element(
                By.XPATH,
                f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[2]/span[1]',
            ).text
            time2 = navegador.find_element(
                By.XPATH, f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[3]/a'
            ).text
            placar2 = navegador.find_element(
                By.XPATH,
                f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[2]/span[3]',
            ).text
            resultados.append(f"📅 {data} | {time1} {placar1}-{placar2} {time2}")

        await query.edit_message_text(
            "📊 Últimos Jogos:\n" + "\n".join(resultados), reply_markup=menu_principal()
        )
    except Exception as e:
        await query.edit_message_text(
            f"❌ Erro: {str(e)}", reply_markup=menu_principal()
        )
    finally:
        if "navegador" in locals():
            navegador.quit()


# ... (Implemente similarmente as funções 'elenco' e 'noticias')
async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
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
        # ... seu código selenium ...
        await query.edit_message_text(
            f"👥 Elenco:\nCoach: {coach}\nJogadores: {', '.join(jogadores)}",
            reply_markup=menu_principal()
        )
    except Exception as e:
        await query.edit_message_text(f"❌ Erro: {str(e)}", reply_markup=menu_principal())
    finally:
        if 'navegador' in locals():
            navegador.quit()
            ,



# ---- CONFIGURAÇÃO DO BOT ----
if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()

    # Registra apenas o start e o handler de callbacks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))

    print("Bot rodando com menus inline...")
    application.run_polling()
