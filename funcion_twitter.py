import snscrape.modules.twitter as sntwitter
import pandas as pd
import sqlite3
import warnings
import re
import emoji
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns



def fetch_tweets(account, start_date, end_date):
    # Construir la consulta de búsqueda
    query = f"{account} since:{start_date} until:{end_date}"

    # Obtener los tweets utilizando snscrape
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        tweet_id = tweet.id
        text = tweet.rawContent
        date = tweet.date.strftime('%Y-%m-%d %H:%M:%S')
        author_id = tweet.user.id
        author_name = tweet.user.displayname
        author_username = tweet.user.username
        retweets = tweet.retweetCount
        replies = tweet.replyCount
        likes = tweet.likeCount
        quotes = tweet.quoteCount

        tweets.append([tweet_id, text, date, author_id, author_name, author_username, retweets, replies, likes, quotes])

        # Romper el bucle si se alcanza el límite de tweets deseados
        if len(tweets) >= 20000:
            break

    # Crear un DataFrame a partir de la lista de tweets
    columns = ["ID", "Text", "Date", "Author ID", "Author Name", "Author Username", "Retweets", "Replies", "Likes", "Quotes"]
    tweets_df = pd.DataFrame(tweets, columns=columns)

    return tweets_df

def export_tweets_to_csv(dataframe, output_location):
    # Exportar el DataFrame a un archivo CSV en la ubicación deseada
    dataframe.to_csv(output_location, index=False)

def data_report(dataframe):
    # Sacamos la cantidad de registros
    total_records = len(dataframe)

    # Sacamos la cantidad de columnas
    total_columns = len(dataframe.columns)

    # Sacamos la lista de columnas
    columns = pd.DataFrame(dataframe.columns.tolist(), columns=["Column Name"])

    # Sacamos la lista de tipos de datos
    types = pd.DataFrame(dataframe.dtypes.tolist(), columns=["Data Type"])

    # Sacamos la cantidad de valores faltantes por columna
    missing_values = pd.DataFrame(dataframe.isnull().sum().tolist(), columns=["Missing Values"])

    # Sacamos el porcentaje de valores faltantes por columna
    percent_missing = pd.DataFrame((dataframe.isnull().sum() / total_records * 100).tolist(), columns=["Percent Missing"])

    # Sacamos la cantidad de valores únicos por columna
    unique_values = pd.DataFrame(dataframe.nunique().tolist(), columns=["Unique Values"])

    # Sacamos el porcentaje de valores únicos por columna
    percent_unique = pd.DataFrame((dataframe.nunique() / total_records * 100).tolist(), columns=["Percent Unique"])

    # Concatenamos todos los resultados en un DataFrame final
    concatenated = pd.concat([columns, types, missing_values, percent_missing, unique_values, percent_unique], axis=1)

    return concatenated

# Obtener inputs del usuario
account = input("Ingrese la cuenta de Twitter a explorar (por ejemplo, @TheBridge_Tech): ")
start_date = input("Ingrese la fecha de inicio en formato YYYY-MM-DD: ")
end_date = input("Ingrese la fecha de fin en formato YYYY-MM-DD: ")
output_location = input("Ingrese la ubicación para exportar el archivo CSV (por ejemplo, tweets.csv): ")

# Obtener los tweets
tweets_df = fetch_tweets(account, start_date, end_date)

# Imprimir el DataFrame
print(tweets_df)

# Exportar los tweets a un archivo CSV
export_tweets_to_csv(tweets_df, output_location)

# Generar el informe
report = data_report(tweets_df)

# Imprimir el informe
print(report)
return (len(tweets_df))