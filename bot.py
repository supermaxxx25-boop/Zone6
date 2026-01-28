import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8430752899:AAE-UEOqtwvSbU20BlP9-ApGwln8WY9R1x4")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue sur ZONE 6\nBot en ligne ✅"
    )

def main():
    if not TOKEN:
        raise RuntimeError("TOKEN manquant")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot démarré")
    app.run_polling()

if __name__ == "__main__":
    main()
