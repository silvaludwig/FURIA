from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeService
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
from time import sleep

# Configurações
TOKEN = "7910113942:AAE09XPX5JHgaFFMGqhKTAYjYa68Wh9jfcE"
logging.basicConfig(level=logging.INFO)


# ---- FUNÇÕES PRINCIPAIS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "E aí, Furioso! Sou o bot da FURIA. Use:\n"
        "/proximos_jogos - Próximas partidas\n"
        "/ultimos_jogos - Resultados recentes\n"
        "/elenco - Jogadores atuais\n"
        "/noticias - Notícias do time"
    )


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")

        prox_jogo = navegador.find_element(
            By.XPATH, '//*[@id="matchesBox"]/div[3]/span'
        ).text
        await update.message.reply_text(f"🔥 **Próximo Jogo:**\n{prox_jogo}")

    except NoSuchElementException:
        await update.message.reply_text(
            "❌ Não consegui encontrar o próximo jogo. A HLTV pode ter atualizado o layout."
        )
    except WebDriverException as e:
        await update.message.reply_text(f"❌ Erro no navegador: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro inesperado: {str(e)}")
    finally:
        if "navegador" in locals():
            navegador.quit()


async def ultimos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")

        resultados = []
        for i in range(1, 4):
            try:
                data = navegador.find_element(
                    By.XPATH, f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[1]/span'
                ).text
                time1 = navegador.find_element(
                    By.XPATH,
                    f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[1]/a',
                ).text
                placar1 = navegador.find_element(
                    By.XPATH,
                    f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[2]/span[1]',
                ).text
                time2 = navegador.find_element(
                    By.XPATH,
                    f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[3]/a',
                ).text
                placar2 = navegador.find_element(
                    By.XPATH,
                    f'//*[@id="matchesBox"]/table/tbody[1]/tr[{i}]/td[2]/div[2]/span[3]',
                ).text
                resultados.append(f"📅 {data} | {time1} {placar1}-{placar2} {time2}")
            except NoSuchElementException:
                continue

        if resultados:
            await update.message.reply_text(
                "📊 **Últimos Resultados:**\n" + "\n".join(resultados)
            )
        else:
            await update.message.reply_text("❌ Nenhum resultado recente encontrado.")

    except WebDriverException as e:
        await update.message.reply_text(f"❌ Erro no navegador: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro inesperado: {str(e)}")
    finally:
        if "navegador" in locals():
            navegador.quit()


async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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
                f"⚫ *Jogadores:*\n- " + "\n- ".join(jogadores)
            )
        else:
            resposta = "❌ Nenhum jogador encontrado."

        await update.message.reply_text(resposta)

    except WebDriverException as e:
        await update.message.reply_text(f"❌ Erro no navegador: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro inesperado: {str(e)}")
    finally:
        if "navegador" in locals():
            navegador.quit()


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        servico = ChromeService(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://draft5.gg/equipe/330-FURIA")
        sleep(3)  # Espera carregar

        # Extrai links das notícias
        links = []
        for i in range(3, 6):  # Ajuste conforme o layout do Draft5
            try:
                link = navegador.find_element(
                    By.XPATH, f'//*[@id="AppContainer"]/div/div/div/div[2]/div[{i}]/a'
                ).get_attribute("href")
                links.append(link)
            except NoSuchElementException:
                continue

        if links:
            resposta = "📢 **Últimas Notícias:**\n" + "\n\n".join(links)
        else:
            resposta = "❌ Nenhuma notícia recente encontrada."

        await update.message.reply_text(resposta)

    except WebDriverException as e:
        await update.message.reply_text(f"❌ Erro no navegador: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro inesperado: {str(e)}")
    finally:
        if "navegador" in locals():
            navegador.quit()


# ---- INICIALIZAÇÃO DO BOT ----
if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("proximos_jogos", proximos_jogos))
    application.add_handler(CommandHandler("ultimos_jogos", ultimos_jogos))
    application.add_handler(CommandHandler("elenco", elenco))
    application.add_handler(CommandHandler("noticias", noticias))

    print("Bot rodando...")
    application.run_polling()
