import os
import google.generativeai as genai

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 ClipMind запущен!\n\n"
        "Отправь фото товара, и я придумаю идею рекламного клипа 📸"
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Анализирую фото...")

    photo_file = await update.message.photo[-1].get_file()

    file_path = "photo.jpg"
    await photo_file.download_to_drive(file_path)

    image = open(file_path, "rb").read()

    response = model.generate_content(
        [
            "Проанализируй это фото товара. "
            "Придумай идею короткого рекламного видео для социальных сетей.",
            {
                "mime_type": "image/jpeg",
                "data": image
            }
        ]
    )

    await update.message.reply_text(
        "🎬 Идея ClipMind:\n\n" + response.text
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, photo))

app.run_polling()
