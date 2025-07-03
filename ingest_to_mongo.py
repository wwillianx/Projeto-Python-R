# Importações necessárias
import pandas as pd  # Para manipulação de dados tabulares
import os  # Para interações com o sistema de arquivos
from pymongo import MongoClient  # Para se conectar ao MongoDB
from pymongo.errors import ConnectionFailure  # Para tratar falhas de conexão
from bson.binary import Binary  # Para armazenar arquivos binários (imagens) no MongoDB
from dotenv import load_dotenv  # Para carregar variáveis de ambiente do arquivo .env

# Carrega as variáveis do arquivo .env (deve estar na raiz do projeto)
load_dotenv()

def conectar_ao_mongo(db_name="vgsales_db"):
    """
    Estabelece uma conexão com o MongoDB.
    Prioriza a URI da variável de ambiente MONGO_URI (do .env).
    Caso não esteja disponível ou falhe, solicita a URI manualmente.
    """

    mongo_uri = os.getenv("MONGO_URI")  # Pega a URI do .env (caso exista)

    # Função auxiliar para testar a conexão com uma URI
    def testar_conexao(uri):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)  # Timeout curto
            client.admin.command("ping")  # Testa se o servidor responde
            return client
        except ConnectionFailure as e:
            print(f"❌ Falha na conexão com MongoDB: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado ao testar conexão: {e}")
            return None

    # Se a URI estiver no .env, tenta conectar com ela
    if mongo_uri:
        client = testar_conexao(mongo_uri)
        if client:
            print("🟢 Conectado ao MongoDB com sucesso via variável de ambiente!")
            return client[db_name]
        else:
            print("⚠️ URI do .env inválida ou conexão falhou.")

    # Caso a URI não esteja no .env ou falhou, solicita manualmente
    print("\n🔌 Variável MONGO_URI não encontrada. Conexão com MongoDB não detectada.")

    while True:
        nova_uri = input("Digite sua URI do MongoDB Atlas (ex: mongodb+srv://user:pass@cluster.../): ").strip()
        client = testar_conexao(nova_uri)
        if client:
            print("✅ Conexão bem-sucedida com a URI informada!")
            print("ℹ️ Lembre-se de atualizar seu arquivo .env com esta URI para uso futuro.")
            return client[db_name]
        else:
            print("❌ Conexão falhou. Verifique sua URI e tente novamente.")

def load_and_clean_data(csv_path='dados/vgsales.csv'):
    """
    Carrega os dados do CSV, remove linhas incompletas e converte ano para inteiro.
    """
    try:
        df = pd.read_csv(csv_path)
        df = df.dropna(subset=['Year', 'Global_Sales'])  # Remove registros sem ano ou vendas
        df['Year'] = df['Year'].astype(int)  # Converte ano para inteiro
        print(f"✅ Dados carregados e limpos de '{csv_path}'. {len(df)} registros.")
        return df
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo CSV não encontrado em '{csv_path}'.")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Erro ao carregar ou limpar dados: {e}")
        return pd.DataFrame()

def insert_into_mongo(df, db):
    """
    Insere os dados do DataFrame na coleção 'games' do banco de dados MongoDB.
    """
    if db is None:
        print("❌ Conexão com o MongoDB não estabelecida. Não é possível inserir dados de jogos.")
        return

    collection = db['games']  # Nome da coleção
    try:
        collection.delete_many({})  # Limpa a coleção antes de inserir (opcional)
        collection.insert_many(df.to_dict(orient="records"))  # Converte e insere os dados
        print(f"✅ Inseridos {len(df)} registros na coleção '{db.name}.games'")
    except Exception as e:
        print(f"❌ Erro ao inserir dados de jogos no MongoDB: {e}")

def insert_graphics_into_mongo(folder='.', db=None, collection_name='graphics'):
    """
    Insere arquivos PNG/PDF da pasta especificada no MongoDB como binários.
    """
    if db is None:
        print("❌ Conexão com o MongoDB não estabelecida. Não é possível inserir gráficos.")
        return

    collection = db[collection_name]
    try:
        collection.delete_many({})  # Limpa a coleção

        # Lista arquivos válidos
        graphics = [f for f in os.listdir(folder) if f.endswith(('.png', '.pdf'))]
        if not graphics:
            print(f"📂 Nenhuma imagem PNG/PDF encontrada na pasta '{folder}' para inserir.")
            return

        for file_name in graphics:
            path = os.path.join(folder, file_name)
            with open(path, 'rb') as f:
                binary_data = Binary(f.read())  # Lê o arquivo como binário

            doc = {
                "filename": file_name,
                "filetype": os.path.splitext(file_name)[1].replace('.', ''),  # Ex: 'pdf', 'png'
                "data": binary_data
            }
            collection.insert_one(doc)
            print(f"🖼️ Gráfico '{file_name}' inserido com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao inserir gráficos no MongoDB: {e}")

def retrieve_graphics_from_mongo(db, pasta_destino="graficos_recuperados", collection_name='graphics'):
    """
    Recupera gráficos binários do MongoDB e salva localmente.
    """
    if db is None:
        print("❌ Conexão com o MongoDB não estabelecida. Não é possível recuperar gráficos.")
        return

    collection = db[collection_name]
    os.makedirs(pasta_destino, exist_ok=True)  # Cria a pasta de destino, se não existir
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
                f.write(doc["data"])  # Salva o arquivo no disco
            print(f"  - {filename} salvo com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao recuperar gráficos do MongoDB: {e}")

# Bloco principal: executado ao rodar diretamente o script
if __name__ == "__main__":
    print("--- Executando script de ingestão (ingest_to_mongo.py) ---")

    db = conectar_ao_mongo()  # Conecta ao MongoDB, preferindo URI do .env

    if db is not None:
        df = load_and_clean_data()  # Carrega e limpa os dados do CSV

        if not df.empty:
            insert_into_mongo(df, db)  # Insere os dados na coleção 'games'

            # Descomente a linha abaixo se quiser testar a inserção de imagens também
            # insert_graphics_into_mongo(folder='.', db=db)

        # Testa a recuperação de gráficos para pasta local
        print("\n--- Testando recuperação de gráficos ---")
        retrieve_graphics_from_mongo(db)
    else:
        print("❌ Falha na conexão com MongoDB. As operações de ingestão e recuperação não foram realizadas.")