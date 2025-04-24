from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import aiohttp
from bs4 import BeautifulSoup

TOKEN = "7910113942:AAE09XPX5JHgaFFMGqhKTAYjYa68Wh9jfcE"


# COMANDOS FURIOSOS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🟡⚫ Olá, furioso! Sou o FURIOSO, bot da Fúria. Use um comando:\n"
        "/proximos_jogos - Próximas partidas\n"
        "/resultados - Últimos resultados\n"
        "/jogadores - Elenco atual"
        # "/noticias - Notícias da FURIA"
    )


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Exemplo com API assíncrona (aiohttp)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://hltv-api.vercel.app/api/matches.json"
            ) as response:
                if response.status == 200:
                    dados = await response.json()
                    resposta = "Próximos jogos da FURIA:\n"
                    for jogo in dados[:3]:  # Exibe os 3 próximos jogos
                        resposta += f"➡ {jogo['data']} - {jogo['times'][0]} vs {jogo['times'][1]}\n"
                    await update.message.reply_text(resposta)
                else:
                    await update.message.reply_text(
                        "❌ API fora do ar. Tente mais tarde!"
                    )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")


async def resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://hltv-api.vercel.app/api/results?team=FURIA"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                dados = await response.json()
                resposta = "Últimos resultados da FURIA:\n"
                for jogo in dados[:5]:
                    resposta += f"✔ {jogo['team1']} {jogo['score']} {jogo['team2']} ({jogo['mapa']})\n"
                await update.message.reply_text(resposta)
                await update.message.reply_text(
                    "Digite /jogador e o nome do jogador pra ver mais sobre ele"
                )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)}")


async def jogadores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://hltv-api.vercel.app/api/team/8297"  # ID da FURIA
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                dados = await response.json()
                resposta = "👾 Elenco da FURIA:\n"
                for jogador in dados["players"]:
                    resposta += (
                        f"➡ {jogador['nickname']} (Rating: {jogador['rating']})\n"
                    )
                await update.message.reply_text(resposta)
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)}")


async def jogador_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome_jogador = context.args[0]  # /jogador KSCERATO
    # Busca dados do jogador na API e formata a resposta
    await update.message.reply_text(f"📊 Estatísticas de {nome_jogador}: ...")


# Configuração do bot
if __name__ == "__main__":
    print("Bot rodando...")

    application = Application.builder().token(TOKEN).build()

    # Registra os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("proximos_jogos", proximos_jogos))
    application.add_handler(CommandHandler("resultados", resultados))
    application.add_handler(CommandHandler("jogador", jogador_info))

    print("Buscando mensagens...")
    application.run_polling(poll_interval=3)
