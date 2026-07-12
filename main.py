import os
from google import genai

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


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

    with open(file_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            "Проанализируй это фото товара. "
            "Создай идею короткого рекламного видео для Instagram/TikTok.",
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_bytes
                }
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
