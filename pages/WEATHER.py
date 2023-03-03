import streamlit as st
import requests
from pprint import pprint
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

#レイアウト等
st.set_page_config(
    page_title="まるちゃんニュース",
    page_icon=":newspaper:",
    layout="wide",
    initial_sidebar_state="expanded",)

#タイトル
st.title("ウェザーニュース")

#画像
st.image("./data/cat-1285634__340.webp", width=500)

# 検索フォームを作成
city_name = st.text_input("都市名を入力してください", "Tokyo")

# APIキーとAPIのURLを指定
api_key = "a593582c3b416764e80a8bd6c55733f9"
current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&lang=ja&units=metric"
forecast_url = forecast_url.format(city=city_name, key="a593582c3b416764e80a8bd6c55733f9")



# 現在の天気を取得する関数
def get_current_weather(city_name):
    params = {
        "q": city_name,
        "appid": api_key,
        "lang": "ja",
        "units": "metric"
    }
    response = requests.get(current_weather_url, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None

# 5日先までの天気予報を取得する関数
def get_forecast(city_name):
    params = {
        "q": city_name,
        "appid": api_key,
        "lang": "ja",
        "units": "metric"
    }
    response = requests.get(forecast_url, params=params)
    if response.status_code == 200:
        forecast_data = response.json()
        return forecast_data
    else:
        return None

# 現在の天気を取得
current_weather_data = get_current_weather(city_name)
if current_weather_data is None:
    st.warning("現在の天気を取得できませんでした。都市名を確認してください。")
else:
    # 現在の天気を表示
    st.write("## 現在の天気")
    st.write(f"{city_name}の現在の天気は{current_weather_data['weather'][0]['description']}です。")
    st.write(f"気温 : {current_weather_data['main']['temp']}℃")
    st.write(f"湿度 : {current_weather_data['main']['humidity']}％")
    st.write(f"風速 : {current_weather_data['wind']['speed']}m/s")

 # 5日先までの天気予報を取得
forecast_data = get_forecast(city_name)
forecast_data = requests.get(forecast_url).json()
if forecast_data is None:
    st.warning("天気予報を取得できませんでした。都市名を確認してください。")
else:
    # 3時間ごとの天気を表示
    df = pd.DataFrame(columns=["気温"])
    st.write("## 気温の予想推移")
    tz = timezone(timedelta(hours=+9), 'JST')
    fig, ax = plt.subplots(figsize=(15,8))
    for dat in forecast_data["list"]:
        jst = str(datetime.fromtimestamp(dat["dt"], tz))[:-9]
        temp = dat["main"]["temp"]
        df.loc[jst] = temp
    ax.plot(df)
    ax.set_xlabel("日付(JST)")
    ax.set_ylabel("気温(℃)")
    ax.set_xlim(0,8)
    st.pyplot(fig)



