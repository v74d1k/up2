import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

TOKEN = "7686244392:AAGge7CFIYo_hoVZ4xAmQT0wx8zpGFYu20c"
OWM_API_KEY = "b86ad5169d6cfe6f60b6578deaf006f5"

landmarks = {
    "chekhov": {
        "name": "Памятник Чехову",
        "description": "Памятник Антону Павловичу Чехову на набережной Томи.",
        "address": "Набережная реки Томи",
        "photo": "https://example.com/chekhov.jpg"
    },
    "wooden": {
        "name": "Деревянное зодчество",
        "description": "Уникальные деревянные дома в центре Томска.",
        "address": "Улицы Белинского и Красноармейская"
    }
}

routes = {
    "historic": {
        "name": "Исторический маршрут",
        "description": "Прогулка по старинным улицам Томска с посещением главных памятников.",
        "stops": ["Памятник Чехову", "Деревянное зодчество", "Томский университет"]
    },
    "nature": {
        "name": "Природный маршрут",
        "description": "Маршрут по паркам и набережным Томска для любителей природы.",
        "stops": ["Парк 400-летия Томска", "Набережная реки Томи"]
    }
}

cafes = {
    "coffee_house": {
        "name": "Coffee House",
        "description": "Уютное кафе с отличным кофе и десертами.",
        "address": "ул. Белинского, 15"
    },
    "vegan_place": {
        "name": "Vegan Place",
        "description": "Веганское кафе с разнообразным меню.",
        "address": "пр. Ленина, 30"
    }
}

info = {
    "transport": "В Томске ходят автобусы, троллейбусы и маршрутки. Билеты можно купить в кассах и у водителя.",
    "emergency": "Телефон экстренных служб: 112",
    "tourist_center": "Туристический центр Томска находится на пл. Ленина, 5."
}

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌤️ Погода", callback_data='weather')],
        [InlineKeyboardButton("📍 Достопримечательности", callback_data='landmarks')],
        [InlineKeyboardButton("🗺️ Маршруты", callback_data='routes')],
        [InlineKeyboardButton("☕ Кафе и рестораны", callback_data='cafes')],
        [InlineKeyboardButton("ℹ️ Полезная информация", callback_data='info')]
    ])

def landmarks_menu_keyboard():
    buttons = [[InlineKeyboardButton(info["name"], callback_data=f"landmark_{key}")] for key, info in landmarks.items()]
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')])
    return InlineKeyboardMarkup(buttons)

def routes_menu_keyboard():
    buttons = [[InlineKeyboardButton(info["name"], callback_data=f"route_{key}")] for key, info in routes.items()]
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')])
    return InlineKeyboardMarkup(buttons)

def cafes_menu_keyboard():
    buttons = [[InlineKeyboardButton(info["name"], callback_data=f"cafe_{key}")] for key, info in cafes.items()]
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')])
    return InlineKeyboardMarkup(buttons)

def info_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("Транспорт", callback_data='info_transport')],
        [InlineKeyboardButton("Экстренные службы", callback_data='info_emergency')],
        [InlineKeyboardButton("Туристический центр", callback_data='info_tourist_center')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в Томский Гид! Выберите пункт меню:", reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'main_menu':
        await query.edit_message_text("Главное меню. Выберите пункт:", reply_markup=main_menu_keyboard())
    elif data == 'weather':
        weather_text = get_weather_text()
        await query.edit_message_text(weather_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')]]))
    elif data == 'landmarks':
        await query.edit_message_text("Выберите достопримечательность:", reply_markup=landmarks_menu_keyboard())
    elif data.startswith('landmark_'):
        key = data.split('_')[1]
        info_item = landmarks.get(key)
        if info_item:
            text = f"{info_item['name']}\n\n{info_item['description']}\nАдрес: {info_item['address']}"
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data='landmarks')]]))
        else:
            await query.edit_message_text("Информация не найдена.", reply_markup=landmarks_menu_keyboard())
    elif data == 'routes':
        await query.edit_message_text("Выберите маршрут:", reply_markup=routes_menu_keyboard())
    elif data.startswith('route_'):
        key = data.split('_')[1]
        info_item = routes.get(key)
        if info_item:
            stops = "\n".join(info_item["stops"])
            text = f"{info_item['name']}\n\n{info_item['description']}\n\nОсновные остановки:\n{stops}"
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data='routes')]]))
        else:
            await query.edit_message_text("Информация не найдена.", reply_markup=routes_menu_keyboard())
    elif data == 'cafes':
        await query.edit_message_text("Выберите кафе или ресторан:", reply_markup=cafes_menu_keyboard())
    elif data.startswith('cafe_'):
        key = data.split('_')[1]
        info_item = cafes.get(key)
        if info_item:
            text = f"{info_item['name']}\n\n{info_item['description']}\nАдрес: {info_item['address']}"
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data='cafes')]]))
        else:
            await query.edit_message_text("Информация не найдена.", reply_markup=cafes_menu_keyboard())
    elif data == 'info':
        await query.edit_message_text("Полезная информация:", reply_markup=info_menu_keyboard())
    elif data == 'info_transport':
        await query.edit_message_text(info["transport"], reply_markup=info_menu_keyboard())
    elif data == 'info_emergency':
        await query.edit_message_text(info["emergency"], reply_markup=info_menu_keyboard())
    elif data == 'info_tourist_center':
        await query.edit_message_text(info["tourist_center"], reply_markup=info_menu_keyboard())

def get_weather_text():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Tomsk&appid={OWM_API_KEY}&units=metric&lang=ru"
        response = requests.get(url).json()
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        wind = response["wind"]["speed"]
        humidity = response["main"]["humidity"]
        return f"Погода в Томске:\nТемпература: {temp}°C\nСостояние: {desc}\nВетер: {wind} м/с\nВлажность: {humidity}%"
    except Exception:
        return "Не удалось получить данные о погоде."

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == '__main__':
    main()
