from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = "8260320049:AAFs6q_Gqb6bvKgCB2chTpQDGccXVi7hEWw"

bot = TeleBot(TOKEN)

CRYPTO_NAME_TO_TICKER = {
    "Bitcoin": "BTCUSDT",
    "Ethereum": "ETHUSDT",
    "Doge": "DOGEUSDT"
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=3)
    for cripto_name in CRYPTO_NAME_TO_TICKER.keys():
        item_button = KeyboardButton(cripto_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, "choose a crypto", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME_TO_TICKER.keys())
def send_price(message):
    cripto_name = message.text
    ticker = CRYPTO_NAME_TO_TICKER[cripto_name]
    price = get_price_by_ticker(ticker=ticker)
    bot.send_message(message.chat.id, f"price of {cripto_name} is {price}")


def get_price_by_ticker(*, ticker: str) -> float:
    endpoint = "https://api.binance.com/api/v3/ticker/price"

    response = requests.get(endpoint, params={"symbol": ticker})
    bitcoin_price = float(response.json()["price"])
    return bitcoin_price


bot.infinity_polling()
