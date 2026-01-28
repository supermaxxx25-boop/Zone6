import os
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

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
ADMIN_ID = 8348647959  # ton ID Telegram

if not TOKEN:
    print("❌ TOKEN manquant")
    raise RuntimeError("TOKEN manquant")

print("✅ TOKEN détecté")

# =========================
# PRODUITS
# =========================

PRODUITS = {
    1: {"nom": "Produit A", "prix": 25, "image": "https://via.placeholder.com/300"},
    2: {"nom": "Produit B", "prix": 30, "image": "https://via.placeholder.com/300"},
    3: {"nom": "Produit C", "prix": 40, "image": "https://via.placeholder.com/300"},
    4: {"nom": "Produit D", "prix": 50, "image": "https://via.placeholder.com/300"},
}

# =========================
# MINI SERVEUR (Railway)
# =========================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
    server.serve_forever()

# =========================
# HANDLERS BOT
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Boutique", callback_data="boutique")],
        [InlineKeyboardButton("🧺 Mon panier", callback_data="panier")],
    ]
    await update.message.reply_text(
        "👋 Bienvenue sur ZONE 6\n💶 Paiement à la livraison 🇫🇷",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def boutique(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    for pid, p in PRODUITS.items():
        await query.message.reply_photo(
            photo=p["image"],
            caption=f"🛍️ {p['nom']}\n💶 {p['prix']} €",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("➕ Ajouter au panier", callback_data=f"add_{pid}")]]
            ),
        )

async def add_panier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    panier = context.user_data.get("panier", [])
    panier.append(int(query.data.split("_")[1]))
    context.user_data["panier"] = panier

    await query.message.reply_text("✅ Produit ajouté au panier")

async def panier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    panier = context.user_data.get("panier", [])
    if not panier:
        await query.message.reply_text("🧺 Ton panier est vide")
        return

    total = sum(PRODUITS[p]["prix"] for p in panier)
    recap = "\n".join(f"- {PRODUITS[p]['nom']}" for p in panier)

    await query.message.reply_text(
        f"🧾 Panier :\n{recap}\n\n💶 Total : {total} €",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✅ Commander", callback_data="commander")]]
        ),
    )

async def commander(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
   
