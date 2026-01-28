import os
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN manquant")

async def start(update, context):
    await update.message.reply_text("✅ Bot en ligne")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot démarré")
app.run_polling()
