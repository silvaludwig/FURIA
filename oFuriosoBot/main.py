from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os


def carregar_config():
    try:
        with open("config.txt", "r") as f:
            for linha in f:
                if linha.startswith("TOKEN="):
                    return linha.split("=")[1].strip()
        return None
    except FileNotFoundError:
        return None


TOKEN = carregar_config() or os.getenv(
    "TELEGRAM_TOKEN"
)  # Fallback para variável de ambiente

if not TOKEN:
    raise ValueError(
        "Token não encontrado. Crie um arquivo config.txt com TOKEN=seu_token"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if any(palavra in texto for palavra in ["próximo", "jogo", "partida"]):
        await proximos_jogos(update, context)
    elif any(palavra in texto for palavra in ["último", "resultado"]):
        await ultimos_jogos(update, context)
    elif any(palavra in texto for palavra in ["elenco", "jogador", "time"]):
        await elenco(update, context)
    elif any(palavra in texto for palavra in ["notícia", "novidade"]):
        await noticias(update, context)
    else:
        await update.message.reply_text(
            "🤔 Não entendi. Você pode perguntar sobre:\n"
            "- Próximos jogos\n- Últimos resultados\n- Elenco\n- Notícias\n"
            "Ou use o menu abaixo:",
            reply_markup=menu_principal(),
        )


# servico = ChromeService(ChromeDriverManager().install())
# navegador = webdriver.Chrome(service=servico)

# TOKEN = "7910113942:AAE09XPX5JHgaFFMGqhKTAYjYa68Wh9jfcE"


# COMANDOS FURIOSOS
def menu_principal():
    teclado = [
        [InlineKeyboardButton("Próximos Jogos", callback_data="proximos_jogos")],
        [InlineKeyboardButton("Últimos Jogos", callback_data="ultimos_jogos")],
        [InlineKeyboardButton("Elenco", callback_data="elenco")],
        [InlineKeyboardButton("Notícias", callback_data="noticias")],
    ]
    return InlineKeyboardMarkup(teclado)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "E aí, suave? Sou o FURIOSO, bot da Fúria. \n" "O que manda pra hj?",
        reply_markup=menu_principal(),
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


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_callback = hasattr(update, "callback_query")
    query = update.callback_query
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")

        prox_jogo = navegador.find_element(
            By.XPATH, '//*[@id="matchesBox"]/div[3]/span'
        ).text

        resposta = f"🔥 Próximo Jogo:\n{prox_jogo}"

        if is_callback:
            await query.edit_message_text(resposta, reply_markup=menu_principal())
        else:
            await update.message.reply_text(resposta, reply_markup=menu_principal())

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


async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-rosterBox")
        sleep(2)  # Espera carregar

        # Coach
        try:
            coach = navegador.find_element(
                By.XPATH,
                '//*[@id="rosterBox"]/div[2]/table/tbody/tr/td[1]/a/div[2]/div',
            ).text
        except NoSuchElementException:
            coach = "Não identificado"

        # Jogadores
        jogadores = []
        for i in range(1, 6):
            try:
                jogador = navegador.find_element(
                    By.XPATH,
                    f'//*[@id="rosterBox"]/div[4]/table/tbody/tr[{i}]/td[1]/a/div[2]/div',
                ).text
                jogadores.append(jogador)
            except NoSuchElementException:
                continue

        if jogadores:
            resposta = (
                f"👥 *Elenco da FURIA*\n"
                f"🎮 *Coach:* {coach}\n"
                f"🟡 *Jogadores:*\n- " + "\n- ".join(jogadores)
            )
        else:
            resposta = "❌ Nenhum jogador encontrado."

        await query.edit_message_text(resposta, reply_markup=menu_principal())

    except WebDriverException as e:
        await query.edit_message_text(f"❌ Erro no navegador: {str(e)}")
    except Exception as e:
        await query.edit_message_text(f"❌ Erro inesperado: {str(e)}")
    finally:
        if "navegador" in locals():
            navegador.quit()


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.edit_message_text(
            "📡 Buscando notícias furiosas...", reply_markup=None
        )  # Feedback inicial

        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://draft5.gg/equipe/330-FURIA")
        sleep(5)

        # Extrai links E títulos (se disponíveis)
        noticias = []
        for i in range(3, 6):  # Adapte para os índices corretos
            try:
                link_element = navegador.find_element(
                    By.XPATH, f'//*[@id="AppContainer"]/div/div/div/div[2]/div[{i}]/a'
                )
                link = link_element.get_attribute("href")
                titulo = link_element.text.strip()  # Título da notícia
                noticias.append(
                    f"• <a href='{link}'>{titulo}</a>"
                    if titulo
                    else f"• <a href='{link}'>Link da notícia</a>"
                )
            except Exception:
                continue

        if noticias:
            resposta = (
                "📰 <b>Últimas Notícias da FURIA:</b>\n\n"
                + "\n".join(noticias)
                + "\n\n🔍 Mais em: <a href='https://draft5.gg/equipe/330-FURIA'>Draft5</a>"
            )
        else:
            resposta = "❌ Nenhuma notícia encontrada no momento."

        await query.edit_message_text(
            resposta,
            reply_markup=menu_principal(),
            parse_mode="HTML",  # Permite formatação HTML (links clicáveis)
            disable_web_page_preview=False,
        )

    except Exception as e:
        await query.edit_message_text(
            f"❌ Falha ao buscar notícias: {str(e)}", reply_markup=menu_principal()
        )
    finally:
        if "navegador" in locals():
            navegador.quit()


# # Configuração do bot
# if __name__ == "__main__":
#     print("Bot rodando...")

#     application = Application.builder().token(TOKEN).build()

#     # Registra apenas o start e o handler de callbacks
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(button_click))

#     print("Buscando mensagens...")
#     application.run_polling(poll_interval=3)

if __name__ == "__main__":
    print("Iniciando bot FURIOSO...")

    # Carrega configurações
    TOKEN = carregar_config() or os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("Token não encontrado!")

    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot pronto para receber mensagens...")
    application.run_polling()
