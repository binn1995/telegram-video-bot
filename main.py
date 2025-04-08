import os
import logging
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Khởi tạo log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Token của bạn
BOT_TOKEN = "7841149691:AAGXNDAGkoEo7X4uKpYbwuhLLwMEgvEO19Q"

# Hàm tải video
async def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[ext=mp4]/best',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('webpage_url')

# Hàm xử lý tin nhắn
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        url = update.message.text.strip()
        try:
            # Xóa tin nhắn chứa link của người dùng
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)

            # Gửi tin nhắn "Đang tải video..."
            loading_message = await update.message.reply_text("⏬ Đang tải video...")

            filepath, webpage_url = await download_video(url)

            # Gửi video
            await update.message.reply_video(video=open(filepath, 'rb'), caption="✅ Tải thành công!\nmade by Rio Vũ Khiêm")
            os.remove(filepath)

            # Tạo nút "Link gốc" với callback_data
            keyboard = [[InlineKeyboardButton("Link gốc", callback_data=webpage_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Gửi tin nhắn chứa nút "Link gốc"
            await update.message.reply_text(reply_markup=reply_markup)

            # Xóa tin nhắn "Đang tải video..."
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=loading_message.message_id)

        except Exception as e:
            logger.error(str(e))
            await update.message.reply_text("❌ Lỗi khi tải video. Đảm bảo link đúng hoặc thử lại sau.")

# Hàm xử lý khi người dùng nhấn nút "Link gốc"
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"Link gốc: {query.data}")

# Hàm khởi động bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(CallbackQueryHandler(button)) # Thêm handler cho button
    print("✅ Bot đang chạy...")
    app.run_polling()

if __name__ == '__main__':
    main()
