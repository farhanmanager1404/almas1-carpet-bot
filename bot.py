from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import jdatetime
from datetime import datetime
import logging
import os

# تنظیمات اولیه - بعداً با محیط اجرا جایگزین می‌شود
BOT_TOKEN = os.getenv('BOT_TOKEN', "YOUR_BOT_TOKEN_HERE")
logging.basicConfig(level=logging.INFO)

def get_persian_date():
    """دریافت تاریخ شمسی"""
    now = datetime.now()
    persian_date = jdatetime.datetime.fromgregorian(datetime=now)
    return f"{persian_date.strftime('%A')} {persian_date.day} {persian_date.strftime('%B')} {persian_date.year}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع ربات"""
    user = update.effective_user
    date = get_persian_date()
    
    welcome_text = (
        f"🌹 سلام {user.first_name}! امروز {date} است\n\n"
        f"من دستیار هوشمند شرکت فرش الماس هستم. "
        f"خیلی خوشحالم که میتونم به شما کمک کنم.\n\n"
        f"اول اجازه بدید شماره شما را ببینم تا شما را بخاطر بسپارم."
    )
    
    keyboard = [[KeyboardButton("📞 تایید شماره تماس", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دریافت شماره تماس"""
    contact = update.message.contact
    name = contact.first_name or "کاربر"
    
    await update.message.reply_text(
        f"✅ شماره شما ثبت شد: {contact.phone_number}\n"
        f"👋 سلام {name} عزیز! به خانواده فرش الماس خوش آمدید!\n\n"
        f"🎨 حالا میتونید از منوی زیر استفاده کنید:",
        reply_markup=ReplyKeyboardMarkup([
            ["🏢 معرفی شرکت", "🎨 کلکسیون‌ها"],
            ["📦 ثبت سفارش", "📞 تماس با ما"],
            ["🌐 سایت و اینستاگرام"]
        ], resize_keyboard=True)
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت متن‌های دریافتی"""
    text = update.message.text
    
    if text == "🏢 معرفی شرکت":
        await update.message.reply_text(
            "🏢 **شرکت فرش الماس**\n\n"
            "تولید کننده انواع فرش‌های:\n"
            "• ۷۰۰ شانه\n• ۱۰۰۰ شانه\n• ۱۲۰۰ شانه\n• ۱۵۰۰ شانه\n\n"
            "با تراکم‌های مختلف از بهترین الیاف اکرولیک\n\n"
            "📜 **دارای استانداردهای:**\n"
            "• ISO 9001\n• ISO 2000\n• CE\n• استاندارد ایران\n\n"
            "📞 **شماره تماس:** 031555555\n"
            "📧 **ایمیل:** info@almascarpet.com\n\n"
            "سی سال تجربه در خدمت شما"
        )
    
    elif text == "🎨 کلکسیون‌ها":
        await update.message.reply_text(
            "🎨 **کلکسیون‌های فرش الماس:**\n\n"
            "• **الماس** (کدهای A1 تا A10)\n"
            "• **بهار** (کدهای B1 تا B10)\n"
            "• **ترنم** (کدهای T1 تا T10)\n"
            "• **وینتیج** (کدهای V1 تا V10)\n\n"
            "📏 **سایزهای موجود:**\n"
            "• ۱۲ متری\n• ۹ متری\n• ۶ متری\n\n"
            "برای ثبت سفارش، گزینه '📦 ثبت سفارش' را انتخاب کنید"
        )
    
    elif text == "📦 ثبت سفارش":
        await update.message.reply_text(
            "📦 **سیستم ثبت سفارش**\n\n"
            "به زودی فعال خواهد شد...\n\n"
            "📞 **راه‌های ارتباطی موقت:**\n"
            "تلفن: 031555555 - داخلی ۴\n"
            "واتساپ: 091234567\n\n"
            "🕐 **ساعات پاسخگویی:**\n"
            "شنبه تا چهارشنبه: ۸:۰۰ تا ۱۶:۰۰"
        )
    
    elif text == "📞 تماس با ما":
        await update.message.reply_text(
            "📞 **راه‌های ارتباطی:**\n\n"
            "**تلفن:** 031555555\n"
            "• مدیریت: داخلی ۱\n"
            "• حسابداری: داخلی ۲\n"
            "• مدیر تولید: داخلی ۳\n"
            "• سفارشات: داخلی ۴\n"
            "• مشاوره: داخلی ۵\n\n"
            "📧 **ایمیل:** info@almascarpet.com\n"
            "📍 **آدرس:** اصفهان، شهرک صنعتی محمودآباد"
        )
    
    elif text == "🌐 سایت و اینستاگرام":
        await update.message.reply_text(
            "🌐 **شبکه‌های اجتماعی و وبسایت:**\n\n"
            "🔗 **وبسایت:** www.almascarpet.com\n"
            "📷 **اینستاگرام:** @almascarpet\n"
            "📱 **واتساپ:** 091234567\n\n"
            "برای مشاهده جدیدترین محصولات و طرح‌ها ما را دنبال کنید!"
        )

def main():
    """تابع اصلی اجرای ربات"""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ لطفاً توکن ربات را در فایل تنظیمات قرار دهید")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ثبت هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🤖 ربات فرش الماس راه‌اندازی شد...")
    print("📁 کدها در GitHub ذخیره شدند")
    print("🔧 آماده اتصال به سرور و Google Sheets")
    
    # در این مرحله فقط کدها ذخیره می‌شوند
    # اجرا در مرحله بعد با سرور انجام می‌شود

if __name__ == '__main__':
    main()
