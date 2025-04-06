from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from stay_alive import keep_alive
import yt_dlp
import os

TOKEN = "7841149691:AAGXNDAGkoEo7X4uKpYbwuhLLwMEgvEO19Q"  # 🔁 Thay bằng token bot Telegram của bạn

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Gửi link video Facebook hoặc TikTok để mình tải nhé!")

def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[ext=mp4]',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if 'facebook.com' in url or 'fb.watch' in url or 'tiktok.com' in url:
        try:
            await update.message.reply_text("⏳ Đang tải video...")
            video_path = download_video(url)
            with open(video_path, 'rb') as f:
                await update.message.reply_video(f, caption="✅ Tải xong rồi nè!\nMade by Rio Vũ Khiêm")
            os.remove(video_path)
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi tải video: {e}")
    else:
        await update.message.reply_text("❓ Gửi link video từ Facebook hoặc TikTok nhé!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
