import io
import zipfile
import time

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

import dbB
import content
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from PIL import Image
import core
from ast import literal_eval

import base64



#Feature dict Standard
feature_filter = {"top5000": True}


## Phrases
welcome = "<h1 style='text-align: center; color: red'>Thematool</h1><h2 style='color: red; text-align:center;margin-bottom:50px'>Take the red pill, fool!</h2>"
offer_string = "<p style='margin-top: 200px; text-align: center;color: red'>I'm gonna make you an offer you can't refuse.</p>"
not_selected = '<p style="color:red; text-align:center; font-size:30px; font-style:bold"> You have to select at least one movie, fool!</p>'
not_enough = '<p style="color:red; font-size=40px";font-style:bold"> Not enough movies match your filter settings, fool.</p>'



#### Cached Database Access
@st.cache(allow_output_mutation=True)
def get_connection():
    return create_engine('mysql+mysqlconnector://root@localhost/thematool')

@st.cache
def load_data():
    with st.spinner('Loading Data...'):
        time.sleep(0.5)
        cluster_scores = pd.read_sql("SELECT * FROM cluster_scores", get_connection()).drop(columns="title")
        top5000 = pd.read_sql("SELECT * FROM masterdata_long_weightedfilms ORDER BY weightedfilms DESC LIMIT 5000", get_connection())
        low5000 = pd.read_sql("SELECT * FROM masterdata_long_weightedfilms ORDER BY weightedfilms ASC LIMIT 5000", get_connection())                             

    return (cluster_scores,top5000,low5000)


cluster_scores,top5000,low5000 = load_data()


#### Merge Data cluster scores to top5000
top5000_meta = top5000.merge(cluster_scores,how="left",on="id")
low5000_meta = low5000.merge(cluster_scores,how="left",on="id")

## Make director genre entries to lists
top5000_meta['director'] = top5000_meta['director'].fillna('[]').apply(literal_eval).apply(lambda x: [i for i in x] if isinstance(x, list) else [])
top5000_meta['genres'] = top5000_meta['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
low5000_meta['director'] = low5000_meta['director'].fillna('[]').apply(literal_eval).apply(lambda x: [i for i in x] if isinstance(x, list) else [])
low5000_meta['genres'] = low5000_meta['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])


#Get Id list and id-title dictionary
movie_ids = list(top5000["id"])
id_dict = top5000.set_index("id")["title"].to_dict()


## Define Pictures
main_bg = "movie_pic3.jpg"
main_bg_ext = "movie_pic3.jpg"

side_bg = "Katze.png"
side_bg_ext = "Katze.png"

file4_ = open("Katze_gespiegeltEND.png", "rb")
contents = file4_.read()
data_url4 = base64.b64encode(contents).decode("utf-8")
file4_.close()



## Markdown for Background Pictures
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    
    </style>
    """,
    unsafe_allow_html=True

)



## Markdown for Main Content not active
st.markdown(welcome, unsafe_allow_html=True)


## Markdown for sidebar
katze = '''<p style="padding-left:50px"> <img width = "100px"  src="data:image/gif;base64,%s" ></p>''' %(data_url4)
st.sidebar.markdown(katze,unsafe_allow_html=True)
st.sidebar.header('User Input Features')


## Sidebar Multiselects
selected_books = st.sidebar.multiselect(label='Enter your favorite movie titles in the box ', options= movie_ids, format_func= lambda x: id_dict[x])
select_genre = st.sidebar.multiselect( label = "Genre", options=dbB.genres,  format_func= lambda x: dbB.genres_display[x])
## Falls Genres ausgewaehlt feature filter anpassen
if (len(select_genre) > 0):
	feature_filter["genre"] = select_genre



## Sidebar Checkboxen
if(st.sidebar.checkbox("Regisseur")):
	feature_filter["director"] = top5000_meta[top5000_meta["id"].isin(selected_books)]["director"].sum()
# Nur Verzierung bisher
if (st.sidebar.checkbox(label = "I like trash", value =False)):
	feature_filter["top5000"] = False

print(feature_filter)


## Markdown for active content
contentgen = st.markdown(offer_string,unsafe_allow_html = True) #st.markdown(html_str, )


# Falls Button gedrueckt
if st.sidebar.button("My precious"):
	if not len(selected_books) == 0:
		df = core.prime_flow(feature_filter, selected_books, cluster_scores,top5000_meta,low5000_meta)
		contentgen.markdown(content.make_content_string(df),unsafe_allow_html= True)
	else:
		contentgen.markdown(not_selected,unsafe_allow_html= True)


