from scripts import preprocess, model

print("🔄 Carregando e processando dados...")
df = preprocess.load_dataset()
preprocess.save_clean_data(df)

print("📈 Executando previsão de vendas futuras:")
model.predict_sales()

print("\n🖼️ Execute: Rscript scripts/analysis.R para gerar os gráficos.")
