from typing import Final
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    filters,
    Application,
)


TOKEN: Final = "7910113942:AAE09XPX5JHgaFFMGqhKTAYjYa68Wh9jfcE"
BOT_FINAL: Final = "@oFuriosoBot"


async def start(update: Update, context: CallbackContext):
    pass


async def proximos_jogos(update: Update, context: CallbackContext):
    pass


async def resultados(update: Update, context: CallbackContext):
    pass
