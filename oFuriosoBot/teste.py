import aiohttp
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import os

# Configurações (use variáveis de ambiente para o token!)
TOKEN = "7910113942:AAE09XPX5JHgaFFMGqhKTAYjYa68Wh9jfcE"
HEADERS = {"User-Agent": "Mozilla/5.0"}


# ---- COMANDOS DO BOT ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensagem de boas-vindas"""
    await update.message.reply_text(
        "🟡⚫ E aí, Furioso! Sou o bot oficial da FURIA. Use um comando:\n"
        "/proximos_jogos - Próximas partidas\n"
        "/ultimos_jogos - Resultados recentes\n"
        "/elenco - Jogadores atuais\n"
        "/noticias - Notícias do time"
    )


async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca os próximos jogos da FURIA no HLTV"""
    try:
        url = "https://www.hltv.org/team/8297/furia"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Seletores atualizados (pode precisar ajustar)
                    next_match = soup.select_one(".upcomingMatches .match")
                    if next_match:
                        teams = next_match.select(".matchTeamName")
                        event = next_match.select_one(".matchEventName").text.strip()
                        date = next_match.select_one(".matchTime").text.strip()

                        resposta = (
                            f"🔥 **Próximo Jogo da FURIA** 🔥\n"
                            f"⏰ {date}\n"
                            f"🏆 {event}\n"
                            f"⚔ {teams[0].text.strip()} vs {teams[1].text.strip()}"
                        )
                    else:
                        resposta = "❌ Nenhum jogo agendado encontrado."

                    await update.message.reply_text(resposta, parse_mode="Markdown")
                else:
                    await update.message.reply_text(
                        "❌ HLTV fora do ar. Tente mais tarde!"
                    )

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao buscar jogos: {str(e)}")


async def ultimos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca os últimos 3 jogos da FURIA"""
    try:
        url = "https://www.hltv.org/team/8297/furia"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    resultados = []
                    matches = soup.select(".results-holder .result")[
                        :3
                    ]  # Limita a 3 jogos

                    for match in matches:
                        date = match.select_one(".date").text.strip()
                        team1 = match.select_one(".team1 .team").text.strip()
                        score = match.select_one(".score").text.strip()
                        team2 = match.select_one(".team2 .team").text.strip()
                        resultados.append(f"📅 {date} | {team1} {score} {team2}")

                    if resultados:
                        resposta = "📊 **Últimos Resultados**\n" + "\n".join(resultados)
                    else:
                        resposta = "❌ Nenhum resultado recente encontrado."

                    await update.message.reply_text(resposta)
                else:
                    await update.message.reply_text("❌ HLTV não respondendo.")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)}")


async def elenco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista o elenco atual da FURIA"""
    try:
        url = "https://www.hltv.org/team/8297/furia"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    players = []
                    for player in soup.select(
                        ".players-container .player"
                    ):  # Ajuste o seletor
                        name = player.select_one(".playerName").text.strip()
                        players.append(f"🎮 {name}")

                    if players:
                        resposta = "👥 **Elenco da FURIA**\n" + "\n".join(players)
                    else:
                        resposta = "❌ Nenhum jogador encontrado."

                    await update.message.reply_text(resposta)
                else:
                    await update.message.reply_text("❌ Falha ao acessar HLTV.")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)}")


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca notícias sobre a FURIA"""
    try:
        url = "https://www.hltv.org/news"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    news = []
                    for item in soup.select(".news-item")[:3]:  # Limita a 3 notícias
                        title = item.select_one(".newsline").text.strip()
                        link = "https://www.hltv.org" + item["href"]
                        news.append(f"📰 {title}\n🔗 {link}")

                    if news:
                        resposta = "📢 **Últimas Notícias**\n" + "\n\n".join(news)
                    else:
                        resposta = "❌ Nenhuma notícia recente."

                    await update.message.reply_text(resposta)
                else:
                    await update.message.reply_text("❌ Site de notícias indisponível.")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)}")


# ---- INICIALIZAÇÃO DO BOT ----
if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()

    # Registra os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("proximos_jogos", proximos_jogos))
    application.add_handler(CommandHandler("ultimos_jogos", ultimos_jogos))
    application.add_handler(CommandHandler("elenco", elenco))
    application.add_handler(CommandHandler("noticias", noticias))

    print("Bot rodando...")
    application.run_polling()
