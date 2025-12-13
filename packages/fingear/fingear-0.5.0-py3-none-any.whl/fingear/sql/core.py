from ..settings import config
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

def get_connetion():
    db_path = os.environ.get('DATABASE_URL')
    if db_path is None:
        db_path = config()['sql_path']
    engine = create_engine(db_path)
    return engine

def get_session():
    Session = sessionmaker(bind=get_connetion())
    session = Session()
    return session

def to_sql(table_name, df, engine=get_connetion()):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

def has_table(table_name, engine=get_connetion()):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return table_name in metadata.tables

def execute(query, engine):
    with engine.connect() as conn:
        return conn.execute(text(query))