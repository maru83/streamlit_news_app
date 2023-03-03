import streamlit as st
import requests
import json

#レイアウト等
st.set_page_config(
    page_title="まるちゃんニュース",
    page_icon=":newspaper:",
    layout="wide",
    initial_sidebar_state="expanded",)

#ニュースの取得
def get_news(topic):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={topic}&apiKey=187762fa24f74c069631396c5110341a"
    response = requests.get(url)
    data = json.loads(response.text)
    return data['articles']

#タイトル
st.title("海外のニュース")

#画像
st.image("./data/cat-1285634__340.webp", width=500)

#トピック
topic = st.selectbox("トピックを選択してください", ("general", "business", "entertainment",  "health", "science", "sports", "technology"))

#記事
articles = get_news(topic)
for article in articles:
    st.write("## " + article['title'])
    st.write(article['description'])
    st.write(article['url'])
    st.write("\n")
