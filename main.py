# main.py
import os
from scripts import preprocess, model, comparisons
# Importa funções específicas de ingest_to_mongo.py
from ingest_to_mongo import conectar_ao_mongo, insert_graphics_into_mongo, retrieve_graphics_from_mongo

# A conexão com o MongoDB NÃO é estabelecida aqui no início
# db será inicializado como None e só receberá um valor quando conectar_ao_mongo for chamado
db = None

# -------------------- INÍCIO --------------------

print("🔄 Carregando e processando dados...")
df = preprocess.load_dataset()
preprocess.save_clean_data(df)

print("📈 Executando previsão de vendas futuras:")
model.prever_vendas_jogo_interativo(df)

print("\n📊 Comparações especiais:")
comparisons.top10_global_by_name(df)

print("\n📊 Iniciando comparação interativa de jogos:")
if df is not None and not df.empty:
    comparisons.comparar_dois_jogos(df)
else:
    print("❌ Não foi possível carregar os dados para comparação ou DataFrame está vazio.")

# --- Pergunta se deseja gerar os gráficos com R ---
resposta_r = input("\n📊 Deseja gerar os gráficos com R agora? (s/n): ").strip().lower()
if resposta_r == 's':
    print("📤 Executando script R para gerar os gráficos...")
    os.system("Rscript scripts/analysis.R")

    # --- Pergunta se deseja salvar no MongoDB ---
    resposta_mongo = input("\n☁️ Deseja salvar os gráficos gerados no MongoDB? (s/n): ").strip().lower()
    if resposta_mongo == 's':
        # Conecta ao MongoDB SOMENTE SE o usuário quiser salvar os gráficos
        if db is None: # Garante que a conexão só seja feita uma vez
            db = conectar_ao_mongo()

        if db is not None: # Verifica se a conexão foi bem-sucedida
            insert_graphics_into_mongo(folder='.', db=db) # Assumindo que o R salva na pasta atual
        else:
            print("❌ Conexão com MongoDB falhou. Gráficos NÃO foram enviados.")
    else:
        print("ℹ️ Gráficos NÃO foram enviados ao MongoDB.")
else:
    print("ℹ️ Gráficos em R não foram gerados.")


# --- Pergunta se deseja recuperar os gráficos do MongoDB ---
resposta_recup = input("\n🔌 Deseja baixar os gráficos salvos no MongoDB? (s/n): ").strip().lower()
if resposta_recup == 's':
    # Conecta ao MongoDB SOMENTE SE o usuário quiser baixar os gráficos
    if db is None: # Garante que a conexão só seja feita uma vez
        db = conectar_ao_mongo()

    if db is not None: # Verifica se a conexão foi bem-sucedida
        retrieve_graphics_from_mongo(db)
    else:
        print("❌ Conexão com MongoDB falhou. Gráficos não foram baixados.")
else:
    print("ℹ️ Ok, gráficos não foram baixados.")

print("\n✔️ Processo concluído.")