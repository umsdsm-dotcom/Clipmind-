
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 ClipMind запущен!\n\nОтправь мне фотографию 📸, и я попробую её проанализировать."
    )

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Анализирую фото...")

    photo_file = await update.message.photo[-1].get_file()
    file_path = "user_photo.jpg"
    await photo_file.download_to_drive(file_path)

    with open(file_path, "rb") as image_file:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Опиши это изображение и предложи идею красивого видео-клипа."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/jpeg;base64,"
                            }
                        }
                    ]
                }
            ]
        )

    await update.message.reply_text(
        "🎬 Анализ готов:\n" + response.choices[0].message.content
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, photo))

app.run_polling()
