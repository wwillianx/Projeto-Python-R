import pandas as pd
from sklearn.linear_model import LinearRegression
import time

def predict_sales():
    start = time.time()
    df = pd.read_csv('data/clean_vgsales.csv')

    X = df[['Year']]
    y = df['Global_Sales']

    model = LinearRegression()
    model.fit(X, y)

    future_years = pd.DataFrame({'Year': [2025, 2026, 2027]})
    predictions = model.predict(future_years)

    for year, pred in zip(future_years['Year'], predictions):
        print(f"🔮 Previsão para {year}: {pred:.2f} milhões de unidades")

    print(f"⏱️ Tempo de execução: {time.time() - start:.2f} segundos")

if __name__ == "__main__":
    predict_sales()
