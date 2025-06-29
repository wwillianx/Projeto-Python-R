import pandas as pd

def load_data(path='dados/vgsales.csv'):
    df = pd.read_csv(path)
    df = df.dropna(subset=['Year', 'Global_Sales'])
    df['Year'] = df['Year'].astype(int)
    return df

def top10_global_by_name(df):
    grouped = df.groupby("Name")["Global_Sales"].sum().reset_index()
    top10 = grouped.sort_values(by="Global_Sales", ascending=False).head(10)
    print("\n🎮 Top 10 jogos mais vendidos (unificando plataformas):\n")
    print(top10.to_string(index=False))

def top10_last_year(df):
    max_year = df['Year'].max()
    last_year_df = df[df['Year'] == max_year]
    grouped = last_year_df.groupby("Name")["Global_Sales"].sum().reset_index()
    top10 = grouped.sort_values(by="Global_Sales", ascending=False).head(10)
    print(f"\n📅 Top 10 jogos mais vendidos em {max_year}:\n")
    print(top10.to_string(index=False))

if __name__ == "__main__":
    df = load_data()
    top10_global_by_name(df)
    top10_last_year(df)
