from pymongo import MongoClient
import os

def recuperar_graficos_do_mongo(pasta_destino="graficos_recuperados"):
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("❌ Variável de ambiente 'MONGO_URI' não definida.")
        return

    client = MongoClient(mongo_uri)
    db = client["vgsales_db"]
    collection = db["graphics"]

    os.makedirs(pasta_destino, exist_ok=True)

    graficos = list(collection.find())

    if not graficos:
        print("📂 Nenhum gráfico encontrado no banco de dados.")
        return

    print(f"\n⬇️ Recuperando {len(graficos)} gráficos do MongoDB para a pasta '{pasta_destino}':")
    for doc in graficos:
        filename = doc["filename"]
        path = os.path.join(pasta_destino, filename)
        with open(path, "wb") as f:
            f.write(doc["data"])
        print(f"  - {filename} salvo com sucesso.")

# --- Chamada interativa no main.py ---
resposta = input("\n🔌 Deseja baixar os gráficos salvos no MongoDB? (s/n): ").strip().lower()
if resposta == 's':
    recuperar_graficos_do_mongo()
else:
    print("ℹ️ Ok, gráficos não foram baixados.")
