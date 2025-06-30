# ingest_to_mongo.py
import pandas as pd
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.binary import Binary
from dotenv import load_dotenv # Adicionado: Importa a função para carregar .env

# Adicionado: Carrega as variáveis de ambiente do arquivo .env
# Certifique-se de que o arquivo .env esteja na raiz do seu projeto
load_dotenv()

def conectar_ao_mongo(db_name="vgsales_db"):
    """
    Establishes and returns a connection to the MongoDB database.
    Prioritizes MONGO_URI environment variable (carregada do .env),
    falls back to interactive input if not found.
    """
    mongo_uri = os.getenv("MONGO_URI")

    def testar_conexao(uri):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            # O comando ismaster é leve e não requer autenticação para testar a conexão.
            client.admin.command("ping")
            return client
        except ConnectionFailure as e:
            print(f"❌ Falha na conexão com MongoDB: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado ao testar conexão: {e}")
            return None


    if mongo_uri:
        client = testar_conexao(mongo_uri)
        if client:
            print("🟢 Conectado ao MongoDB com sucesso via variável de ambiente!")
            return client[db_name]
        else:
            # Esta mensagem aparecerá se a URI do .env for inválida ou a conexão falhar
            print("⚠️ URI da variável de ambiente é inválida ou conexão falhou. Tente novamente.")
    else:
        # Esta parte será executada se MONGO_URI não for encontrada no ambiente (nem no .env)
        print("\n🔌 Variável MONGO_URI não encontrada. Conexão com MongoDB não detectada.")

    while True:
        nova_uri = input("Digite sua URI do MongoDB Atlas (ex: mongodb+srv://user:pass@cluster.../): ").strip()

        client = testar_conexao(nova_uri)
        if client:
            print("✅ Conexão bem-sucedida com a URI informada!")
            # Não perguntamos para salvar como variável de ambiente temporária,
            # pois a ideia é que ela já esteja no .env para persistir.
            # Se o usuário digitou, ele provavelmente corrigiu um erro no .env ou não o usou.
            # Para evitar sobrescrever o .env programaticamente, vamos apenas usar a URI.
            # Se você realmente quiser salvar programaticamente no .env, seria uma lógica mais complexa.
            print("ℹ️ Lembre-se de atualizar seu arquivo .env com esta URI para uso futuro.")
            return client[db_name]
        else:
            print("❌ Conexão falhou. Verifique sua URI e tente novamente.")

def load_and_clean_data(csv_path='dados/vgsales.csv'):
    """Loads, cleans, and returns the video game sales DataFrame."""
    try:
        df = pd.read_csv(csv_path)
        df = df.dropna(subset=['Year', 'Global_Sales'])
        df['Year'] = df['Year'].astype(int)
        print(f"✅ Dados carregados e limpos de '{csv_path}'. {len(df)} registros.")
        return df
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo CSV não encontrado em '{csv_path}'.")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Erro ao carregar ou limpar dados: {e}")
        return pd.DataFrame()


def insert_into_mongo(df, db):
    """Inserts DataFrame records into the 'games' collection."""
    if db is None:
        print("❌ Conexão com o MongoDB não estabelecida. Não é possível inserir dados de jogos.")
        return

    collection = db['games']
    try:
        collection.delete_many({})
        collection.insert_many(df.to_dict(orient="records"))
        print(f"✅ Inseridos {len(df)} registros na coleção '{db.name}.games'")
    except Exception as e:
        print(f"❌ Erro ao inserir dados de jogos no MongoDB: {e}")

def insert_graphics_into_mongo(folder='.', db=None, collection_name='graphics'):
    """Inserts PNG/PDF graphics from a folder into the specified MongoDB collection."""
    if db is None:
        print("❌ Conexão com o MongoDB não estabelecida. Não é possível inserir gráficos.")
        return

    collection = db[collection_name]
    try:
        collection.delete_many({})

        graphics = [f for f in os.listdir(folder) if f.endswith(('.png', '.pdf'))]
        if not graphics:
            print(f"📂 Nenhuma imagem PNG/PDF encontrada na pasta '{folder}' para inserir.")
            return

        for file_name in graphics:
            path = os.path.join(folder, file_name)
            with open(path, 'rb') as f:
                binary_data = Binary(f.read())

            doc = {
                "filename": file_name,
                "filetype": os.path.splitext(file_name)[1].replace('.', ''),
                "data": binary_data
            }
            collection.insert_one(doc)
            print(f"🖼️ Gráfico '{file_name}' inserido com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao inserir gráficos no MongoDB: {e}")

def retrieve_graphics_from_mongo(db, pasta_destino="graficos_recuperados", collection_name='graphics'):
    """Retrieves graphics from MongoDB and saves them locally."""
    if db is None:
        print("❌ Conexão com o MongoDB não estabelecida. Não é possível recuperar gráficos.")
        return

    collection = db[collection_name]

    os.makedirs(pasta_destino, exist_ok=True)
    graficos = list(collection.find())

    if not graficos:
        print("📂 Nenhum gráfico encontrado no banco de dados.")
        return

    print(f"\n⬇️ Recuperando {len(graficos)} gráficos do MongoDB para a pasta '{pasta_destino}':")
    try:
        for doc in graficos:
            filename = doc["filename"]
            path = os.path.join(pasta_destino, filename)
            with open(path, "wb") as f:
                f.write(doc["data"])
            print(f"  - {filename} salvo com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao recuperar gráficos do MongoDB: {e}")


if __name__ == "__main__":
    print("--- Executando script de ingestão (ingest_to_mongo.py) ---")
    db = conectar_ao_mongo() # Agora tentará pegar do .env primeiro
    if db is not None:
        df = load_and_clean_data()
        if not df.empty:
            insert_into_mongo(df, db)
            # insert_graphics_into_mongo(folder='.', db=db) # Descomente para testar inserção de gráficos aqui

        print("\n--- Testando recuperação de gráficos ---")
        retrieve_graphics_from_mongo(db)
    else:
        print("❌ Falha na conexão com MongoDB. As operações de ingestão e recuperação não foram realizadas.")