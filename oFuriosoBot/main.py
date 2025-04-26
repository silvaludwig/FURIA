from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os


# ---- CONFIGURAÇÃO ----
def carregar_config():
    try:
        with open("config.txt", "r") as f:
            for linha in f:
                if linha.startswith("TOKEN="):
                    return linha.split("=")[1].strip()
        return None
    except FileNotFoundError:
        return None


TOKEN = carregar_config() or os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Token não encontrado. Crie config.txt com TOKEN=seu_token")


# ---- MENU ----
def menu_principal():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Próximos Jogos", callback_data="proximos_jogos")],
            [InlineKeyboardButton("Últimos Jogos", callback_data="ultimos_jogos")],
            [InlineKeyboardButton("Elenco", callback_data="elenco")],
            [InlineKeyboardButton("Notícias", callback_data="noticias")],
        ]
    )


# ---- HANDLERS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(
        update,
        "🟡⚫ E aí, Furioso! Pode me perguntar:\n"
        "- Quando é o próximo jogo?\n"
        "- Quais os últimos resultados?\n"
        "- Quem está no elenco?\n"
        "- Últimas notícias!",
        menu_principal(),
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "proximos_jogos":
        await proximos_jogos(update, context)
    elif query.data == "ultimos_jogos":
        await ultimos_jogos(update, context)
    elif query.data == "elenco":
        await elenco(update, context)
    elif query.data == "noticias":
        await noticias(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if any(p in texto for p in ["pr[óo]ximo", "jogo", "partida"]):
        await proximos_jogos(update, context)
    elif any(p in texto for p in ["[uú]ltimo", "resultado", "game", "jogos"]):
        await ultimos_jogos(update, context)
    elif any(p in texto for p in ["elenco", "jogador", "time"]):
        await elenco(update, context)
    elif any(p in texto for p in ["notícia", "novidade"]):
        await noticias(update, context)
    else:
        await send_response(
            update,
            "🤔 Não entendi. Você pode perguntar sobre:\n"
            "- Próximos jogos\n- Últimos resultados\n"
            "- Elenco\n- Notícias\n"
            "Ou use o menu abaixo:",
            menu_principal(),
        )


# ---- FUNÇÕES PRINCIPAIS ----
async def send_response(update: Update, text: str, reply_markup=None):
    """Envia resposta tratando tanto mensagens quanto callbacks de forma segura"""
    try:
        if update.callback_query:  # Verifica direto se existe o atributo
            await update.callback_query.edit_message_text(
                text=text, reply_markup=reply_markup, parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                text=text, reply_markup=reply_markup, parse_mode="Markdown"
            )
    except AttributeError:
        # Fallback seguro se a estrutura do update for inesperada
        await update.message.reply_text(text, reply_markup=reply_markup)


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")

        prox_jogo = navegador.find_element(
            By.XPATH, '//*[@id="matchesBox"]/div[3]/span'
        ).text

        await send_response(update, f"🔥 Próximo Jogo:\n{prox_jogo}", menu_principal())

    except Exception as e:
        await send_response(
            update, f"❌ Erro ao buscar jogos: {str(e)}", menu_principal()
        )
    finally:
        if "navegador" in locals():
            navegador.quit()


async def ultimos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
        sleep(2)  # Espera carregar

        resultados = []
        for i in range(1, 4):  # Pega os 3 últimos jogos
            try:
                # Extrai todos os dados de uma vez
                jogo = navegador.find_element(
                    By.XPATH, f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]'
                )

                data = jogo.find_element(By.XPATH, "./td[1]/span").text
                time1 = jogo.find_element(By.XPATH, "./td[2]/div[1]/a").text
                time2 = jogo.find_element(By.XPATH, "./td[2]/div[3]/a").text
                placar = jogo.find_element(By.XPATH, "./td[2]/div[2]").text.replace(
                    "\n", " "
                )

                resultados.append(f"📅 {data}: {time1} {placar} {time2}")
            except Exception as e:
                print(f"Erro ao extrair jogo {i}: {str(e)}")
                continue

        resposta = (
            "📊 Últimos Jogos:\n" + "\n".join(resultados)
            if resultados
            else "❌ Nenhum resultado recente"
        )

        await send_response(update, resposta, menu_principal())

    except Exception as e:
        await send_response(
            update, f"❌ Erro ao buscar resultados: {str(e)}", menu_principal()
        )
    finally:
        if "navegador" in locals():
            navegador.quit()


async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-rosterBox")
        sleep(2)

        # Coach
        try:
            coach = navegador.find_element(
                By.XPATH,
                '//*[@id="rosterBox"]/div[2]/table/tbody/tr/td[1]/a/div[2]/div',
            ).text
        except Exception:
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
            except Exception:
                continue

        resposta = (
            f"👥 *Elenco da FURIA*\n"
            f"🎮 *Coach:* {coach}\n"
            f"🟡 *Jogadores:*\n- " + "\n- ".join(jogadores)
            if jogadores
            else "❌ Nenhum jogador encontrado."
        )

        await send_response(update, resposta, menu_principal())

    except Exception as e:
        await send_response(
            update, f"❌ Erro ao buscar elenco: {str(e)}", menu_principal()
        )
    finally:
        if "navegador" in locals():
            navegador.quit()


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Feedback inicial
        await send_response(
            update, "📡 Buscando as últimas notícias furiosas...", reply_markup=None
        )

        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://draft5.gg/equipe/330-FURIA")
        sleep(3)  # Espera carregar

        # Extração dos dados
        noticias = []
        for i in range(3, 6):  # Ajuste conforme a estrutura do site
            try:
                elemento = navegador.find_element(
                    By.XPATH, f'//*[@id="AppContainer"]/div/div/div/div[2]/div[{i}]/a'
                )
                link = elemento.get_attribute("href")
                titulo = elemento.text.strip()

                # Formato MarkdownV2 (mais compatível)
                noticias.append(f"• [{titulo}]({link})")
            except Exception as e:
                print(f"Erro ao extrair notícia {i}: {str(e)}")
                continue

        # Construção da resposta
        if noticias:
            resposta = (
                "📰 *Últimas Notícias da FURIA:*\n\n"
                + "\n\n".join(noticias)
                + "\n\n🔍 [Mais notícias no Draft5](https://draft5.gg/equipe/330-FURIA)"
            )
        else:
            resposta = "❌ Nenhuma notícia encontrada no momento."

        # Envio com formatação correta
        await send_response(
            update,
            text=resposta,
            reply_markup=menu_principal(),
            # parse_mode="Markdown",  # Parâmetro corrigido
        )

    except Exception as e:
        error_msg = f"❌ Falha ao buscar notícias:\n`{str(e)}`"
        await send_response(
            update,
            text=error_msg,
            reply_markup=menu_principal(),
            # parse_mode="Markdown",
        )
    finally:
        if "navegador" in locals():
            navegador.quit()


# ---- INICIALIZAÇÃO ----
if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot FURIOSO rodando...")
    application.run_polling()
