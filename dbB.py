import pandas as pd
import io
import zipfile
from sqlalchemy import create_engine
import mysql.connector


str_db_typ = 'mysql+mysqlconnector://'
str_db_user = 'root'
str_db_password = ''                         # Wenn vorhanden, dann ':passwort'
str_db_adr = '@localhost'                    # Wenn der DB-Server nicht auf dem Standard-Port läuft: '@IP:Port' Bspw.: @127.0.0.1:8080
str_db_schema = '/thematool'
str_connection = str_db_typ + str_db_user + str_db_password + str_db_adr + str_db_schema

engine = create_engine(str_connection)








genres = pd.Series(['Action',
 'Adventure',
 'Animation',
 'Comedy',
 'Crime',
 'Documentary',
 'Drama',
 'Family',
 'Fantasy',
 'Foreign',
 'History',
 'Horror',
 'Music',
 'Mystery',
 'Romance',
 'Science Fiction',
 'TV Movie',
 'Thriller',
 'War',
 'Western'])

genres_display = {'Action': 'Juicy Action', 'Adventure': "Exciting Adventure", 'Animation': "Playful Animation", 'Comedy': "Funny Comedy", 'Crime': "Dreadful Crime", 'Documentary': 'Interesting Documentary', 'Drama':"Tearful Drama", 'Family':"Harmonious Family", 'Fantasy':"Fantastic Fantasy", 'Foreign':"Strange and Foreign", 'History':"Informed History",
'Horror':"Bloody Horror", 'Music':"Musical Music", 'Mystery': "Mysterious Mystery", 'Romance': "Romantic Romance", 'Science Fiction':"Insightful Science Fiction",
'Thriller':"Thrilling Thriller", 'TV Movie':"Boring TV Movie", 'War': "Brutal War", 'Western':"Unlawful Western"}





