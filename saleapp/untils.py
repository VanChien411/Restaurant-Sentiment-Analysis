from saleapp import app
import json
import hashlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import gc
from pyvi import ViTokenizer, ViPosTagger
from saleapp import client, review_data, restaurant_data, data_merge
import seaborn as sns

def get_data_mau():
    print(os.path.join(os.getcwd(), 'saleapp/data/2_Reviews.csv'))
    data = review_data.copy()

    return data.sample(5)

def get_data_nha_hang_mau():
    print(os.path.join(os.getcwd(), 'saleapp/data/2_Reviews.csv'))
    data = restaurant_data.copy()

    return data.sample(5)

def so_luong_nha_hang_theo_quan():
    plt.close()

    if os.path.exists("plot.png"):
        # Xóa file "plot.png"
        os.remove(os.path.join(os.getcwd(), "static/image/plot.png"))

    data = restaurant_data.copy()

    plt.pie(data.District.value_counts().values, labels=data.District.value_counts().index,
            autopct='%1.1f%%')
    plt.title("Biểu đồ thể hiện số lượng nhà hàng theo quận")
    plt.savefig(os.path.join(os.getcwd(), "static/image/plot.png"))

    plt.close()

def predict_emotion(text):
    text = ViTokenizer.tokenize(text)

    result = client.predict(
        text,  # str  in 'Input' Textbox component
        api_name="/predict"
    )
    # print(text)
    #
    # print(result)

    return result

def load_all_res():
    data = restaurant_data.copy()

    return data

def search_by_name(name, page=1):
    data = restaurant_data.copy()

    data = data[data['Restaurant'].str.lower().str.contains(name.lower())]

    page_size = app.config['PAGE_SIZE']

    start = (page - 1) * page_size
    end = start + page_size


    return data.iloc[start:end], len(data['Restaurant'])

def load_product(name=None, page=1):
    data = restaurant_data.copy()

    page_size = app.config['PAGE_SIZE']

    start = (page - 1) * page_size
    end = start + page_size


    return data, len(data['Restaurant'])


def load_comments(id):
    data = review_data.copy()

    data = data[data['IDRestaurant'] == int(id)]

    return data

def load_res_by_id(id):

    data = restaurant_data.copy()

    data = data[data['ID'] == int(id)].iloc[0]

    return data

def get_merge_table(id):
    data = data_merge.copy()

    data = data[data['IDRestaurant'] == int(id)]

    return data

def restaurant_evaluation(id):
    data = data_merge.copy()

    data = data[data['IDRestaurant'] == int(id)]

    avg_rating = data['Rating'].mean()

    name = data['Restaurant'].iloc[0]
    danh_gia = ''

    if avg_rating >= 6.0:
        danh_gia = "Đánh giá cao"
    elif avg_rating >= 4.0:
        danh_gia = "Đánh giá trung bình"
    else:
        danh_gia = "Đánh giá thấp"

    return {"name": name,
            "avg": round(avg_rating, 2),
            "danhgia": danh_gia}

import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def vizualize_restaurant(id):
    # Generate some sample data for visualization
    data = data_merge.copy()

    data = data[data['IDRestaurant'] == int(id)]

    plt.switch_backend('agg')

    # Create a seaborn pairplot
    sns.lineplot(data=data, x='Time_y', y='Rating')  # Sử dụng sns.lineplot() thay vì ax.plot()
    plt.xlabel('Thời gian đánh giá')
    plt.ylabel('Điểm đánh giá')
    plt.title('Tỉ lệ đánh giá theo thời gian')

    # # Save the plot to a PNG file
    plt.savefig(os.path.join(os.getcwd(), "static/image/Time_plot.png"))

    plt.close()
    return os.path.join(os.getcwd(), "static/image/Time_plot.png")

def find_Adj_word(list_text):
    words = []
    for i in range(len(list_text)):
        try:
            list_text[i] = ViTokenizer.tokenize(list_text[i])
            list_text_array = list_text[i].split()
            # print(list_text_array)
            for j in range(len(list_text_array)):
                # print(ViPosTagger.postagging(list_text_array[j])[1])
                if ViPosTagger.postagging(list_text_array[j])[1][0] == 'A':
                    words.append(list_text_array[j])
        except:
            pass
    return words

import re

def remove_emoji(text):
  try:
      emoji_pattern = re.compile("["
          u"\U0001F1E0-\U0001F1FF"  # emojis
          u"\U00002700-\U000027BF"  # dingbats
          u"\U0001f600-\U0001f64F"  # emoticons
          u"\U0001f300-\U0001f5FF"  # symbols & pictographs
          u"\U0001f680-\U0001f6FF"  # transport & object symbols
          u"\U0001f1A0-\U0001f1FF"  # flags (iOS)
                              "]+", flags=re.UNICODE)
      return emoji_pattern.sub(r'', text)
  except:
      return ""


from wordcloud import WordCloud

def word_cloud_from_list(data):
    data = [word if isinstance(word, str) else '' for word in data]
    text = ' '.join(data)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    return plt


def get_word_cloud(id):
    data = data_merge.copy()

    data = data[data['IDRestaurant'] == int(id)]

    stop_words = []
    with open(os.path.join(os.getcwd(), "data/vietnamese-stopwords.txt"),'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()


    data = data['Comment'].tolist()

    data = find_Adj_word(data)

    data = [remove_emoji(i) for i in data]

    data = [word if isinstance(word, str) else '' for word in data]

    text = ' '.join(data)

    plt.switch_backend('agg')

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    plt.savefig(os.path.join(os.getcwd(), "static/image/Word_cloud_res.png"))

    plt.close()

    return 1

