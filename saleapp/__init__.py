from flask import Flask
from gradio_client import Client
import pandas as pd
import os

app = Flask(__name__)

client = Client("ShynBui/ShynBui-comment_classification")

restaurant_data = pd.read_csv(os.path.join(os.getcwd(), 'data/1_Restaurants.csv'))
review_data = pd.read_csv(os.path.join(os.getcwd(), 'data/2_Reviews.csv'))
data_merge = restaurant_data.copy().merge(review_data.copy(), how='right', left_on='ID', right_on='IDRestaurant')
data_merge.loc[:, 'Time_y'] = pd.to_datetime(data_merge['Time_y'])

app.config['PAGE_SIZE'] = 12
app.config['COMMENT_SIZE'] = 8
app.config['PAGE_INF'] = 9999

