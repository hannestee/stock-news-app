import requests
import smtplib
from email.message import EmailMessage

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"
api_key_stock = ""
api_key_news = ""
my_email = ""
password = ""

stock_api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key_stock
}

news_api_parameters = {
    "qinTitle": "tesla OR tsla OR Elon",
    "sources": 'the-washington-post',
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": api_key_news
}


def get_close_prices():
    response = requests.get(url=STOCK_ENDPOINT, params=stock_api_parameters)
    response.raise_for_status()
    data = response.json()
    daily_data = data["Time Series (Daily)"]

    close_prices = []
    for day in daily_data:
        close_prices.append(daily_data[day]["4. close"])
    close_price_yesterday = close_prices[0]
    close_price_dby = close_prices[1]
    calculate_stock(float(close_price_yesterday), float(close_price_dby))


def calculate_stock(price_yesterday, price_dby):
    symbol_up = u"\U0001F53A"
    symbol_down = u"\U0001F53B"
    price_difference = abs((price_yesterday - price_dby) / price_dby * 100)

    if price_difference >= 10:
        if price_yesterday > price_dby:
            get_news(symbol_up, int(price_difference))
        else:
            get_news(symbol_down, int(price_difference))
    else:
        print("No significant price change")


def get_news(symbol, price_difference):
    response = requests.get(url=NEWS_ENDPOINT, params=news_api_parameters)
    response.raise_for_status()
    data = response.json()

    article_ready = []
    for article in data["articles"]:
        article_ready.append({'title': article["title"], 'content': article["content"]})

    send_news(article_ready, symbol, price_difference)


def send_news(articles, symbol, price_difference):
    price_difference = str(price_difference)
    title = articles[0]['title']
    content = articles[0]['content']
    to_ = ""

    em = EmailMessage()
    em.set_content("{}".format(content))
    em['To'] = to_
    em['From'] = my_email
    em['Subject'] = title + symbol + price_difference + "%"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.send_message(em)


get_close_prices()
