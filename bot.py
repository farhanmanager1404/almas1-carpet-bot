from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import jdatetime
from datetime import datetime
import logging
import os

BOT_TOKEN = os.getenv('BOT_TOKEN', "8173424191:AAH8602bfeYajQKQ1ux5mIE01CIPC_xuGRk")
logging.basicConfig(level=logging.INFO)

def get_persian_date():
    now = datetime.now()
    persian_date = jdatetime.datetime.fromgregorian(datetime=now)
    return persian_date.strftime("%Y/%m/%d")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = get_persian_date()
    
    keyboard = [[KeyboardButton("📞 ارسال شماره تماس", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"🌹 سلام! امروز {date} است\n"
        f"من دستیار هوشمند شرکت فرش الماس هستم\n\n"
        f"لطفاً شماره تماس خود را ارسال کنید:",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    name = contact.first_name or "کاربر"
    
    await update.message.reply_text(
        f"✅ شماره شما ثبت شد: {contact.phone_number}\n"
        f"👋 سلام {name} عزیز! به خانواده فرش الماس خوش آمدید!\n\n"
        f"🎨 برای مشاهده محصولات و ثبت سفارش از منوی زیر استفاده کنید:",
        reply_markup=ReplyKeyboardMarkup([
            ["🏢 معرفی شرکت", "🎨 کلکسیون‌ها"],
            ["📦 ثبت سفارش", "📞 تماس با ما"],
            ["🌐 سایت و اینستاگرام"]
        ], resize_keyboard=True)
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🏢 معرفی شرکت":
        await update.message.reply_text(
            "🏢 شرکت فرش الماس\n\n"
            "• تولید کننده فرش‌های 700 تا 1500 شانه\n"
            "• با بهترین الیاف اکرولیک\n"
            "• دارای استانداردهای ISO 9001, CE\n"
            "• 30 سال تجربه\n\n"
            "📞 تلفن: 031555555"
        )
    
    elif text == "🎨 کلکسیون‌ها":
        await update.message.reply_text(
            "🎨 کلکسیون‌های فرش الماس:\n\n"
            "• الماس (کدهای A1 تا A10)\n"
            "• بهار (کدهای B1 تا B10)\n"
            "• ترنم (کدهای T1 تا T10)\n"
            "• وینتیج (کدهای V1 تا V10)\n\n"
            "📏 سایزها: 12 متری, 9 متری, 6 متری\n\n"
            "برای ثبت سفارش گزینه '📦 ثبت سفارش' را انتخاب کنید"
        )
    
    elif text == "📦 ثبت سفارش":
        await update.message.reply_text(
            "📦 برای ثبت سفارش:\n\n"
            "1. کلکسیون مورد نظر را انتخاب کنید\n"
            "2. کد طرح را مشخص کنید\n"
            "3. سایز و تعداد را انتخاب کنید\n\n"
            "📞 یا مستقیماً با ما تماس بگیرید:\n"
            "031555555 - داخلی 4\n\n"
            "🕐 پاسخگویی: شنبه تا چهارشنبه 8-16"
        )
    
    elif text == "📞 تماس با ما":
        await update.message.reply_text(
            "📞 راه‌های ارتباطی:\n\n"
            "تلفن: 031555555\n"
            "مدیریت: داخلی 1\n"
            "حسابداری: داخلی 2\n"
            "مدیر تولید: داخلی 3\n"
            "سفارشات: داخلی 4\n"
            "مشاوره: داخلی 5"
        )
    
    elif text == "🌐 سایت و اینستاگرام":
        await update.message.reply_text(
            "🌐 شبکه‌های اجتماعی:\n\n"
            "🔗 وبسایت: www.almascarpet.com\n"
            "📷 اینستاگرام: instagram.com/almascarpet\n\n"
            "برای مشاهده جدیدترین طرح‌ها ما را دنبال کنید"
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🤖 ربات فرش الماس راه‌اندازی شد...")
    print("✅ ربات آماده است! به @almas_carpet_bot بروید و /start بفرستید")
    
    application.run_polling()

if __name__ == '__main__':
    main()
