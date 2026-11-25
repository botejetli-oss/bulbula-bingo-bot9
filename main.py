import os
import random
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

players = {}
drawn = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in players:
        players[user.id] = random.sample(range(1, 601), 25)
        players[user.id][12] = 0

    await update.message.reply_text(
        "🎱 BAGA NAGAAAN BULBULA BINGO DHUFTAN!\n\n"
        "Kaardii kee argachuuf /card tuqi.\n"
        "Lakkoofsa waamame ilaaluuf /numbers tuqi.\n"
        "Taphni kun bilisaa dha."
    )

async def card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        players[user_id] = random.sample(range(1, 601), 25)
        players[user_id][12] = 0

    nums = players[user_id]
    msg = "🎫 KAARDII BINGO KEE\n\n"
    for i in range(5):
        msg += "  ".join(
            "FREE" if nums[i*5+j] == 0
            else str(nums[i*5+j])
            for j in range(5)
        ) + "\n"
    await update.message.reply_text(msg)

async def numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📢 LAKKOOFSA WAAMAMAN:\n"
    msg += ", ".join(map(str, sorted(drawn))) if drawn else "Ammaaf hin jiru."
    await update.message.reply_text(msg)

async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Admin qofa!")
        return
    remaining = list(set(range(1, 601)) - drawn)
    if not remaining:
        await update.message.reply_text("Lakkoofsi dhumeera!")
        return
    number = random.choice(remaining)
    drawn.add(number)
    await update.message.reply_text(f"📢 LAKKOOFSA HAARAA: {number}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("card", card))
    app.add_handler(CommandHandler("numbers", numbers))
    app.add_handler(CommandHandler("draw", draw))
    app.run_polling()

if __name__ == "__main__":
    main()
