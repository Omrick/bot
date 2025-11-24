import os
import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Setup logging lebih detail
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token dari environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# States untuk conversation
SELECT_PAIR, SELECT_POSITION, ENTRY_PRICE, STOPLOSS, RISK_AMOUNT, TAKE_PROFIT = range(6)

class TradingBot:
    def __init__(self):
        self.application = None
        self.user_data = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Memulai bot dan menampilkan menu utama"""
        keyboard = [
            [KeyboardButton("📊 ENTRY BARU"), KeyboardButton("ℹ️ CARA PAKAI")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "🤖 **FUTURES TRADING CALCULATOR**\n\n"
            "✅ **BOT AKTIF 24/7**\n\n"
            "Fitur:\n"
            "• Position Size Calculator\n"
            "• Risk/Reward Ratio\n" 
            "• Margin & Leverage Calculator\n"
            "• PNL Calculation\n\n"
            "Klik **📊 ENTRY BARU** untuk mulai!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def keep_alive(self):
        """Function untuk menjaga bot tetap aktif"""
        while True:
            logger.info("🤖 Bot masih aktif dan running...")
            await asyncio.sleep(3600)  # Log every hour

    def run(self):
        """Menjalankan bot"""
        if not TOKEN:
            logger.error("❌ TELEGRAM_BOT_TOKEN tidak ditemukan!")
            return

        # Buat application
        self.application = Application.builder().token(TOKEN).build()
        
        # Conversation handler untuk trading flow
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex("^(📊 ENTRY BARU)$"), self.new_entry)],
            states={
                SELECT_PAIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_pair)],
                SELECT_POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.select_position)],
                ENTRY_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.entry_price)],
                STOPLOSS: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.stoploss)],
                RISK_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.risk_amount)],
                TAKE_PROFIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.take_profit)],
            },
            fallbacks=[MessageHandler(filters.Regex("^(🔙 KEMBALI|cancel)$"), self.cancel)]
        )
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(conv_handler)
        self.application.add_handler(MessageHandler(filters.Regex("^(ℹ️ CARA PAKAI)$"), self.help_info))
        self.application.add_handler(MessageHandler(filters.Regex("^(📊 ENTRY BARU)$"), self.new_entry))
        
        # Start bot dengan error handling
        logger.info("🚀 Starting Trading Bot...")
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

    # ... (semua method lainnya sama seperti sebelumnya)
    async def new_entry(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Implementation sama seperti sebelumnya
        pass
    
    # ... semua method lainnya

if __name__ == '__main__':
    bot = TradingBot()
    bot.run()
