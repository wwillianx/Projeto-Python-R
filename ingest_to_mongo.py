import pandas as pd
import os
from pymongo import MongoClient

def load_and_clean_data(csv_path='dados/vgsales.csv'):
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['Year', 'Global_Sales'])
    df['Year'] = df['Year'].astype(int)
    return df

def insert_into_mongo(df, db_name='vgsales_db', collection_name='games'):
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("❌ Variável de ambiente 'MONGO_URI' não definida.")
    
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    collection.delete_many({})  # limpa coleção (opcional)
    collection.insert_many(df.to_dict(orient="records"))
    print(f"✅ Inseridos {len(df)} registros em '{db_name}.{collection_name}'")

if __name__ == "__main__":
    df = load_and_clean_data()
    insert_into_mongo(df)
