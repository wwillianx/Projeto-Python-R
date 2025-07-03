# main.py

# Importa bibliotecas e módulos locais
import os
from scripts import preprocess, model, comparisons  # Módulos do seu projeto
from ingest_to_mongo import conectar_ao_mongo, insert_graphics_into_mongo, retrieve_graphics_from_mongo  # Funções de MongoDB

# Inicializa a variável de conexão com o MongoDB como None.
# A conexão será feita somente se o usuário quiser interagir com o banco.
db = None

# -------------------- INÍCIO DO FLUXO --------------------

print("🔄 Carregando e processando dados...")
df = preprocess.load_dataset()          # Carrega os dados (do CSV, banco, etc.)
preprocess.save_clean_data(df)         # Salva uma versão limpa dos dados

# Previsão de vendas para um jogo escolhido pelo usuário
print("📈 Executando previsão de vendas futuras:")
model.prever_vendas_jogo_interativo(df)

# Exibe o top 10 de jogos mais vendidos globalmente
print("\n📊 Comparações especiais:")
comparisons.top10_global_by_name(df)

# Compara dois jogos escolhidos pelo usuário
print("\n📊 Iniciando comparação interativa de jogos:")
if df is not None and not df.empty:
    comparisons.comparar_dois_jogos(df)
else:
    print("❌ Não foi possível carregar os dados para comparação ou DataFrame está vazio.")

# -------------------- GERAR GRÁFICOS COM R --------------------

# Pergunta ao usuário se deseja gerar gráficos usando R
resposta_r = input("\n📊 Deseja gerar os gráficos com R agora? (s/n): ").strip().lower()
if resposta_r == 's':
    print("📤 Executando script R para gerar os gráficos...")
    os.system("Rscript scripts/analysis.R")  # Executa o script analysis.R com o R instalado

    # -------------------- SALVAR GRÁFICOS NO MONGODB --------------------
    resposta_mongo = input("\n☁️ Deseja salvar os gráficos gerados no MongoDB? (s/n): ").strip().lower()
    if resposta_mongo == 's':
        # Conecta ao MongoDB apenas se ainda não estiver conectado
        if db is None:
            db = conectar_ao_mongo()

        # Insere os arquivos de imagem (PDF/PNG) no banco, se conexão for bem-sucedida
        if db is not None:
            insert_graphics_into_mongo(folder='.', db=db)  # Considera que os arquivos estão na pasta atual
        else:
            print("❌ Conexão com MongoDB falhou. Gráficos NÃO foram enviados.")
    else:
        print("ℹ️ Gráficos NÃO foram enviados ao MongoDB.")
else:
    print("ℹ️ Gráficos em R não foram gerados.")

# -------------------- BAIXAR GRÁFICOS DO MONGODB --------------------

# Pergunta ao usuário se deseja baixar os gráficos armazenados no MongoDB
resposta_recup = input("\n🔌 Deseja baixar os gráficos salvos no MongoDB? (s/n): ").strip().lower()
if resposta_recup == 's':
    # Conecta ao banco apenas se ainda não estiver conectado
    if db is None:
        db = conectar_ao_mongo()

    if db is not None:
        retrieve_graphics_from_mongo(db)  # Recupera os arquivos e salva localmente
    else:
        print("❌ Conexão com MongoDB falhou. Gráficos não foram baixados.")
else:
    print("ℹ️ Ok, gráficos não foram baixados.")

# -------------------- FIM DO PROCESSO --------------------
print("\n✔️ Processo concluído.")