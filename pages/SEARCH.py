import streamlit as st
import requests

#レイアウト等
st.set_page_config(
    page_title="まるちゃんニュース",
    page_icon=":newspaper:",
    layout="wide",
    initial_sidebar_state="expanded",)

# ニュースの取得
def get_news(query):
    api_key = "187762fa24f74c069631396c5110341a"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["articles"]:
            return data["articles"]
    return []

# 画像の表示
def display_image(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.content
    except:
        pass
    return None

# タイトルと画像の表示
def display_news(news):
    st.write(f"## {news['title']}")
    image_url = news["urlToImage"]
    image = display_image(image_url)
    if image:
        st.image(image, caption=news["description"], width=500)
    else:
        st.image("./data/noimage.png", caption="No image available", width=500)
    st.write(news["description"])
    st.write(f"Source: [{news['source']['name']}]({news['url']})")
    st.write("\n")



# タイトル
st.title("ニュース検索")

#画像
st.image("./data/cat-1285634__340.webp", width=500)

# 検索フォーム
query = st.text_input("検索🔎")

# 検索結果の表示
if query:
    news_list = get_news(query)
    if news_list:
        for i, news in enumerate(news_list):
            #表示件数
            if i < 15: 
                display_news(news)
            else:
                break
    else:
        st.warning("記事が見つかりませんでした。")