import requests
import json
from datetime import date
from datetime import timedelta
from twilio.rest import Client

# from twilio.rest import Client

STOCK_NAME = "AMZN"
COMPANY_NAME = "Amazon"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

twilio_SID = "TWILIO SID"
twilio_AUTH = "TWILIO AUTH"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

stock_params = {
  'function': "TIME_SERIES_DAILY_ADJUSTED",
  'symbol': STOCK_NAME,
  'outputsize': "compact",
  'apikey': "STOCK API KEY",
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
# response = requests.get('https://www.alphavantage.co/query?')
response.raise_for_status()
stonks = response.json()
data_list = [value for (key,value) in stonks.items()]
friday_close = float(data_list[1]['2023-02-24']['4. close'])
thursday_close = float(data_list[1]['2023-02-23']['4. close'])

diff = abs(friday_close - thursday_close)
diff_percent = (diff / float(friday_close)) *100
# print(diff_percent)

if diff_percent > 2:
  news_params = {
    "apiKey": "NEWS API KEY",
    "qInTitle": "amazon"
  }
  news_response = requests.get(NEWS_ENDPOINT, news_params)
  articles = news_response.json()["articles"]
  three_articles = articles[:3]
  # print(three_articles)

  # headline: {article title}. \nBrief: {article description}
  # [new_item for item in list]
  # each item in new list will be a string with article title and description
  formatted_articles = [f"headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
  # print(formatted_articles)
  
  client = Client(twilio_SID, twilio_AUTH)

  for article in formatted_articles:
    message = client.messages \
    .create(
      body=article,
      from_="+18445791012",
      to="+18505444561"
    )
  
