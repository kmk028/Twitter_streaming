import sqlite3
import pandas as pd
import pathlib
from sqlite3 import Error
from sqlalchemy import create_engine

engine = create_engine("sqlite:///test.db")


def get_tweet_data():
    try:
        sql_df = pd.read_sql_table("tweet", con=engine)
        return sql_df
    except Error as e:
        print(e)
