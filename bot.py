import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 8348647959

if not TOKEN:
    raise RuntimeError("TOKEN manquant")

print("Bot démarré avec TOKEN OK")

# =========================
# PRODUITS
# =========================

PRODUITS = {
    1: {"nom": "Produit A", "prix": 25},
    2: {"nom": "Produit B", "prix": 30},
    3: {"nom": "Produit C", "prix": 40},
    4: {"nom": "Produit D", "prix": 50},
}

# =========================
# COMMANDES
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Boutique", callback_data="boutique")],
        [InlineKeyboardButton("🧺 Panier", callback_data="panier")],
    ]
    await update.message.reply_text(
        "👋 Bienvenue sur ZONE 6\nPaiement à la livraison 🇫🇷",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def boutique(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    for pid, p in PRODUITS.items():
        await query.message.reply_text(
            f"🛍️ {p['nom']} – {p['prix']} €",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("➕ Ajouter", callback_data=f"add_{pid}")]]
            ),
        )

async def add_panier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    panier = context.user_data.get("panier", [])
    panier.append(int(query.data.split("_")[1]))
    context.user_data["panier"] = panier

    await query.message.reply_text("✅ Ajouté au
