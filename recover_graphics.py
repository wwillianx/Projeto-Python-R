from pymongo import MongoClient  # Importa o cliente MongoDB para conexão
import os  # Módulo para interagir com o sistema operacional

# Função para recuperar os gráficos armazenados no MongoDB e salvar no disco
def recuperar_graficos_do_mongo(pasta_destino="graficos_recuperados"):
    mongo_uri = os.getenv("MONGO_URI")  # Lê a variável de ambiente com a URI do MongoDB
    if not mongo_uri:
        print("❌ Variável de ambiente 'MONGO_URI' não definida.")
        return

    client = MongoClient(mongo_uri)  # Conecta ao MongoDB
    db = client["vgsales_db"]        # Seleciona o banco de dados
    collection = db["graphics"]      # Seleciona a coleção onde os gráficos estão armazenados

    os.makedirs(pasta_destino, exist_ok=True)  # Cria a pasta de destino se não existir

    graficos = list(collection.find())  # Recupera todos os documentos da coleção

    if not graficos:
        print("📂 Nenhum gráfico encontrado no banco de dados.")
        return

    print(f"\n⬇️ Recuperando {len(graficos)} gráficos do MongoDB para a pasta '{pasta_destino}':")
    for doc in graficos:
        filename = doc["filename"]                     # Nome do arquivo a ser salvo
        path = os.path.join(pasta_destino, filename)   # Caminho completo para o arquivo
        with open(path, "wb") as f:                    # Abre o arquivo em modo binário para escrita
            f.write(doc["data"])                       # Escreve o conteúdo binário no arquivo
        print(f"  - {filename} salvo com sucesso.")

# --- Chamada interativa no main.py ---
resposta = input("\n🔌 Deseja baixar os gráficos salvos no MongoDB? (s/n): ").strip().lower()
if resposta == 's':
    recuperar_graficos_do_mongo()  # Chama a função se o usuário confirmar
else:
    print("ℹ️ Ok, gráficos não foram baixados.")
