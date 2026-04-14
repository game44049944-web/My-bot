import requests
import time
import json

TOKEN = "8747474289:AAEbOhodMYSHWgQ4TgODbloWkSNDYEhlttc"
ADMIN_ID = 123456789

URL = f"https://api.telegram.org/bot{TOKEN}/"
last_update = 0

DATA_FILE = "data.json"

# 💾 база заказов
def load():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"orders": []}

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load()

print("🚀 BOT STARTED")

# 📩 меню
def send_menu(chat_id):
    keyboard = {
        "keyboard": [
            ["🔥 Free Fire", "⚔️ Mobile Legends"],
            ["🎮 PUBG Mobile"],
            ["💳 Как оплатить", "📸 Я оплатил"],
            ["🧾 Чеки", "📊 Статистика"]
        ],
        "resize_keyboard": True
    }

    # главное меню
    requests.post(URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": "👋 Добро пожаловать в донат-магазин!",
        "reply_markup": keyboard
    })

    # чек канал
    inline = {
        "inline_keyboard": [
            [
                {
                    "text": "🧾 Открыть чеки",
                    "url": "https://t.me/chekcanal_bot"
                }
            ]
        ]
    }

    requests.post(URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": "🧾 Доказательства оплат:",
        "reply_markup": inline
    })

# 💰 цены
def prices(text):
    text = text.lower()

    if "mobile legends" in text:
        return """⚔️ Mobile Legends 💎

8 💎 — 1.3 сомони
35 💎 — 5.3 сомони
88 💎 — 13.2 сомони
122 💎 — 19.8 сомони
264 💎 — 39.6 сомони
440 💎 — 66.0 сомони
734 💎 — 105.6 сомони
933 💎 — 132.0 сомони
1410 💎 — 198.0 сомони
1881 💎 — 264.0 сомони
2845 💎 — 396.0 сомони
6163 💎 — 858.0 сомони

👉 выбери пакет"""

    if "free fire" in text:
        return """🔥 Free Fire 💎

100 + 5 = 11 сомони
310 + 16 = 32 сомони
520 + 26 = 53 сомони
1060 + 53 = 105 сомони
2180 + 218 = 213 сомони

🛠 услуги:
😃 неделя — 18
😃 месяц — 118
🎯 пропуск — 30

👉 выбирай"""

    if "pubg" in text:
        return """🎮 PUBG Mobile UC

60 UC — 12 сомони
300+25 — 55
1500+300 — 245
3000+850 — 500
6000+2100 — 985
12000+4200 — 1950
18000+6300 — 2910

👉 выбирай"""

    return None

# 🤖 продажи
def sales(text):
    text = text.lower()

    if "free fire" in text:
        return "🔥 Free Fire 💎\n💰 топ выбор\n⚡ быстро"

    if "mobile legends" in text:
        return "⚔️ Mobile Legends 💎\n💰 лучший вариант"

    if "pubg" in text:
        return "🎮 PUBG UC\n💰 от 12 сомони"

    return None

# 🧾 чек
def send_receipt(order):
    msg = f"""
🧾 НОВАЯ ЗАЯВКА

👤 ID: {order['user_id']}
🆔 #{order['id']}
💬 {order['text']}

⚠️ статус: {order['status']}
"""

    requests.post(URL + "sendMessage", json={
        "chat_id": "@your_receipt_channel",
        "text": msg
    })

# 🔁 цикл
while True:
    try:
        r = requests.get(URL + f"getUpdates?offset={last_update}")
        updates = r.json()

        for u in updates.get("result", []):
            last_update = u["update_id"] + 1

            msg = u.get("message")
            if not msg:
                continue

            chat_id = msg["chat"]["id"]
            user_id = msg["from"]["id"]
            text = msg.get("text", "")

            print("➡️", text)

            # 🚀 старт
            if text == "/start":
                send_menu(chat_id)

            # 💰 цены
            reply = prices(text)
            if reply:
                requests.post(URL + "sendMessage", json={
                    "chat_id": chat_id,
                    "text": reply
                })
                continue

            # 🤖 продажи
            reply = sales(text)
            if reply:
                requests.post(URL + "sendMessage", json={
                    "chat_id": chat_id,
                    "text": reply
                })
                continue

            # 💳 оплата
            if text == "💳 как оплатить":
                requests.post(URL + "sendMessage", json={
                    "chat_id": chat_id,
                    "text": "💳 Оплата вручную\nПосле оплаты нажми 📸 Я оплатил"
                })

            # 📸 заявка
            elif text == "📸 я оплатил":

                order = {
                    "id": len(data["orders"]) + 1,
                    "user_id": user_id,
                    "text": "ожидает проверки",
                    "status": "pending"
                }

                data["orders"].append(order)
                save()

                send_receipt(order)

                requests.post(URL + "sendMessage", json={
                    "chat_id": chat_id,
                    "text": f"📩 заявка #{order['id']} принята"
                })

            # 📊 статистика
            elif text == "📊 статистика":
                requests.post(URL + "sendMessage", json={
                    "chat_id": chat_id,
                    "text": f"📊 заявок: {len(data['orders'])}"
                })

            else:
                requests.post(URL + "sendMessage", json={
                    "chat_id": chat_id,
                    "text": "👉 используй /start"
                })

        time.sleep(1)

    except Exception as e:
        print("Ошибка:", e)
        time.sleep(2)