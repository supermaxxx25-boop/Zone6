import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8430752899:AAGsIkKcdwFuYEsRq6JI_A-hRX7p92qlAck")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue sur ZONE 6\nBot en ligne ✅"
    )

def main():
    print("TOKEN =", TOKEN)
    if not TOKEN:
        raise RuntimeError("TOKEN manquant")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot démarré")
    app.run_polling()

if __name__ == "__main__":
    main()
